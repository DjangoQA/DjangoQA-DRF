from django.utils.translation import gettext_lazy as _


def login_menu_answer(tg_id: str):
    return {
        "method": "sendMessage",
        "chat_id": tg_id,
        "text": _(
            "We currently support below methods to login.\nWhich one do you prefer?"
        ),
        "reply_markup": {
            "keyboard": [
                [{"text": _("Phone Number"), "request_contact": True}],
                [_("Google Account")],
                [_("Cancel")],
            ], "resize_keyboard": True
        },
    }
