from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads.callbacks import login_callback_payload


User = get_user_model()


def login_callback_action(callback: dict):
    # INITIALIZING VARIABLES:
    tg_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]

    # ACTION:
    return login_callback_payload(tg_id, message_id)
