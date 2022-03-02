from django.utils.translation import gettext_lazy as _


def request_username_answer(tg_id: str, contact: str = None):
    text = _("Please Send your desired Username:")

    if contact:
        text = f"You successfully authenticated as {contact} !\n\n{text}"

    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": text,
        "reply_markup": {
            "keyboard": [
                [_("Cancel")],
            ],
            "resize_keyboard": True,
        },
    }
