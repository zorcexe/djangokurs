from django import forms
from django.core.exceptions import ValidationError

from . import models


class EmailForm(forms.Form):
    """Ein Form, dass nicht von Modelform erbt, zb. Email"""

    name = forms.CharField(max_length=100)


class EventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__"
        exclude = ("author",)

        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d %H:%M"), attrs={"type": "datetime-local"}
            ),
            "min_group": forms.RadioSelect(),
        }

    def clean_sub_title(self) -> str | None:
        """Methode, um den Sub-title zu cleanen/validieren."""
        sub_title: str | None = self.cleaned_data["sub_title"]
        illegal_characters = ("*", "+")
        if isinstance(sub_title, str) and sub_title.startswith(illegal_characters):
            raise ValidationError("Im Substring befinden sich illegale Zeichen")

        return sub_title

    def clean(self):
        """Clean Methode für Kreuzfeld-Validierung."""
        # erstellt das cleaned_data Dictionary,
        # ruft clean_<FELDNAME> auf
        super().clean()

        name = self.cleaned_data["name"]
        sub_title = self.cleaned_data["sub_title"]

        if isinstance(sub_title, str) and isinstance(name, str):
            if "munich" in name and "berlin" in sub_title:

                # Fehler, die an den Feldern direkt angezeigt werden
                self.add_error("name", "Munich ist nicht erlaubt")
                self.add_error("sub_title", "Berlin ist nicht erlaubt")

                raise ValidationError(
                    "Munich im Namen und Berlin im Subtitle ist nicht erlaubt"
                )

        return self.cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = "__all__"

    # message = forms.CharField(max_length=100, required=False)
