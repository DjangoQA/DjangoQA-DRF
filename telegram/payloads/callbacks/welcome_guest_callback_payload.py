from django.utils.translation import gettext_lazy as _


def welcome_guest_callback_payload(chat_id: str, message_id: str, username: str):
    print("wtf?")
    print(username)
    return {
        "method": "editMessageText",
        "chat_id": chat_id,
        "message_id": message_id,
        "text": _(
            f"Hi {username} 👋 \nWelcome to DjangoQa official bot. If you need any assistance, I’m always here."
        ),
        "reply_markup": {
            "inline_keyboard": [[{"text": _("Login"), "callback_data": "login"}]]
        },
        
    }
