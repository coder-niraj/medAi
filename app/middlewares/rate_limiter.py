from datetime import datetime, timedelta, timezone
from typing import Any

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request
from dataclasses import dataclass

from middlewares import idempotency


def get_rate_limit_key(request: Request) -> str:
    # Use user_id if authenticated, fall back to IP for guests
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return str(user_id)
    return get_remote_address(request)


limiter = Limiter(
    key_func=get_rate_limit_key, default_limits=["60/minute"]  # applies to all routes
)
