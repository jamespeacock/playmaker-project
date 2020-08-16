"""
Django settings for api project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from distutils.util import strtobool

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))

# ONLY SET MY_HOST in prod
HOSTNAME = os.environ.get('MY_HOST', 'http://localhost:5000')
FRONTEND = os.environ.get('MY_HOST', 'http://localhost:3000')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tvlz#$1m-b4mdr=g%o!*bv7*t=+jr#q-m1$$)l(uezk^_$7508'

# SPOTIFY
SPOTIFY_CLIENT_ID = '06fdc33f688440e6bff40f6eb930f21c'
SPOTIFY_CLIENT_SECRET = 'f83c328423054a73a3daa9ae9045e538'
SPOTIFY_REDIRECT_URI = HOSTNAME + '/api/login/get_auth'
READ_LIBRARY = 'user-library-read playlist-modify-public user-read-recently-played user-top-read '
CONTROL_PLAYBACK = 'streaming user-modify-playback-state app-remote-control user-read-playback-state user-read-currently-playing '
CONTROL_FOLLOW = 'user-follow-read user-follow-modify'
SPOTIFY_SCOPE = READ_LIBRARY + CONTROL_PLAYBACK + CONTROL_FOLLOW
# Scope for future (playback): ["user-read-birthdate", "user-read-email", "user-read-private"]
DEFAULT_MS_ADDITION = 500
DEFAULT_MS_OFFSET = DEFAULT_MS_ADDITION * 5
DEFAULT_INACTIVE_LEN = 300  # (seconds)
TURN_OFF_IDLE_CONTROLLERS = True  # TODO fix last_active or active check before turning on.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.environ.get("DEBUG", "True"))

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'feedback',
    'playmaker',
    'playmaker.controller',
    'playmaker.listener',
    'playmaker.login',
    'playmaker.playlists',
    'playmaker.rooms',
    'playmaker.songs',
    'rest_auth',
    'rest_auth.registration',
    'rest_framework',
    'rest_framework.authtoken',
]

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Playmaker Team <noreply@playmaker.social>'

SITE_ID = int(os.environ.get("SITE_ID", 1))

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_COOKIE_NAME = "csrftoken"

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'api._urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'templates')],
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

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'playmaker',
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'test'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_USER_MODEL = "playmaker.User"
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
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'social_core.backends.spotify.SpotifyOAuth2',
)

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'playmaker.shared.utils.exception_handler'
}

# LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/var/www/static/'
STATIC_ROOT = STATIC_URL
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
STATICFILES_DIRS = [
    '/static/',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}