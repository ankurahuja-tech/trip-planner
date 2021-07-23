from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / 'trip_planner'

# django-environ
env = environ.Env()
environ.Env.read_env(env_file='.env')

# ==============================================================================
# CORE SETTINGS
# ==============================================================================

SECRET_KEY = env('DJANGO_SECRET_KEY')

DEBUG = env.bool('DJANGO_DEBUG', False)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

SITE_ID = 1

# ==============================================================================
# APPS SETTINGS
# ==============================================================================

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    # django-allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

LOCAL_APPS = [
    'trip_planner.accounts.apps.AccountsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ==============================================================================
# MIDDLEWARE SETTINGS
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# TEMPLATES SETTINGS
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================================================================
# DATABASES SETTINGS
# ==============================================================================

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


# ==============================================================================
# AUTHENTICATION AND AUTHORIZATION SETTINGS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNATIONALIZATION SETTINGS
# ==============================================================================

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ==============================================================================
# STATIC FILES SETTINGS
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [APPS_DIR / 'static',]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# ==============================================================================
# MEDIA FILES SETTINGS
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = APPS_DIR / 'media'

# ==============================================================================
# THIRD-PARTY SETTINGS
# ==============================================================================

# django-allauth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]