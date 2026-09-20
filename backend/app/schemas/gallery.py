from typing import Optional
from pydantic import BaseModel

from app.schemas.common import PaginatedResponse, TimestampRead


class GalleryImageBase(BaseModel):
    public_id: str
    image_url: str
    title: Optional[str] = None
    caption: Optional[str] = None


class GalleryImageRead(GalleryImageBase, TimestampRead):
    pass


class GalleryImageUploadResponse(BaseModel):
    message: str
    image: GalleryImageRead


class GalleryListResponse(PaginatedResponse["GalleryImageRead"]):
    pass
