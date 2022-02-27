from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


from .permissions import TokenPermission
from .actions import (
    start_action,
    guest_action,
    login_menu_action,
    username_required_action,
)


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
            tg_id = message["chat"]["id"]
            state = cache.get(tg_id)
            self.dispatcher(state, message)

        return Response(self.payload, status.HTTP_200_OK)

    def dispatcher(self, state, message):
        """
        Simply checks the state and set payload to required action.

        - has nothing to do with 'dispatch' in django.
        """
        
        print("state: ", state)

        if not state or ("text" in message and message["text"] == "/start"):
            # if state is None or /start command entered then start the conversation.
            self.payload = start_action(message)

        elif state == "GUEST":
            self.payload = guest_action(message)

        elif state == "LOGIN-MENU":
            self.payload = login_menu_action(message)

        elif state == "USERNAME-REQUIRED":
            self.payload = username_required_action(message)
