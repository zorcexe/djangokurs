from django.urls import path
from django.contrib.auth.views import LoginView
from .views import SignUpView

app_name = "user"

urlpatterns = [
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
