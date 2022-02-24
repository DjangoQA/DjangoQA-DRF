import random

from datetime import datetime

from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password

from config import settings
from config.settings import OTP_EXPIRE_TIME


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/avatars/user_<id>
    filename = f'user_{instance.id}_{int(datetime.now().timestamp())}.{filename.split(".")[-1]}'
    return f'users/avatars/{filename}'


class RedisConnection:
    """
    Redis connection is singleton model which generate a code and save that with key in database as otp code
    """
    _instance = None

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(*args, **kwargs)
        return cls._instance

    @staticmethod
    def set_otp(key):
        otp_code = random.randint(1111, 9999)
        cache.set(key, make_password(str(otp_code)), OTP_EXPIRE_TIME)
        return otp_code

    @staticmethod
    def verify_otp(key, otp_verify):
        otp_code = cache.get(key)
        if otp_code:
            if check_password(otp_verify, otp_code):
                return True, True
            return True, False
        return False, False
