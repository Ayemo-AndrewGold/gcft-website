from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_pagination_params, PaginationParams, verify_api_key
from app.schemas.gallery import GalleryImageRead, GalleryImageUploadResponse, GalleryListResponse
from app.services.gallery_service import GalleryService

router = APIRouter(prefix="/gallery", tags=["Gallery"])


@router.get("", response_model=GalleryListResponse)
def list_gallery_images(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
):
    """Get paginated list of gallery images."""
    service = GalleryService(db)
    items, total = service.get_images(skip=pagination.skip, limit=pagination.limit)
    return GalleryListResponse(total=total, items=items)


@router.post("/upload", response_model=GalleryImageUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_gallery_image(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    caption: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Upload an image file to Cloudinary and record in database."""
    service = GalleryService(db)
    content = await file.read()
    image_record = service.upload_and_save(
        file_content=content,
        title=title,
        caption=caption,
    )
    return GalleryImageUploadResponse(
        message="Image uploaded successfully",
        image=image_record,
    )


@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
def delete_gallery_image(
    image_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Delete a gallery image from Cloudinary and database."""
    service = GalleryService(db)
    success = service.delete_image(image_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gallery image with ID {image_id} not found",
        )
    return {"message": f"Gallery image {image_id} deleted successfully"}
