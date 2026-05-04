from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

# 1. Initialize the limiter
# 'key_func' tells the limiter to track users by their IP address
limiter = Limiter(key_func=get_remote_address)
