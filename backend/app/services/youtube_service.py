import logging
from typing import List, Optional
import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models.video import Video

logger = logging.getLogger("gcft_api.services.youtube")
settings = get_settings()


class YouTubeService:
    def __init__(self, db: Session):
        self.db = db
        self.api_key = settings.youtube_api_key
        self.channel_id = settings.youtube_channel_id

    def get_videos(self, skip: int = 0, limit: int = 20) -> tuple[List[Video], int]:
        query = select(Video).order_by(Video.published_at.desc())
        total = self.db.query(Video).count()
        videos = self.db.scalars(query.offset(skip).limit(limit)).all()
        return list(videos), total

    def get_video_by_id(self, video_id: int) -> Optional[Video]:
        return self.db.get(Video, video_id)

    async def fetch_and_upsert_videos(self) -> int:
        if not self.api_key or not self.channel_id:
            logger.warning("YouTube API key or Channel ID not configured.")
            return 0

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "key": self.api_key,
            "channelId": self.channel_id,
            "part": "snippet",
            "order": "date",
            "maxResults": 25,
            "type": "video",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                logger.error(f"Error fetching videos from YouTube API: {e}")
                return 0

        upserted_count = 0
        items = data.get("items", [])
        for item in items:
            yt_id = item.get("id", {}).get("videoId")
            snippet = item.get("snippet", {})
            if not yt_id or not snippet:
                continue

            existing = self.db.query(Video).filter(Video.youtube_id == yt_id).first()
            if not existing:
                video = Video(
                    youtube_id=yt_id,
                    title=snippet.get("title", ""),
                    description=snippet.get("description", ""),
                    thumbnail_url=snippet.get("thumbnails", {}).get("high", {}).get("url"),
                )
                self.db.add(video)
                upserted_count += 1
            else:
                existing.title = snippet.get("title", existing.title)
                existing.description = snippet.get("description", existing.description)
                existing.thumbnail_url = snippet.get("thumbnails", {}).get("high", {}).get("url") or existing.thumbnail_url

        self.db.commit()
        return upserted_count
