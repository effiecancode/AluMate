from decouple import config

if config("ENVIRONMENT", default=False) == "development":
    from .development import *  # noqa F403, F401
elif config("ENVIRONMENT", default=False) == "staging":
    from .staging import *  # noqa F403, F401
else:
    from .production import *  # noqa F403, F401
