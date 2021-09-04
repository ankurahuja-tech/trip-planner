from .base import *

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0", ".herokuapp.com"]

USE_DB = env.bool("USE_DB", default=False)

if USE_DB:
    DATABASES = {
        "default": env.db(),
    }
    # https://stackoverflow.com/questions/12538510/getting-databaseoperations-object-has-no-attribute-geo-db-type-error-when-do
    DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

if EMAIL_BACKEND != "django.core.mail.backends.console.EmailBackend":
    EMAIL_HOST = env("EMAIL_HOST")
    EMAIL_HOST_USER = env("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# https://stackoverflow.com/questions/41483068/djangos-httpresponseredirect-is-http-instead-of-https/41488430
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True


# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================
USE_WHITENOISE = env.bool("USE_WHITENOISE", default=False)

if USE_WHITENOISE:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
    whitenoise_middleware_index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware") + 1
    MIDDLEWARE.insert(whitenoise_middleware_index, "whitenoise.middleware.WhiteNoiseMiddleware")
