from datetime import datetime
from typing import Optional
from pydantic import BaseModel, computed_field

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
    @computed_field
    @property
    def watch_url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.youtube_id}"

    @computed_field
    @property
    def embed_url(self) -> str:
        return f"https://www.youtube.com/embed/{self.youtube_id}"


# Backwards-compatible alias; new code should use PaginatedResponse[VideoRead].
class VideoListResponse(PaginatedResponse["VideoRead"]):
    pass
