"""
Projekt-URLs
"""

from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("", include("pages.urls")),
    path("api/events/", include("events.api.urls")),
    path("admin/", admin.site.urls),
    path("events/", include("events.urls")),  # siehe events/urls.py
    path("accounts/", include("user.urls")),  # Signup
    path("accounts/", include("django.contrib.auth.urls")),
] + debug_toolbar_urls()
