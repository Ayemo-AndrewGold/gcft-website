import pytest
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.models.podcast_episode import PodcastEpisode
from sqlalchemy.pool import StaticPool
from app.models.live_status import LiveStatus
from app.models.video import Video
from app.services.base import BaseService
from app.services.mixlr_client import (
    MixlrClient,
    clean_title,
    map_included,
    parse_iso_datetime,
)
from app.services.podcast_service import PodcastService
from app.services.mixlr_service import MixlrService
from app.services.youtube_service import YouTubeService
from app.schemas.live import LivePlatformStatus, LiveStatusRead
from app.schemas.podcast import PodcastListResponse, PodcastEpisodeRead

# Setup SQLite in-memory engine with StaticPool for fast, shared-memory test execution
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def _make_client(**overrides):
    from app.config import get_settings

    settings = get_settings()
    kwargs = {
        "channel_name": settings.mixlr_channel_name or "gcftmedia",
        "channel_id": settings.mixlr_channel_id or "654",
    }
    kwargs.update(overrides)
    return MixlrClient(**kwargs)


@pytest.mark.asyncio
async def test_podcast_rss_sync_and_embeds(db_session: Session):
    service = PodcastService(db_session, client=_make_client())
    stats = await service.sync_from_rss()

    assert stats["total_parsed"] > 0
    assert stats["new"] > 0

    episodes, total = service.get_episodes(skip=0, limit=20)
    assert total > 0
    assert len(episodes) > 0

    first_ep = episodes[0]
    assert first_ep.guid.startswith("mixlr:recording/")
    assert first_ep.recording_id is not None
    assert first_ep.audio_url.endswith(".mp3")
    assert first_ep.embed_url == f"https://gcftmedia.mixlr.com/recordings/{first_ep.recording_id}/embed"
    assert not first_ep.title.lower().endswith(".mp3")
    assert first_ep.duration is not None and first_ep.duration > 0

    # Test idempotency / deduplication
    second_sync = await service.sync_from_rss()
    assert second_sync["new"] == 0
    assert second_sync["updated"] == stats["total_parsed"]


def test_podcast_search_and_pagination(db_session: Session):
    service = PodcastService(db_session)
    episodes, total = service.get_episodes(skip=0, limit=5)
    assert len(episodes) <= 5

    # Test search with a known keyword from the feed like "SERVICE" or "PRAYER"
    results, search_total = service.get_episodes(search="SERVICE")
    assert search_total >= 1
    for ep in results:
        assert "SERVICE" in ep.title.upper() or (ep.description and "SERVICE" in ep.description.upper())


def test_podcast_get_latest_and_by_id(db_session: Session):
    service = PodcastService(db_session)
    latest = service.get_latest_episode()
    assert latest is not None
    assert latest.id is not None

    by_id = service.get_episode_by_id(latest.id)
    assert by_id is not None
    assert by_id.guid == latest.guid


@pytest.mark.asyncio
async def test_mixlr_live_service(db_session: Session):
    service = MixlrService(db_session)
    live_status = await service.fetch_live_status()

    # Verify live platform structure
    assert isinstance(live_status.is_live, bool)
    assert live_status.embed_url == "https://gcftmedia.mixlr.com/embed"
    assert "gcft" in live_status.channel_name.lower() or live_status.channel_name == "GCFTMEDIA"

    # Verify combined live status reporting both Mixlr & YouTube
    combined = await service.get_combined_live_status()
    assert isinstance(combined, LiveStatusRead)
    assert combined.mixlr is not None
    assert combined.youtube is not None
    assert combined.mixlr.embed_url == "https://gcftmedia.mixlr.com/embed"


def test_live_manual_override(db_session: Session):
    service = MixlrService(db_session)
    override = service.update_manual_status(
        platform="mixlr",
        is_live=True,
        title="SPECIAL PRAYER VIGIL",
        stream_url="https://gcftmedia.mixlr.com",
    )
    assert override.is_live is True
    assert override.stream_title == "SPECIAL PRAYER VIGIL"

    # Reset manual status
    service.update_manual_status(platform="mixlr", is_live=False)


def test_fastapi_live_endpoint(client: TestClient):
    response = client.get("/live")
    assert response.status_code == 200
    data = response.json()
    assert "is_live" in data
    assert "mixlr" in data
    assert "youtube" in data
    assert data["mixlr"]["embed_url"] == "https://gcftmedia.mixlr.com/embed"


def test_fastapi_podcasts_endpoints(client: TestClient):
    # Test default rolling 3
    default_res = client.get("/podcasts")
    assert default_res.status_code == 200
    default_data = default_res.json()
    assert len(default_data["items"]) == 3
    assert default_data["count"] == 3

    response = client.get("/podcasts?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert len(data["items"]) > 3

    item = data["items"][0]
    assert "recording_id" in item
    assert "embed_url" in item
    assert item["embed_url"].startswith("https://gcftmedia.mixlr.com/recordings/")
    assert "audio_url" in item

    # Test /podcasts/latest
    latest_res = client.get("/podcasts/latest")
    assert latest_res.status_code == 200
    latest_data = latest_res.json()
    assert latest_data["id"] == item["id"]

    # Test /podcasts/{id}
    detail_res = client.get(f"/podcasts/{item['id']}")
    assert detail_res.status_code == 200
    assert detail_res.json()["guid"] == item["guid"]


# ---------------------------------------------------------------------------
# Offline unit tests for the refactored Mixlr layer (no network required)
# ---------------------------------------------------------------------------

def _channel_view_payload():
    return {
        "data": {
            "id": "654",
            "attributes": {
                "live": True,
                "username": "gcftmedia",
                "profile_image_url": "https://img/logo.png",
                "artwork_url": "https://img/art.png",
                "legacy_livepage_url": "https://mixlr.com/gcftmedia",
                "media": {},
            },
            "relationships": {"current_broadcast": {"data": {"id": "99"}}},
        },
        "included": [
            {
                "type": "broadcast",
                "id": "99",
                "attributes": {
                    "event_id": "7",
                    "title": "Sunday Broadcast",
                    "listener_count": 42,
                    "progressive_stream_url": "https://stream/audio.m3u8",
                    "started_at": "2026-09-20T10:00:00Z",
                },
            },
            {
                "type": "event",
                "id": "7",
                "attributes": {
                    "title": "SUNDAY THANKSGIVING SERVICE",
                    "legacy_url": "https://mixlr.com/gcftmedia/events/5311432",
                    "started_at": "2026-09-20T10:00:00Z",
                },
            },
        ],
    }


def test_mixlr_client_pure_helpers():
    assert clean_title("Sunday Service.mp3 ") == "Sunday Service"
    assert clean_title("Prayer Meeting") == "Prayer Meeting"

    dt = parse_iso_datetime("2026-09-20T10:00:00Z")
    assert dt is not None and dt.tzinfo is not None
    assert parse_iso_datetime("not-a-date") is None
    assert parse_iso_datetime(None) is None

    mapped = map_included(_channel_view_payload()["included"])
    assert mapped[("broadcast", "99")]["title"] == "Sunday Broadcast"

    client = MixlrClient(channel_name="gcftmedia", channel_id="654")
    assert client.embed_url == "https://gcftmedia.mixlr.com/embed"
    assert client.recording_page_url("123") == "https://gcftmedia.mixlr.com/recordings/123"
    assert client.recording_embed_url("123").endswith("/recordings/123/embed")

    status = client.build_live_status_from_channel_view(_channel_view_payload())
    assert status.is_live is True
    # Event title wins over broadcast title
    assert status.title == "SUNDAY THANKSGIVING SERVICE"
    assert status.event_title == "SUNDAY THANKSGIVING SERVICE"
    assert status.broadcast_title == "Sunday Broadcast"
    assert status.audio_stream_url == "https://stream/audio.m3u8"
    assert status.listener_count == 42
    assert status.stream_url == "https://mixlr.com/gcftmedia/events/5311432"

    rec = client.parse_recording_item(
        {
            "id": "555",
            "attributes": {
                "title": "Midweek Service.mp3",
                "description": "Midweek",
                "duration": 3600,
                "created_at": "2026-09-19T18:00:00Z",
                "media": {},
            },
        }
    )
    assert rec["guid"] == "mixlr:recording/555"
    assert rec["title"] == "Midweek Service"
    assert rec["embed_url"] == "https://gcftmedia.mixlr.com/recordings/555/embed"
    assert rec["published_at"] is not None


@pytest.mark.asyncio
async def test_live_cache_is_instance_scoped_and_persists_new_columns(db_session: Session):
    """Regression test: old module-global cache leaked across instances; new one must not.
    Also verifies event_title/broadcast_title/audio_stream_url round-trip through the DB."""
    client_a = MixlrClient(channel_name="gcftmedia", channel_id="654")
    client_b = MixlrClient(channel_name="gcftmedia", channel_id="654")
    svc_a = MixlrService(db_session, client=client_a)
    svc_b = MixlrService(db_session, client=client_b)

    calls = {"n": 0}

    async def fake_v3():
        calls["n"] += 1
        return client_a.build_live_status_from_channel_view(_channel_view_payload())

    client_a.fetch_live_v3 = fake_v3  # type: ignore[method-assign]

    async def explode():
        raise AssertionError("svc_b must not share svc_a cache or HTTP")

    client_b.fetch_live_v3 = explode  # type: ignore[method-assign]
    client_b.fetch_live_legacy = explode  # type: ignore[method-assign]

    first = await svc_a.fetch_live_status()
    second = await svc_a.fetch_live_status()  # served from svc_a instance cache
    assert calls["n"] == 1
    assert first.title == second.title == "SUNDAY THANKSGIVING SERVICE"

    # New columns persisted …
    row = svc_a.get_db_live_status("mixlr")
    assert row is not None
    assert row.event_title == "SUNDAY THANKSGIVING SERVICE"
    assert row.broadcast_title == "Sunday Broadcast"
    assert row.audio_stream_url == "https://stream/audio.m3u8"
    assert row.channel_artwork_url == "https://img/art.png"

    # … and restored by the DB fallback path
    svc_a.invalidate_cache()

    async def fail_all():
        return None

    client_a.fetch_live_v3 = fail_all  # type: ignore[method-assign]
    client_a.fetch_live_legacy = fail_all  # type: ignore[method-assign]
    fallback = await svc_a.fetch_live_status(force_refresh=True)
    assert fallback.event_title == "SUNDAY THANKSGIVING SERVICE"
    assert fallback.audio_stream_url == "https://stream/audio.m3u8"

    # combined status injects YouTube state instead of hardcoding offline
    combined = await svc_a.get_combined_live_status(
        youtube_status=LivePlatformStatus(is_live=True, channel_name="GCFT Church")
    )
    assert combined.active_platform == "both"
    assert combined.is_live is True


@pytest.mark.asyncio
async def test_podcast_mixlr_sync_preserves_mp3_and_upserts(db_session: Session):
    """sync_from_mixlr with a stubbed client: inserts new rows, then updates
    without clobbering an RSS-sourced .mp3 audio_url."""
    client = MixlrClient(channel_name="gcftmedia", channel_id="654")
    service = PodcastService(db_session, client=client)

    async def fake_search(page_size: int = 25):
        return [
            {
                "id": "777",
                "attributes": {
                    "title": "Song Service.mp3",
                    "description": "Songs",
                    "duration": 1800,
                    "created_at": "2026-09-18T18:00:00Z",
                    "media": {},
                },
            }
        ]

    client.search_recordings_raw = fake_search  # type: ignore[method-assign]
    stats = await service.sync_from_mixlr()
    assert stats == {"total_parsed": 1, "new": 1, "updated": 0}

    ep = db_session.query(PodcastEpisode).filter(PodcastEpisode.recording_id == "777").first()
    assert ep is not None
    assert ep.title == "Song Service"  # .mp3 stripped by shared clean_title
    assert ep.embed_url == "https://gcftmedia.mixlr.com/recordings/777/embed"

    # Simulate an RSS sync having stored a direct MP3 enclosure afterwards
    ep.audio_url = "https://audio.mixlr.com/777.mp3"
    db_session.commit()

    stats2 = await service.sync_from_mixlr()
    assert stats2["updated"] == 1
    db_session.refresh(ep)
    assert ep.audio_url == "https://audio.mixlr.com/777.mp3"


def test_shared_paginate_helper(db_session: Session):
    """BaseService.paginate is the single counting path for videos/gallery/podcasts."""
    for i in range(5):
        db_session.add(Video(youtube_id=f"yt-{i}", title=f"Video {i}"))
    db_session.commit()

    service = YouTubeService(db_session)
    items, total = service.get_videos(skip=1, limit=2)
    assert total >= 5
    assert len(items) == 2

    base = BaseService(db_session)
    assert base.get_by_id(Video, items[0].id) is not None
