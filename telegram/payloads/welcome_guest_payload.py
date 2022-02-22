from django.utils.translation import gettext_lazy as _


def welcome_guest_payload(tg_id: str, username: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _(
            f"Hi {username} 👋 \nWelcome to DjangoQa official bot. If you need any assistance, I’m always here."
        ),
        "reply_markup": {
            "inline_keyboard": [[{"text": _("Login"), "callback_data": "login"}]]
        },
    }
