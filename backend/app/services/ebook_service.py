import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from app.config import get_settings
from app.models.ebook import EBook
from app.schemas.ebook import EBookCreate, EBookUpdate
from app.services.base import BaseService
from app.utils.cloudinary import configure_cloudinary

logger = logging.getLogger("gcft_api.services.ebook")


class EBookService(BaseService[EBook]):
    def __init__(self, db: Session, settings=None):
        super().__init__(db, settings or get_settings())
        self.folder = f"{self.settings.cloudinary_folder}/ebooks"
        configure_cloudinary(self.settings)

    def get_ebooks(
        self,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        is_featured: Optional[bool] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[EBook], int]:
        """Fetch paginated e-books with optional filters."""
        query = select(EBook).order_by(
            EBook.is_featured.desc(),
            EBook.published_at.desc().nullslast(),
            EBook.id.desc(),
        )

        if category:
            query = query.where(EBook.category.ilike(category.strip()))

        if is_featured is not None:
            query = query.where(EBook.is_featured == is_featured)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.where(
                or_(
                    EBook.title.ilike(pattern),
                    EBook.author.ilike(pattern),
                    EBook.description.ilike(pattern),
                    EBook.category.ilike(pattern),
                )
            )

        return self.paginate(query, skip=skip, limit=limit)

    def get_ebook_by_id(self, ebook_id: int) -> Optional[EBook]:
        return self.get_by_id(EBook, ebook_id)

    def create_ebook(self, payload: EBookCreate) -> EBook:
        ebook = EBook(**payload.model_dump())
        self.db.add(ebook)
        self.db.commit()
        self.db.refresh(ebook)
        return ebook

    def update_ebook(self, ebook_id: int, payload: EBookUpdate) -> Optional[EBook]:
        ebook = self.get_ebook_by_id(ebook_id)
        if not ebook:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(ebook, key, value)

        self.db.commit()
        self.db.refresh(ebook)
        return ebook

    def delete_ebook(self, ebook_id: int) -> bool:
        ebook = self.get_ebook_by_id(ebook_id)
        if not ebook:
            return False
        self.db.delete(ebook)
        self.db.commit()
        return True

    def increment_download(self, ebook_id: int) -> Optional[EBook]:
        ebook = self.get_ebook_by_id(ebook_id)
        if not ebook:
            return None
        ebook.download_count = (ebook.download_count or 0) + 1
        self.db.commit()
        self.db.refresh(ebook)
        return ebook

    async def upload_asset(
        self,
        file_bytes: bytes,
        filename: str,
        resource_type: str = "raw",
        subfolder: str = "files",
    ) -> Dict[str, Any]:
        """Upload a raw document or image cover to Cloudinary asynchronously."""
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
        format_label: Optional[str] = None,
        page_count: Optional[int] = None,
        is_featured: bool = False,
    ) -> EBook:
        """Upload document and optional cover, then save the EBook record."""
        # 1. Upload the book file (PDF / EPUB)
        doc_res = await self.upload_asset(
            file_bytes, filename, resource_type="raw", subfolder="documents"
        )
        download_url = doc_res.get("secure_url") or doc_res.get("url")
        file_size_bytes = doc_res.get("bytes")

        # 2. Upload cover artwork if provided
        cover_image_url = None
        if cover_bytes and cover_filename:
            cover_res = await self.upload_asset(
                cover_bytes, cover_filename, resource_type="image", subfolder="covers"
            )
            cover_image_url = cover_res.get("secure_url") or cover_res.get("url")

        # 3. Create EBook record
        payload = EBookCreate(
            title=title,
            author=author,
            description=description,
            category=category,
            badge_label=badge_label or "DIGITAL PDF & EPUB",
            format_label=format_label or "Free Theological Resource",
            page_count=page_count,
            cover_image_url=cover_image_url,
            download_url=download_url,
            file_size_bytes=file_size_bytes,
            is_featured=is_featured,
        )
        return self.create_ebook(payload)
