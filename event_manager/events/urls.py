"""
Event-URLs
"""

from django.urls import path, re_path

# from .views import hello
from . import views

app_name = "events"  # im Template auf die App zugreifen
# im Template: events:hello

# Hinweis: für komplexe URLs kann man re_path (regex path)
# events/pattern/a23-4334343
# pattern = r"^pattern/(?P<number>[a-z]{1,2}\d{2}-\d*)"


urlpatterns = [
    # re_path(pattern, views.hello)
    # Kategorien
    path("categories", views.categories, name="categories"),
    path("category/<int:pk>", views.category_detail, name="category_detail"),
    path("category/create", views.category_create, name="category_create"),
    path("category/update/<int:pk>", views.category_update, name="category_update"),
    # Events
    path("", views.EventListView.as_view(), name="event_list"),
    path("<int:pk>", views.EventDetailView.as_view(), name="event_detail"),
    path("create", views.EventCreateView.as_view(), name="event_create"),
    path("update/<int:pk>", views.EventUpdateView.as_view(), name="event_update"),
    path("delete/<int:pk>", views.EventDeleteView.as_view(), name="event_delete"),
]
