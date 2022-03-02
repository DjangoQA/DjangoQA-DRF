from django.utils.translation import gettext_lazy as _


def faild_login_answer(tg_id: str, error: str = None):
    text = _("Sorry! Google authentication failed.")
    if error == "duplicate":
        text += _("\n\nSelected email is already registered.")
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": text,
        "reply_markup": {
            "keyboard": [
                [_("/start")],
            ],
            "resize_keyboard": True,
        },
    }
