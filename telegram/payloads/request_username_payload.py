from django.utils.translation import gettext_lazy as _


def request_username_payload(tg_id: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _("Please Send your desired Username:"),
        "reply_markup": {
            "keyboard": [
                [_("Cancel")],
            ]
        },
    }
