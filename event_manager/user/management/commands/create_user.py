"""
Sub-Kommando für das Anlegen von Userns

python manage.py create_user n=10
"""

from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from user.factories import UserFactory


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "-n",
            "--number",
            type=int,
            help="Number of Users to be generated",
            required=True,
        )
        parser.epilog = "Usage: python manage.py create_users -n 10"

    def handle(self, *args, **kwargs):
        number: int = kwargs.get("number")

        # Alle User außer admin löschen
        get_user_model().objects.exclude(username="admin").delete()
        for _ in range(number):
            user = UserFactory()
        print(f"{number} User erfolgreich angelegt.")
