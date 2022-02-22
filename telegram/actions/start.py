from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads import request_phone_number, request_username

User = get_user_model()


def start(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]

    # ACTION:
    user, created = User.objects.get_or_create(telegram_id=tg_id)
    if created or not user.phone_number:
        # if user is created right now or phone_number is empty,
        # we need to ask for phone number.
        cache.set(tg_id, "contact_required")
        return request_phone_number(tg_id)
    elif not user.username:
        # if user has phone number but not username,
        # we need to ask for username.
        cache.set(tg_id, "username_required")
        return request_username(tg_id)
    else:
        cache.set(tg_id, "menu")
        # TODO: show menu
