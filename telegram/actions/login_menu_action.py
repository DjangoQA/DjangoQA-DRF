from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads import (
    welcome_guest_payload,
    invalid_phone_number_payload,
    request_username_payload,
    google_login_payload
)

User = get_user_model()


def login_menu_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    text = message["text"].lower() if "text" in message else None
    name = message["chat"]["first_name"]

    # ACTION:
    if "contact" in message:
        contact_user_id = message["contact"]["user_id"]
        contact_phone_number = message["contact"]["phone_number"]
        user = User.objects.get(telegram_id=tg_id)

        # avoid getting other users contact
        if tg_id != contact_user_id:
            return invalid_phone_number_payload(tg_id)

        else:
            user.phone_number = contact_phone_number.lstrip("+")
            user.save()
            cache.set(tg_id, "USERNAME-REQUIRED")
            return request_username_payload(tg_id)
    
    elif text == "google account" or text == "google":
        cache.set(tg_id, "GOOGLE-LOGIN")
        # TODO: implement google login
        return google_login_payload(tg_id)
    
    elif text == "cancel":
        print("gpeiorjgoi")
        # jump '1' step back from currently LOGIN_MENU to GUEST
        cache.set(tg_id, "GUEST")
        return welcome_guest_payload(tg_id, name)
