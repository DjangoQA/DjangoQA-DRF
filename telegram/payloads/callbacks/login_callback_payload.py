from django.utils.translation import gettext_lazy as _


def login_callback_payload(chat_id: str, message_id: str):
    return {
        "method": "editMessageText",
        "chat_id": chat_id,
        "message_id": message_id,
        "text": "We currently support below login methods. Which one do you prefer?",
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
                [{"text": _("Back"), "callback_data": "welcome"}],
            ],
        },
    }
