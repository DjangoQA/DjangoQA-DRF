from django.utils.translation import gettext_lazy as _


def invalid_phone_number(tg_id):
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
