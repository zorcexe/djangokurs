"""
eine User-Fabrik zum Testen und Anlegen von Usern im System.
"""

import factory
from typing import Final
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

DEFAULT_PASSWORD: Final = "abc"
user_name_list = ["bob", "alice", "trudy", "mallory", "eve", "grumpy"]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = factory.Iterator(user_name_list)
    email = factory.Faker(provider="email")
    password = factory.LazyFunction(lambda: make_password(DEFAULT_PASSWORD))
