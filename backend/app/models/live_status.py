from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class LiveStatus(Base):
    __tablename__ = "live_status"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    platform: Mapped[str] = mapped_column(String(50), default="mixlr", nullable=False, index=True)
    is_live: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    stream_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    stream_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    embed_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    channel_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    channel_logo_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    listener_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

