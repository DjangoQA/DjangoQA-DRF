from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from accounts.api.serializers import OTPPhoneNumberSerializer
from accounts.tasks import phone_number_verification


class OTPAPIView(GenericAPIView):
    """
    Create a one time password and send for user email or phone number.
    """
    serializer_class = OTPPhoneNumberSerializer

    @staticmethod
    def get_otp_sender():
        return phone_number_verification

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.get_otp_sender().delay(serializer.validated_data)
        return Response(status=status.HTTP_200_OK)
