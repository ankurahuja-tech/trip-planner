from .base import *

DEBUG = True

SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure$(c%=,/$8C6ku#y+}aw.Sd)2')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS += ['debug_toolbar',]

# Django debug_toolbar
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]

INTERNAL_IPS = [
    '127.0.0.1',
]