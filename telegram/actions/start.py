from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def start(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]

    # ACTION:
    user, created = User.objects.get_or_create(telegram_id=tg_id)
    if created or not user.phone_number:
        # if user is created right now or phone_number is empty,
        # we need to ask for phone number.
        cache.set(tg_id, "contact_required")
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": _("Please share your phone number to Signup:"),
            "reply_markup": {
                "keyboard": [[{"text": _("Share Contact"), "request_contact": True}]],
                "resize_keyboard": True,
                "one_time_keyboard": True,
            },
        }
    elif not user.username:
        # if user has phone number but not username,
        # we need to ask for username.
        cache.set(tg_id, "username_required")
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": _("Please enter your desired Username:"),
            "reply_markup": {"remove_keyboard": True},
        }
    else:
        cache.set(tg_id, "menu")
        # TODO: show menu
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": f"enjoy token dear {user.username}! http://blahblah..",
            "reply_markup": {"remove_keyboard": True},
        }
