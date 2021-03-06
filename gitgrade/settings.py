"""
Django settings for gitgrade project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
debug_str = os.environ.get("DJANGO_DEBUG", "True")
DEBUG = debug_str.lower() == "true"
print(f"{DEBUG=}")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "repo",
    "bootstrap5",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gitgrade.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "gitgrade", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "gitgrade.context_processors.github_sso_url",
                "gitgrade.context_processors.github_username",
                "gitgrade.context_processors.gitgrade_version",
            ],
        },
    },
]

WSGI_APPLICATION = "gitgrade.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASE_USERNAME = os.environ.get("DATABASE_USERNAME", "invalid_default")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "invalid_default")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "database")

if not DEBUG and "invalid_default" in (DATABASE_USERNAME, DATABASE_PASSWORD):
    raise Exception("DATABASE_USERNAME and DATABASE_PASSWORD required when not in DEBUG mode.")

TEST_DATABASE = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": BASE_DIR / "db.sqlite3",
}

PRODUCTION_DATABASE = {
    "ENGINE": "django.db.backends.postgresql_psycopg2",
    "NAME": "gitgrade",
    "USER": DATABASE_USERNAME,
    "PASSWORD": DATABASE_PASSWORD,
    "HOST": DATABASE_HOST,
    "PORT": "5432",
}

DATABASES = {"default": TEST_DATABASE if DEBUG else PRODUCTION_DATABASE}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "gitgrade", "static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Formatting: https://docs.python.org/3/library/string.html#formatspec
# Attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes
# Date Formatting: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{asctime} {filename}:{lineno:<d} {name} {levelname:>8s}: {message}",
            "style": "{",
            "datefmt": "%X",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "git": {"level": "WARNING"},
        "github": {"level": "WARNING"},
        "urllib3": {"level": "WARNING"},
    },
}

# SSO Settings

GITGRADE_BASE_URL = os.environ.get("GITGRADE_BASE_URL", "https://gitigrade.net")
GITHUB_SSO_CLIENT_ID = os.environ.get("GITHUB_SSO_CLIENT_ID", "invalid_default")
GITHUB_SSO_CLIENT_SECRET = os.environ.get("GITHUB_SSO_CLIENT_SECRET", "invalid_default")
GITHUB_TOKEN_KEY = "github_token"
