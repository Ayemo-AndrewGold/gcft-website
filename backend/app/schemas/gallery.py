from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class GalleryImageBase(BaseModel):
    public_id: str
    image_url: str
    title: Optional[str] = None
    caption: Optional[str] = None


class GalleryImageRead(GalleryImageBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GalleryImageUploadResponse(BaseModel):
    message: str
    image: GalleryImageRead


class GalleryListResponse(BaseModel):
    total: int
    items: List[GalleryImageRead]
