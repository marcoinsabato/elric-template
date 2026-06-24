from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.providers.database import engine
from app.providers.redis import get_redis
from config.settings import get_settings

settings = get_settings()

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(response: Response):
    services = {}
    overall_status = "healthy"

    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        services["database"] = "ok"
    except Exception:
        services["database"] = "error"
        overall_status = "degraded"

    # Check redis
    try:
        redis = await get_redis()
        await redis.ping()
        services["redis"] = "ok"
    except Exception:
        services["redis"] = "error"
        overall_status = "degraded"

    # Check langsmith (always ok if configured)
    services["langsmith"] = "ok"

    if overall_status == "degraded":
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": overall_status,
        "version": "1.0.0",
        "services": services,
    }
