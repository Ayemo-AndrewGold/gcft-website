import logging
import time
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models.live_status import LiveStatus
from app.schemas.live import LivePlatformStatus, LiveStatusRead

logger = logging.getLogger("gcft_api.services.mixlr")
settings = get_settings()

# In-memory cache variables for low-latency live status
_cached_mixlr_status: Optional[LivePlatformStatus] = None
_cache_expires_at: float = 0.0


class MixlrService:
    def __init__(self, db: Session):
        self.db = db
        self.channel_name = settings.mixlr_channel_name
        self.cache_ttl = settings.mixlr_live_cache_seconds

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
        global _cached_mixlr_status, _cache_expires_at
        status_rec = self.get_db_live_status(platform)

        if not status_rec:
            status_rec = LiveStatus(
                platform=platform,
                is_live=is_live if is_live is not None else False,
                stream_title=title,
                stream_url=stream_url,
                embed_url=embed_url or f"https://{self.channel_name}.mixlr.com/embed",
                channel_name=self.channel_name,
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
        _cached_mixlr_status = None
        _cache_expires_at = 0.0

        return status_rec

    async def fetch_live_status(self, force_refresh: bool = False) -> LivePlatformStatus:
        """
        Fetch real-time live broadcasting status from Mixlr API (v3 channel_view endpoint).
        Extracts event title (e.g. sermon title), broadcast title, live progressive audio stream,
        listener counts, artwork, and embed widget URLs.
        Uses in-memory TTL caching to prevent rate-limiting and minimize latency.
        """
        global _cached_mixlr_status, _cache_expires_at
        now = time.time()

        if not force_refresh and _cached_mixlr_status is not None and now < _cache_expires_at:
            return _cached_mixlr_status

        if not self.channel_name:
            return LivePlatformStatus(is_live=False)

        channel_view_url = f"https://apicdn.mixlr.com/v3/channel_view/{self.channel_name}"
        embed_url = f"https://{self.channel_name}.mixlr.com/embed"
        fallback_stream_url = f"https://mixlr.com/{self.channel_name}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=8.0, headers=headers) as client:
                res = await client.get(channel_view_url)
                if res.status_code == 200:
                    d = res.json()
                    data_obj = d.get("data", {})
                    attrs = data_obj.get("attributes", {})
                    is_live = attrs.get("live", False)
                    channel_name = attrs.get("username", self.channel_name)

                    # Extract logo & artwork
                    media = attrs.get("media", {})
                    channel_logo = (
                        media.get("logo", {}).get("image", {}).get("medium")
                        or attrs.get("profile_image_url")
                    )
                    channel_artwork = (
                        media.get("artwork", {}).get("image", {}).get("large")
                        or attrs.get("artwork_url")
                    )

                    # Map included items by (type, id)
                    included = {
                        (i.get("type"), str(i.get("id"))): i.get("attributes", {})
                        for i in d.get("included", [])
                    }

                    # If broadcasting live
                    current_broadcast_id = str(
                        data_obj.get("relationships", {})
                        .get("current_broadcast", {})
                        .get("data", {})
                        .get("id", "")
                    )
                    broadcast_attrs = included.get(("broadcast", current_broadcast_id), {})

                    event_id = str(broadcast_attrs.get("event_id", ""))
                    event_attrs = included.get(("event", event_id), {})

                    event_title = event_attrs.get("title")
                    broadcast_title = broadcast_attrs.get("title")
                    listener_count = broadcast_attrs.get("listener_count")
                    audio_stream_url = broadcast_attrs.get("progressive_stream_url")

                    # Primary title: prefer event title (e.g. sermon title), fallback to broadcast title
                    primary_title = event_title or broadcast_title

                    # Update artwork if event has specific artwork
                    event_artwork = (
                        event_attrs.get("media", {}).get("artwork", {}).get("image", {}).get("large")
                        or event_attrs.get("artwork_url")
                    )
                    if event_artwork:
                        channel_artwork = event_artwork

                    # Started at timestamp
                    started_at = None
                    raw_started = broadcast_attrs.get("started_at") or event_attrs.get("started_at")
                    if raw_started:
                        try:
                            started_at = datetime.fromisoformat(raw_started.replace("Z", "+00:00"))
                        except ValueError:
                            started_at = None

                    # Stream URL: prefer event legacy_url (e.g. https://mixlr.com/gcftmedia/events/5311432), fallback to legacy_livepage_url
                    stream_url = (
                        event_attrs.get("legacy_url")
                        or attrs.get("legacy_livepage_url")
                        or fallback_stream_url
                    )

                    result = LivePlatformStatus(
                        is_live=is_live,
                        title=primary_title,
                        event_title=event_title,
                        broadcast_title=broadcast_title,
                        stream_url=stream_url,
                        embed_url=embed_url,
                        audio_stream_url=audio_stream_url,
                        channel_name=channel_name,
                        channel_logo_url=channel_logo,
                        channel_artwork_url=channel_artwork,
                        listener_count=listener_count,
                        started_at=started_at,
                    )

                    self._persist_status_to_db(result)
                    _cached_mixlr_status = result
                    _cache_expires_at = now + self.cache_ttl
                    return result
                else:
                    logger.warning(f"Mixlr v3 channel_view returned status {res.status_code}, attempting legacy...")
        except Exception as e:
            logger.warning(f"Error fetching Mixlr v3 channel_view: {e}, attempting legacy fallback...")

        # Legacy fallback if v3 fails
        return await self._legacy_fetch_live_status(now)

    async def _legacy_fetch_live_status(self, now: float) -> LivePlatformStatus:
        """Legacy fallback to api.mixlr.com/users/{channel} endpoint."""
        global _cached_mixlr_status, _cache_expires_at
        user_api_url = f"https://api.mixlr.com/users/{self.channel_name}"
        embed_url = f"https://{self.channel_name}.mixlr.com/embed"
        fallback_stream_url = f"https://{self.channel_name}.mixlr.com"

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                user_res = await client.get(user_api_url)
                if user_res.status_code != 200:
                    return self._fallback_from_db()

                user_data = user_res.json()
                is_live = user_data.get("is_live", False)
                channel_obj = user_data.get("channel") or {}

                channel_name = channel_obj.get("name") or user_data.get("username", self.channel_name)
                channel_logo = channel_obj.get("logo_url") or user_data.get("profile_image_url")
                stream_url = channel_obj.get("url") or fallback_stream_url

                title: Optional[str] = None
                started_at: Optional[datetime] = None
                listener_count: Optional[int] = None

                broadcast_ids = user_data.get("broadcast_ids", [])
                if is_live and broadcast_ids:
                    b_id = broadcast_ids[0]
                    try:
                        b_res = await client.get(f"https://api.mixlr.com/broadcasts/{b_id}")
                        if b_res.status_code == 200:
                            b_data = b_res.json()
                            title = b_data.get("title")
                            listener_count = b_data.get("listener_count")
                            if b_data.get("url"):
                                stream_url = b_data.get("url")
                            raw_started = b_data.get("started_at")
                            if raw_started:
                                try:
                                    started_at = datetime.fromisoformat(raw_started.replace("Z", "+00:00"))
                                except ValueError:
                                    started_at = None
                    except Exception as be:
                        logger.warning(f"Failed to fetch legacy Mixlr broadcast details: {be}")

                result = LivePlatformStatus(
                    is_live=is_live,
                    title=title,
                    stream_url=stream_url,
                    embed_url=embed_url,
                    channel_name=channel_name,
                    channel_logo_url=channel_logo,
                    listener_count=listener_count,
                    started_at=started_at,
                )

                self._persist_status_to_db(result)
                _cached_mixlr_status = result
                _cache_expires_at = now + self.cache_ttl
                return result
        except Exception as e:
            logger.error(f"Error in legacy Mixlr fetch: {e}")
            return self._fallback_from_db()

    def _fallback_from_db(self) -> LivePlatformStatus:
        """Fallback to the last known database record when external APIs fail."""
        status_rec = self.get_db_live_status("mixlr")
        if not status_rec:
            return LivePlatformStatus(
                is_live=False,
                embed_url=f"https://{self.channel_name}.mixlr.com/embed" if self.channel_name else None,
            )

        return LivePlatformStatus(
            is_live=status_rec.is_live,
            title=status_rec.stream_title,
            stream_url=status_rec.stream_url,
            embed_url=status_rec.embed_url or f"https://{self.channel_name}.mixlr.com/embed",
            channel_name=status_rec.channel_name or self.channel_name,
            channel_logo_url=status_rec.channel_logo_url,
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
                    stream_url=live_info.stream_url,
                    embed_url=live_info.embed_url,
                    channel_name=live_info.channel_name,
                    channel_logo_url=live_info.channel_logo_url,
                    listener_count=live_info.listener_count,
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
                status_rec.listener_count = live_info.listener_count
                status_rec.started_at = live_info.started_at
            self.db.commit()
        except Exception as dbe:
            self.db.rollback()
            logger.warning(f"Could not persist live status to DB: {dbe}")

    async def get_combined_live_status(self) -> LiveStatusRead:
        """
        Return unified live status showing both Mixlr and YouTube streams.
        Allows the frontend to dynamically display audio and video streams together.
        """
        mixlr_status = await self.fetch_live_status()

        # YouTube Live placeholder (can be expanded when YouTube Live integration is added)
        youtube_status = LivePlatformStatus(
            is_live=False,
            channel_name="GCFT Church",
        )

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
