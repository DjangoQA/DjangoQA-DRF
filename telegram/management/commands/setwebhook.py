from requests import post
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Set Webhook for Telegram Bot API"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u", "--url", type=str, help="Telegram bot API Webhook URL"
        )

    def handle(self, *args, **kwargs):
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook"
        if kwargs["url"]:
            url += f"?url={kwargs['url']}"
        self.stdout.write(post(url).text)
