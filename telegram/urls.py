from django.urls import path

from .views import *

app_name = "telegram"

urlpatterns = [
    path("webhook/<token>/", WebhookGenericApiView.as_view(), name="webhook"),
]
