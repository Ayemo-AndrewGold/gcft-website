from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.common import PaginatedResponse, TimestampRead


class VideoBase(BaseModel):
    youtube_id: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    published_at: Optional[datetime] = None


class VideoCreate(VideoBase):
    pass


class VideoRead(VideoBase, TimestampRead):
    pass


# Backwards-compatible alias; new code should use PaginatedResponse[VideoRead].
class VideoListResponse(PaginatedResponse["VideoRead"]):
    pass
