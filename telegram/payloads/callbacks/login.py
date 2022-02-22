import string
from django.utils.translation import gettext_lazy as _


def login(chat_id: string, message_id: string):
    return {
        "method": "editMessageReplyMarkup",
        "chat_id": chat_id,
        "message_id": message_id,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": _("Phone number"), "callback_data": "phone_login"}],
                [
                    {
                        "text": _("Google Account"),
                        "url": "https://www.google.com",
                        "callback_data": "google_login",
                    }
                ],
                [{"text": _("Return"), "callback_data": "welcome"}],
            ],
        },
    }