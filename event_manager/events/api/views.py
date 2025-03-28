from rest_framework import generics, permissions, authentication
from events.models import Category
from . import serializers


class CategoryListCreateApiView(generics.ListCreateAPIView):
    """Auflisten und Anlegen von Kategorien via Api.

    TOken Auth:
    curl http://127.0.0.1:8000/api/events/categories -H "Authorization: Token 183922d..."


    """

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class CategoryRetrieveAPiView(generics.RetrieveUpdateDestroyAPIView):
    """Holen, Löschen und Updaten einer Kategorie"""

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
