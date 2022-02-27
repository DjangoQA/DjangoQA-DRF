from django.utils.translation import gettext_lazy as _


def username_duplicate_error_answer(tg_id, text):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": f"Username was already taken.\n\n{text}",
    }
