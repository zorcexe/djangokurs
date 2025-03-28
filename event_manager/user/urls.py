from django.urls import path
from django.contrib.auth.views import LoginView
from rest_framework.authtoken.views import obtain_auth_token
from .views import SignUpView

app_name = "user"


urlpatterns = [
    path("token", obtain_auth_token, name="api_token"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
