import uuid as uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.postgres.fields import CICharField
from django.utils.translation import gettext_lazy as _
from django.db import models

from accounts.utils import user_directory_path
from accounts.validators import TelegramUsernameValidator, PhoneNumberValidator


class User(AbstractUser):
    ascii_username_validator = ASCIIUsernameValidator()
    tg_username_validator = TelegramUsernameValidator()
    phone_number_validator = PhoneNumberValidator()

    uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False, verbose_name=_('uuid'))
    username = CICharField(
        _('username'),
        max_length=32,
        unique=True,
        help_text=_('Required. 32 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[ascii_username_validator, tg_username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=12, validators=[phone_number_validator])

    avatar = models.ImageField(upload_to=user_directory_path, verbose_name=_('avatar'))
    telegram_id = models.BigIntegerField(verbose_name=_('telegram id'), null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'user'
