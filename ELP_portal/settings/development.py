from .common import (
    BASE_DIR,
    config,
)
from .common import *

DEBUG = config("DEBUG", cast=bool)

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
]

ALLOWED_HOSTS = ["*", ".localhost", ".ngrok.io", "127.0.0.1"]
CORS_ORIGIN_ALLOW_ALL = True

SECRET_KEY = config("SECRET_KEY")

# Uncomment this if you prefer using SQLite3 db

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR + ".db",
#     }
# }

# Uncomment this if you prefer using PostgreSQL db

# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    },
    'test': { # All tests are carried out on this db
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('TEST_DB_NAME', default='test_elpportal'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    },
}
