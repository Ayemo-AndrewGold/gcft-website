from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.common import PaginatedResponse, TimestampRead


class EBookBase(BaseModel):
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    badge_label: Optional[str] = None
    format_label: Optional[str] = None
    page_count: Optional[int] = None
    cover_image_url: Optional[str] = None
    download_url: str
    file_size_bytes: Optional[int] = None
    is_featured: bool = False
    published_at: Optional[datetime] = None


class EBookCreate(EBookBase):
    pass


class EBookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    badge_label: Optional[str] = None
    format_label: Optional[str] = None
    page_count: Optional[int] = None
    cover_image_url: Optional[str] = None
    download_url: Optional[str] = None
    file_size_bytes: Optional[int] = None
    is_featured: Optional[bool] = None
    published_at: Optional[datetime] = None


class EBookRead(EBookBase, TimestampRead):
    download_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class EBookListResponse(PaginatedResponse[EBookRead]):
    pass
