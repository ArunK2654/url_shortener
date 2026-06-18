from fastapi import HTTPException
from .redis_client import redis_client
from .logger import logger

LIMIT = 3
WINDOW = 60


def check_rate_limit(ip: str):
    key = f"rate_limit:{ip}"

    count = redis_client.incr(key)

    if count == 1:
        redis_client.expire(key, WINDOW)

    if count > LIMIT:
        logger.warning(
            f"rate_limit_exceeded ip={ip}"
        )
        raise HTTPException(status_code=429,detail="Rate limit exceeded")