import logging
import time
from datetime import datetime, timezone
from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.live_status import LiveStatus
from app.models.video import Video
from app.schemas.live import LivePlatformStatus
from app.services.base import BaseService
from app.services.youtube_client import YouTubeClient

logger = logging.getLogger("gcft_api.services.youtube")


def extract_video_id(url: Optional[str]) -> Optional[str]:
    """Extract a YouTube video id from watch, embed, short-link, live and shorts URLs."""
    if not url:
        return None
    if "/embed/" in url:
        return url.split("/embed/")[-1].split("?")[0].split("/")[0] or None
    if "watch?v=" in url:
        return url.split("watch?v=")[-1].split("&")[0] or None
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0].split("/")[0] or None
    for marker in ("/live/", "/shorts/"):
        if marker in url:
            return url.split(marker)[-1].split("?")[0].split("/")[0] or None
    return None


class YouTubeLiveCache:
    """Mutable live-status cache shared across per-request service instances.

    A single instance is provided app-wide (see ``get_youtube_live_cache``),
    so the 100-quota-unit live check stays cached between requests while the
    service itself remains stateless and test-friendly (tests inject a fresh
    holder instead of poking class attributes).
    """

    def __init__(self):
        self.status: Optional[LivePlatformStatus] = None
        self.expires_at: float = 0.0
        self.manual_override: bool = False

    def get(self, now: float) -> Optional[LivePlatformStatus]:
        if self.status is not None and now < self.expires_at:
            return self.status
        return None

    def set(self, status: LivePlatformStatus, ttl_seconds: float, *, manual: bool = False) -> None:
        self.status = status
        self.expires_at = time.time() + ttl_seconds
        self.manual_override = manual

    def clear(self) -> None:
        self.status = None
        self.expires_at = 0.0
        self.manual_override = False


class YouTubeService(BaseService[Video]):
    def __init__(
        self,
        db: Session,
        settings=None,
        client: Optional[YouTubeClient] = None,
        cache: Optional[YouTubeLiveCache] = None,
    ):
        super().__init__(db, settings or get_settings())
        self.client = client or YouTubeClient(
            api_key=self.settings.youtube_api_key,
            channel_id=self.settings.youtube_channel_id,
        )
        self.cache = cache or YouTubeLiveCache()
        self.cache_ttl = getattr(self.settings, "youtube_live_cache_seconds", 180)
        # Manual admin overrides outlive the API polling window.
        self.manual_cache_ttl = 86400

    # -- Videos Database Operations ---------------------------------------

    def get_videos(self, skip: int = 0, limit: int = 20) -> Tuple[List[Video], int]:
        """Fetch paginated videos sorted by publication date descending."""
        query = select(Video).order_by(Video.published_at.desc().nullslast(), Video.id.desc())
        return self.paginate(query, skip=skip, limit=limit)

    def get_video_by_id(self, video_id: int) -> Optional[Video]:
        """Fetch a single video by primary key."""
        return self.get_by_id(Video, video_id)

    def get_video_by_youtube_id(self, youtube_id: str) -> Optional[Video]:
        """Fetch a single video by its YouTube videoId."""
        query = select(Video).where(Video.youtube_id == youtube_id)
        return self.db.scalars(query).first()

    async def fetch_and_upsert_videos(self, max_results: Optional[int] = None) -> int:
        """
        Fetch latest uploads using the channel's uploads playlist (1 quota unit)
        and upsert them into the database.
        """
        if not self.client.is_configured:
            logger.warning("YouTube API key or Channel ID not configured.")
            return 0

        limit = max_results or getattr(self.settings, "youtube_recordings_sync_limit", 25)
        recordings = await self.client.fetch_recent_recordings(max_results=limit)
        if not recordings:
            logger.info("No recordings returned from YouTube uploads playlist.")
            return 0

        upserted_count = 0
        for rec in recordings:
            yt_id = rec["youtube_id"]
            existing = self.get_video_by_youtube_id(yt_id)

            if not existing:
                video = Video(
                    youtube_id=yt_id,
                    title=rec["title"],
                    description=rec["description"],
                    thumbnail_url=rec["thumbnail_url"],
                    published_at=rec["published_at"],
                )
                self.db.add(video)
                upserted_count += 1
            else:
                existing.title = rec["title"]
                existing.description = rec["description"]
                if rec["thumbnail_url"]:
                    existing.thumbnail_url = rec["thumbnail_url"]
                if rec["published_at"]:
                    existing.published_at = rec["published_at"]
                upserted_count += 1

        self.db.commit()
        logger.info(f"Upserted {upserted_count} YouTube videos.")
        return upserted_count

    # -- Live Status Operations -------------------------------------------

    def get_db_live_status(self, platform: str = "youtube") -> Optional[LiveStatus]:
        """Fetch the latest persisted live status record for YouTube."""
        query = (
            select(LiveStatus)
            .where(LiveStatus.platform == platform)
            .order_by(LiveStatus.updated_at.desc())
            .limit(1)
        )
        return self.db.scalars(query).first()

    async def fetch_live_status(self, force_refresh: bool = False) -> LivePlatformStatus:
        """
        Get live broadcasting state.
        Uses the shared in-memory cache to strictly preserve quota (100 units/call).
        Falls back to database record if external API fails.
        """
        if force_refresh:
            self.cache.manual_override = False

        now = time.time()
        if not force_refresh:
            cached = self.cache.get(now)
            if cached is not None:
                return cached

        if not self.client.is_configured:
            return self._fallback_from_db()

        result = await self.client.fetch_live_status()
        if result is None:
            logger.warning("YouTube live status check failed; falling back to DB.")
            return self._fallback_from_db()

        self._persist_status_to_db(result)
        self.cache.set(result, self.cache_ttl)
        return result

    def _fallback_from_db(self) -> LivePlatformStatus:
        """Fallback to the last known database record when external API fails or is unconfigured."""
        status_rec = self.get_db_live_status("youtube")
        if not status_rec:
            return LivePlatformStatus(
                is_live=False,
                channel_name=self.client.channel_name,
                stream_url=self.client.livepage_url,
                embed_url=None,
            )

        video_id = extract_video_id(status_rec.embed_url or status_rec.stream_url)
        return LivePlatformStatus(
            is_live=status_rec.is_live,
            video_id=video_id,
            title=status_rec.stream_title,
            stream_url=status_rec.stream_url or self.client.livepage_url,
            embed_url=status_rec.embed_url,
            channel_name=status_rec.channel_name or self.client.channel_name,
            channel_logo_url=status_rec.channel_logo_url,
            channel_artwork_url=status_rec.channel_artwork_url,
            started_at=status_rec.started_at,
        )

    def _persist_status_to_db(self, live_info: LivePlatformStatus):
        """Save latest live broadcast info to DB without failing the request on DB error."""
        try:
            status_rec = self.get_db_live_status("youtube")
            if not status_rec:
                status_rec = LiveStatus(
                    platform="youtube",
                    is_live=live_info.is_live,
                    stream_title=live_info.title,
                    stream_url=live_info.stream_url,
                    embed_url=live_info.embed_url,
                    channel_name=live_info.channel_name,
                    channel_logo_url=live_info.channel_logo_url,
                    channel_artwork_url=live_info.channel_artwork_url,
                    started_at=live_info.started_at,
                )
                self.db.add(status_rec)
            else:
                status_rec.is_live = live_info.is_live
                status_rec.stream_title = live_info.title
                status_rec.stream_url = live_info.stream_url
                status_rec.embed_url = live_info.embed_url
                status_rec.channel_name = live_info.channel_name
                status_rec.channel_logo_url = live_info.channel_logo_url
                status_rec.channel_artwork_url = live_info.channel_artwork_url
                status_rec.started_at = live_info.started_at

            self.db.commit()
        except Exception as dbe:
            self.db.rollback()
            logger.warning(f"Could not persist YouTube live status to DB: {dbe}")

    def update_manual_status(
        self,
        is_live: Optional[bool] = None,
        title: Optional[str] = None,
        stream_url: Optional[str] = None,
        embed_url: Optional[str] = None,
        video_id: Optional[str] = None,
        clear_override: bool = False,
    ) -> LivePlatformStatus:
        """Manually override or update YouTube live status (e.g. by church media admin)."""
        if clear_override:
            self.cache.clear()
            return self._fallback_from_db()

        status_rec = self.get_db_live_status("youtube")

        final_embed_url = embed_url
        final_stream_url = stream_url
        if video_id:
            if not final_embed_url:
                final_embed_url = f"https://www.youtube.com/embed/{video_id}"
            if not final_stream_url:
                final_stream_url = f"https://www.youtube.com/watch?v={video_id}"

        if not status_rec:
            status_rec = LiveStatus(
                platform="youtube",
                is_live=is_live if is_live is not None else False,
                stream_title=title,
                stream_url=final_stream_url or self.client.livepage_url,
                embed_url=final_embed_url,
                channel_name=self.client.channel_name,
            )
            self.db.add(status_rec)
        else:
            if is_live is not None:
                status_rec.is_live = is_live
            if title is not None:
                status_rec.stream_title = title
            if final_stream_url is not None:
                status_rec.stream_url = final_stream_url
            if final_embed_url is not None:
                status_rec.embed_url = final_embed_url

        self.db.commit()
        self.db.refresh(status_rec)

        manual_status = LivePlatformStatus(
            is_live=status_rec.is_live,
            video_id=video_id or extract_video_id(status_rec.embed_url or status_rec.stream_url),
            title=status_rec.stream_title,
            stream_url=status_rec.stream_url,
            embed_url=status_rec.embed_url,
            channel_name=status_rec.channel_name or self.client.channel_name,
            channel_logo_url=status_rec.channel_logo_url,
            channel_artwork_url=status_rec.channel_artwork_url,
            started_at=status_rec.started_at,
        )

        self.cache.set(manual_status, self.manual_cache_ttl, manual=True)
        return manual_status
