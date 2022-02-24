from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class OTPAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:send-otp')
        self.valid_data = {'phone_number': '989101916484'}
        self.invalid_data = {'phone_number': '09101916484', 'bad_param': 'bad value'}

    def test_valid_email(self):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_email(self):
        response = self.client.post(self.url, data=self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
