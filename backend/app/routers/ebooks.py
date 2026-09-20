from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from app.dependencies import (
    ensure_found,
    get_ebook_service,
    get_pagination_params,
    PaginationParams,
    verify_api_key,
)
from app.schemas.ebook import EBookCreate, EBookListResponse, EBookRead, EBookUpdate
from app.services.ebook_service import EBookService

router = APIRouter(prefix="/ebooks", tags=["E-Books"])

ALLOWED_DOCUMENT_TYPES = {
    "application/pdf",
    "application/epub+zip",
    "application/x-epub",
    "application/octet-stream",
}

ALLOWED_COVER_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/avif",
}


@router.get("", response_model=EBookListResponse)
def list_ebooks(
    category: Optional[str] = Query(None, description="Filter by book category"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    search: Optional[str] = Query(None, description="Search in title, author, description"),
    pagination: PaginationParams = Depends(get_pagination_params),
    service: EBookService = Depends(get_ebook_service),
):
    """Get paginated list of downloadable church e-books and study guides."""
    items, total = service.get_ebooks(
        skip=pagination.skip,
        limit=pagination.limit,
        category=category,
        is_featured=is_featured,
        search=search,
    )
    return EBookListResponse(total=total, count=len(items), items=items)


@router.get("/{ebook_id}", response_model=EBookRead)
def get_ebook(ebook_id: int, service: EBookService = Depends(get_ebook_service)):
    """Get single e-book details by ID."""
    return ensure_found(service.get_ebook_by_id(ebook_id), f"E-Book with ID {ebook_id} not found")


@router.post("", response_model=EBookRead, status_code=status.HTTP_201_CREATED)
def create_ebook(
    payload: EBookCreate,
    service: EBookService = Depends(get_ebook_service),
    _: str = Depends(verify_api_key),
):
    """Create an e-book entry directly with an existing download URL (Admin protected)."""
    return service.create_ebook(payload)


@router.post("/upload", response_model=EBookRead, status_code=status.HTTP_201_CREATED)
async def upload_ebook(
    file: UploadFile = File(..., description="PDF or EPUB document file"),
    cover: Optional[UploadFile] = File(None, description="Optional cover image (JPG, PNG, WebP)"),
    title: str = Form(..., description="Book title"),
    author: Optional[str] = Form(None, description="Author name"),
    description: Optional[str] = Form(None, description="Book overview/synopsis"),
    category: Optional[str] = Form(None, description="Category name"),
    badge_label: Optional[str] = Form("DIGITAL PDF & EPUB", description="UI badge tag"),
    format_label: Optional[str] = Form("Free Theological Resource", description="Format tag"),
    page_count: Optional[int] = Form(None, description="Total page count"),
    is_featured: bool = Form(False, description="Pin to featured section"),
    service: EBookService = Depends(get_ebook_service),
    _: str = Depends(verify_api_key),
):
    """Upload e-book file (and optional cover) to Cloudinary and register in database (Admin)."""
    if file.content_type and file.content_type not in ALLOWED_DOCUMENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported: PDF, EPUB.",
        )
    if cover and cover.content_type and cover.content_type not in ALLOWED_COVER_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid cover type '{cover.content_type}'. Supported: JPEG, PNG, WebP, GIF, AVIF.",
        )

    file_bytes = await file.read()
    cover_bytes = await cover.read() if cover else None

    return await service.upload_and_create(
        file_bytes=file_bytes,
        filename=file.filename or "document.pdf",
        title=title,
        cover_bytes=cover_bytes,
        cover_filename=cover.filename if cover else None,
        author=author,
        description=description,
        category=category,
        badge_label=badge_label,
        format_label=format_label,
        page_count=page_count,
        is_featured=is_featured,
    )


@router.put("/{ebook_id}", response_model=EBookRead)
def update_ebook(
    ebook_id: int,
    payload: EBookUpdate,
    service: EBookService = Depends(get_ebook_service),
    _: str = Depends(verify_api_key),
):
    """Update e-book metadata (Admin protected)."""
    updated = service.update_ebook(ebook_id, payload)
    return ensure_found(updated, f"E-Book with ID {ebook_id} not found")


@router.post("/{ebook_id}/download")
def download_ebook(ebook_id: int, service: EBookService = Depends(get_ebook_service)):
    """Increment download statistics and retrieve download URL."""
    ebook = service.increment_download(ebook_id)
    ensure_found(ebook, f"E-Book with ID {ebook_id} not found")
    return {
        "id": ebook.id,
        "title": ebook.title,
        "download_url": ebook.download_url,
        "download_count": ebook.download_count,
    }


@router.delete("/{ebook_id}", status_code=status.HTTP_200_OK)
def delete_ebook(
    ebook_id: int,
    service: EBookService = Depends(get_ebook_service),
    _: str = Depends(verify_api_key),
):
    """Delete an e-book entry (Admin protected)."""
    deleted = service.delete_ebook(ebook_id)
    ensure_found(deleted or None, f"E-Book with ID {ebook_id} not found")
    return {"message": f"Successfully deleted e-book {ebook_id}"}
