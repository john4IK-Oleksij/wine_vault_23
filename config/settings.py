"""
Django settings for Wine Vault project.
Global artisan wine marketplace.
"""

import os
from pathlib import Path
from typing import Any, Literal

import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    try:
        from dotenv import load_dotenv

        load_dotenv(env_file)
    except ImportError:
        with open(env_file, encoding="utf-8") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.getenv(
    "SECRET_KEY",
    "django-insecure-w&ivi0kgt5g4@&g+7g&0qk8(*$-le_092j_ur918*7k!0aw6qg",
)

# DEBUG is True locally, but can be set to False via DJANGO_DEBUG=False on Railway
DEBUG: bool = os.getenv("DJANGO_DEBUG", "True").lower() in ("true", "1")

# Allowed hosts and CSRF trusted origins for Railway and local development
ALLOWED_HOSTS: list[str] = [
    host.strip() for host in os.getenv("ALLOWED_HOSTS", "*").split(",") if host.strip()
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    "https://*.railway.app",
    "http://127.0.0.1",
    "http://localhost",
]


# Application definition

INSTALLED_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Домени Wine Vault:
    "accounts",
    "wines",
]

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "config.urls"

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# Use PostgreSQL from DATABASE_URL if provided (Railway), else fallback to SQLite
database_url: str | None = os.getenv("DATABASE_URL")
if database_url:
    DATABASES: dict[str, dict[str, Any]] = {
        "default": dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES: dict[str, dict[str, Any]] = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
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


# Internationalization (Мова та часовий пояс)
LANGUAGE_CODE: str = "uk"
TIME_ZONE: str = "Europe/Kyiv"
USE_I18N: bool = True
USE_TZ: bool = True


# Static files (CSS, JavaScript, Images)
STATIC_URL: str = "static/"
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"
STATIC_ROOT.mkdir(parents=True, exist_ok=True)

STORAGES: dict[str, dict[str, Any]] = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Default primary key field type
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"

# Маршрути автентифікації сомельє
LOGIN_URL: str = "login"
LOGIN_REDIRECT_URL: str = "wine-list"  # після входу сомельє потрапляє у свій винний льох
LOGOUT_REDIRECT_URL: str = "login"     # після виходу повертаємо на форму входу

# Session Security & Timeout (Обмеження сесії адмінки та сомельє до 24 годин)
SESSION_COOKIE_AGE: int = 86400  # 24 години в секундах (24 * 60 * 60)
SESSION_EXPIRE_AT_BROWSER_CLOSE: bool = False
SESSION_COOKIE_HTTPONLY: bool = True
SESSION_COOKIE_SECURE: bool = not DEBUG
SESSION_COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"

