from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.common import PaginatedResponse, TimestampRead


class AudioResourceBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    badge_label: Optional[str] = None
    parts_count: Optional[int] = None
    duration_seconds: Optional[int] = None
    duration_text: Optional[str] = None
    cover_image_url: Optional[str] = None
    audio_url: str
    file_size_bytes: Optional[int] = None
    is_featured: bool = False
    published_at: Optional[datetime] = None


class AudioResourceCreate(AudioResourceBase):
    pass


class AudioResourceUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    badge_label: Optional[str] = None
    parts_count: Optional[int] = None
    duration_seconds: Optional[int] = None
    duration_text: Optional[str] = None
    cover_image_url: Optional[str] = None
    audio_url: Optional[str] = None
    file_size_bytes: Optional[int] = None
    is_featured: Optional[bool] = None
    published_at: Optional[datetime] = None


class AudioResourceRead(AudioResourceBase, TimestampRead):
    listen_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class AudioResourceListResponse(PaginatedResponse[AudioResourceRead]):
    pass
