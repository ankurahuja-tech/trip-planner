from .base import *

DEBUG = True

SECRET_KEY = env("DJANGO_SECRET_KEY", default="django-insecure$(c%=,/$8C6ku#y+}aw.Sd)2")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "0.0.0.0",
]


DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

INSTALLED_APPS += [
    "debug_toolbar",
]


# E-mail
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

if EMAIL_BACKEND == "django.core.mail.backends.smtp.EmailBackend":
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Django debug_toolbar
MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

# https://stackoverflow.com/questions/26898597/django-debug-toolbar-and-docker
DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG,
}
