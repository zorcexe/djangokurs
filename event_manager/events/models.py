from functools import partial
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator
from .validators import datetime_in_future


User = get_user_model()  # aktuelles User-Model (siehe settings)


class Category(models.Model):
    """Klasse für eine Event-Kategorie."""

    # beim Anlegen Zeitstempel setzen
    created_at = models.DateTimeField(auto_now_add=True)

    # beim Update Zeitstempel setzen
    updated_at = models.DateTimeField(auto_now=True)
    # x = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    # blank => Kann im Formular leer sein, null => kann in DB null sein
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("Kategorie")
        verbose_name_plural = _("Kategorien")

    def dummy(self) -> str:
        return "abc"

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    """ein spezifischer terminierter Event."""

    class Group(models.IntegerChoices):
        BIG = 10, _("große Gruppe")
        SMALL = 5, _("kleine Gruppe")
        UNLIMITED = 0, _("kein Limit")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True, null=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # Zeitpunkt des Termins (muss in Zukunft liegen)
    date = models.DateTimeField(
        validators=[partial(datetime_in_future, 2)],
    )
    min_group = models.PositiveIntegerField(choices=Group.choices, default=0)

    # related name, um von einem Kategorie-Objekt auf die Events zuzugreifen,
    # z.B. sport.events.all()
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events",
    )
    # bob.events.all()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="events",
    )

    class Meta:
        pass
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=["author", "name", "date"], name="unique_author_event"
        #     ),
        # ]

    def get_absolute_url(self) -> str:
        """Heimseite des Events."""
        return reverse("events:event_detail", args=(self.pk,))

    def __str__(self) -> str:
        return self.name
