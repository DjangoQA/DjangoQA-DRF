from django.utils.translation import gettext_lazy as _


def welcome_user_callback_payload(chat_id: str, message_id: str, username: str):
    return {
        "method": "editMessageText",
        "chat_id": chat_id,
        "message_id": message_id,
        "text": _(
            f"How you doing {username}? \nWelcome back. If you need any assistance, I’m always here."
        ),
        "reply_markup": {
            "inline_keyboard": [[{"text": _("Profile"), "callback_data": "profile"}]]
        },
    }
