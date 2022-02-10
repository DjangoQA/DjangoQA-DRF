from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class OTPEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)


class OTPPhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number',)
