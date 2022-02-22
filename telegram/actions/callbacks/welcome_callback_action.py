from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads.callbacks import (
    welcome_guest_callback_payload,
    welcome_user_callback_payload,
)


User = get_user_model()


def welcome_callback_action(callback: dict):
    # INITIALIZING VARIABLES:
    tg_id = callback["message"]["chat"]["id"]
    name = callback["message"]["chat"]["first_name"]
    message_id = callback["message"]["message_id"]
    state = cache.get(tg_id)

    # ACTION:
    if state == "guest":
        return welcome_guest_callback_payload(tg_id, message_id, name)
    else:
        name = User.objects.get(tg_id=tg_id).username
        return welcome_user_callback_payload(tg_id, message_id, name)
