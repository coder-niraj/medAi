import time
from fastapi import   Request

async def logger(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    process_time = time.time() - start
    print(f"{request.method} {request.url} completed in {process_time:.3f}s")

    return response