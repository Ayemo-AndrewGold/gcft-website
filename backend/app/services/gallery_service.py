import asyncio
import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from sqlalchemy import select, or_, func
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader
import cloudinary.utils
from app.config import get_settings
from app.models.gallery_image import GalleryImage
from app.services.base import BaseService

logger = logging.getLogger("gcft_api.services.gallery")


class GalleryService(BaseService[GalleryImage]):
    def __init__(self, db: Session, settings=None):
        super().__init__(db, settings or get_settings())
        self.folder = self.settings.cloudinary_folder

        if self.settings.cloudinary_url:
            cloudinary.config(cloudinary_url=self.settings.cloudinary_url)
        elif (
            self.settings.cloudinary_cloud_name
            and self.settings.cloudinary_api_key
            and self.settings.cloudinary_api_secret
        ):
            cloudinary.config(
                cloud_name=self.settings.cloudinary_cloud_name,
                api_key=self.settings.cloudinary_api_key,
                api_secret=self.settings.cloudinary_api_secret,
                secure=True,
            )

    def generate_transform_urls(self, public_id: str, secure_url: str) -> Tuple[str, str]:
        """Generate automatic responsive variant URLs (thumbnail & optimized view)."""
        cloud_name = self.settings.cloudinary_cloud_name
        if not cloud_name and secure_url:
            m = re.search(r"res\.cloudinary\.com/([^/]+)/", secure_url)
            if m:
                cloud_name = m.group(1)

        cloud_kwargs: Dict[str, Any] = {"cloud_name": cloud_name} if cloud_name else {}

        try:
            thumb_url, _ = cloudinary.utils.cloudinary_url(
                public_id,
                transformation=[
                    {"width": 400, "height": 300, "crop": "fill", "gravity": "auto"},
                    {"fetch_format": "auto", "quality": "auto"},
                ],
                secure=True,
                **cloud_kwargs,
            )
            opt_url, _ = cloudinary.utils.cloudinary_url(
                public_id,
                transformation=[
                    {"width": 1600, "crop": "limit"},
                    {"fetch_format": "auto", "quality": "auto"},
                ],
                secure=True,
                **cloud_kwargs,
            )
            return thumb_url, opt_url
        except Exception as e:
            logger.warning(f"Could not generate Cloudinary transformed URLs for {public_id}: {e}")
            return secure_url, secure_url

    def get_images(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[GalleryImage], int]:
        """Fetch paginated gallery images with optional filters."""
        query = select(GalleryImage).order_by(GalleryImage.created_at.desc())

        if category:
            query = query.where(GalleryImage.category.ilike(category.strip()))

        if is_featured is not None:
            query = query.where(GalleryImage.is_featured == is_featured)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    GalleryImage.title.ilike(pattern),
                    GalleryImage.caption.ilike(pattern),
                    GalleryImage.category.ilike(pattern),
                    GalleryImage.tags.ilike(pattern),
                )
            )

        return self.paginate(query, skip=skip, limit=limit)

    def get_image_by_id(self, image_id: int) -> Optional[GalleryImage]:
        return self.get_by_id(GalleryImage, image_id)

    def get_categories(self) -> List[Dict[str, Any]]:
        """Fetch all distinct categories and their image counts."""
        query = (
            select(GalleryImage.category, func.count(GalleryImage.id).label("count"))
            .where(GalleryImage.category.isnot(None))
            .where(GalleryImage.category != "")
            .group_by(GalleryImage.category)
            .order_by(func.count(GalleryImage.id).desc())
        )
        results = self.db.execute(query).all()
        return [{"category": r[0], "count": r[1]} for r in results]

    def create_image_record(
        self,
        public_id: str,
        image_url: str,
        thumbnail_url: Optional[str] = None,
        optimized_url: Optional[str] = None,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        file_size_bytes: Optional[int] = None,
        format: Optional[str] = None,
        is_featured: bool = False,
    ) -> GalleryImage:
        image = GalleryImage(
            public_id=public_id,
            image_url=image_url,
            thumbnail_url=thumbnail_url,
            optimized_url=optimized_url,
            title=title,
            caption=caption,
            category=category,
            tags=tags,
            width=width,
            height=height,
            file_size_bytes=file_size_bytes,
            format=format,
            is_featured=is_featured,
        )
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    async def upload_and_save(
        self,
        file_content: bytes,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        is_featured: bool = False,
    ) -> GalleryImage:
        """Upload raw image to Cloudinary, calculate variants, and save to DB."""
        # Cloudinary SDK is blocking — run in a thread to keep the loop free.
        upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload,
            file_content,
            folder=self.folder,
            resource_type="image",
        )
        public_id = upload_result.get("public_id")
        secure_url = upload_result.get("secure_url") or upload_result.get("url")
        width = upload_result.get("width")
        height = upload_result.get("height")
        bytes_size = upload_result.get("bytes")
        file_fmt = upload_result.get("format")

        thumb_url, opt_url = self.generate_transform_urls(public_id, secure_url)

        return self.create_image_record(
            public_id=public_id,
            image_url=secure_url,
            thumbnail_url=thumb_url,
            optimized_url=opt_url,
            title=title,
            caption=caption,
            category=category,
            tags=tags,
            width=width,
            height=height,
            file_size_bytes=bytes_size,
            format=file_fmt,
            is_featured=is_featured,
        )

    async def bulk_upload(
        self,
        files: List[Tuple[str, bytes]],
        category: Optional[str] = None,
        default_is_featured: bool = False,
    ) -> List[GalleryImage]:
        """Upload multiple images simultaneously."""
        records = []
        for filename, content in files:
            derived_title = filename.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
            rec = await self.upload_and_save(
                file_content=content,
                title=derived_title,
                category=category,
                is_featured=default_is_featured,
            )
            records.append(rec)
        return records

    def update_image(
        self,
        image_id: int,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[str] = None,
        is_featured: Optional[bool] = None,
    ) -> Optional[GalleryImage]:
        image = self.get_image_by_id(image_id)
        if not image:
            return None

        if title is not None:
            image.title = title
        if caption is not None:
            image.caption = caption
        if category is not None:
            image.category = category
        if tags is not None:
            image.tags = tags
        if is_featured is not None:
            image.is_featured = is_featured

        self.db.commit()
        self.db.refresh(image)
        return image

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
