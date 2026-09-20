import logging
import re
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Tuple
import feedparser
import httpx
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models.podcast_episode import PodcastEpisode

logger = logging.getLogger("gcft_api.services.podcast")
settings = get_settings()


class PodcastService:
    def __init__(self, db: Session):
        self.db = db
        self.rss_url = settings.podcast_rss_url
        self.channel_name = settings.mixlr_channel_name

    def get_episodes(
        self,
        skip: int = 0,
        limit: int = 3,
        search: Optional[str] = None,
    ) -> Tuple[List[PodcastEpisode], int]:
        """Fetch paginated podcast episodes with optional search filtering."""
        query = select(PodcastEpisode).order_by(PodcastEpisode.published_at.desc())

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    PodcastEpisode.title.ilike(search_pattern),
                    PodcastEpisode.description.ilike(search_pattern),
                )
            )

        count_query = select(func.count()).select_from(query.subquery())
        total = self.db.scalar(count_query) or 0
        episodes = self.db.scalars(query.offset(skip).limit(limit)).all()
        return list(episodes), total

    def get_episode_by_id(self, episode_id: int) -> Optional[PodcastEpisode]:
        """Fetch a single episode by its database ID."""
        return self.db.get(PodcastEpisode, episode_id)

    def get_latest_episode(self) -> Optional[PodcastEpisode]:
        """Fetch the most recently published podcast episode."""
        query = select(PodcastEpisode).order_by(PodcastEpisode.published_at.desc()).limit(1)
        return self.db.scalars(query).first()

    def sync_from_rss(self) -> Dict[str, int]:
        """
        Synchronize podcast episodes from the Mixlr RSS feed into the database.
        Performs upsert deduplication based on unique guid.
        """
        if not self.rss_url:
            logger.warning("Podcast RSS URL is not configured.")
            return {"total_parsed": 0, "new": 0, "updated": 0}

        feed = feedparser.parse(self.rss_url)
        feed_channel_image = (
            feed.feed.get("image", {}).get("href")
            or feed.feed.get("image", {}).get("url")
            or None
        )

        new_count = 0
        updated_count = 0

        for entry in feed.entries:
            guid = getattr(entry, "id", None) or getattr(entry, "guid", None) or entry.get("link")
            if not guid:
                continue

            # Clean title (strip legacy .mp3 filenames)
            raw_title = getattr(entry, "title", "Untitled Episode")
            title = re.sub(r"\.mp3\s*$", "", raw_title, flags=re.IGNORECASE).strip()

            # Description / summary
            description = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""

            # Extract audio enclosure and file size
            audio_url = ""
            file_size_bytes: Optional[int] = None
            for enclosure in getattr(entry, "enclosures", []):
                href = enclosure.get("href")
                enc_type = enclosure.get("type", "")
                if href and (enc_type.startswith("audio/") or enc_type == "" or "mp3" in href):
                    audio_url = href
                    if enclosure.get("length"):
                        try:
                            file_size_bytes = int(enclosure["length"])
                        except (ValueError, TypeError):
                            file_size_bytes = None
                    break

            if not audio_url and hasattr(entry, "link"):
                audio_url = entry.link

            # Extract duration (Mixlr outputs integer seconds in itunes_duration)
            duration_val: Optional[int] = None
            raw_duration = getattr(entry, "itunes_duration", None)
            if raw_duration:
                if str(raw_duration).isdigit():
                    duration_val = int(raw_duration)
                elif ":" in str(raw_duration):
                    # In case of HH:MM:SS or MM:SS
                    parts = [int(p) for p in str(raw_duration).split(":") if p.isdigit()]
                    if len(parts) == 3:
                        duration_val = parts[0] * 3600 + parts[1] * 60 + parts[2]
                    elif len(parts) == 2:
                        duration_val = parts[0] * 60 + parts[1]

            # Extract image artwork (per-episode image or fallback to feed channel image)
            image_url = (
                entry.get("image", {}).get("href")
                or getattr(entry, "itunes_image", None)
                or feed_channel_image
            )

            # Link and recording ID extraction
            recording_page_url = entry.get("link")
            recording_id: Optional[str] = None
            match = re.search(r"recording/(\d+)", guid) or (
                re.search(r"/recordings/(\d+)", recording_page_url) if recording_page_url else None
            )
            if match:
                recording_id = match.group(1)

            # Construct dynamic Mixlr recording embed URL
            embed_url: Optional[str] = None
            if recording_id and self.channel_name:
                embed_url = f"https://{self.channel_name}.mixlr.com/recordings/{recording_id}/embed"

            # Parse publication date
            published_at: Optional[datetime] = None
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

            # Upsert into DB
            existing = self.db.query(PodcastEpisode).filter(PodcastEpisode.guid == guid).first()
            if not existing:
                episode = PodcastEpisode(
                    guid=guid,
                    recording_id=recording_id,
                    title=title,
                    description=description,
                    audio_url=audio_url,
                    embed_url=embed_url,
                    image_url=image_url,
                    recording_page_url=recording_page_url,
                    file_size_bytes=file_size_bytes,
                    duration=duration_val,
                    published_at=published_at,
                )
                self.db.add(episode)
                new_count += 1
            else:
                existing.recording_id = recording_id
                existing.title = title
                existing.description = description
                existing.audio_url = audio_url
                existing.embed_url = embed_url
                existing.image_url = image_url
                existing.recording_page_url = recording_page_url
                existing.file_size_bytes = file_size_bytes
                existing.duration = duration_val
                if published_at:
                    existing.published_at = published_at
                updated_count += 1

        self.db.commit()
        total_parsed = len(feed.entries)
        logger.info(
            f"Podcast sync complete: {total_parsed} parsed, {new_count} new, {updated_count} updated."
        )
        return {"total_parsed": total_parsed, "new": new_count, "updated": updated_count}

    def resolve_channel_id(self) -> Optional[str]:
        """Resolve numeric Mixlr channel ID from configuration or channel_view API."""
        if settings.mixlr_channel_id:
            return settings.mixlr_channel_id
        if not self.channel_name:
            return None
        try:
            with httpx.Client(timeout=5.0) as client:
                res = client.get(f"https://apicdn.mixlr.com/v3/channel_view/{self.channel_name}")
                if res.status_code == 200:
                    ch_id = str(res.json().get("data", {}).get("id", ""))
                    if ch_id:
                        return ch_id
        except Exception as e:
            logger.warning(f"Failed to auto-resolve Mixlr channel ID: {e}")
        return "654"

    def sync_from_mixlr(self, page_size: int = 25) -> Dict[str, int]:
        """
        Synchronize latest broadcast recordings from Mixlr v3 recording_search API.
        Captures real-time recorded services, prayer meetings, and song services.
        """
        channel_id = self.resolve_channel_id()
        if not channel_id:
            logger.warning("No Mixlr channel ID available for recording search sync.")
            return {"total_parsed": 0, "new": 0, "updated": 0}

        url = f"https://apicdn.mixlr.com/v3/recording_search?search[channel_id]={channel_id}&page[size]={page_size}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
        }

        try:
            with httpx.Client(timeout=10.0, headers=headers) as client:
                res = client.get(url)
                if res.status_code != 200:
                    logger.error(f"Mixlr recording search failed with status {res.status_code}: {res.text[:200]}")
                    return {"total_parsed": 0, "new": 0, "updated": 0}
                data = res.json().get("data", [])
        except Exception as e:
            logger.error(f"Error querying Mixlr recording search: {e}")
            return {"total_parsed": 0, "new": 0, "updated": 0}

        new_count = 0
        updated_count = 0

        for item in data:
            rec_id = str(item.get("id"))
            if not rec_id:
                continue

            guid = f"mixlr:recording/{rec_id}"
            attrs = item.get("attributes", {})
            raw_title = attrs.get("title", "Untitled Service")
            title = re.sub(r"\.mp3\s*$", "", raw_title, flags=re.IGNORECASE).strip()
            duration = attrs.get("duration")

            created_at_raw = attrs.get("created_at")
            published_at: Optional[datetime] = None
            if created_at_raw:
                try:
                    published_at = datetime.fromisoformat(created_at_raw)
                except Exception:
                    published_at = None

            artwork = attrs.get("media", {}).get("artwork", {})
            image_url = (
                artwork.get("image", {}).get("large")
                or artwork.get("image", {}).get("medium")
                or artwork.get("image_seo", {}).get("og_image")
            )

            rec_page_url = f"https://{self.channel_name}.mixlr.com/recordings/{rec_id}" if self.channel_name else None
            embed_url = f"https://{self.channel_name}.mixlr.com/recordings/{rec_id}/embed" if self.channel_name else None

            existing = self.db.query(PodcastEpisode).filter(
                or_(PodcastEpisode.guid == guid, PodcastEpisode.recording_id == rec_id)
            ).first()

            if not existing:
                episode = PodcastEpisode(
                    guid=guid,
                    recording_id=rec_id,
                    title=title,
                    description=attrs.get("description") or title,
                    audio_url=rec_page_url or "",
                    embed_url=embed_url,
                    image_url=image_url,
                    recording_page_url=rec_page_url,
                    duration=duration,
                    published_at=published_at,
                )
                self.db.add(episode)
                new_count += 1
            else:
                existing.recording_id = rec_id
                existing.title = title
                if attrs.get("description"):
                    existing.description = attrs.get("description")
                if embed_url:
                    existing.embed_url = embed_url
                if image_url:
                    existing.image_url = image_url
                if rec_page_url:
                    existing.recording_page_url = rec_page_url
                if duration:
                    existing.duration = duration
                if published_at:
                    existing.published_at = published_at
                # Preserve direct MP3 enclosure if previously set by RSS, otherwise default to recording page
                if not existing.audio_url or not existing.audio_url.endswith(".mp3"):
                    if rec_page_url:
                        existing.audio_url = rec_page_url
                updated_count += 1

        self.db.commit()
        total_parsed = len(data)
        logger.info(
            f"Mixlr v3 recording sync complete: {total_parsed} parsed, {new_count} new, {updated_count} updated."
        )
        return {"total_parsed": total_parsed, "new": new_count, "updated": updated_count}

    def sync_all(self) -> Dict[str, Any]:
        """
        Complete sync across Mixlr v3 recording API and RSS feed.
        Ensures both real-time recorded broadcasts and RSS enclosures are indexed.
        """
        mixlr_stats = self.sync_from_mixlr()
        rss_stats = self.sync_from_rss()
        return {
            "mixlr_recordings": mixlr_stats,
            "rss_feed": rss_stats,
            "total_new": mixlr_stats["new"] + rss_stats["new"],
            "total_updated": mixlr_stats["updated"] + rss_stats["updated"],
        }
