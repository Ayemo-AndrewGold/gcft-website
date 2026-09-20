import logging
from typing import Any, Dict, List, Optional, Tuple
import httpx
from app.schemas.live import LivePlatformStatus
from app.utils.datetime import parse_iso_datetime

logger = logging.getLogger("gcft_api.services.youtube_client")

YT_BASE_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeClient:
    """
    HTTP client for YouTube Data API v3.
    Designed with quota optimization in mind:
    - Channel metadata & uploads playlist ID are cached in memory (called once).
    - Past recordings sync uses playlistItems.list on uploads playlist (1 quota unit).
    - Live stream detection uses search.list with eventType=live (100 quota units).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        channel_id: Optional[str] = None,
        channel_name: str = "GCFT Church",
    ):
        self.api_key = api_key
        self.channel_id = channel_id
        self._channel_name = channel_name

        # Cached channel details (uploads playlist ID, name, logo)
        self._uploads_playlist_id: Optional[str] = None
        self._cached_channel_title: Optional[str] = None
        self._cached_channel_logo: Optional[str] = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.channel_id)

    @property
    def channel_name(self) -> str:
        return self._cached_channel_title or self._channel_name

    @property
    def channel_url(self) -> Optional[str]:
        return f"https://www.youtube.com/channel/{self.channel_id}" if self.channel_id else None

    @property
    def livepage_url(self) -> Optional[str]:
        return f"https://www.youtube.com/channel/{self.channel_id}/live" if self.channel_id else None

    def get_default_uploads_playlist_id(self) -> Optional[str]:
        """
        Derive the uploads playlist ID by replacing the second character 'C' with 'U'.
        YouTube channel IDs standard: UC... -> UU...
        """
        if self.channel_id and len(self.channel_id) > 2 and self.channel_id.startswith("UC"):
            return f"UU{self.channel_id[2:]}"
        return None

    async def get_channel_details(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Fetch channel contentDetails and snippet.
        Returns (uploads_playlist_id, channel_title, channel_logo_url).
        Results are cached on the client instance so subsequent calls cost 0 quota.
        """
        if self._uploads_playlist_id:
            return self._uploads_playlist_id, self._cached_channel_title, self._cached_channel_logo

        if not self.is_configured:
            logger.warning("YouTube API key or Channel ID not configured.")
            return None, None, None

        params = {
            "part": "contentDetails,snippet",
            "id": self.channel_id,
            "key": self.api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{YT_BASE_URL}/channels", params=params)
                resp.raise_for_status()
                data = resp.json()
                items = data.get("items", [])
                if items:
                    item = items[0]
                    related = item.get("contentDetails", {}).get("relatedPlaylists", {})
                    self._uploads_playlist_id = related.get("uploads") or self.get_default_uploads_playlist_id()

                    snippet = item.get("snippet", {})
                    self._cached_channel_title = snippet.get("title") or self._channel_name
                    thumbnails = snippet.get("thumbnails", {})
                    self._cached_channel_logo = (
                        thumbnails.get("high", {}).get("url")
                        or thumbnails.get("default", {}).get("url")
                    )
                else:
                    self._uploads_playlist_id = self.get_default_uploads_playlist_id()
        except Exception as e:
            logger.error(f"Error fetching YouTube channel details: {e}")
            self._uploads_playlist_id = self.get_default_uploads_playlist_id()

        return self._uploads_playlist_id, self._cached_channel_title, self._cached_channel_logo

    async def fetch_recent_recordings(self, max_results: int = 25) -> List[Dict[str, Any]]:
        """
        Fetch recent video recordings/uploads using playlistItems.list.
        Costs ONLY 1 quota unit (compared to 100 units for search.list).
        """
        if not self.is_configured:
            logger.warning("YouTube API key or Channel ID not configured.")
            return []

        uploads_id, _, _ = await self.get_channel_details()
        if not uploads_id:
            logger.error("Could not determine YouTube uploads playlist ID.")
            return []

        params = {
            "part": "snippet,contentDetails",
            "playlistId": uploads_id,
            "maxResults": min(max(max_results, 1), 50),
            "key": self.api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{YT_BASE_URL}/playlistItems", params=params)
                resp.raise_for_status()
                items = resp.json().get("items", [])
        except Exception as e:
            logger.error(f"Error fetching YouTube recordings from uploads playlist: {e}")
            return []

        recordings: List[Dict[str, Any]] = []
        for item in items:
            video_id = (
                item.get("contentDetails", {}).get("videoId")
                or item.get("snippet", {}).get("resourceId", {}).get("videoId")
            )
            if not video_id:
                continue

            snippet = item.get("snippet", {})
            title = snippet.get("title", "")
            description = snippet.get("description", "")
            thumbnails = snippet.get("thumbnails", {})
            thumbnail_url = (
                thumbnails.get("maxres", {}).get("url")
                or thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url")
            )
            published_at = parse_iso_datetime(snippet.get("publishedAt"))

            recordings.append({
                "youtube_id": video_id,
                "title": title,
                "description": description,
                "thumbnail_url": thumbnail_url,
                "published_at": published_at,
            })

        return recordings

    async def fetch_live_status(self) -> Optional[LivePlatformStatus]:
        """
        Check if the channel is currently live broadcasting.
        Uses search.list with eventType=live (costs 100 quota units).
        Callers must implement caching to preserve daily quota!
        """
        if not self.is_configured:
            logger.warning("YouTube API key or Channel ID not configured.")
            return None

        params = {
            "part": "snippet",
            "channelId": self.channel_id,
            "eventType": "live",
            "type": "video",
            "maxResults": 1,
            "key": self.api_key,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{YT_BASE_URL}/search", params=params)
                resp.raise_for_status()
                items = resp.json().get("items", [])
        except Exception as e:
            logger.error(f"Error checking YouTube live status: {e}")
            return None

        if items:
            item = items[0]
            video_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})
            title = snippet.get("title")
            thumbnails = snippet.get("thumbnails", {})
            artwork_url = (
                thumbnails.get("high", {}).get("url")
                or thumbnails.get("default", {}).get("url")
            )
            published_at = parse_iso_datetime(snippet.get("publishedAt"))
            channel_title = snippet.get("channelTitle") or self.channel_name

            return LivePlatformStatus(
                is_live=True,
                video_id=video_id,
                title=title,
                stream_url=f"https://www.youtube.com/watch?v={video_id}" if video_id else self.livepage_url,
                embed_url=f"https://www.youtube.com/embed/{video_id}" if video_id else None,
                channel_name=channel_title,
                channel_artwork_url=artwork_url,
                channel_logo_url=self._cached_channel_logo,
                started_at=published_at,
            )

        # Offline status
        return LivePlatformStatus(
            is_live=False,
            video_id=None,
            title=None,
            stream_url=self.livepage_url,
            embed_url=None,
            channel_name=self.channel_name,
            channel_logo_url=self._cached_channel_logo,
            started_at=None,
        )
