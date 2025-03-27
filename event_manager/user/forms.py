from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        labels = {"privacy": "Datenschutzerklärung"}

    privacy = forms.BooleanField(required=False)

    def clean_privacy(self):
        """Die Datenschutzerklärung muss angeglickt werden, ansonsten wird ein
        ValidationError ausgelöst"""

        privacy = self.cleaned_data["privacy"]
        if not privacy:
            raise ValidationError(
                """Bitte bestätigen Sie, dass Sie die
                Datenschutzerklärung gelesen haben!"""
            )
        return privacy
