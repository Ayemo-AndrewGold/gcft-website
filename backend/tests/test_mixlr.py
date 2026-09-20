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
from app.services.podcast_service import PodcastService
from app.services.mixlr_service import MixlrService
from app.schemas.live import LiveStatusRead
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


def test_podcast_rss_sync_and_embeds(db_session: Session):
    service = PodcastService(db_session)
    stats = service.sync_from_rss()

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
    second_sync = service.sync_from_rss()
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
