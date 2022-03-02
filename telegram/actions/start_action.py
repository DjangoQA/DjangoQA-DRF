from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from telegram.answers import (
    welcome_user_answer,
    welcome_guest_answer,
    request_username_answer,
    faild_login_answer,
)

User = get_user_model()


def start_action(message: dict, text: str = None):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    name = message["chat"]["first_name"]

    # ACTION:
    user, created = User.objects.get_or_create(telegram_id=tg_id)

    # its unnessary to check if its created, because at the end we care about:
    # 1. if the user has a phone number or email
    # 2. if user has a username
    if user.username:
        # authenticated user.
        cache.set(tg_id, "USER")
        return welcome_user_answer(tg_id, user.username)

    elif user.email and text == "/start successful-login":
        cache.set(tg_id, "USERNAME-REQUIRED")
        return request_username_answer(tg_id, user.email)

    elif text == "/start failed-login":
        cache.set(tg_id, "GUEST")
        return faild_login_answer(tg_id)

    elif text == "/start failed-login-duplicate":
        cache.set(tg_id, "GUEST")
        return faild_login_answer(tg_id, "duplicate")

    else:
        # otherwise it will be our guest.
        cache.set(tg_id, "GUEST")
        return welcome_guest_answer(tg_id, name)
