import requests

from django.db import IntegrityError
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .helper import exchange_authorization_code
from .permissions import TokenPermission
from .actions import (
    start_action,
    guest_action,
    login_menu_action,
    username_required_action,
)


User = get_user_model()


class WebhookGenericApiView(GenericAPIView):
    permission_classes = [TokenPermission]

    def post(self, request, *args, **kwargs):
        """
        Inspect the incoming request for messages,
        calls dispatcher and returns the payload to Telegram API.
        """

        self.payload = {}

        message = request.data["message"] if "message" in request.data else None

        if message and message["chat"]["type"] == "private":
            text = message["text"] if "text" in message else None
            start = text.startswith("/start") if text else False
            tg_id = message["chat"]["id"]
            state = cache.get(tg_id)

            if start or not state:
                self.payload = start_action(message, text)
            else:
                self.payload = self.dispatcher(state, message)

        return Response(self.payload, status.HTTP_200_OK)

    def dispatcher(self, state, message):
        """
        Simply checks the state and set payload to required action.

        - has nothing to do with 'dispatch' in django.
        """

        if state == "GUEST":
            return guest_action(message)

        if state == "LOGIN-MENU":
            return login_menu_action(message)

        if state == "USERNAME-REQUIRED":
            return username_required_action(message)


class GoogleLoginGenericApiView(GenericAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tg_id = None
        self.authorization_code = None
        self.access_token = None
        self.email = None

    def get(self, request, *args, **kwargs):
        # PHASE 1: Get authorization code
        # check required params and user's state in cache
        # 403 in case of missing params or state
        self.authorization_code = request.GET.get("code")
        self.tg_id = request.GET.get("state")

        if (
            self.authorization_code
            and self.tg_id
            and (cache.get(self.tg_id) == "GOOGLE-LOGIN")
        ):
            return self.exchange_token()

        return Response(status.HTTP_403_FORBIDDEN)

    def exchange_token(self):
        # PHASE 2: Exchange authorization code for access token
        # request access token from google in exchange to authorization code
        # calls self.get_user_info() in case of success

        exchange_response = exchange_authorization_code(self.authorization_code)

        if not "access_token" in exchange_response:
            # TODO: SAVE TO LOGS
            print("ERROR IN 'exchange_response':", exchange_response)
            return redirect("https://t.me/djangoqabot?start=failed-login")

        self.access_token = exchange_response["access_token"]
        return self.get_user_info()

    def get_user_info(self):
        # PHASE 3: Get user info
        # request user info from google api
        # calls self.save_email() in case of success
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo/",
            headers={
                "Authorization": "Bearer " + self.access_token,
            },
        ).json()

        if not "email" in response:
            # TODO: SAVE TO LOGS
            print("ERROR IN 'exchange_response':", response)
            return redirect("https://t.me/djangoqabot?start=failed-login")

        self.email = response["email"]
        return self.save_email()

    def save_email(self):
        # PHASE 4: Save email to DB
        try:
            User.objects.filter(telegram_id=self.tg_id).update(email=self.email)

        except IntegrityError:
            return redirect("https://t.me/djangoqabot?start=failed-login-duplicate")

        else:
            return redirect("https://t.me/djangoqabot?start=successful-login")
