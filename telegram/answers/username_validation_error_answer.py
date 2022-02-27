from django.utils.translation import gettext_lazy as _


def username_validation_error_answer(tg_id, message, text):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": f"{message}\n\n{text}",
    }
