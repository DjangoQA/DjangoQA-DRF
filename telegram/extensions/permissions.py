from rest_framework import permissions
from django.conf import settings


class TokenPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.kwargs["token"] == settings.TELEGRAM_BOT_ENDPOINT
