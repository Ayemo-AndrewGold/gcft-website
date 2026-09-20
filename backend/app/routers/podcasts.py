from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_podcast_pagination_params, PaginationParams, verify_api_key
from app.schemas.podcast import PodcastEpisodeRead, PodcastListResponse
from app.services.podcast_service import PodcastService

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.get("", response_model=PodcastListResponse)
def list_podcasts(
    search: Optional[str] = Query(None, description="Search term to filter by title or description"),
    pagination: PaginationParams = Depends(get_podcast_pagination_params),
    db: Session = Depends(get_db),
):
    """
    Get paginated list of podcast episodes.
    Defaults to the rolling latest 3 episodes for the week.
    Pass custom ?limit=... and ?skip=... to browse the full archive.
    """
    service = PodcastService(db)
    items, total = service.get_episodes(
        skip=pagination.skip,
        limit=pagination.limit,
        search=search,
    )
    return PodcastListResponse(total=total, count=len(items), items=items)



@router.get("/latest", response_model=PodcastEpisodeRead)
def get_latest_podcast(db: Session = Depends(get_db)):
    """Get the most recently published podcast episode."""
    service = PodcastService(db)
    episode = service.get_latest_episode()
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No podcast episodes found in archive",
        )
    return episode


@router.get("/{episode_id}", response_model=PodcastEpisodeRead)
def get_podcast_episode(episode_id: int, db: Session = Depends(get_db)):
    """Get a single podcast episode by ID."""
    service = PodcastService(db)
    episode = service.get_episode_by_id(episode_id)
    if not episode:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Podcast episode with ID {episode_id} not found",
        )
    return episode


@router.post("/sync", status_code=status.HTTP_200_OK)
def sync_podcasts(
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Manually trigger podcast & recordings synchronization.
    Pulls latest recordings from Mixlr v3 recording search API and RSS feed,
    parses metadata, generates embed URLs, and upserts into DB.
    """
    service = PodcastService(db)
    stats = service.sync_all()
    return {
        "message": f"Sync completed: {stats['total_new']} new, {stats['total_updated']} updated",
        "stats": stats,
    }
