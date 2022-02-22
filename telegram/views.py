from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from telegram.payloads.callbacks import login, welcome

from .permissions import TokenPermission
from .actions import start, contact_required, username_required, phone_login


class WebhookGenericApiView(GenericAPIView):
    permission_classes = [TokenPermission]

    def post(self, request, *args, **kwargs):
        """
        Processes the incoming message and only calls the required Action.
        """
        self.payload = {}

        # process the incoming message
        if (
            "message" in request.data
            and request.data["message"]["chat"]["type"] == "private"
        ):
            message = request.data["message"]

            # now its safe to get chat_id key.
            tg_id = message["chat"]["id"]

            # get the state from cache using tg_id.
            state = cache.get(tg_id)

            # detecting Start command ->
            if not state or ("text" in message and message["text"] == "/start"):
                # if state is None, we need to call start action.
                self.payload = start(message)

            elif state == "contact_required":
                self.payload = contact_required(message)

            elif state == "username_required":
                self.payload = username_required(message)

            elif state == "menu":
                # TODO: show menu
                pass

        elif "callback_query" in request.data:
            # now its safe to get below keys.
            callback = request.data["callback_query"]
            tg_id = callback["message"]["chat"]["id"]
            message_id = callback["message"]["message_id"]
            data = callback["data"]

            if data == "welcome":
                self.payload = welcome(tg_id, message_id)
            if data == "login":
                self.payload = login(tg_id, message_id)

        return Response(self.payload, status.HTTP_200_OK)
