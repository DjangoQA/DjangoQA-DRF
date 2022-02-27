from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


from accounts.validators import TelegramUsernameValidator
from telegram.answers import (
    username_validation_error_answer,
    username_duplicate_error_answer,
    request_username_answer,
    welcome_guest_answer,
)
from telegram.answers.success_signup_answer import success_signup_answer


User = get_user_model()


def username_required_action(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]
    text = _("Please enter your desired Username:")
    validator = TelegramUsernameValidator()

    # ACTION:
    if "text" in message:
        username = message["text"]
    else:
        # repeat the message if no text is entered.
        return request_username_answer(tg_id)

    if username.lower() == "cancel":
        # jump '2' step back from currently USERNAME_REQUIRED to GUEST
        cache.set(tg_id, "GUEST")
        return welcome_guest_answer(tg_id, username)

    try:
        validator(username)
        User.objects.filter(telegram_id=tg_id).update(username=username)

    except ValidationError as error:
        return username_validation_error_answer(tg_id, error.message, text)

    except IntegrityError:
        return username_duplicate_error_answer(tg_id, text)

    else:
        cache.set(tg_id, "USER")
        return success_signup_answer(tg_id, username)
