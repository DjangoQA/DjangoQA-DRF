from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


from accounts.validators import TelegramUsernameValidator
from telegram.payloads import (
    username_validation_error_payload,
    username_duplicate_error_payload,
    request_username_payload,
    welcome_guest_payload,
)
from telegram.payloads.success_signup_payload import success_signup_payload


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
        return request_username_payload(tg_id)

    if username.lower() == "cancel":
        # jump '2' step back from currently USERNAME_REQUIRED to GUEST
        cache.set(tg_id, "GUEST")
        return welcome_guest_payload(tg_id, username)

    try:
        validator(username)
        User.objects.filter(telegram_id=tg_id).update(username=username)

    except ValidationError as error:
        return username_validation_error_payload(tg_id, error.message, text)

    except IntegrityError:
        return username_duplicate_error_payload(tg_id, text)

    else:
        cache.set(tg_id, "USER")
        return success_signup_payload(tg_id, username)
