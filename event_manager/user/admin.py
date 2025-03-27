from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Detailseite Felder für Admin (Anpassen des Fieldsets für Admin)
    fieldsets = UserAdmin.fieldsets
    fieldsets += (("Additional info", {"fields": ("address",)}),)
