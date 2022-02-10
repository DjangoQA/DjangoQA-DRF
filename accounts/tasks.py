from celery import shared_task
from django.core.mail import send_mail

from accounts.utils import RedisConnection
from config import settings

redis = RedisConnection()

email_content = {
    'subject': 'Email Verification',
    'from_email': settings.EMAIL_HOST_USER,
    'auth_user': settings.EMAIL_HOST_USER,
    'auth_password': settings.EMAIL_HOST_PASSWORD,
}


@shared_task
def email_verification(validated_data):
    email = validated_data.get('email', None)
    if email:
        otp_code = redis.set_otp(email)
        email_content['message'], email_content['recipient_list'] = f'Hi, Your code is: {otp_code}', [email]
        send_mail(**email_content)


@shared_task
def phone_number_verification(validated_data):
    # TODO-1: create phone number verification
    pass
