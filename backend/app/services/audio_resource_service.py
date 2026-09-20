import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from app.config import get_settings
from app.models.audio_resource import AudioResource
from app.schemas.audio_resource import AudioResourceCreate, AudioResourceUpdate
from app.services.base import BaseService
from app.utils.cloudinary import configure_cloudinary

logger = logging.getLogger("gcft_api.services.audio_resource")


class AudioResourceService(BaseService[AudioResource]):
    def __init__(self, db: Session, settings=None):
        super().__init__(db, settings or get_settings())
        self.folder = f"{self.settings.cloudinary_folder}/audio"
        configure_cloudinary(self.settings)

    def get_audio_resources(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[AudioResource], int]:
        """Fetch paginated audiobooks/series with optional filters."""
        query = select(AudioResource).order_by(
            AudioResource.is_featured.desc(),
            AudioResource.published_at.desc().nullslast(),
            AudioResource.id.desc(),
        )

        if category:
            query = query.where(AudioResource.category.ilike(category.strip()))

        if is_featured is not None:
            query = query.where(AudioResource.is_featured == is_featured)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    AudioResource.title.ilike(pattern),
                    AudioResource.author.ilike(pattern),
                    AudioResource.description.ilike(pattern),
                    AudioResource.category.ilike(pattern),
                )
            )

        return self.paginate(query, skip=skip, limit=limit)

    def get_audio_resource_by_id(self, resource_id: int) -> Optional[AudioResource]:
        return self.get_by_id(AudioResource, resource_id)

    def create_audio_resource(self, payload: AudioResourceCreate) -> AudioResource:
        resource = AudioResource(**payload.model_dump())
        self.db.add(resource)
        self.db.commit()
        self.db.refresh(resource)
        return resource

    def update_audio_resource(
        self, resource_id: int, payload: AudioResourceUpdate
    ) -> Optional[AudioResource]:
        resource = self.get_audio_resource_by_id(resource_id)
        if not resource:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(resource, key, value)

        self.db.commit()
        self.db.refresh(resource)
        return resource

    def delete_audio_resource(self, resource_id: int) -> bool:
        resource = self.get_audio_resource_by_id(resource_id)
        if not resource:
            return False
        self.db.delete(resource)
        self.db.commit()
        return True

    def increment_listen(self, resource_id: int) -> Optional[AudioResource]:
        resource = self.get_audio_resource_by_id(resource_id)
        if not resource:
            return None
        resource.listen_count = (resource.listen_count or 0) + 1
        self.db.commit()
        self.db.refresh(resource)
        return resource

    async def upload_asset(
        self,
        file_bytes: bytes,
        filename: str,
        resource_type: str = "video",
        subfolder: str = "tracks",
    ) -> Dict[str, Any]:
        """Upload audio (Cloudinary uses resource_type='video' for audio) or cover image."""
        folder_path = f"{self.folder}/{subfolder}"
        # Derive a readable public_id from the original filename; Cloudinary
        # appends a suffix on collision (unique_filename=True).
        public_id = (filename.rsplit(".", 1)[0] or "upload")[:100]
        return await asyncio.to_thread(
            cloudinary.uploader.upload,
            file_bytes,
            folder=folder_path,
            public_id=public_id,
            resource_type=resource_type,
            unique_filename=True,
        )

    async def upload_and_create(
        self,
        file_bytes: bytes,
        filename: str,
        title: str,
        cover_bytes: Optional[bytes] = None,
        cover_filename: Optional[str] = None,
        author: Optional[str] = None,
        description: Optional[str] = None,
        category: Optional[str] = None,
        badge_label: Optional[str] = None,
        parts_count: Optional[int] = None,
        duration_seconds: Optional[int] = None,
        duration_text: Optional[str] = None,
        is_featured: bool = False,
    ) -> AudioResource:
        """Upload audio and optional cover, then save the AudioResource record."""
        # 1. Upload audio file (resource_type='video' covers mp3/m4a/wav in Cloudinary)
        audio_res = await self.upload_asset(
            file_bytes, filename, resource_type="video", subfolder="tracks"
        )
        audio_url = audio_res.get("secure_url") or audio_res.get("url")
        file_size_bytes = audio_res.get("bytes")
        if not duration_seconds and audio_res.get("duration"):
            duration_seconds = int(audio_res["duration"])

        # 2. Upload cover artwork if provided
        cover_image_url = None
        if cover_bytes and cover_filename:
            cover_res = await self.upload_asset(
                cover_bytes, cover_filename, resource_type="image", subfolder="covers"
            )
            cover_image_url = cover_res.get("secure_url") or cover_res.get("url")

        # 3. Create record
        payload = AudioResourceCreate(
            title=title,
            author=author,
            description=description,
            category=category,
            badge_label=badge_label or "AUDIO BOOK",
            parts_count=parts_count,
            duration_seconds=duration_seconds,
            duration_text=duration_text,
            cover_image_url=cover_image_url,
            audio_url=audio_url,
            file_size_bytes=file_size_bytes,
            is_featured=is_featured,
        )
        return self.create_audio_resource(payload)
