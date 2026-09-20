from typing import Optional, List
from pydantic import BaseModel

from app.schemas.common import PaginatedResponse, TimestampRead


class GalleryImageBase(BaseModel):
    public_id: str
    image_url: str
    thumbnail_url: Optional[str] = None
    optimized_url: Optional[str] = None
    title: Optional[str] = None
    caption: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    file_size_bytes: Optional[int] = None
    format: Optional[str] = None
    is_featured: bool = False


class GalleryImageRead(GalleryImageBase, TimestampRead):
    pass


class GalleryImageUpdate(BaseModel):
    title: Optional[str] = None
    caption: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None
    is_featured: Optional[bool] = None


class GalleryImageUploadResponse(BaseModel):
    message: str
    image: GalleryImageRead


class GalleryBulkUploadResponse(BaseModel):
    message: str
    total_uploaded: int
    items: List[GalleryImageRead]


class GalleryListResponse(PaginatedResponse["GalleryImageRead"]):
    pass


class CategoryCount(BaseModel):
    category: str
    count: int


class GalleryCategoriesResponse(BaseModel):
    total_categories: int
    categories: List[CategoryCount]
