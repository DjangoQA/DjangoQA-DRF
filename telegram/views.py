from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .extensions.permissions import TokenPermission
from .actions import start, save_contact, save_username


class WebhookGenericApiView(GenericAPIView):
    permission_classes = [TokenPermission]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.payload = {}
        self.status = status.HTTP_200_OK

    def post(self, request, *args, **kwargs):
        """
        Processes the incoming message and only calls the required Action.
        any message that passed the KeyErrors results as HTTP_200_OK.
        """
        try:
            # required key OR KeyError:
            message = request.data["message"]

            # chat type must be private
            if message["chat"]["type"] == "private":
                # safe keys:
                tg_id = message["chat"]["id"]
                state = cache.get(tg_id)

                if "text" in message:
                    # user sent messsge with text

                    if message["text"] == "/start":
                        # user issued start command

                        self.payload = start(message)
                    elif state == "username":
                        # user send username

                        self.payload = save_username(message)
                elif "contact" in message:
                    # user shared contact

                    self.payload = save_contact(message)
        except KeyError:
            self.status = status.HTTP_400_BAD_REQUEST
            self.payload = "Json structure is not right."
        finally:
            # finale response independent of errors

            return Response(self.payload, self.status)
