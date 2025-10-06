from datetime import datetime, timezone, timedelta
import os

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "600"))
in_memory_cache = {}

def get_cached(key: str) -> any:
    if key in in_memory_cache:
        value, timestamp = in_memory_cache[key]
        if datetime.now(timezone.utc) - timestamp < timedelta(seconds=CACHE_TTL_SECONDS):
            return value
        del in_memory_cache[key]
    return None

def set_cached(key: str, value: any):
    in_memory_cache[key] = (value, datetime.now(timezone.utc))
