import string
from django.utils.translation import gettext_lazy as _


def welcome(chat_id: string, message_id: string):
    return {
        "method": "editMessageReplyMarkup",
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": {
            "inline_keyboard": [[{"text": _("Login"), "callback_data": "login"}]],
        },
    }
