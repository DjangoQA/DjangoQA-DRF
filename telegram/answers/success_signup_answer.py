from django.utils.translation import gettext_lazy as _


def success_signup_answer(tg_id: str, username: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _(f"Dear {username}, Your account has been created successfully!"),
        "reply_markup": {
            "remove_keyboard": True,
        },
    }
