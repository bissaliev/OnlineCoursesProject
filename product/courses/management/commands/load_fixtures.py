from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

User = get_user_model()

BASE_DIR = settings.BASE_DIR


class Command(BaseCommand):
    help = "load fixtures"

    def load_fixtures(self):
        dirname = BASE_DIR / "fixtures"
        fixtures = [
            "users.json",
            "courses.json",
            "groups.json",
            "lessons.json",
            "subscriptions.json",
        ]
        for fixture in fixtures:
            fixture_path = dirname / fixture
            call_command("loaddata", fixture_path)
            self.stdout.write(
                self.style.SUCCESS(f"Фикстура {fixture} загружена!")
            )

    def handle(self, *args, **options):
        self.load_fixtures()
