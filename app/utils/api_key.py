import hashlib
import secrets
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import get_settings
from database.models.api_key import ApiKey

settings = get_settings()


def generate_api_key() -> str:
    random_part = secrets.token_urlsafe(32)
    return f"{settings.API_KEY_PREFIX}{random_part}"


def hash_api_key(key: str) -> str:
    return hashlib.sha256(key.encode()).hexdigest()


async def create_api_key_record(name: str, session: AsyncSession) -> tuple[ApiKey, str]:
    key = generate_api_key()
    key_hash = hash_api_key(key)
    prefix = key[:12]

    api_key = ApiKey(
        name=name,
        key_hash=key_hash,
        prefix=prefix,
        is_active=True,
        created_at=datetime.utcnow(),
    )

    session.add(api_key)
    await session.commit()
    await session.refresh(api_key)

    return api_key, key
