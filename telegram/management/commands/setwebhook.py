from requests import post
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Set Webhook for Telegram Bot API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url", type=str, help="Telegram bot API Webhook HOST-ONLY url."
        )

    def handle(self, *args, **kwargs):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
        if kwargs["url"]:
            url += f"?url={kwargs['url']}/{settings.TELEGRAM_BOT_ENDPOINT}/"
        self.stdout.write(post(url).text)
