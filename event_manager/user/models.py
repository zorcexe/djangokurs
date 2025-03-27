from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Eigenes Usermodel. Muss in den settings registriert werden.

    AUTH_USER_MODEL = 'user.User'
    """

    address = models.CharField(max_length=200, blank=True, null=True)
    # activation_token = models.CharField(max_length=200, blank=True, null=True)
