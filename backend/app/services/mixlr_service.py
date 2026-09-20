"""Live-status service: cache + DB persistence around MixlrClient HTTP."""

import logging
import time
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.live_status import LiveStatus
from app.schemas.live import LivePlatformStatus, LiveStatusRead
from app.services.base import BaseService
from app.services.mixlr_client import MixlrClient

logger = logging.getLogger("gcft_api.services.mixlr")


class MixlrService(BaseService[LiveStatus]):
    """Thin orchestrator: MixlrClient fetches/parses, this class caches + persists."""

    def __init__(
        self,
        db: Session,
        settings=None,
        client: Optional[MixlrClient] = None,
    ):
        super().__init__(db, settings or get_settings())
        self.client = client or MixlrClient(
            channel_name=self.settings.mixlr_channel_name,
            channel_id=self.settings.mixlr_channel_id,
        )
        self.cache_ttl = self.settings.mixlr_live_cache_seconds
        self._cached_status: Optional[LivePlatformStatus] = None
        self._cache_expires_at: float = 0.0

    # -- DB ---------------------------------------------------------------

    def get_db_live_status(self, platform: str = "mixlr") -> Optional[LiveStatus]:
        """Fetch the most recent persisted live status for a platform."""
        query = (
            select(LiveStatus)
            .where(LiveStatus.platform == platform)
            .order_by(LiveStatus.updated_at.desc())
            .limit(1)
        )
        return self.db.scalars(query).first()

    def update_manual_status(
        self,
        platform: str = "mixlr",
        is_live: Optional[bool] = None,
        title: Optional[str] = None,
        stream_url: Optional[str] = None,
        embed_url: Optional[str] = None,
    ) -> LiveStatus:
        """Manually override or update live status (e.g. by admin)."""
        status_rec = self.get_db_live_status(platform)

        if not status_rec:
            status_rec = LiveStatus(
                platform=platform,
                is_live=is_live if is_live is not None else False,
                stream_title=title,
                stream_url=stream_url,
                embed_url=embed_url or self.client.embed_url,
                channel_name=self.client.channel_name,
            )
            self.db.add(status_rec)
        else:
            if is_live is not None:
                status_rec.is_live = is_live
            if title is not None:
                status_rec.stream_title = title
            if stream_url is not None:
                status_rec.stream_url = stream_url
            if embed_url is not None:
                status_rec.embed_url = embed_url

        self.db.commit()
        self.db.refresh(status_rec)

        # Invalidate cache so changes take effect immediately
        self._cached_status = None
        self._cache_expires_at = 0.0
        return status_rec

    def invalidate_cache(self) -> None:
        self._cached_status = None
        self._cache_expires_at = 0.0

    # -- live fetch ---------------------------------------------------------

    async def fetch_live_status(self, force_refresh: bool = False) -> LivePlatformStatus:
        """
        Real-time status via MixlrClient (v3 channel_view, legacy fallback).
        Instance-level TTL cache prevents rate-limiting and minimizes latency.
        """
        now = time.time()
        if (
            not force_refresh
            and self._cached_status is not None
            and now < self._cache_expires_at
        ):
            return self._cached_status

        if not self.client.channel_name:
            return LivePlatformStatus(is_live=False)

        result = await self.client.fetch_live_v3()
        if result is None:
            logger.warning("Mixlr v3 channel_view failed, attempting legacy fallback...")
            result = await self.client.fetch_live_legacy()
        if result is None:
            return self._fallback_from_db()

        self._persist_status_to_db(result)
        self._cached_status = result
        self._cache_expires_at = now + self.cache_ttl
        return result

    def _fallback_from_db(self) -> LivePlatformStatus:
        """Fallback to the last known database record when external APIs fail."""
        status_rec = self.get_db_live_status("mixlr")
        if not status_rec:
            return LivePlatformStatus(is_live=False, embed_url=self.client.embed_url)

        return LivePlatformStatus(
            is_live=status_rec.is_live,
            title=status_rec.stream_title,
            event_title=status_rec.event_title,
            broadcast_title=status_rec.broadcast_title,
            stream_url=status_rec.stream_url,
            embed_url=status_rec.embed_url or self.client.embed_url,
            audio_stream_url=status_rec.audio_stream_url,
            channel_name=status_rec.channel_name or self.client.channel_name,
            channel_logo_url=status_rec.channel_logo_url,
            channel_artwork_url=status_rec.channel_artwork_url,
            listener_count=status_rec.listener_count,
            started_at=status_rec.started_at,
        )

    def _persist_status_to_db(self, live_info: LivePlatformStatus):
        """Save latest live broadcast info to DB without failing the request on DB error."""
        try:
            status_rec = self.get_db_live_status("mixlr")
            if not status_rec:
                status_rec = LiveStatus(
                    platform="mixlr",
                    is_live=live_info.is_live,
                    stream_title=live_info.title,
                    event_title=live_info.event_title,
                    broadcast_title=live_info.broadcast_title,
                    stream_url=live_info.stream_url,
                    embed_url=live_info.embed_url,
                    audio_stream_url=live_info.audio_stream_url,
                    channel_name=live_info.channel_name,
                    channel_logo_url=live_info.channel_logo_url,
                    channel_artwork_url=live_info.channel_artwork_url,
                    listener_count=live_info.listener_count,
                    started_at=live_info.started_at,
                )
                self.db.add(status_rec)
            else:
                status_rec.is_live = live_info.is_live
                status_rec.stream_title = live_info.title
                status_rec.event_title = live_info.event_title
                status_rec.broadcast_title = live_info.broadcast_title
                status_rec.stream_url = live_info.stream_url
                status_rec.embed_url = live_info.embed_url
                status_rec.audio_stream_url = live_info.audio_stream_url
                status_rec.channel_name = live_info.channel_name
                status_rec.channel_logo_url = live_info.channel_logo_url
                status_rec.channel_artwork_url = live_info.channel_artwork_url
                status_rec.listener_count = live_info.listener_count
                status_rec.started_at = live_info.started_at
            self.db.commit()
        except Exception as dbe:
            self.db.rollback()
            logger.warning(f"Could not persist live status to DB: {dbe}")

    async def get_combined_live_status(
        self, youtube_status: Optional[LivePlatformStatus] = None
    ) -> LiveStatusRead:
        """
        Unified status for Mixlr (audio) + YouTube (video).
        Pass an explicit ``youtube_status`` to inject the real YouTube state;
        defaults to the offline placeholder for backwards compatibility.
        """
        mixlr_status = await self.fetch_live_status()
        if youtube_status is None:
            youtube_status = LivePlatformStatus(is_live=False, channel_name="GCFT Church")

        is_any_live = mixlr_status.is_live or youtube_status.is_live
        active_platform: Optional[str] = None
        if mixlr_status.is_live and youtube_status.is_live:
            active_platform = "both"
        elif mixlr_status.is_live:
            active_platform = "mixlr"
        elif youtube_status.is_live:
            active_platform = "youtube"

        return LiveStatusRead(
            is_live=is_any_live,
            active_platform=active_platform,
            mixlr=mixlr_status,
            youtube=youtube_status,
            manual_override=False,
            updated_at=datetime.now(timezone.utc),
        )
