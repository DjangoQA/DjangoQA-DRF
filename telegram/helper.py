import requests
from django.conf import settings


def get_authorize_url(tg_id: str) -> str:
    return settings.TELEGRAM_OATH_BASE_URL + "".join(
        [
            f"{k}={v}&"
            for k, v in {
                "response_type": settings.TELEGRAM_OATH_RESPONSE_TYPE,
                "client_id": settings.TELEGRAM_OATH_CLIENT_ID,
                "redirect_uri": settings.TELEGRAM_OATH_REDIRECT_URI,
                "scope": settings.TELEGRAM_OATH_SCOPE,
                "state": tg_id,
            }.items()
        ]
    )


def exchange_authorization_code(code: str) -> dict:
    return requests.post(
        "https://www.googleapis.com/oauth2/v4/token",
        data={
            "code": code,
            "client_id": settings.TELEGRAM_OATH_CLIENT_ID,
            "client_secret": settings.TELEGRAM_OATH_CLIENT_SECRET,
            "redirect_uri": settings.TELEGRAM_OATH_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
    ).json()
