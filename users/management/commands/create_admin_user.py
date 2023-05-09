from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from users.models import User


class Command(BaseCommand):
    help = "Create Admin User"

    def handle(self, *args, **kwargs):
        User.objects.create_superuser(username="admin_test", password="12345")

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin test created! | username: admin_test | password:12345"
            )
        )
