from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.api.serializers import OTPEmailSerializer
from accounts.tasks import email_verification


class OTPAPIView(GenericAPIView):
    """
    Create a one time password and send for user email or phone number.
    """
    serializer_class = OTPEmailSerializer

    # TODO-1: add lookup_url_kwarg for email and phone number opt send
    # TODO-2: edit url
    # TODO-3: override get_serializer method and add phone number serializer
    # TODO-4: override get_otp_sender method and add phone_number_verification

    @staticmethod
    def get_otp_sender():
        return email_verification

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_otp_sender().delay(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
