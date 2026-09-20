from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    """Shared integer primary key."""

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


class TimestampMixin(PrimaryKeyMixin):
    """Shared id + created_at/updated_at columns used by most models."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
