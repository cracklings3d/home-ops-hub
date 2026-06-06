"""Production settings — secure, uses env vars."""
import os
from pathlib import Path

from .base import *  # noqa: F401,F403

DEBUG = False

_secret := os.environ.get("SECRET_KEY")
if not _secret:
    raise ValueError("SECRET_KEY environment variable must be set in production")

SECRET_KEY = _secret

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h.strip()]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}