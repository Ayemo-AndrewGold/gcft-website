from datetime import datetime
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class TimestampRead(BaseModel):
    """Shared id + timestamp fields for all read schemas."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):
    """Single generic envelope replacing Video/Podcast/Gallery list responses."""

    total: int
    count: Optional[int] = None
    items: List[T]

    model_config = ConfigDict(from_attributes=True)
