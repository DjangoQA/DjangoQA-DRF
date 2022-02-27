from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.payloads import login_menu_payload

User = get_user_model()


def guest_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    text = message["text"].lower() if "text" in message else None
    
    # ACTION:
    if text == "login":
        cache.set(tg_id, "LOGIN-MENU")
        return login_menu_payload(tg_id)
    
    # HINT: Add more actions for guests here.