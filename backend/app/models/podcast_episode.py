from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class PodcastEpisode(Base):
    __tablename__ = "podcast_episodes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    guid: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    recording_id: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_url: Mapped[str] = mapped_column(String(512), nullable=False)
    embed_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    recording_page_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    file_size_bytes: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # duration in seconds
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

