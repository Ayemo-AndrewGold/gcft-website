"""Shared parsing helpers for external media APIs (Mixlr, YouTube)."""

import logging
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger("gcft_api.utils.datetime")


def parse_iso_datetime(raw: Any) -> Optional[datetime]:
    """Parse ISO 8601 / RFC 3339 timestamps, tolerating a trailing 'Z'."""
    if not raw or not isinstance(raw, str):
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to parse datetime string '{raw}': {e}")
        return None
