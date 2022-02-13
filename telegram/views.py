from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class WebhookGenericApiView(GenericAPIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.payload = {}
        self.status = status.HTTP_200_OK

    def start(self):
        tg_id = self.message["chat"]["id"]
        user, created = User.objects.get_or_create(telegram_id=tg_id)
        if created or not user.phone_number:
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": _("Please share your phone number to Signup"),
                "reply_markup": {
                    "keyboard": [
                        [{"text": _("Share Contact"), "request_contact": True}]
                    ],
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                },
            }
        else:
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": "enjoy token!",
            }

    def contact(self):
        tg_id = self.message["chat"]["id"]
        contact_user_id = self.message["contact"]["user_id"]
        phone_number = self.message["contact"]["phone_number"]
        if tg_id != contact_user_id:
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": _("The shared contact is not yours!"),
                "reply_markup": {
                    "keyboard": [
                        [{"text": _("Share Contact"), "request_contact": True}]
                    ],
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                },
            }
        else:
            user, created = User.objects.update_or_create(
                telegram_id=tg_id, defaults={"phone_number": phone_number}
            )
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": "enjoy token!",
            }

    def post(self, request, *args, **kwargs):
        try:
            # parsing message from telegram
            message = self.message = request.data["message"]
            if "text" in message:
                if message["text"] == "/start":
                    # user issued start command
                    self.start()
            elif "contact" in message:
                # user shared contact
                self.contact()
        except KeyError:
            self.status = status.HTTP_400_BAD_REQUEST
            self.payload = "Json structure is not right."
        finally:
            # finalize response
            return Response(self.payload, status=self.status)
