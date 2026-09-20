from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class VideoBase(BaseModel):
    youtube_id: str
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    published_at: Optional[datetime] = None


class VideoCreate(VideoBase):
    pass


class VideoRead(VideoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VideoListResponse(BaseModel):
    total: int
    items: List[VideoRead]
