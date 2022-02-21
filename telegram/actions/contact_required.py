from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def contact_required(message: dict):
    # INITIALIZING VARIABLES:
    tg_id = message["chat"]["id"]

    # cheking if user sent contact:
    if "contact" in message:
        contact_user_id = message["contact"]["user_id"]
        contact_phone_number = message["contact"]["phone_number"]
    else:
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

    # ACTION:
    user = User.objects.get(telegram_id=tg_id)
    if tg_id != contact_user_id:
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": _("The shared contact is not yours!"),
            "reply_markup": {
                "keyboard": [[{"text": _("Share Contact"), "request_contact": True}]],
                "resize_keyboard": True,
                "one_time_keyboard": True,
            },
        }
    else:
        user.phone_number = contact_phone_number.lstrip("+")
        user.save()
        cache.set(tg_id, "username_required")
        return {
            "method": "sendMessage",
            "chat_id": tg_id,
            "text": _("Please enter your desired Username:"),
            "reply_markup": {"remove_keyboard": True},
        }
