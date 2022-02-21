from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.validators import TelegramUsernameValidator


User = get_user_model()


def username_required(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    username = message["text"]

    # ACTION:
    validator = TelegramUsernameValidator()
    text = _("Please enter your desired Username:")
    # setting username-state again for the next messages in case of error:
    cache.set(tg_id, "username_required")
    try:
        # validating username:
        validator(username)
        # trying to save username:
        User.objects.filter(telegram_id=tg_id).update(username=username)
    except ValidationError as error:
        # validation error occurred.
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": f"{error.message}\n\n{text}",
        }
    except IntegrityError:
        # duplicate username error occurred.
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": f"Username was already taken.\n\n{text}",
        }
    else:
        cache.set(tg_id, "menu")
        # TODO: show menu
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": f"enjoy token dear {username}! http://blahblah..",
            "reply_markup": {"remove_keyboard": True},
        }
