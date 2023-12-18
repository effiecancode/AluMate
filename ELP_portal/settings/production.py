# WARNING: DO NOT UPDATE ANYTHING IN THIS FILE UNLESS \
# VERIFIED BY A PEER

from .common import (
    config,
    os,
)
from .common import *


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "https://elpportal-9sefci4sz-elptechhub.vercel.app",
    "http://elpportal.s3-website-us-east-1.amazonaws.com",
    "https://elpportal.s3-website-us-east-1.amazonaws.com",
    "https://techhub-portal-frontend-v2-sepia.vercel.app",
    "https://1-elpportal.vercel.app",
    "https://miniature-space-system-j9pg7v74v7gfp4r-3000.app.github.dev"
]

CORS_ORIGIN_WHITELIST = [
    "http://localhost:3000",
    "http://localhost",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "https://elpportal-9sefci4sz-elptechhub.vercel.app",
    "http://elpportal.s3-website-us-east-1.amazonaws.com",
    "https://elpportal.s3-website-us-east-1.amazonaws.com",
    "https://techhub-portal-frontend-v2-sepia.vercel.app",
    "https://1-elpportal.vercel.app",
    "https://miniature-space-system-j9pg7v74v7gfp4r-3000.app.github.dev"
]
# SECURITY WARNING: don't run with debug turned on in production!
# Setting debug to true for troubleshooting.
DEBUG = True
ALLOWED_HOSTS = ["*"]

# SET SECRET_KEY DEPENDING ON ENVIRONMENT
# config = USED BY HEROKU
# os.environ = USED BY GITHUB SECRETS

if "SECRET_KEY" not in os.environ:
    SECRET_KEY = config("SECRET_KEY")
else:
    SECRET_KEY = os.environ["SECRET_KEY"]

# VALUES BEING USED FROM GITHUB SECRETS. CONFIG CANNOT BE USED. DO NOT
# UPDATE THE CODE.

# AWS S3 settings

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["RDS_DB_NAME"]
        if "RDS_DB_NAME" in os.environ
        else config("RDS_DB_NAME"),
        "USER": os.environ["RDS_USERNAME"]
        if "RDS_USERNAME" in os.environ
        else config("RDS_USERNAME"),
        "PASSWORD": os.environ["RDS_PASSWORD"]
        if "RDS_PASSWORD" in os.environ
        else config("RDS_PASSWORD"),
        "HOST": os.environ["RDS_HOSTNAME"]
        if "RDS_HOSTNAME" in os.environ
        else config("RDS_HOSTNAME"),
        "PORT": os.environ["RDS_PORT"]
        if "RDS_PORT" in os.environ
        else config("RDS_PORT"),
    }
}
