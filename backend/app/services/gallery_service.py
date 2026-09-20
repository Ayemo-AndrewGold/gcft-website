import asyncio
import logging
from typing import List, Optional, Tuple
from sqlalchemy import select
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
from app.config import get_settings
from app.models.gallery_image import GalleryImage
from app.services.base import BaseService

logger = logging.getLogger("gcft_api.services.gallery")


class GalleryService(BaseService[GalleryImage]):
    def __init__(self, db: Session, settings=None):
        super().__init__(db, settings or get_settings())
        if self.settings.cloudinary_url:
            cloudinary.config(cloudinary_url=self.settings.cloudinary_url)

    def get_images(self, skip: int = 0, limit: int = 20) -> Tuple[List[GalleryImage], int]:
        query = select(GalleryImage).order_by(GalleryImage.created_at.desc())
        return self.paginate(query, skip=skip, limit=limit)

    def get_image_by_id(self, image_id: int) -> Optional[GalleryImage]:
        return self.get_by_id(GalleryImage, image_id)

    def create_image_record(self, public_id: str, image_url: str, title: Optional[str] = None, caption: Optional[str] = None) -> GalleryImage:
        image = GalleryImage(
            public_id=public_id,
            image_url=image_url,
            title=title,
            caption=caption,
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    async def upload_and_save(self, file_content: bytes, title: Optional[str] = None, caption: Optional[str] = None) -> GalleryImage:
        # Cloudinary SDK is blocking — run in a thread to keep the loop free.
        upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload, file_content, folder="gcft_gallery"
        )
        public_id = upload_result.get("public_id")
        secure_url = upload_result.get("secure_url") or upload_result.get("url")

        return self.create_image_record(
            public_id=public_id,
            image_url=secure_url,
            title=title,
            caption=caption,
        )

    def delete_image(self, image_id: int) -> bool:
        image = self.get_image_by_id(image_id)
        if not image:
            return False

        try:
            cloudinary.uploader.destroy(image.public_id)
        except Exception as e:
            logger.error(f"Failed to delete Cloudinary asset {image.public_id}: {e}")

        self.db.delete(image)
        self.db.commit()
        return True
