from datetime import datetime

import structlog
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from app.providers.database import AsyncSessionLocal
from app.providers.redis import get_redis
from app.utils.api_key import hash_api_key
from config.settings import get_settings
from database.models.api_key import ApiKey

settings = get_settings()
logger = structlog.get_logger()


class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/health" or request.url.path.startswith("/test-errors"):
            return await call_next(request)

        if request.client and request.client.host in ("127.0.0.1", "localhost", "::1") and request.client.port == 8000:
            logger.debug("api_key.skipped", reason="localhost", client_host=request.client.host)
            return await call_next(request)


        api_key_header = request.headers.get(settings.API_KEY_HEADER)

        if not api_key_header:
            return JSONResponse(
                status_code=HTTP_401_UNAUTHORIZED,
                content={"detail": "API key missing"},
            )


        key_hash = hash_api_key(api_key_header)
        redis = await get_redis()

        cached_key_id = await redis.get(f"apikey:{key_hash}")

        if cached_key_id:
            request.state.api_key_id = cached_key_id
            logger.info("api_key.validated", source="cache", api_key_id=cached_key_id)
            return await call_next(request)

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ApiKey).where(ApiKey.key_hash == key_hash)
            )
            api_key = result.scalar_one_or_none()

            if not api_key:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid API key"},
                )

            if not api_key.is_active:
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "API key is inactive"},
                )

            if api_key.expires_at and api_key.expires_at < datetime.utcnow():
                return JSONResponse(
                    status_code=HTTP_401_UNAUTHORIZED,
                    content={"detail": "API key has expired"},
                )

            api_key.last_used_at = datetime.utcnow()
            session.add(api_key)
            await session.commit()

            await redis.setex(f"apikey:{key_hash}", 300, str(api_key.id))

            request.state.api_key_id = str(api_key.id)
            logger.info("api_key.validated", source="database", api_key_id=str(api_key.id))

        return await call_next(request)
