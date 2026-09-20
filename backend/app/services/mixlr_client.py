"""Single low-level client for all Mixlr HTTP + parsing.

Owns every Mixlr URL, header, timeout and JSON-mapping helper so that
``MixlrService`` (live status) and ``PodcastService`` (recordings) no longer
duplicate channel_view / recording_search logic.
"""

import logging
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx

from app.schemas.live import LivePlatformStatus
from app.utils.datetime import parse_iso_datetime as _parse_iso_datetime

logger = logging.getLogger("gcft_api.services.mixlr_client")

V3_BASE = "https://apicdn.mixlr.com/v3"
LEGACY_BASE = "https://api.mixlr.com"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
# gcftmedia's known numeric channel id — used only when auto-resolution fails
# and no explicit MIXLR_CHANNEL_ID is configured.
DEFAULT_CHANNEL_ID = "654"


def clean_title(raw: str) -> str:
    """Strip legacy '.mp3' filename suffixes from Mixlr titles."""
    return re.sub(r"\.mp3\s*$", "", raw or "", flags=re.IGNORECASE).strip()


def parse_iso_datetime(raw: Any) -> Optional[datetime]:
    """Backwards-compatible re-export of the shared ISO parser."""
    return _parse_iso_datetime(raw)


def map_included(included: List[Dict[str, Any]]) -> Dict[tuple, Dict[str, Any]]:
    """Index a JSON:API ``included`` array by (type, id)."""
    return {
        (item.get("type"), str(item.get("id"))): item.get("attributes", {})
        for item in included or []
    }


class MixlrClient:
    """Stateless Mixlr API helper. Holds config, never touches the DB."""

    def __init__(
        self,
        channel_name: Optional[str] = None,
        channel_id: Optional[str] = None,
        timeout: float = 8.0,
    ):
        self.channel_name = (channel_name or "").strip() or None
        self.channel_id = (channel_id or "").strip() or None
        self.timeout = timeout
        self.headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}

    # -- URL builders (single source of truth) ---------------------------

    @property
    def embed_url(self) -> Optional[str]:
        if not self.channel_name:
            return None
        return f"https://{self.channel_name}.mixlr.com/embed"

    @property
    def livepage_url(self) -> Optional[str]:
        if not self.channel_name:
            return None
        return f"https://mixlr.com/{self.channel_name}"

    def recording_page_url(self, recording_id: str) -> Optional[str]:
        if not self.channel_name or not recording_id:
            return None
        return f"https://{self.channel_name}.mixlr.com/recordings/{recording_id}"

    def recording_embed_url(self, recording_id: str) -> Optional[str]:
        page = self.recording_page_url(recording_id)
        return f"{page}/embed" if page else None

    # -- raw HTTP ---------------------------------------------------------

    async def get_channel_view_raw(self) -> Optional[Dict[str, Any]]:
        """GET v3/channel_view — returns decoded JSON or None on failure."""
        if not self.channel_name:
            return None
        url = f"{V3_BASE}/channel_view/{self.channel_name}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
                res = await client.get(url)
                if res.status_code != 200:
                    logger.warning(f"Mixlr v3 channel_view returned status {res.status_code}")
                    return None
                return res.json()
        except Exception as e:
            logger.warning(f"Error fetching Mixlr v3 channel_view: {e}")
            return None

    async def resolve_channel_id(self) -> Optional[str]:
        """Numeric channel id: explicit config → channel_view → default fallback."""
        if self.channel_id:
            return self.channel_id
        data = await self.get_channel_view_raw()
        if data:
            ch_id = str(data.get("data", {}).get("id", "") or "")
            if ch_id:
                return ch_id
        logger.warning("Could not auto-resolve Mixlr channel ID, using default.")
        return DEFAULT_CHANNEL_ID if self.channel_name else None

    async def search_recordings_raw(self, page_size: int = 25) -> List[Dict[str, Any]]:
        """GET v3/recording_search — returns raw ``data`` items (empty on failure)."""
        channel_id = await self.resolve_channel_id()
        if not channel_id:
            logger.warning("No Mixlr channel ID available for recording search.")
            return []
        url = f"{V3_BASE}/recording_search?search[channel_id]={channel_id}&page[size]={page_size}"
        try:
            async with httpx.AsyncClient(timeout=10.0, headers=self.headers) as client:
                res = await client.get(url)
                if res.status_code != 200:
                    logger.error(
                        f"Mixlr recording search failed: {res.status_code} {res.text[:200]}"
                    )
                    return []
                return res.json().get("data", []) or []
        except Exception as e:
            logger.error(f"Error querying Mixlr recording search: {e}")
            return []

    async def get_legacy_user_raw(self) -> Optional[Dict[str, Any]]:
        if not self.channel_name:
            return None
        try:
            async with httpx.AsyncClient(timeout=6.0, headers=self.headers) as client:
                res = await client.get(f"{LEGACY_BASE}/users/{self.channel_name}")
                if res.status_code != 200:
                    return None
                return res.json()
        except Exception as e:
            logger.warning(f"Error fetching legacy Mixlr user: {e}")
            return None

    async def get_legacy_broadcast_raw(self, broadcast_id: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient(timeout=6.0, headers=self.headers) as client:
                res = await client.get(f"{LEGACY_BASE}/broadcasts/{broadcast_id}")
                if res.status_code != 200:
                    return None
                return res.json()
        except Exception as e:
            logger.warning(f"Failed to fetch legacy Mixlr broadcast details: {e}")
            return None

    # -- parsing (pure, easily unit-tested) --------------------------------

    def build_live_status_from_channel_view(self, payload: Dict[str, Any]) -> LivePlatformStatus:
        """Map a v3 channel_view document to LivePlatformStatus."""
        data_obj = payload.get("data", {})
        attrs = data_obj.get("attributes", {})
        is_live = bool(attrs.get("live", False))
        channel_name = attrs.get("username") or self.channel_name

        media = attrs.get("media", {})
        channel_logo = (
            media.get("logo", {}).get("image", {}).get("medium")
            or attrs.get("profile_image_url")
        )
        channel_artwork = (
            media.get("artwork", {}).get("image", {}).get("large")
            or attrs.get("artwork_url")
        )

        included = map_included(payload.get("included", []))
        rel = data_obj.get("relationships") or {}
        current_broadcast = rel.get("current_broadcast") or {}
        cb_data = current_broadcast.get("data") or {}
        current_broadcast_id = str(cb_data.get("id") or "")
        broadcast_attrs = included.get(("broadcast", current_broadcast_id), {})
        event_id = str(broadcast_attrs.get("event_id", ""))
        event_attrs = included.get(("event", event_id), {})

        event_title = event_attrs.get("title")
        broadcast_title = broadcast_attrs.get("title")
        primary_title = event_title or broadcast_title

        event_artwork = (
            event_attrs.get("media", {}).get("artwork", {}).get("image", {}).get("large")
            or event_attrs.get("artwork_url")
        )
        if event_artwork:
            channel_artwork = event_artwork

        started_at = parse_iso_datetime(
            broadcast_attrs.get("started_at") or event_attrs.get("started_at")
        )
        stream_url = (
            event_attrs.get("legacy_url")
            or attrs.get("legacy_livepage_url")
            or self.livepage_url
        )

        return LivePlatformStatus(
            is_live=is_live,
            title=primary_title,
            event_title=event_title,
            broadcast_title=broadcast_title,
            stream_url=stream_url,
            embed_url=self.embed_url,
            audio_stream_url=broadcast_attrs.get("progressive_stream_url"),
            channel_name=channel_name,
            channel_logo_url=channel_logo,
            channel_artwork_url=channel_artwork,
            listener_count=broadcast_attrs.get("listener_count"),
            started_at=started_at,
        )

    def build_live_status_from_legacy(
        self, user_data: Dict[str, Any], broadcast_data: Optional[Dict[str, Any]] = None
    ) -> LivePlatformStatus:
        """Map legacy api.mixlr.com user (+ optional broadcast) payloads."""
        is_live = bool(user_data.get("is_live", False))
        channel_obj = user_data.get("channel") or {}
        channel_name = (
            channel_obj.get("name") or user_data.get("username") or self.channel_name
        )
        channel_logo = channel_obj.get("logo_url") or user_data.get("profile_image_url")
        stream_url = channel_obj.get("url") or self.livepage_url

        title: Optional[str] = None
        started_at: Optional[datetime] = None
        listener_count: Optional[int] = None
        if broadcast_data:
            title = broadcast_data.get("title")
            listener_count = broadcast_data.get("listener_count")
            if broadcast_data.get("url"):
                stream_url = broadcast_data.get("url")
            started_at = parse_iso_datetime(broadcast_data.get("started_at"))

        return LivePlatformStatus(
            is_live=is_live,
            title=title,
            stream_url=stream_url,
            embed_url=self.embed_url,
            channel_name=channel_name,
            channel_logo_url=channel_logo,
            listener_count=listener_count,
            started_at=started_at,
        )

    def parse_recording_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Map one v3 recording_search item to a PodcastEpisode-ready dict."""
        rec_id = str(item.get("id") or "")
        if not rec_id:
            return None
        attrs = item.get("attributes", {})
        title = clean_title(attrs.get("title") or "Untitled Service")

        artwork = attrs.get("media", {}).get("artwork", {})
        image_url = (
            artwork.get("image", {}).get("large")
            or artwork.get("image", {}).get("medium")
            or artwork.get("image_seo", {}).get("og_image")
        )
        return {
            "guid": f"mixlr:recording/{rec_id}",
            "recording_id": rec_id,
            "title": title,
            "description": attrs.get("description") or title,
            "audio_url": self.recording_page_url(rec_id) or "",
            "embed_url": self.recording_embed_url(rec_id),
            "image_url": image_url,
            "recording_page_url": self.recording_page_url(rec_id),
            "duration": attrs.get("duration"),
            "published_at": parse_iso_datetime(attrs.get("created_at")),
        }

    # -- composed fetchers used by MixlrService ----------------------------

    async def fetch_live_v3(self) -> Optional[LivePlatformStatus]:
        payload = await self.get_channel_view_raw()
        if payload is None:
            return None
        return self.build_live_status_from_channel_view(payload)

    async def fetch_live_legacy(self) -> Optional[LivePlatformStatus]:
        user_data = await self.get_legacy_user_raw()
        if user_data is None:
            return None
        broadcast_data = None
        if user_data.get("is_live") and user_data.get("broadcast_ids"):
            broadcast_data = await self.get_legacy_broadcast_raw(
                str(user_data["broadcast_ids"][0])
            )
        return self.build_live_status_from_legacy(user_data, broadcast_data)
