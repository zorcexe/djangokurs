from rest_framework import serializers
from events.models import Category, Event


class EventInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("pk", "name", "date", "author")

    author = serializers.StringRelatedField()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer für die Kategorien mit den Events."""

    # zusätzliches Feld
    events = EventInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"
        # exclude = ("events",)
