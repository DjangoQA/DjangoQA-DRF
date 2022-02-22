from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads import request_phone_number, invalid_phone_number, request_username


User = get_user_model()


def contact_required(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]

    # cheking if user sent contact:
    if "contact" in message:
        contact_user_id = message["contact"]["user_id"]
        contact_phone_number = message["contact"]["phone_number"]
    else:
        return request_phone_number(tg_id)

    # ACTION:
    user = User.objects.get(telegram_id=tg_id)
    if tg_id != contact_user_id:
        return invalid_phone_number(tg_id)
    else:
        user.phone_number = contact_phone_number.lstrip("+")
        user.save()
        if user.username:
            cache.set(tg_id, "menu")
            # TODO: show menu
        else:
            cache.set(tg_id, "username_required")
            return request_username(tg_id)
