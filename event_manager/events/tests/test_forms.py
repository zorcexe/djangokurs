"""
Test Event Formular
"""

import uuid
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse

from events.factories import CategoryFactory, EventFactory
from events.models import Category, Event
from user.factories import UserFactory

User = get_user_model()


def create_group(group_name: str) -> Group:
    """Erstelle Gruppe mit Gruppenname."""
    return Group.objects.create(name=group_name)


def create_admin_user():
    # Create a superuser
    random_name = str(uuid.uuid4())
    return User.objects.create_superuser(
        username=random_name, email="admin@example.com", password="adminpass"
    )


def create_user(moderator=False) -> User:
    """Erstelle einen neuen User. Optional einer moderatoren Gruppe"""
    user = UserFactory()
    if moderator:
        moderators_group = create_group("Moderatoren")
        user.groups.add(moderators_group)

    return user


class EventFormTest(TestCase):
    """Create und Update Formulare für Events testen"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = create_user()
        cls.event = EventFactory(author=cls.user)

    def test_event_valid_update(self):
        """Prüfe ob der Autor seinen Event updaten darf."""
        self.client.force_login(self.user)
        url = reverse("events:event_update", args=(self.event.pk,))

        # Aus einem Modelinstanz ein Dict erstellen, um es als Payload für
        # den Update-Request zu nutzen
        pay_load = model_to_dict(self.event, exclude=["author"])
        pay_load["name"] = "aaaa"

        # der einfachheit halber nur POST prüfen
        response = self.client.post(url, pay_load)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        event = Event.objects.get(name=pay_load["name"])
        self.assertEqual(event.name, pay_load["name"])

        # hier noch Redirect und Template prüfen...


class CategoryFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()

    def setUp(self):
        self.pay_load = {
            "name": "Test Kategorien",
            "sub_title": "Test Sub",
            "description": "Test desc",
        }

    def test_create_category(self):
        """Teste, ob Kategorie angelegt werden kann."""
        url = reverse("events:category_create")
        # GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "events/category_create.html")

        # POST
        response = self.client.post(url, self.pay_load)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302
        # Prüfen, ob das Objekt eingetragen wurde in DB
        category = Category.objects.get(name=self.pay_load["name"])
        self.assertEqual(category.name, self.pay_load["name"])

        self.assertRedirects(
            response,
            reverse("events:category_detail", args=(category.pk,)),
            target_status_code=HTTPStatus.OK,
        )


# class EventURLTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.event: Event = EventFactory()
#         cls.client = Client()
