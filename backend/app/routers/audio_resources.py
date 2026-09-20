from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status

from app.dependencies import (
    ensure_found,
    get_audio_resource_service,
    get_pagination_params,
    PaginationParams,
    verify_api_key,
)
from app.schemas.audio_resource import (
    AudioResourceCreate,
    AudioResourceListResponse,
    AudioResourceRead,
    AudioResourceUpdate,
)
from app.services.audio_resource_service import AudioResourceService

router = APIRouter(prefix="/audio-resources", tags=["Audio Resources"])

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/x-m4a",
    "audio/wav",
    "audio/x-wav",
    "audio/webm",
    "audio/ogg",
}

ALLOWED_COVER_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/avif",
}


@router.get("", response_model=AudioResourceListResponse)
def list_audio_resources(
    category: Optional[str] = Query(None, description="Filter by audio category"),
    is_featured: Optional[bool] = Query(None, description="Filter by featured status"),
    search: Optional[str] = Query(None, description="Search in title, narrator, description"),
    pagination: PaginationParams = Depends(get_pagination_params),
    service: AudioResourceService = Depends(get_audio_resource_service),
):
    """Get paginated list of curated church audiobooks, audio series, and devotionals."""
    items, total = service.get_audio_resources(
        skip=pagination.skip,
        limit=pagination.limit,
        category=category,
        is_featured=is_featured,
        search=search,
    )
    return AudioResourceListResponse(total=total, count=len(items), items=items)


@router.get("/{resource_id}", response_model=AudioResourceRead)
def get_audio_resource(
    resource_id: int, service: AudioResourceService = Depends(get_audio_resource_service)
):
    """Get single audio resource details by ID."""
    return ensure_found(
        service.get_audio_resource_by_id(resource_id),
        f"Audio Resource with ID {resource_id} not found",
    )


@router.post("", response_model=AudioResourceRead, status_code=status.HTTP_201_CREATED)
def create_audio_resource(
    payload: AudioResourceCreate,
    service: AudioResourceService = Depends(get_audio_resource_service),
    _: str = Depends(verify_api_key),
):
    """Create an audio resource directly with an existing stream/audio URL (Admin protected)."""
    return service.create_audio_resource(payload)


@router.post("/upload", response_model=AudioResourceRead, status_code=status.HTTP_201_CREATED)
async def upload_audio_resource(
    file: UploadFile = File(..., description="MP3, M4A, or WAV audio file"),
    cover: Optional[UploadFile] = File(None, description="Optional album/series cover image"),
    title: str = Form(..., description="Audio title"),
    author: Optional[str] = Form(None, description="Narrator / Speaker name"),
    description: Optional[str] = Form(None, description="Overview / description"),
    category: Optional[str] = Form(None, description="Category name"),
    badge_label: Optional[str] = Form("AUDIO BOOK", description="UI badge tag"),
    parts_count: Optional[int] = Form(None, description="Number of parts / episodes in series"),
    duration_text: Optional[str] = Form(None, description="Formatted duration, e.g. '3 hrs 45 mins'"),
    duration_seconds: Optional[int] = Form(None, description="Duration in seconds"),
    is_featured: bool = Form(False, description="Pin to featured section"),
    service: AudioResourceService = Depends(get_audio_resource_service),
    _: str = Depends(verify_api_key),
):
    """Upload audio track (and optional cover) to Cloudinary and save record in database (Admin)."""
    if file.content_type and file.content_type not in ALLOWED_AUDIO_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type '{file.content_type}'. Supported: MP3, M4A, WAV, OGG, WebM.",
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
        filename=file.filename or "track.mp3",
        title=title,
        cover_bytes=cover_bytes,
        cover_filename=cover.filename if cover else None,
        author=author,
        description=description,
        category=category,
        badge_label=badge_label,
        parts_count=parts_count,
        duration_seconds=duration_seconds,
        duration_text=duration_text,
        is_featured=is_featured,
    )


@router.put("/{resource_id}", response_model=AudioResourceRead)
def update_audio_resource(
    resource_id: int,
    payload: AudioResourceUpdate,
    service: AudioResourceService = Depends(get_audio_resource_service),
    _: str = Depends(verify_api_key),
):
    """Update audio resource metadata (Admin protected)."""
    updated = service.update_audio_resource(resource_id, payload)
    return ensure_found(updated, f"Audio Resource with ID {resource_id} not found")


@router.post("/{resource_id}/listen")
def track_listen(
    resource_id: int, service: AudioResourceService = Depends(get_audio_resource_service)
):
    """Increment listen statistics for an audio track."""
    resource = service.increment_listen(resource_id)
    ensure_found(resource, f"Audio Resource with ID {resource_id} not found")
    return {
        "id": resource.id,
        "title": resource.title,
        "listen_count": resource.listen_count,
    }


@router.delete("/{resource_id}", status_code=status.HTTP_200_OK)
def delete_audio_resource(
    resource_id: int,
    service: AudioResourceService = Depends(get_audio_resource_service),
    _: str = Depends(verify_api_key),
):
    """Delete an audio resource entry (Admin protected)."""
    deleted = service.delete_audio_resource(resource_id)
    ensure_found(deleted or None, f"Audio Resource with ID {resource_id} not found")
    return {"message": f"Successfully deleted audio resource {resource_id}"}
