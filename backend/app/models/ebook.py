from datetime import datetime
from typing import Optional
from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.base import TimestampMixin


class EBook(TimestampMixin, Base):
    __tablename__ = "ebooks"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)

    # UI Badges & Metadata
    badge_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    format_label: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    page_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Media & File Assets
    cover_image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    download_url: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    download_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
