import time

import structlog
from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.providers.redis import get_redis
from config.settings import get_settings

settings = get_settings()
logger = structlog.get_logger()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health":
            return await call_next(request)

        if not hasattr(request.state, "api_key_id"):
            return await call_next(request)

        api_key_id = request.state.api_key_id
        redis = await get_redis()

        window = int(time.time() / settings.RATE_LIMIT_WINDOW)
        key = f"ratelimit:{api_key_id}:{window}"

        count = await redis.incr(key)

        if count == 1:
            await redis.expire(key, settings.RATE_LIMIT_WINDOW)

        if count > settings.RATE_LIMIT_REQUESTS:
            logger.warning(
                "rate_limit.exceeded",
                api_key_id=api_key_id,
                count=count,
                limit=settings.RATE_LIMIT_REQUESTS,
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        logger.debug(
            "rate_limit.checked",
            api_key_id=api_key_id,
            count=count,
            limit=settings.RATE_LIMIT_REQUESTS,
        )

        return await call_next(request)
