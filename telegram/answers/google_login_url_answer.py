from django.utils.translation import gettext_lazy as _
from telegram.helper import get_authorize_url


def google_login_answer(tg_id: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": get_authorize_url(tg_id),
        "reply_markup": {"remove_keyboard": True},
    }
