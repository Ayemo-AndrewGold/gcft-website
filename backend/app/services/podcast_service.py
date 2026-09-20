"""Podcast/recordings service: RSS + Mixlr v3 recording search, fully async."""

import asyncio
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import feedparser
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models.podcast_episode import PodcastEpisode
from app.services.base import BaseService
from app.services.mixlr_client import MixlrClient, clean_title

logger = logging.getLogger("gcft_api.services.podcast")


def parse_duration(raw: Any) -> Optional[int]:
    """Mixlr RSS ``itunes_duration`` is usually integer seconds; also accept MM:SS/HH:MM:SS."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text.isdigit():
        return int(text)
    if ":" in text:
        parts = [p for p in text.split(":") if p.isdigit()]
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
    return None


def extract_recording_id(guid: Optional[str], page_url: Optional[str]) -> Optional[str]:
    """Pull the numeric recording id from a guid or recording page URL."""
    if guid and (m := re.search(r"recording/(\d+)", guid)):
        return m.group(1)
    if page_url and (m := re.search(r"/recordings/(\d+)", page_url)):
        return m.group(1)
    return None


class PodcastService(BaseService[PodcastEpisode]):
    def __init__(
        self,
        db: Session,
        settings=None,
        client: Optional[MixlrClient] = None,
    ):
        super().__init__(db, settings or get_settings())
        self.rss_url = self.settings.podcast_rss_url
        self.client = client or MixlrClient(
            channel_name=self.settings.mixlr_channel_name,
            channel_id=self.settings.mixlr_channel_id,
        )

    # -- reads (sync DB access, shared paginate helper) ---------------------

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
        return self.paginate(query, skip=skip, limit=limit)

    def get_episode_by_id(self, episode_id: int) -> Optional[PodcastEpisode]:
        """Fetch a single episode by its database ID."""
        return self.get_by_id(PodcastEpisode, episode_id)

    def get_latest_episode(self) -> Optional[PodcastEpisode]:
        """Fetch the most recently published podcast episode."""
        query = (
            select(PodcastEpisode).order_by(PodcastEpisode.published_at.desc()).limit(1)
        )
        return self.db.scalars(query).first()

    # -- RSS parsing (pure helpers, shared upsert path) ----------------------

    def parse_rss_entry(self, entry: Any, feed_channel_image: Optional[str]) -> Dict[str, Any]:
        guid = (
            getattr(entry, "id", None)
            or getattr(entry, "guid", None)
            or entry.get("link")
        )
        title = clean_title(getattr(entry, "title", "Untitled Episode"))
        description = (
            getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
        )

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

        image_url = (
            entry.get("image", {}).get("href")
            or getattr(entry, "itunes_image", None)
            or feed_channel_image
        )
        recording_page_url = entry.get("link")
        recording_id = extract_recording_id(guid, recording_page_url)
        embed_url = (
            self.client.recording_embed_url(recording_id) if recording_id else None
        )

        published_at: Optional[datetime] = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

        return {
            "guid": guid,
            "recording_id": recording_id,
            "title": title,
            "description": description,
            "audio_url": audio_url,
            "embed_url": embed_url,
            "image_url": image_url,
            "recording_page_url": recording_page_url,
            "file_size_bytes": file_size_bytes,
            "duration": parse_duration(getattr(entry, "itunes_duration", None)),
            "published_at": published_at,
        }

    _EPISODE_FIELDS = (
        "guid",
        "recording_id",
        "title",
        "description",
        "audio_url",
        "embed_url",
        "image_url",
        "recording_page_url",
        "file_size_bytes",
        "duration",
        "published_at",
    )

    def _upsert_episode(self, data: Dict[str, Any], preserve_mp3: bool = False) -> str:
        """Insert or update one episode. Returns 'new' or 'updated'."""
        guid = data.get("guid")
        rec_id = data.get("recording_id")
        existing = (
            self.db.query(PodcastEpisode)
            .filter(
                or_(PodcastEpisode.guid == guid, PodcastEpisode.recording_id == rec_id)
                if rec_id
                else (PodcastEpisode.guid == guid)
            )
            .first()
        )
        clean = {k: data.get(k) for k in self._EPISODE_FIELDS}
        if not existing:
            self.db.add(PodcastEpisode(**clean))
            return "new"

        for key, value in clean.items():
            if value is None:
                continue
            if preserve_mp3 and key == "audio_url":
                # Keep a direct MP3 enclosure previously set by RSS over page URLs.
                if existing.audio_url and existing.audio_url.endswith(".mp3"):
                    continue
            setattr(existing, key, value)
        return "updated"

    # -- sync (fully async; blocking feedparser runs in a thread) ------------

    async def sync_from_rss(self) -> Dict[str, int]:
        """
        Synchronize podcast episodes from the Mixlr RSS feed into the database.
        Upsert deduplication is based on unique guid.
        """
        if not self.rss_url:
            logger.warning("Podcast RSS URL is not configured.")
            return {"total_parsed": 0, "new": 0, "updated": 0}

        feed = await asyncio.to_thread(feedparser.parse, self.rss_url)
        feed_channel_image = (
            feed.feed.get("image", {}).get("href")
            or feed.feed.get("image", {}).get("url")
            or None
        )

        new_count = updated_count = 0
        for entry in feed.entries:
            data = self.parse_rss_entry(entry, feed_channel_image)
            if not data.get("guid"):
                continue
            if self._upsert_episode(data) == "new":
                new_count += 1
            else:
                updated_count += 1

        self.db.commit()
        total_parsed = len(feed.entries)
        logger.info(
            f"Podcast sync complete: {total_parsed} parsed, {new_count} new, {updated_count} updated."
        )
        return {"total_parsed": total_parsed, "new": new_count, "updated": updated_count}

    async def sync_from_mixlr(self, page_size: int = 25) -> Dict[str, int]:
        """
        Synchronize latest broadcast recordings from Mixlr v3 recording_search API.
        Captures real-time recorded services, prayer meetings, and song services.
        """
        items = await self.client.search_recordings_raw(page_size=page_size)
        # search_recordings_raw already returns [] with logging on failure.

        new_count = updated_count = 0
        for item in items:
            data = self.client.parse_recording_item(item)
            if not data:
                continue
            if self._upsert_episode(data, preserve_mp3=True) == "new":
                new_count += 1
            else:
                updated_count += 1

        self.db.commit()
        total_parsed = len(items)
        logger.info(
            f"Mixlr v3 recording sync complete: {total_parsed} parsed, {new_count} new, {updated_count} updated."
        )
        return {"total_parsed": total_parsed, "new": new_count, "updated": updated_count}

    async def sync_all(self) -> Dict[str, Any]:
        """
        Complete sync across Mixlr v3 recording API and RSS feed.
        Ensures both real-time recorded broadcasts and RSS enclosures are indexed.
        """
        mixlr_stats = await self.sync_from_mixlr()
        rss_stats = await self.sync_from_rss()
        return {
            "mixlr_recordings": mixlr_stats,
            "rss_feed": rss_stats,
            "total_new": mixlr_stats["new"] + rss_stats["new"],
            "total_updated": mixlr_stats["updated"] + rss_stats["updated"],
        }

    # Backwards-compat alias (was sync, now delegates to the async client).
    async def resolve_channel_id(self) -> Optional[str]:
        return await self.client.resolve_channel_id()
