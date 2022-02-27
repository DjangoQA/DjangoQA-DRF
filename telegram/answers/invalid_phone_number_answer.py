from django.utils.translation import gettext_lazy as _


def invalid_phone_number_answer(tg_id):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _("The shared contact is not yours!"),
        "reply_markup": {
            "keyboard": [
                [{"text": _("Phone Number"), "request_contact": True}],
                [_("Cancel")],
            ]
        },
    }
