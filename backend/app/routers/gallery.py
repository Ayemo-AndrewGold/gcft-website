from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import ensure_found, get_pagination_params, PaginationParams, verify_api_key
from app.schemas.gallery import (
    GalleryImageRead,
    GalleryImageUpdate,
    GalleryImageUploadResponse,
    GalleryBulkUploadResponse,
    GalleryListResponse,
    GalleryCategoriesResponse,
)
from app.services.gallery_service import GalleryService

router = APIRouter(prefix="/gallery", tags=["Gallery"])

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/avif",
    "image/heic",
}


@router.get("", response_model=GalleryListResponse)
def list_gallery_images(
    category: Optional[str] = Query(None, description="Filter images by category (e.g. services, youth, outreach)"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status for homepage showcase"),
    search: Optional[str] = Query(None, description="Search term matching title, caption, category, or tags"),
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
):
    """
    Get paginated gallery images with optional category, featured, and search filters.
    Includes both thumbnail and web-optimized responsive variants.
    """
    service = GalleryService(db)
    items, total = service.get_images(
        skip=pagination.skip,
        limit=pagination.limit,
        category=category,
        is_featured=is_featured,
        search=search,
    )
    return GalleryListResponse(total=total, count=len(items), items=items)


@router.get("/categories", response_model=GalleryCategoriesResponse)
def get_gallery_categories(db: Session = Depends(get_db)):
    """Get list of distinct gallery categories with image counts for frontend filter tabs."""
    service = GalleryService(db)
    categories = service.get_categories()
    return GalleryCategoriesResponse(total_categories=len(categories), categories=categories)


@router.get("/{image_id}", response_model=GalleryImageRead)
def get_gallery_image(image_id: int, db: Session = Depends(get_db)):
    """Get detailed metadata for a single gallery image."""
    service = GalleryService(db)
    return ensure_found(
        service.get_image_by_id(image_id),
        f"Gallery image with ID {image_id} not found",
    )


@router.post("/upload", response_model=GalleryImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_gallery_image(
    file: UploadFile = File(..., description="Image file to upload (JPEG, PNG, WebP, etc.)"),
    title: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    is_featured: bool = Form(False),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Upload a single image to Cloudinary and store metadata with responsive URLs.
    Protected by API key (X-API-Key).
    """
    if file.content_type and file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported: JPEG, PNG, WebP, GIF, AVIF, HEIC.",
        )

    service = GalleryService(db)
    content = await file.read()
    image_record = await service.upload_and_save(
        file_content=content,
        title=title,
        caption=caption,
        category=category,
        tags=tags,
        is_featured=is_featured,
    )
    return GalleryImageUploadResponse(
        message="Image uploaded and optimized successfully",
        image=image_record,
    )


@router.post("/upload/bulk", response_model=GalleryBulkUploadResponse, status_code=status.HTTP_201_CREATED)
async def bulk_upload_gallery_images(
    files: List[UploadFile] = File(..., description="Multiple image files to upload"),
    category: Optional[str] = Form(None),
    is_featured: bool = Form(False),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Upload multiple images in a batch.
    Automatically assigns category and extracts titles from filenames.
    Protected by API key (X-API-Key).
    """
    if not files:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No files provided for upload.")

    service = GalleryService(db)
    file_tuples = []
    for f in files:
        if f.content_type and f.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File '{f.filename}' has unsupported type '{f.content_type}'.",
            )
        content = await f.read()
        file_tuples.append((f.filename or "image", content))

    uploaded_records = await service.bulk_upload(
        files=file_tuples,
        category=category,
        default_is_featured=is_featured,
    )

    return GalleryBulkUploadResponse(
        message=f"Successfully uploaded {len(uploaded_records)} images",
        total_uploaded=len(uploaded_records),
        items=uploaded_records,
    )


@router.patch("/{image_id}", response_model=GalleryImageRead)
def update_gallery_image(
    image_id: int,
    update_data: GalleryImageUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Update metadata (title, caption, category, tags, featured status) for a gallery image.
    Protected by API key (X-API-Key).
    """
    service = GalleryService(db)
    return ensure_found(
        service.update_image(
            image_id=image_id,
            title=update_data.title,
            caption=update_data.caption,
            category=update_data.category,
            tags=update_data.tags,
            is_featured=update_data.is_featured,
        ),
        f"Gallery image with ID {image_id} not found",
    )


@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Delete a gallery image from Cloudinary and database.
    Protected by API key (X-API-Key).
    """
    service = GalleryService(db)
    success = service.delete_image(image_id)
    ensure_found(success or None, f"Gallery image with ID {image_id} not found")
    return {"message": f"Gallery image {image_id} deleted successfully"}
