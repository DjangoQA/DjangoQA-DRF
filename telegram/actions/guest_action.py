from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.answers import login_menu_answer
from telegram.answers import request_username_answer

User = get_user_model()


def guest_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    text = message["text"].lower() if "text" in message else None
    user = User.objects.get(telegram_id=tg_id)
    contact = user.phone_number if user.phone_number else user.email

    # ACTION:
    if text == "login":
        if contact:
            cache.set(tg_id, "USERNAME-REQUIRED")
            return request_username_answer(tg_id, contact)
        else:
            cache.set(tg_id, "LOGIN-MENU")
            return login_menu_answer(tg_id)

    # HINT: Add more actions for guests here.
