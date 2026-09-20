from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base
from app.models.base import PrimaryKeyMixin


class LiveStatus(PrimaryKeyMixin, Base):
    __tablename__ = "live_status"

    platform: Mapped[str] = mapped_column(String(50), default="mixlr", nullable=False, index=True)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stream_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    # Extra titles exposed by LivePlatformStatus; kept so persist/fallback round-trips losslessly.
    event_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    broadcast_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stream_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    embed_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    audio_stream_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    channel_logo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    channel_artwork_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    listener_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

