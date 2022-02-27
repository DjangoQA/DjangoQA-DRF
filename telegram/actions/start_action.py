from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads import welcome_user_payload, welcome_guest_payload

User = get_user_model()


def start_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    name = message["chat"]["first_name"]

    # ACTION:
    user, created = User.objects.get_or_create(telegram_id=tg_id)

    # its unnessary to check if its created, because at the end we care about:
    # 1. if the user has a phone number or email
    # 2. if user has a username
    if (user.phone_number or user.email) and user.username:
        # authenticated user.
        cache.set(tg_id, "USER")
        return welcome_user_payload(tg_id, user.username)
    else:
        # otherwise it will be our guest.
        cache.set(tg_id, "GUEST")
        return welcome_guest_payload(tg_id, name)
