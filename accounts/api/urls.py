from django.urls import path
from .views import OTPAPIView

app_name = 'accounts'

urlpatterns = [
    path('otp/', OTPAPIView.as_view(), name='send-otp'),
]
