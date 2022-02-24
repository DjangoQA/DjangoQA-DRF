from celery import shared_task

from _helpers.ghasedak.ghasedak_api import Ghasedak
from accounts.utils import RedisConnection
from config import settings
from config.settings import GHASEDAK_TOKEN, GHASEDAK_TYPE, GHASEDAK_TEMPLATE, GHASEDAK_PARAM1

redis = RedisConnection()
ghasedak = Ghasedak(GHASEDAK_TOKEN)


@shared_task
def phone_number_verification(validated_data):
    phone_number = validated_data.get('phone_number', None)
    if phone_number:
        otp_code = redis.set_otp(phone_number)
        is_sent = ghasedak.verification({
            'receptor': str(phone_number),
            'type': GHASEDAK_TYPE,
            'template': GHASEDAK_TEMPLATE,
            'param1': GHASEDAK_PARAM1
        })
