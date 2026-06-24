from typing import Optional

from redis.asyncio import Redis

from config.settings import get_settings

settings = get_settings()

redis_client: Optional[Redis] = None


async def init_redis():
    global redis_client
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return redis_client


async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        redis_client = None
