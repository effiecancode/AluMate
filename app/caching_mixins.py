from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils.cache import get_cache_key
from functools import wraps

# Load the time to live set in the settings file
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

class CacheMixin:
    """
    A mixin class to add caching behavior to views.
    """

    def cache_view(self, view_func):
        """
        Apply caching to a view function.

        This method returns a decorator that applies caching to a view function.
        The caching behavior is based on the cache timeout specified in the
        application's settings.

        Args:
            view_func (function): The view function to which caching will be applied.

        Returns:
            function: A decorated version of the original view function with caching.
        """
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            # Generate a custom cache key based on view name, arguments, and kwargs
            cache_key = get_cache_key(request, key_prefix=f"custom_cache_prefix:{view_func.__name__}")

            # Check if the result is already cached
            result = cache.get(cache_key)
            if result is None:
                # If not cached, execute the original view function and cache the result
                result = view_func(*args, **kwargs)
                cache.set(cache_key, result, CACHE_TTL)
            return result

        return wrapped_view
