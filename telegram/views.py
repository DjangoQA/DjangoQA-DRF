from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .extensions.permissions import TokenPermission
from .actions import start, contact_required, username_required


class WebhookGenericApiView(GenericAPIView):
    permission_classes = [TokenPermission]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.payload = {}
        self.status = status.HTTP_200_OK

    def post(self, request, *args, **kwargs):
        """
        Processes the incoming message and only calls the required Action.
        any message that passed the KeyErrors return HTTP_200_OK.
        """
        try:
            # required key OR KeyError:
            message = request.data["message"]

            # chat type must be private.
            if message["chat"]["type"] == "private":
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

        except KeyError:
            self.status = status.HTTP_400_BAD_REQUEST
            self.payload = "Json structure is not right."
        finally:
            # finale response independent of errors
            return Response(self.payload, self.status)
