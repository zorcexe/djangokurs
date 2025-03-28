import logging
from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    CreateView,
    UpdateView,
)
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from . import models
from .forms import CategoryForm, EventForm


logger = logging.getLogger("django")


def group_check(user) -> bool:
    """
    Boolsche Funktion für den user_passes_test-Decorator
    Wird für functions-basierte Views gentutzt, siehe category_add.
    """
    return user.groups.filter(name="Moderatoren").exists()


def dummy_check(user) -> bool:
    return False


class UserIsOwnerOrModeratorMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return (
            self.get_object().author == self.request.user
            or self.request.user.groups.filter(name="Moderatoren").exists()
        )


class EventDeleteView(SuccessMessageMixin, UserIsOwnerOrModeratorMixin, DeleteView):
    model = models.Event
    success_message = _("Event wurde erfolgreich gelöscht.")
    # Nach Löschen an diese URL weiterleiten:
    success_url = reverse_lazy("events:event_list")
    # Templatename ist: event_confirm_delete.html


class EventUpdateView(SuccessMessageMixin, UserIsOwnerOrModeratorMixin, UpdateView):
    model = models.Event
    form_class = EventForm
    success_message = _("Event wurde erfolgreich editiert.")


class EventCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = models.Event
    form_class = EventForm
    success_message = _("Event wurde erfolgreich angelegt.")
    # generische Templatename: event_form.html

    def form_valid(self, form):
        """Wenn das Formular valide ist, wird diese Methode aufgerufen"""

        # Author ist der angemeldete User, da im Form der User exkludiert
        # wurde
        # logger.error(f"INfo message bla blubb: {self.request.user}")
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Es sind Fehler aufgeteten")
        return super().form_invalid(form)

    def __get_success_url(self) -> str:
        """ERstelle die URL, an die weitergeleitet werden soll nach
        Eintragen in DB.

        nicht nötig, wenn man get_absolute_url importiert hat
        """
        print("Angelegtes Objekt:", self.object)
        return reverse("events:event_detail", args=(self.object.pk,))


class EventDetailView(DetailView):
    # events/3
    # events/event_detail.html , im Template object
    model = models.Event


class EventListView(ListView):
    # Template liegt unter events/event_list.html, im Template object_list
    model = models.Event
    # https://djangoheroes.friendlybytes.net/working_with_forms/create_event_views.html
    queryset = models.Event.objects.select_related("author", "category").all()
    paginate_by = 5  # zeige 10 Events auf einer Seite

    def get_queryset(self) -> QuerySet:
        querystring = self.request.GET.get("q")
        qs = super().get_queryset()

        # Wenn ?name=xx in der URL übergben wurde, filtere nach Name
        if querystring is not None:
            return qs.filter(name__contains=querystring)
        return qs


def category_update(request, pk):
    """View zum Updaten einer Kategorie."""
    # breakpoint()
    category = get_object_or_404(models.Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)

    if form.is_valid():
        category = form.save()
        # Zusätzliches Feld addressieren
        # print("message:", form.cleaned_data["message"])
        return redirect("events:category_detail", category.pk)

    return render(
        request,
        "events/category_create.html",
        {"form": form, "category": category},
    )


# @user_passes_test(group_check)
# @user_passes_test(dummy_check)
def category_create(request):
    """Funktion zum Anlegen einer Kategorie."""
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect("events:category_detail", category.pk)
    else:
        form = CategoryForm()

    return render(
        request,
        "events/category_create.html",
        {"form": form},
    )


def category_detail(request, pk):
    """
    kategorie Detailseite

    events/category/3
    """
    category = get_object_or_404(models.Category, pk=pk)

    return render(
        request,
        "events/category_detail.html",
        {"category": category},
    )


def categories(request):
    """
    Auflistung aller Kategorien

    events/categories
    """
    categories = models.Category.objects.all()

    return render(
        request,
        "events/categories.html",
        {"categories": categories},
    )


def hello(request: HttpRequest) -> HttpResponse:
    """
    events/hello
    """
    print(dir(request))
    print(f"User: {request.user}")
    print(f"Methode: {request.method}")  # GET oder POST
    print(f"Headers: {request.headers}")
    # raise Http404("Address not found") zeigt 404 Fehler an
    return HttpResponse("ja, hallo")
