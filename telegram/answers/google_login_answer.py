from django.utils.translation import gettext_lazy as _


def google_login_answer(tg_id: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": "https://www.google.com",
        "reply_markup": {"remove_keyboard": True},
    }
