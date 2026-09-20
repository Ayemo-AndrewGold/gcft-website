import logging
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.audio_resource import AudioResource
from app.models.ebook import EBook
from app.models.podcast_episode import PodcastEpisode
from app.models.video import Video
from app.schemas.audio_resource import AudioResourceRead
from app.schemas.ebook import EBookRead
from app.schemas.library import LibraryFeaturedResponse
from app.schemas.video import VideoRead

logger = logging.getLogger("gcft_api.services.library")


def format_duration(seconds: Optional[int]) -> Optional[str]:
    if not seconds:
        return None
    mins = seconds // 60
    if mins < 60:
        return f"{mins} mins"
    hours = mins // 60
    rem_mins = mins % 60
    if rem_mins == 0:
        return f"{hours} hr" if hours == 1 else f"{hours} hrs"
    return f"{hours} hr {rem_mins} mins" if hours == 1 else f"{hours} hrs {rem_mins} mins"


class LibraryService:
    """
    Unified aggregator service for the Archives & Media Library homepage section.
    Delivers top featured resources across Audio, E-Books, and YouTube in a single fast query.
    """

    def __init__(self, db: Session, settings=None):
        self.db = db
        self.settings = settings or get_settings()

    def get_featured(self, limit: int = 3) -> LibraryFeaturedResponse:
        # 1. Fetch E-Books (prioritizing is_featured=True, then published_at)
        ebook_query = (
            select(EBook)
            .order_by(EBook.is_featured.desc(), EBook.published_at.desc().nullslast(), EBook.id.desc())
            .limit(limit)
        )
        ebook_records = list(self.db.scalars(ebook_query).all())
        ebooks = [EBookRead.model_validate(eb) for eb in ebook_records]

        # 2. Fetch Audio Resources
        audio_query = (
            select(AudioResource)
            .order_by(
                AudioResource.is_featured.desc(),
                AudioResource.published_at.desc().nullslast(),
                AudioResource.id.desc(),
            )
            .limit(limit)
        )
        audio_records = list(self.db.scalars(audio_query).all())

        # Fallback: if no dedicated audiobooks exist yet, populate from latest podcast episodes
        if not audio_records:
            podcast_query = (
                select(PodcastEpisode)
                .order_by(PodcastEpisode.published_at.desc().nullslast(), PodcastEpisode.id.desc())
                .limit(limit)
            )
            podcast_records = list(self.db.scalars(podcast_query).all())
            audio_items: List[AudioResourceRead] = []
            for ep in podcast_records:
                duration_text = format_duration(ep.duration)

                audio_items.append(
                    AudioResourceRead(
                        id=ep.id,
                        title=ep.title,
                        author="GCFT Media",
                        description=ep.description,
                        category="Sermon Audio",
                        badge_label="SERMON AUDIO",
                        parts_count=1,
                        duration_seconds=ep.duration,
                        duration_text=duration_text,
                        cover_image_url=ep.image_url,
                        audio_url=ep.audio_url,
                        file_size_bytes=ep.file_size_bytes,
                        listen_count=0,
                        is_featured=False,
                        published_at=ep.published_at,
                        created_at=ep.created_at,
                        updated_at=ep.updated_at,
                    )
                )
        else:
            audio_items = [AudioResourceRead.model_validate(ar) for ar in audio_records]

        # 3. Fetch YouTube Videos
        video_query = (
            select(Video)
            .order_by(Video.published_at.desc().nullslast(), Video.id.desc())
            .limit(limit)
        )
        video_records = list(self.db.scalars(video_query).all())
        videos = [VideoRead.model_validate(v) for v in video_records]

        return LibraryFeaturedResponse(audio=audio_items, ebooks=ebooks, videos=videos)
