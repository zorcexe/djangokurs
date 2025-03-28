"""
Testen der öffentlichen URLS
"""

from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from events.factories import CategoryFactory, EventFactory
from events.models import Category, Event


class CategoryURLTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # cls.category = CategoryFactory()
        cls.event: Event = EventFactory()

    def setUp(self):
        # wird vor jedem Test ausgeführt
        self.client = Client()

    def test_category_overview_public(self):
        """Testen, ob die Kategorieseite öffentlich zugänglich ist."""
        url = reverse("events:categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, text=self.event.category.name)
        self.assertTemplateUsed(response, "events/categories.html")

    def test_category_detail(self):
        url = reverse("events:category_detail", args=(self.event.category.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        # more tests here ...


class EventURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.event: Event = EventFactory()
        cls.client = Client()

    def test_if_create_event_non_public(self):
        """Prüfen, ob ein anonymer user zum Login weitergeleitet wird,
        wenn ein Create aufgerufen wird."""
        url = reverse("events:event_create")  # Anlegen eines Events
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            "/accounts/login/?next=/events/create",
            target_status_code=HTTPStatus.OK,
        )

    def test_if_create_event_logged_in(self):
        """Prüfen ob eingeloggter User das Event-Create Formular nutzen kann."""
        url = reverse("events:event_create")
        # eingeloggter Client:
        self.client.force_login(self.event.author)
        # mit eingeloggtem User Request abfeuern:
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "events/event_form.html")
