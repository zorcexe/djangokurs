from pathlib import Path
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7v3#_$=6lq^l8g63rra-4k!wp7dkf=xzpx6+wh@9kzv4vr9$1("

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["example.com", "localhost", "127.0.0.1", "*"]


MESSAGE_TAGS = {
    messages.DEBUG: "alert-secondary",  # bootstrap css klasse
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# Nach Login und Logout weiterleiten
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


INSTALLED_APPS = [
    "user",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "rest_framework",
    "rest_framework.authtoken",
    "events",
    "pages",
]

if DEBUG:
    INSTALLED_APPS.extend(
        [
            "debug_toolbar",
            "django_extensions",
        ]
    )

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
MIDDLEWARE.extend(["debug_toolbar.middleware.DebugToolbarMiddleware"])

ROOT_URLCONF = "event_manager.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "event_manager/templates"],
        "APP_DIRS": True,  # suche in den Apps nach Templates
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Crispy Forms
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

# ASGI_APPLICATION =  ...
WSGI_APPLICATION = "event_manager.wsgi.application"

# ab Django 4.2
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# Beim Entwickeln Passwort-Vallidierung rausnehmen
if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ]
else:
    AUTH_PASSWORD_VALIDATORS = []


# User Model
AUTH_USER_MODEL = "user.User"

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "de-de"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ("en", _("English")),
    ("de", _("German")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# der physische Ort, wo die Daten liegen
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Alle statischen Dateien sammeln mit: python manage.py collectstatic
STATIC_ROOT = BASE_DIR / "staticfiles"  # aus Versionierung ausschließen!

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
