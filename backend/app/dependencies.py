from functools import lru_cache
from typing import Callable, Optional
from fastapi import Depends, Header, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import get_db

settings = get_settings()


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20


def pagination_params(default_limit: int = 20) -> Callable[..., PaginationParams]:
    """Factory for pagination dependencies — one validation path, per-route defaults."""

    def _dep(
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(
            default_limit, ge=1, le=100, description="Maximum number of records to return"
        ),
    ) -> PaginationParams:
        return PaginationParams(skip=skip, limit=limit)

    return _dep


get_pagination_params = pagination_params(20)
get_podcast_pagination_params = pagination_params(3)


def ensure_found(obj, detail: str):
    """Shared 404 guard so routers don't repeat HTTPException boilerplate."""
    if obj is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return obj


def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Optional/Mandatory API key validation dependency for protected administrative endpoints.
    """
    if not settings.api_key:
        return x_api_key or ""

    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return x_api_key


# -- service factories (inject settings + shared MixlrClient) -----------------

def get_mixlr_client():
    from app.services.mixlr_client import MixlrClient

    return MixlrClient(
        channel_name=settings.mixlr_channel_name,
        channel_id=settings.mixlr_channel_id,
    )


def get_mixlr_service(db: Session = Depends(get_db)):
    from app.services.mixlr_service import MixlrService

    return MixlrService(db, settings=settings, client=get_mixlr_client())


def get_podcast_service(db: Session = Depends(get_db)):
    from app.services.podcast_service import PodcastService

    return PodcastService(db, settings=settings, client=get_mixlr_client())


def get_youtube_client():
    from app.services.youtube_client import YouTubeClient

    return YouTubeClient(
        api_key=settings.youtube_api_key,
        channel_id=settings.youtube_channel_id,
    )


@lru_cache()
def get_youtube_live_cache():
    """App-wide shared YouTube live cache (protects the 100-unit live check)."""
    from app.services.youtube_service import YouTubeLiveCache

    return YouTubeLiveCache()


def get_youtube_service(db: Session = Depends(get_db)):
    from app.services.youtube_service import YouTubeService

    return YouTubeService(
        db, settings=settings, client=get_youtube_client(), cache=get_youtube_live_cache()
    )
