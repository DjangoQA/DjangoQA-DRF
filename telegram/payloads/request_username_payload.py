from django.utils.translation import gettext_lazy as _


def request_username_payload(tg_id):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _("Please enter your desired Username:"),
        "reply_markup": {"remove_keyboard": True},
    }
