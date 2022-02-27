from django.utils.translation import gettext_lazy as _


def welcome_user_answer(tg_id: str, username: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _(
            f"How you doing {username}?\nIf you need any assistance, I’m always here."
        ),
    }
