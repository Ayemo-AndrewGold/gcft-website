from unittest.mock import patch
import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from app.config import get_settings
from app.models.gallery_image import GalleryImage
from app.services.gallery_service import GalleryService

settings = get_settings()
AUTH_HEADERS = {"X-API-Key": settings.api_key or "your-secret-api-key-here"}


def test_gallery_transform_urls(db_session: Session):
    service = GalleryService(db_session)
    thumb_url, opt_url = service.generate_transform_urls(
        public_id="gcft_gallery/sample_1",
        secure_url="https://res.cloudinary.com/gcft/image/upload/v12345/gcft_gallery/sample_1.jpg",
    )
    assert "w_400" in thumb_url or "400" in thumb_url
    assert "w_1600" in opt_url or "1600" in opt_url
    assert "f_auto" in thumb_url
    assert "q_auto" in opt_url


@pytest.mark.asyncio
async def test_gallery_upload_and_save(db_session: Session):
    service = GalleryService(db_session)

    mock_upload_response = {
        "public_id": "gcft_gallery/test_photo_1",
        "secure_url": "https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/test_photo_1.jpg",
        "width": 1920,
        "height": 1080,
        "bytes": 245000,
        "format": "jpg",
    }

    with patch("cloudinary.uploader.upload", return_value=mock_upload_response):
        image = await service.upload_and_save(
            file_content=b"fake_image_content",
            title="Sunday Celebration",
            caption="Worship service snapshot",
            category="services",
            tags="worship,sunday",
            is_featured=True,
        )

        assert image.id is not None
        assert image.public_id == "gcft_gallery/test_photo_1"
        assert image.title == "Sunday Celebration"
        assert image.category == "services"
        assert image.width == 1920
        assert image.height == 1080
        assert image.file_size_bytes == 245000
        assert image.is_featured is True
        assert image.thumbnail_url is not None
        assert image.optimized_url is not None


def test_gallery_get_images_and_filters(db_session: Session):
    service = GalleryService(db_session)

    # Insert a few diverse gallery images
    service.create_image_record(
        public_id="gcft_gallery/img_service",
        image_url="https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/img_service.jpg",
        title="Sunday Service",
        category="services",
        is_featured=True,
    )
    service.create_image_record(
        public_id="gcft_gallery/img_youth",
        image_url="https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/img_youth.jpg",
        title="Youth Camp 2026",
        category="youth",
        is_featured=False,
    )
    service.create_image_record(
        public_id="gcft_gallery/img_outreach",
        image_url="https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/img_outreach.jpg",
        title="Community Outreach",
        category="outreach",
        is_featured=False,
    )

    # All images
    all_images, total = service.get_images(limit=10)
    assert total >= 3

    # Filter by category
    youth_images, youth_total = service.get_images(category="youth")
    assert youth_total >= 1
    assert all(img.category == "youth" for img in youth_images)

    # Filter by featured
    featured_images, featured_total = service.get_images(is_featured=True)
    assert featured_total >= 1
    assert all(img.is_featured is True for img in featured_images)

    # Search filter
    search_results, search_total = service.get_images(search="Outreach")
    assert search_total >= 1
    assert any("Outreach" in img.title for img in search_results)


def test_gallery_categories_endpoint(client: TestClient):
    res = client.get("/gallery/categories")
    assert res.status_code == 200
    data = res.json()
    assert "total_categories" in data
    assert "categories" in data
    assert len(data["categories"]) > 0


def test_gallery_api_endpoints(client: TestClient):
    # 1. Unauthenticated upload should fail (401)
    res = client.post(
        "/gallery/upload",
        files={"file": ("test.png", b"\x89PNG\r\n\x1a\n", "image/png")},
    )
    assert res.status_code == 401

    # 2. Authenticated upload with mock
    mock_upload_response = {
        "public_id": "gcft_gallery/api_upload_test",
        "secure_url": "https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/api_upload_test.png",
        "width": 800,
        "height": 600,
        "bytes": 50000,
        "format": "png",
    }

    with patch("cloudinary.uploader.upload", return_value=mock_upload_response):
        res = client.post(
            "/gallery/upload",
            headers=AUTH_HEADERS,
            files={"file": ("test.png", b"\x89PNG\r\n\x1a\n", "image/png")},
            data={"title": "Praise Night", "category": "conferences", "is_featured": "true"},
        )
        assert res.status_code == 201
        data = res.json()
        assert data["message"] == "Image uploaded and optimized successfully"
        image_id = data["image"]["id"]
        assert data["image"]["title"] == "Praise Night"
        assert data["image"]["category"] == "conferences"
        assert data["image"]["is_featured"] is True

    # 3. GET single image
    res = client.get(f"/gallery/{image_id}")
    assert res.status_code == 200
    assert res.json()["id"] == image_id

    # 4. PATCH update image metadata
    res = client.patch(
        f"/gallery/{image_id}",
        headers=AUTH_HEADERS,
        json={"title": "Updated Praise Night", "is_featured": False},
    )
    assert res.status_code == 200
    assert res.json()["title"] == "Updated Praise Night"
    assert res.json()["is_featured"] is False

    # 5. Bulk upload with unique public_ids
    counter = 0
    def dynamic_upload(*args, **kwargs):
        nonlocal counter
        counter += 1
        return {
            "public_id": f"gcft_gallery/bulk_photo_{counter}",
            "secure_url": f"https://res.cloudinary.com/gcft/image/upload/v1/gcft_gallery/bulk_photo_{counter}.jpg",
            "width": 1200,
            "height": 800,
            "bytes": 60000,
            "format": "jpg",
        }

    with patch("cloudinary.uploader.upload", side_effect=dynamic_upload):
        res = client.post(
            "/gallery/upload/bulk",
            headers=AUTH_HEADERS,
            files=[
                ("files", ("photo-1.jpg", b"fake1", "image/jpeg")),
                ("files", ("photo-2.jpg", b"fake2", "image/jpeg")),
            ],
            data={"category": "worship", "is_featured": "false"},
        )
        assert res.status_code == 201
        bulk_data = res.json()
        assert bulk_data["total_uploaded"] == 2
        assert len(bulk_data["items"]) == 2

    # 6. DELETE image
    with patch("cloudinary.uploader.destroy", return_value={"result": "ok"}):
        del_res = client.delete(f"/gallery/{image_id}", headers=AUTH_HEADERS)
        assert del_res.status_code == 200

        # Confirm 404 after deletion
        get_res = client.get(f"/gallery/{image_id}")
        assert get_res.status_code == 404
