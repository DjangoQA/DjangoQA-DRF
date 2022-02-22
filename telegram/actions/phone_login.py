import string


from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


def phone_login(tg_id: string, inline_message_id: string, data: string):
    
    # getting user from db
    user = User.objects.get(telegram_id=tg_id)

    if not( user.phone_number or user.email):
        pass
