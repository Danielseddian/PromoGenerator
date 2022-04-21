from datetime import timedelta
from pathlib import Path
from os import environ
from os.path import join

BASE_DIR = Path(__file__).resolve().parent.parent

context_processors = "django.template.context_processors."
contrib = "django.contrib."
middleware = "django.middleware."
password_validation = contrib + "auth.password_validation."

DJANGO_APPS = [
    contrib + "admin",
    contrib + "auth",
    contrib + "contenttypes",
    contrib + "sessions",
    contrib + "messages",
    contrib + "staticfiles",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
]

LOCAL_APPS = [
    "generator.apps.GeneratorConfig",
]

OTHER_APPS = [
    "djoser",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + OTHER_APPS

MIDDLEWARE = [
    middleware + "security.SecurityMiddleware",
    contrib + "sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    middleware + "common.CommonMiddleware",
    middleware + "csrf.CsrfViewMiddleware",
    contrib + "auth.middleware.AuthenticationMiddleware",
    contrib + "messages.middleware.MessageMiddleware",
    middleware + "clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                context_processors + "debug",
                context_processors + "request",
                contrib + "auth.context_processors.auth",
                contrib + "messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": environ.get("DB_NAME", "db.sqlite3"),
        "USER": environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": environ.get("DB_HOST", "localhost"),
        "PORT": environ.get("DB_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": password_validation + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": password_validation + "MinimumLengthValidator",
    },
    {
        "NAME": password_validation + "CommonPasswordValidator",
    },
    {
        "NAME": password_validation + "NumericPasswordValidator",
    },
]

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(days=30)}

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_URLS_REGEX = r"^/generator/.*$"

STATIC_ROOT = join(BASE_DIR, "back_static")

STATIC_URL = "/back_static/"

MEDIA_ROOT = join(BASE_DIR, "media")

MEDIA_URL = "/media/"

SECRET_KEY = environ.get("SECRET_KEY", "some_secret_key")

DEBUG = environ.get("DEBUG", True)

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost web 127.0.0.1").split()

WSGI_APPLICATION = "PromoGenerator.wsgi.application"

ROOT_URLCONF = "PromoGenerator.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
