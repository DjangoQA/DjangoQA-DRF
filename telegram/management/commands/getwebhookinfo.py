from requests import post
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Use this Command to get current webhook status. Requires no parameters"

    def handle(self, *args, **kwargs):
        self.stdout.write(post(f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/setWebhook").text)
