from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .forms import SignUpForm


class RedirectIfAuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            return redirect(self.redirect_to)

        return super().dispatch(request, *args, **kwargs)


class SignUpView(RedirectIfAuthenticatedMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    redirect_to = "pages:homepage"

    def form_valid(self, form):
        response = super().form_valid(form)
        print("user:", self.object, type(self.object))
        # Aktivierungsemail senden (accounts/activate?token=830984093)
        return super().form_valid(form)
