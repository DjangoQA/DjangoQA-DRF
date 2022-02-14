from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError
from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from accounts.validators import TelegramUsernameValidator


User = get_user_model()


class WebhookGenericApiView(GenericAPIView):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.payload = {}
        self.status = status.HTTP_200_OK

    def start(self):
        tg_id = self.tg_id
        user, created = User.objects.get_or_create(telegram_id=tg_id)
        if created or not user.phone_number:
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": _("Please share your phone number to Signup:"),
                "reply_markup": {
                    "keyboard": [
                        [{"text": _("Share Contact"), "request_contact": True}]
                    ],
                    "resize_keyboard": True,
                    "one_time_keyboard": True,
                },
            }
        elif not user.username:
            cache.set(tg_id, "username", 180)
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": _("Please enter your desired Username:"),
                "reply_markup": {"remove_keyboard": True},
            }
        else:
            cache.delete(tg_id)
            # TODO: send token
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": f"enjoy token dear {user.username}! http://blahblah..",
                "reply_markup": {"remove_keyboard": True},
            }

    def save_contact(self):
        tg_id = self.tg_id
        contact_user_id = self.message["contact"]["user_id"]
        phone_number = self.message["contact"]["phone_number"].lstrip("+")
        user = User.objects.get(telegram_id=tg_id)
        if user.phone_number:
            return
        elif tg_id != contact_user_id:
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
            user.phone_number = phone_number
            user.save()
            if not user.username:
                cache.set(tg_id, "username", 180)
                self.payload = {
                    "method": "sendMessage",
                    "chat_id": tg_id,
                    "text": _("Please enter your desired Username:"),
                    "reply_markup": {"remove_keyboard": True},
                }
            else:
                cache.delete(tg_id)
                # TODO: send token
                self.payload = {
                    "method": "sendMessage",
                    "chat_id": tg_id,
                    "text": f"enjoy token dear {user.username}! http://blahblah..",
                    "reply_markup": {"remove_keyboard": True},
                }

    def save_username(self):
        tg_id = self.tg_id
        username = self.message["text"]
        validator = TelegramUsernameValidator()
        text = _("Please enter your desired Username:")
        # setting username-state again for the next messages in case of error:
        cache.set(tg_id, "username", 180)
        try:
            # validating username:
            validator(username)
            # trying to save username:
            User.objects.filter(telegram_id=tg_id).update(username=username)
        except ValidationError as error:
            # validation error occurred.
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": f"{error.message}\n\n{text}",
            }
        except IntegrityError:
            # duplicate username error occurred.
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": f"Username was already taken.\n\n{text}",
            }
        else:
            cache.delete(tg_id)
            # TODO: send token
            self.payload = {
                "method": "sendMessage",
                "chat_id": tg_id,
                "text": f"enjoy token dear {username}! http://blahblah..",
                "reply_markup": {"remove_keyboard": True},
            }

    def post(self, request, *args, **kwargs):
        if kwargs["token"] != settings.TELEGRAM_BOT_ENDPOINT:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            # parsing message from telegram
            message = self.message = request.data["message"]
            tg_id = self.tg_id = self.message["chat"]["id"]
            if message["chat"]["type"] == "private":
                if "text" in message:
                    # user sent messsge with text
                    if message["text"] == "/start":
                        # user issued start command
                        self.start()
                    elif state := cache.get(tg_id):
                        if state == "username":
                            # user send username
                            self.save_username()
                elif "contact" in message:
                    # user shared contact
                    self.save_contact()
        except KeyError:
            self.status = status.HTTP_400_BAD_REQUEST
            self.payload = "Json structure is not right."
        finally:
            # finalize response
            return Response(self.payload, self.status)
