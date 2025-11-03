from __future__ import annotations

import time
from collections import defaultdict, deque
from functools import wraps
from typing import Callable, Deque, Dict

from flask import current_app, request
from werkzeug.exceptions import TooManyRequests


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._requests: Dict[str, Deque[float]] = defaultdict(deque)

    def check(self, key: str, limit: int, window: int) -> None:
        now = time.time()
        bucket = self._requests[key]
        while bucket and now - bucket[0] > window:
            bucket.popleft()
        if len(bucket) >= limit:
            raise TooManyRequests("Too many requests, please try again later.")
        bucket.append(now)


limiter = InMemoryRateLimiter()


def limit_auth_route(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        window = current_app.config.get("RATELIMIT_WINDOW_SECONDS", 60)
        limit = current_app.config.get("RATELIMIT_AUTH", 5)
        key = f"auth:{request.remote_addr or 'unknown'}:{request.endpoint}"
        limiter.check(key, limit, window)
        return func(*args, **kwargs)

    return wrapper
