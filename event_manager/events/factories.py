import factory
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from . import models

categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    """Erstellt ein Kategorie-Objekt aus der Liste."""

    class Meta:
        model = models.Category
        django_get_or_create = ("name",)

    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence", locale="de_DE")
    description = factory.Faker("paragraph", nb_sentences=2)


class EventFactory(factory.django.DjangoModelFactory):
    """Erstellt ein Event-Objekt aus der Liste."""

    class Meta:
        model = models.Event

    name = factory.Faker("sentence", locale="de_DE")
    description = factory.Faker("paragraph", locale="de_DE", nb_sentences=2)
    sub_title = factory.Faker("sentence", locale="de_DE")
    date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=30))
    min_group = factory.LazyAttribute(
        lambda _: random.choice(list(models.Event.Group.values))
    )
    # nur für Testing (langsam bei vielen Objekten! Besser Übergabe
    # beim Instanziieren, siehe events/factories.py)
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory("user.factories.UserFactory")
