from datetime import datetime, timezone
from io import BytesIO
from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.models.audio_resource import AudioResource
from app.models.ebook import EBook
from app.models.podcast_episode import PodcastEpisode
from app.models.video import Video
from app.services.audio_resource_service import AudioResourceService
from app.services.ebook_service import EBookService
from app.services.library_service import LibraryService

settings = get_settings()
AUTH_HEADERS = {"X-API-Key": settings.api_key or "your-secret-api-key-here"}


# -- E-Books Tests -------------------------------------------------------------

def test_ebook_crud_and_endpoints(client: TestClient, db_session):
    headers = AUTH_HEADERS

    # 1. Create EBook via API
    payload = {
        "title": "Grace in the Wilderness: A Study of Exodus",
        "author": "Dr. E. Cole",
        "description": "Comprehensive commentary on Exodus.",
        "category": "Theological Commentary",
        "badge_label": "DIGITAL PDF & EPUB",
        "format_label": "Free Theological Resource",
        "page_count": 184,
        "cover_image_url": "https://example.com/exodus.jpg",
        "download_url": "https://example.com/exodus.pdf",
        "file_size_bytes": 10485760,
        "is_featured": True,
    }

    # Unauthorized attempt
    res_unauth = client.post("/ebooks", json=payload)
    assert res_unauth.status_code == 401

    # Authorized creation
    res_create = client.post("/ebooks", json=payload, headers=headers)
    assert res_create.status_code == 201
    created = res_create.json()
    assert created["id"] is not None
    assert created["title"] == payload["title"]
    assert created["page_count"] == 184
    assert created["download_count"] == 0

    ebook_id = created["id"]

    # 2. Get single e-book
    res_get = client.get(f"/ebooks/{ebook_id}")
    assert res_get.status_code == 200
    assert res_get.json()["title"] == payload["title"]

    # 3. List e-books with filters & search
    res_list = client.get("/ebooks?category=Theological%20Commentary")
    assert res_list.status_code == 200
    assert res_list.json()["total"] >= 1

    res_search = client.get("/ebooks?search=Wilderness")
    assert res_search.status_code == 200
    assert res_search.json()["total"] >= 1

    # 4. Update e-book
    res_update = client.put(
        f"/ebooks/{ebook_id}",
        json={"title": "Grace in the Wilderness (2nd Edition)", "page_count": 192},
        headers=headers,
    )
    assert res_update.status_code == 200
    assert res_update.json()["title"] == "Grace in the Wilderness (2nd Edition)"
    assert res_update.json()["page_count"] == 192

    # 5. Download tracking
    res_dl = client.post(f"/ebooks/{ebook_id}/download")
    assert res_dl.status_code == 200
    dl_data = res_dl.json()
    assert dl_data["download_count"] == 1
    assert dl_data["download_url"] == payload["download_url"]

    # 6. Delete e-book
    res_del = client.delete(f"/ebooks/{ebook_id}", headers=headers)
    assert res_del.status_code == 200

    # Verify not found after deletion
    res_not_found = client.get(f"/ebooks/{ebook_id}")
    assert res_not_found.status_code == 404


def test_ebook_upload_endpoint(client: TestClient):
    headers = AUTH_HEADERS

    fake_pdf = BytesIO(b"%PDF-1.4 fake pdf content")
    fake_cover = BytesIO(b"fake image content")

    mock_doc_resp = {"secure_url": "https://cloudinary.com/doc.pdf", "bytes": 50000}
    mock_cover_resp = {"secure_url": "https://cloudinary.com/cover.jpg"}

    with patch.object(EBookService, "upload_asset") as mock_upload:
        mock_upload.side_effect = [mock_doc_resp, mock_cover_resp]

        files = {
            "file": ("devotion.pdf", fake_pdf, "application/pdf"),
            "cover": ("cover.jpg", fake_cover, "image/jpeg"),
        }
        data = {
            "title": "The Habit of Solitude",
            "author": "Pastor Bennett",
            "description": "Workbook on reducing digital noise.",
            "category": "Devotional",
            "page_count": "92",
            "is_featured": "true",
        }

        res = client.post("/ebooks/upload", files=files, data=data, headers=headers)
        assert res.status_code == 201
        res_data = res.json()
        assert res_data["title"] == "The Habit of Solitude"
        assert res_data["download_url"] == "https://cloudinary.com/doc.pdf"
        assert res_data["cover_image_url"] == "https://cloudinary.com/cover.jpg"
        assert res_data["page_count"] == 92


# -- Audio Resources Tests -----------------------------------------------------

def test_audio_resource_crud_and_endpoints(client: TestClient, db_session):
    headers = AUTH_HEADERS

    # 1. Create Audio Resource
    payload = {
        "title": "Romans Unleashed: The Architecture of Grace",
        "author": "Pastor Bennett",
        "description": "Verse-by-verse journey through Romans.",
        "category": "Audio Series",
        "badge_label": "AUDIO SERIES • 8 PARTS",
        "parts_count": 8,
        "duration_text": "5 hrs 10 mins",
        "duration_seconds": 18600,
        "cover_image_url": "https://example.com/romans.jpg",
        "audio_url": "https://example.com/romans.mp3",
        "is_featured": True,
    }

    res_create = client.post("/audio-resources", json=payload, headers=headers)
    assert res_create.status_code == 201
    created = res_create.json()
    assert created["id"] is not None
    assert created["title"] == payload["title"]
    assert created["badge_label"] == "AUDIO SERIES • 8 PARTS"
    assert created["listen_count"] == 0

    audio_id = created["id"]

    # 2. Get single audio resource
    res_get = client.get(f"/audio-resources/{audio_id}")
    assert res_get.status_code == 200
    assert res_get.json()["parts_count"] == 8

    # 3. List audio resources
    res_list = client.get("/audio-resources?category=Audio%20Series")
    assert res_list.status_code == 200
    assert res_list.json()["total"] >= 1

    # 4. Listen tracking
    res_listen = client.post(f"/audio-resources/{audio_id}/listen")
    assert res_listen.status_code == 200
    assert res_listen.json()["listen_count"] == 1

    # 5. Update audio resource
    res_update = client.put(
        f"/audio-resources/{audio_id}",
        json={"duration_text": "5 hrs 15 mins"},
        headers=headers,
    )
    assert res_update.status_code == 200
    assert res_update.json()["duration_text"] == "5 hrs 15 mins"

    # 6. Delete audio resource
    res_del = client.delete(f"/audio-resources/{audio_id}", headers=headers)
    assert res_del.status_code == 200


def test_audio_resource_upload_endpoint(client: TestClient):
    headers = AUTH_HEADERS

    fake_mp3 = BytesIO(b"fake mp3 audio stream")
    fake_cover = BytesIO(b"fake album art")

    mock_audio_resp = {"secure_url": "https://cloudinary.com/audio.mp3", "bytes": 25000000, "duration": 7200}
    mock_cover_resp = {"secure_url": "https://cloudinary.com/audio_cover.jpg"}

    with patch.object(AudioResourceService, "upload_asset") as mock_upload:
        mock_upload.side_effect = [mock_audio_resp, mock_cover_resp]

        files = {
            "file": ("sermon.mp3", fake_mp3, "audio/mpeg"),
            "cover": ("cover.jpg", fake_cover, "image/jpeg"),
        }
        data = {
            "title": "Morning Whispers: 30 Days in the Psalms",
            "author": "Elena Vance",
            "description": "Daily 8-minute morning meditations.",
            "category": "Devotional Audio",
            "badge_label": "DEVOTIONAL AUDIO • 30 DAYS",
            "duration_text": "4 hrs 20 mins",
            "is_featured": "true",
        }

        res = client.post("/audio-resources/upload", files=files, data=data, headers=headers)
        assert res.status_code == 201
        res_data = res.json()
        assert res_data["title"] == "Morning Whispers: 30 Days in the Psalms"
        assert res_data["audio_url"] == "https://cloudinary.com/audio.mp3"
        assert res_data["cover_image_url"] == "https://cloudinary.com/audio_cover.jpg"


# -- Unified Featured Feed Tests -----------------------------------------------

def test_unified_library_featured_endpoint(client: TestClient, db_session):
    # Seed an EBook
    ebook = EBook(
        title="Foundations for Little Hands: Family Devotions",
        author="GCFT Children Ministry",
        description="Illustrated dinner table conversations.",
        category="Family",
        badge_label="FAMILY RESOURCE GUIDE",
        format_label="Printable PDF Included",
        page_count=120,
        download_url="https://example.com/family.pdf",
        is_featured=True,
    )
    db_session.add(ebook)

    # Seed an AudioResource
    audio = AudioResource(
        title="The Contemplative Heart: Walking with the Desert Fathers",
        author="Dr. E. Cole",
        description="An audio-guided journey through stillness.",
        category="Audio Book",
        badge_label="AUDIO BOOK • 6 PARTS",
        parts_count=6,
        duration_text="3 hrs 45 mins",
        audio_url="https://example.com/heart.mp3",
        is_featured=True,
    )
    db_session.add(audio)

    # Seed a YouTube Video
    video = Video(
        youtube_id="featured_yt_777",
        title="Anchored in Turbulent Seas (Full Message)",
        description="Pastor David Bennett delivers an exposition of Paul's words.",
        thumbnail_url="https://img.youtube.com/vi/featured_yt_777/hqdefault.jpg",
        published_at=datetime(2026, 9, 20, 10, 0, 0, tzinfo=timezone.utc),
    )
    db_session.add(video)
    db_session.commit()

    # Call unified GET /library/featured
    response = client.get("/library/featured?limit=3")
    assert response.status_code == 200
    data = response.json()

    # Verify 3 tabs in response
    assert "audio" in data
    assert "ebooks" in data
    assert "videos" in data

    # Verify Audio card details
    assert len(data["audio"]) >= 1
    found_audio = next(a for a in data["audio"] if a["title"] == audio.title)
    assert found_audio["badge_label"] == "AUDIO BOOK • 6 PARTS"
    assert found_audio["duration_text"] == "3 hrs 45 mins"

    # Verify E-Book card details
    assert len(data["ebooks"]) >= 1
    found_ebook = next(e for e in data["ebooks"] if e["title"] == ebook.title)
    assert found_ebook["page_count"] == 120
    assert found_ebook["format_label"] == "Printable PDF Included"

    # Verify Video card details
    assert len(data["videos"]) >= 1
    found_video = next(v for v in data["videos"] if v["youtube_id"] == "featured_yt_777")
    assert found_video["watch_url"] == "https://www.youtube.com/watch?v=featured_yt_777"
    assert found_video["embed_url"] == "https://www.youtube.com/embed/featured_yt_777"


def test_library_featured_fallback_to_podcasts_when_no_audiobooks(client: TestClient, db_session):    # Clear audio resources
    db_session.query(AudioResource).delete()

    # Seed a podcast episode
    podcast = PodcastEpisode(
        guid="mixlr-service-broadcast-fallback",
        recording_id="998877",
        title="Special Healing Service",
        description="Sunday miracle broadcast",
        audio_url="https://apicdn.mixlr.com/broadcasts/998877.mp3",
        duration=3600,
        published_at=datetime(2026, 9, 15, 10, 0, 0, tzinfo=timezone.utc),
    )
    db_session.add(podcast)
    db_session.commit()

    # Call GET /library/featured
    response = client.get("/library/featured")
    assert response.status_code == 200
    data = response.json()

    # Audio tab should gracefully fall back to the podcast episode
    assert len(data["audio"]) >= 1
    fallback_item = next((a for a in data["audio"] if a["title"] == "Special Healing Service"), None)
    assert fallback_item is not None
    assert fallback_item["duration_text"] == "1 hr"
    assert fallback_item["audio_url"] == podcast.audio_url


def test_upload_endpoints_reject_unsupported_types(client: TestClient):
    # .exe is neither PDF nor EPUB
    res = client.post(
        "/ebooks/upload",
        headers=AUTH_HEADERS,
        files={"file": ("evil.exe", b"MZ fake", "application/x-msdownload")},
        data={"title": "Nope"},
    )
    assert res.status_code == 400

    # PDF is not an audio track
    res = client.post(
        "/audio-resources/upload",
        headers=AUTH_HEADERS,
        files={"file": ("doc.pdf", b"%PDF-1.4 fake", "application/pdf")},
        data={"title": "Nope"},
    )
    assert res.status_code == 400

    # Bad cover image type is rejected even when the main file is valid
    res = client.post(
        "/ebooks/upload",
        headers=AUTH_HEADERS,
        files={
            "file": ("book.pdf", b"%PDF-1.4 fake", "application/pdf"),
            "cover": ("cover.pdf", b"%PDF-1.4 fake", "application/pdf"),
        },
        data={"title": "Nope"},
    )
    assert res.status_code == 400
