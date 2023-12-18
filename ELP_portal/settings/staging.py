from typing import Any

import dj_database_url

from ELP_portal.settings.common import (
    ALLOWED_HOSTS,
    CORS_ALLOWED_ORIGINS,
    config,
)

DEBUG = True

ALLOWED_HOSTS += [
    "*",
]

CORS_ALLOWED_ORIGINS += [
    "*",
]

DATABASES: dict[Any, Any] = {
    "default": dj_database_url.config(default=config("DATABASE_URL_STAGING"))
}
