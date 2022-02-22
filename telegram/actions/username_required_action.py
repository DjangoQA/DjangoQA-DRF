from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.validators import TelegramUsernameValidator
from telegram.payloads import (
    username_validation_error,
    username_duplicate_error,
    request_username,
)

User = get_user_model()


def username_required_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    
    # cheking if user sent text:
    if "text" in message:
        username = message["text"]
    else:
        return request_username(tg_id)

    validator = TelegramUsernameValidator()
    # setting text to ask again in case of error
    text = _("Please enter your desired Username:")

    # ACTION:

    # setting username-state again for the next messages in case of error:
    cache.set(tg_id, "username_required")

    try:
        # validating username:
        validator(username)
        # trying to save username:
        User.objects.filter(telegram_id=tg_id).update(username=username)
    except ValidationError as error:
        # validation error occurred.
        return username_validation_error(tg_id, error.message, text)
    except IntegrityError:
        # duplicate username error occurred.
        return username_duplicate_error(tg_id, text)
    else:
        cache.set(tg_id, "menu")
        # TODO: show menu
