import pytest
import time
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from app.config import get_settings
from app.models.video import Video
from app.models.live_status import LiveStatus
from app.schemas.live import LivePlatformStatus
from app.services.youtube_client import YouTubeClient
from app.services.youtube_service import YouTubeLiveCache, YouTubeService, extract_video_id
from app.utils.datetime import parse_iso_datetime

settings = get_settings()
AUTH_HEADERS = {"X-API-Key": settings.api_key or "your-secret-api-key-here"}


# -- Helper / Unit Tests for YouTubeClient -------------------------------------

def test_parse_iso_datetime():
    dt = parse_iso_datetime("2026-09-20T18:30:00Z")
    assert dt is not None
    assert dt.year == 2026
    assert dt.month == 9
    assert dt.day == 20
    assert dt.hour == 18
    assert dt.minute == 30
    assert dt.tzinfo == timezone.utc

    assert parse_iso_datetime(None) is None
    assert parse_iso_datetime("invalid-date") is None


def test_youtube_client_channel_derivation():
    client = YouTubeClient(api_key="fake-key", channel_id="UCbtIQ5Uv5KwTKxdbZaKbH1Q")
    assert client.get_default_uploads_playlist_id() == "UUbtIQ5Uv5KwTKxdbZaKbH1Q"
    assert client.channel_url == "https://www.youtube.com/channel/UCbtIQ5Uv5KwTKxdbZaKbH1Q"
    assert client.livepage_url == "https://www.youtube.com/channel/UCbtIQ5Uv5KwTKxdbZaKbH1Q/live"


@pytest.mark.asyncio
async def test_youtube_client_channel_details():
    client = YouTubeClient(api_key="fake-key", channel_id="UCbtIQ5Uv5KwTKxdbZaKbH1Q")

    mock_channel_resp = {
        "items": [
            {
                "snippet": {
                    "title": "GCFT Live Channel",
                    "thumbnails": {"high": {"url": "https://example.com/logo.jpg"}},
                },
                "contentDetails": {
                    "relatedPlaylists": {"uploads": "UUbtIQ5Uv5KwTKxdbZaKbH1Q"}
                },
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_channel_resp
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        uploads_id, title, logo = await client.get_channel_details()
        assert uploads_id == "UUbtIQ5Uv5KwTKxdbZaKbH1Q"
        assert title == "GCFT Live Channel"
        assert logo == "https://example.com/logo.jpg"
        assert mock_get.call_count == 1

        # Second call should use cached attributes without HTTP call
        uploads_id2, title2, logo2 = await client.get_channel_details()
        assert uploads_id2 == uploads_id
        assert mock_get.call_count == 1


@pytest.mark.asyncio
async def test_youtube_client_fetch_recent_recordings():
    client = YouTubeClient(api_key="fake-key", channel_id="UCbtIQ5Uv5KwTKxdbZaKbH1Q")
    client._uploads_playlist_id = "UUbtIQ5Uv5KwTKxdbZaKbH1Q"

    mock_playlist_resp = {
        "items": [
            {
                "contentDetails": {"videoId": "vid_123"},
                "snippet": {
                    "title": "Sunday Service - Divine Favor",
                    "description": "Powerful sermon on favor.",
                    "thumbnails": {"high": {"url": "https://example.com/thumb.jpg"}},
                    "publishedAt": "2026-09-20T10:00:00Z",
                },
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_playlist_resp
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        recordings = await client.fetch_recent_recordings(max_results=5)
        assert len(recordings) == 1
        assert recordings[0]["youtube_id"] == "vid_123"
        assert recordings[0]["title"] == "Sunday Service - Divine Favor"
        assert recordings[0]["thumbnail_url"] == "https://example.com/thumb.jpg"
        assert recordings[0]["published_at"] is not None


@pytest.mark.asyncio
async def test_youtube_client_fetch_live_status():
    client = YouTubeClient(api_key="fake-key", channel_id="UCbtIQ5Uv5KwTKxdbZaKbH1Q")

    # Live scenario
    mock_live_resp = {
        "items": [
            {
                "id": {"videoId": "live_vid_777"},
                "snippet": {
                    "title": "GCFT Sunday Service LIVE",
                    "channelTitle": "GCFT Media",
                    "publishedAt": "2026-09-20T09:00:00Z",
                    "thumbnails": {"high": {"url": "https://example.com/live_art.jpg"}},
                },
            }
        ]
    }

    with patch("httpx.AsyncClient.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_live_resp
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        live_status = await client.fetch_live_status()
        assert live_status.is_live is True
        assert live_status.video_id == "live_vid_777"
        assert live_status.embed_url == "https://www.youtube.com/embed/live_vid_777"
        assert live_status.stream_url == "https://www.youtube.com/watch?v=live_vid_777"
        assert live_status.title == "GCFT Sunday Service LIVE"

    # Offline scenario
    mock_offline_resp = {"items": []}
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_resp = MagicMock()
        mock_resp.json.return_value = mock_offline_resp
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        offline_status = await client.fetch_live_status()
        assert offline_status.is_live is False
        assert offline_status.video_id is None
        assert offline_status.embed_url is None


# -- Service Tests -------------------------------------------------------------

def test_extract_video_id_variants():
    assert extract_video_id("https://www.youtube.com/watch?v=abc123&list=xyz") == "abc123"
    assert extract_video_id("https://www.youtube.com/embed/abc123") == "abc123"
    assert extract_video_id("https://www.youtube.com/embed/abc123?autoplay=1") == "abc123"
    assert extract_video_id("https://youtu.be/abc123") == "abc123"
    assert extract_video_id("https://youtu.be/abc123?t=30") == "abc123"
    assert extract_video_id("https://www.youtube.com/live/abc123") == "abc123"
    assert extract_video_id("https://www.youtube.com/shorts/abc123") == "abc123"
    assert extract_video_id(None) is None
    assert extract_video_id("https://www.youtube.com/channel/UCxyz") is None


@pytest.mark.asyncio
async def test_youtube_service_upsert_and_paginate(db_session):
    mock_client = MagicMock(spec=YouTubeClient)
    mock_client.is_configured = True
    mock_client.fetch_recent_recordings = AsyncMock(return_value=[
        {
            "youtube_id": "yt_001",
            "title": "Sunday Celebration",
            "description": "Faith and glory",
            "thumbnail_url": "https://img.youtube.com/vi/yt_001/hqdefault.jpg",
            "published_at": datetime(2026, 9, 20, 10, 0, 0, tzinfo=timezone.utc),
        },
        {
            "youtube_id": "yt_002",
            "title": "Midweek Communion",
            "description": "Grace manifested",
            "thumbnail_url": "https://img.youtube.com/vi/yt_002/hqdefault.jpg",
            "published_at": datetime(2026, 9, 16, 18, 0, 0, tzinfo=timezone.utc),
        },
    ])

    service = YouTubeService(db=db_session, client=mock_client)
    upserted = await service.fetch_and_upsert_videos()
    assert upserted == 2

    videos, total = service.get_videos(skip=0, limit=100)
    by_yt_id = {v.youtube_id: v for v in videos}
    assert total >= 2
    assert "yt_001" in by_yt_id and "yt_002" in by_yt_id
    # Newest first
    assert videos[0].youtube_id == "yt_001"

    # Re-sync with title update
    mock_client.fetch_recent_recordings = AsyncMock(return_value=[
        {
            "youtube_id": "yt_001",
            "title": "Sunday Celebration (Updated)",
            "description": "Faith and glory updated",
            "thumbnail_url": "https://img.youtube.com/vi/yt_001/hqdefault.jpg",
            "published_at": datetime(2026, 9, 20, 10, 0, 0, tzinfo=timezone.utc),
        }
    ])
    upserted_again = await service.fetch_and_upsert_videos()
    assert upserted_again == 1

    updated_video = service.get_video_by_youtube_id("yt_001")
    assert updated_video.title == "Sunday Celebration (Updated)"


@pytest.mark.asyncio
async def test_youtube_service_live_status_caching_and_db_persistence(db_session):
    mock_client = MagicMock(spec=YouTubeClient)
    mock_client.is_configured = True
    mock_client.fetch_live_status = AsyncMock(return_value=LivePlatformStatus(
        is_live=True,
        video_id="live_999",
        title="Live Service Right Now",
        stream_url="https://www.youtube.com/watch?v=live_999",
        embed_url="https://www.youtube.com/embed/live_999",
        channel_name="GCFT Media",
    ))

    # Each service gets a fresh holder by default; inject one explicitly here
    # to prove sharing works across instances using the same holder.
    shared_cache = YouTubeLiveCache()

    # Reset in-memory cache (fresh holder is already empty)
    assert shared_cache.get(time.time()) is None

    service = YouTubeService(db=db_session, client=mock_client, cache=shared_cache)
    status = await service.fetch_live_status()

    assert status.is_live is True
    assert status.video_id == "live_999"
    assert mock_client.fetch_live_status.call_count == 1

    # Second call uses in-memory cache (call_count stays 1)
    status2 = await service.fetch_live_status()
    assert status2.is_live is True
    assert mock_client.fetch_live_status.call_count == 1

    # A second instance sharing the holder reuses the entry (no extra quota)
    sibling = YouTubeService(db=db_session, client=mock_client, cache=shared_cache)
    status3 = await sibling.fetch_live_status()
    assert status3.is_live is True
    assert mock_client.fetch_live_status.call_count == 1

    # Check DB persistence
    db_rec = service.get_db_live_status("youtube")
    assert db_rec is not None
    assert db_rec.is_live is True
    assert db_rec.stream_title == "Live Service Right Now"
    assert db_rec.embed_url == "https://www.youtube.com/embed/live_999"


# -- FastAPI Endpoint Tests ---------------------------------------------------

def test_videos_endpoints(client: TestClient, db_session):
    # Seed a video
    video = Video(
        youtube_id="demo_vid_888",
        title="Praise and Worship Night",
        description="Evening of worship",
        thumbnail_url="https://img.youtube.com/vi/demo_vid_888/hqdefault.jpg",
        published_at=datetime(2026, 9, 18, 19, 0, 0, tzinfo=timezone.utc),
    )
    db_session.add(video)
    db_session.commit()
    db_session.refresh(video)

    # Test GET /videos
    response = client.get("/videos")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    item = next(i for i in data["items"] if i["youtube_id"] == "demo_vid_888")
    assert item["title"] == "Praise and Worship Night"
    # Check computed fields
    assert item["watch_url"] == "https://www.youtube.com/watch?v=demo_vid_888"
    assert item["embed_url"] == "https://www.youtube.com/embed/demo_vid_888"

    # Test GET /videos/{id}
    res_single = client.get(f"/videos/{video.id}")
    assert res_single.status_code == 200
    single_data = res_single.json()
    assert single_data["youtube_id"] == "demo_vid_888"
    assert single_data["watch_url"] == "https://www.youtube.com/watch?v=demo_vid_888"
    assert single_data["embed_url"] == "https://www.youtube.com/embed/demo_vid_888"


def test_unified_live_endpoint(client: TestClient, db_session):
    # Seed YouTube live status in DB
    yt_rec = LiveStatus(
        platform="youtube",
        is_live=True,
        stream_title="Sunday Miracle Service",
        stream_url="https://www.youtube.com/watch?v=stream_abc",
        embed_url="https://www.youtube.com/embed/stream_abc",
        channel_name="GCFT Church",
    )
    db_session.add(yt_rec)
    db_session.commit()

    with patch.object(YouTubeService, "fetch_live_status", new_callable=AsyncMock) as mock_yt_live:
        mock_yt_live.return_value = LivePlatformStatus(
            is_live=True,
            video_id="stream_abc",
            title="Sunday Miracle Service",
            stream_url="https://www.youtube.com/watch?v=stream_abc",
            embed_url="https://www.youtube.com/embed/stream_abc",
            channel_name="GCFT Church",
        )

        response = client.get("/live")
        assert response.status_code == 200
        data = response.json()

        assert data["is_live"] is True
        assert data["youtube"] is not None
        assert data["youtube"]["is_live"] is True
        assert data["youtube"]["video_id"] == "stream_abc"
        assert data["youtube"]["embed_url"] == "https://www.youtube.com/embed/stream_abc"
        assert data["mixlr"] is not None
        assert data["active_platform"] in ("youtube", "both")


def test_live_manual_override_for_youtube(client: TestClient):
    # Put manual override for youtube
    payload = {
        "platform": "youtube",
        "is_live": True,
        "video_id": "manual_yt_101",
        "stream_title": "Special Broadcast",
        "stream_url": "https://www.youtube.com/watch?v=manual_yt_101",
        "embed_url": "https://www.youtube.com/embed/manual_yt_101",
    }

    # Protected endpoint requires X-API-Key (from settings, like the gallery tests)
    res = client.put("/live/status", json=payload, headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert data["is_live"] is True
    assert data["youtube"] is not None
    assert data["youtube"]["is_live"] is True
    assert data["youtube"]["video_id"] == "manual_yt_101"
    assert data["youtube"]["embed_url"] == "https://www.youtube.com/embed/manual_yt_101"
