import time

last_cache_clear_times = {}

def clear_cache(cached_func, interval_in_seconds: int):
    global last_cache_clear_times
    current_time = time.time()
    last_clear_time = last_cache_clear_times.get(cached_func.__name__, 0)

    if current_time - last_clear_time > interval_in_seconds:
        cached_func.cache_clear()
        last_cache_clear_times[cached_func.__name__] = current_time
