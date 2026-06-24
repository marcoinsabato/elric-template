import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ApiKey(SQLModel, table=True):
    __tablename__ = "api_keys"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    key_hash: str = Field(unique=True)
    prefix: str
    is_active: bool = Field(default=True)
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
