from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from app.dependencies import (
    PaginationParams,
    ensure_found,
    get_podcast_pagination_params,
    get_podcast_service,
    verify_api_key,
)
from app.schemas.podcast import PodcastEpisodeRead, PodcastListResponse
from app.services.podcast_service import PodcastService

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.get("", response_model=PodcastListResponse)
def list_podcasts(
    search: Optional[str] = Query(None, description="Search term to filter by title or description"),
    pagination: PaginationParams = Depends(get_podcast_pagination_params),
    service: PodcastService = Depends(get_podcast_service),
):
    """
    Get paginated list of podcast episodes.
    Defaults to the rolling latest 3 episodes for the week.
    Pass custom ?limit=... and ?skip=... to browse the full archive.
    """
    items, total = service.get_episodes(
        skip=pagination.skip,
        limit=pagination.limit,
        search=search,
    )
    return PodcastListResponse(total=total, count=len(items), items=items)



@router.get("/latest", response_model=PodcastEpisodeRead)
def get_latest_podcast(service: PodcastService = Depends(get_podcast_service)):
    """Get the most recently published podcast episode."""
    return ensure_found(service.get_latest_episode(), "No podcast episodes found in archive")


@router.get("/{episode_id}", response_model=PodcastEpisodeRead)
def get_podcast_episode(
    episode_id: int, service: PodcastService = Depends(get_podcast_service)
):
    """Get a single podcast episode by ID."""
    return ensure_found(
        service.get_episode_by_id(episode_id),
        f"Podcast episode with ID {episode_id} not found",
    )


@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_podcasts(
    service: PodcastService = Depends(get_podcast_service),
    _: str = Depends(verify_api_key),
):
    """
    Manually trigger podcast & recordings synchronization.
    Pulls latest recordings from Mixlr v3 recording search API and RSS feed,
    parses metadata, generates embed URLs, and upserts into DB.
    """
    stats = await service.sync_all()
    return {
        "message": f"Sync completed: {stats['total_new']} new, {stats['total_updated']} updated",
        "stats": stats,
    }
