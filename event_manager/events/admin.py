from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class EventInlineAdmin(admin.TabularInline):
    model = models.Event
    fields = ["name", "is_active"]
    readonly_fields = ["name", "is_active"]
    extra = 0
    can_delete = False


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    # Felder, die in der Übersicht angezeigt werden
    # dummy ist eine Methode im Category-Model
    list_display = ("id", "name", "updated_at", "number_events", "dummy")
    search_fields = ["name"]

    # das sind die klickbaren Felder
    list_display_links = ("id", "name")
    inlines = [EventInlineAdmin]

    def number_events(self, obj):
        """Die anzahl an Events einer kategorie.
        obj => Kategorie
        """
        return obj.events.count()


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "author", "category", "is_active")
    list_display_links = ("id", "name")
    # autocomplete_fields = ["category"]  # ??
    search_fields = ("name", "sub_title", "category")  # Suche in diesen Feldern
    actions = ["make_active", "make_inactive"]
    fieldsets = (
        ("Standard info", {"fields": ("name", "date", "category", "author")}),
        (
            "Detail Infos",
            {"fields": ("description", "min_group", "sub_title", "is_active")},
        ),
    )

    @admin.action(description=_("Setze ausgewählte Events active"))
    def make_active(self, request, queryset):
        # queryset => sind die ausgewählten Datensätze
        queryset.update(is_active=True)

    @admin.action(description=_("Setze ausgewählte Events inactive"))
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # print("User:", request.user.username)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)
