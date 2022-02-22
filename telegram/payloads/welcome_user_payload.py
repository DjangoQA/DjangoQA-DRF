from django.utils.translation import gettext_lazy as _


def welcome_user_payload(tg_id: str, username: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _(
            f"How you doing {username}? \nWelcome back. If you need any assistance, I’m always here."
        ),
        "reply_markup": {
            "inline_keyboard": [[{"text": _("Profile"), "callback_data": "profile"}]]
        },
    }
