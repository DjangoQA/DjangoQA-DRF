from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneNumberValidator(validators.RegexValidator):
    regex = r'^(98)+?9\d{9}$'
    message = _('Phone number is invalid')
    flags = 0


@deconstructible
class TelegramUsernameValidator(validators.RegexValidator):
    regex = r'^(?=.{5,32}$)(?![0-9_])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0
