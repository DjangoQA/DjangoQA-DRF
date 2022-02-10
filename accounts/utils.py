import random

import redis

from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password

from config import settings


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/avatars/user_<id>
    filename = f'user_{instance.id}_{int(datetime.now().timestamp())}.{filename.split(".")[-1]}'
    return f'users/avatars/{filename}'


class RedisConnection:
    _instance = None

    def __init__(self):
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.db = settings.REDIS_DB

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(*args, **kwargs)
        return cls._instance

    def __redis_connect(self):
        return redis.Redis(host=self.host, port=self.port, db=self.db)

    @staticmethod
    def __redis_disconnect(redis_instance):
        redis_instance.close()

    def set_otp(self, key):
        redis_instance = self.__redis_connect()
        otp_code = random.randint(1111, 9999)
        redis_instance.set(key, make_password(str(otp_code)))
        redis_instance.expire(key, 180)
        self.__redis_disconnect(redis_instance)
        return otp_code

    def verify_otp(self, key, otp_verify):
        redis_instance = self.__redis_connect()
        otp_code = redis_instance.get(key)
        self.__redis_disconnect(redis_instance)
        if otp_code:
            if check_password(otp_verify, otp_code.decode('utf8')):
                return True, True
            return True, False
        return False, False
