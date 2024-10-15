from functools import wraps
from collections import deque


class LRUCache:
    def __init__(self, capacity=100):
        """
        Initialize the LRUCache with a specified capacity.

        Args:
            capacity (int): Maximum number of key-value pairs to be stored in the cache.
        """
        self.capacity = capacity
        self.cache = dict()
        self.lru_queue = deque()

    def get(self, key):
        """
        Retrieve a value from the cache based on the provided key.

        Args:
            key: Key to look up in the cache.

        Returns:
            Value corresponding to the key if found, else None.
        """
        if key in self.cache:
            self.lru_queue.remove(key)
            self.lru_queue.append(key)
            return self.cache[key]
        return None

    def put(self, key, value):
        """
        Add a new key-value pair to the cache or update an existing one.

        Args:
            key: Key to be added or updated.
            value: Value corresponding to the key.
        """
        if key in self.cache:
            self.lru_queue.remove(key)
        elif len(self.cache) >= self.capacity:
            lru_key = self.lru_queue.popleft()
            del self.cache[lru_key]

        self.cache[key] = value
        self.lru_queue.append(key)


def cached_generator(capacity=100):
    """
    Create a decorator for caching generator function results using an LRUCache.

    Args:
        capacity (int): Maximum number of key-value pairs to be stored in the cache.

    Returns:
        A decorator function that caches the results of the provided generator function. The first argument of the decorated function is considered as the key for caching.
    """
    cache = LRUCache(capacity)

    def decorator(func):
        @wraps(func)
        def wrapper(key, *args, **kwargs):
            value = cache.get(key)
            if value is not None:
                for element in value:
                    yield element
            else:
                new_value = []
                for element in func(key, *args, **kwargs):
                    new_value.append(element)
                    yield element
                cache.put(key, new_value)

        return wrapper

    return decorator
