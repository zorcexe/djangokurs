import random
from typing import Final
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from events.factories import EventFactory, CategoryFactory
from events.models import Event, Category

NUMBER_CATEGORIES: Final = 12
NUMBER_EVENTS: Final = 100


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # Lösche Kategorien und Events
        Category.objects.all().delete()
        print("Kategorien und Events wurden erfolgreich gelöscht")

        categories = CategoryFactory.create_batch(NUMBER_CATEGORIES)
        users = get_user_model().objects.all()

        for _ in range(NUMBER_EVENTS):
            EventFactory(
                category=random.choice(categories),
                author=random.choice(users),
            )

        print(f"{NUMBER_EVENTS} Events erfolgreich angelegt")
