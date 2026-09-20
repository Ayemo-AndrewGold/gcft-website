from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import ensure_found, get_pagination_params, PaginationParams, verify_api_key
from app.schemas.video import VideoRead, VideoListResponse
from app.services.youtube_service import YouTubeService

router = APIRouter(prefix="/videos", tags=["Videos"])


@router.get("", response_model=VideoListResponse)
def list_videos(
    pagination: PaginationParams = Depends(get_pagination_params),
    db: Session = Depends(get_db),
):
    """Get paginated list of videos."""
    service = YouTubeService(db)
    items, total = service.get_videos(skip=pagination.skip, limit=pagination.limit)
    return VideoListResponse(total=total, count=len(items), items=items)


@router.get("/{video_id}", response_model=VideoRead)
def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get a single video by ID."""
    service = YouTubeService(db)
    return ensure_found(service.get_video_by_id(video_id), f"Video with ID {video_id} not found")


@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_videos(
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """Manually trigger YouTube API synchronization."""
    service = YouTubeService(db)
    count = await service.fetch_and_upsert_videos()
    return {"message": f"Successfully synchronized {count} videos"}
