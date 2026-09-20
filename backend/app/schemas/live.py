from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LivePlatformStatus(BaseModel):
    is_live: bool = False
    video_id: Optional[str] = None
    title: Optional[str] = None
    event_title: Optional[str] = None
    broadcast_title: Optional[str] = None
    stream_url: Optional[str] = None
    embed_url: Optional[str] = None
    audio_stream_url: Optional[str] = None
    channel_name: Optional[str] = None
    channel_logo_url: Optional[str] = None
    channel_artwork_url: Optional[str] = None
    listener_count: Optional[int] = None
    started_at: Optional[datetime] = None



class LiveStatusRead(BaseModel):
    is_live: bool
    active_platform: Optional[str] = None  # "mixlr", "youtube", "both", or None
    mixlr: LivePlatformStatus
    youtube: Optional[LivePlatformStatus] = None
    manual_override: bool = False
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LiveStatusUpdate(BaseModel):
    platform: str = "mixlr"
    is_live: Optional[bool] = None
    video_id: Optional[str] = None
    stream_title: Optional[str] = None
    stream_url: Optional[str] = None
    embed_url: Optional[str] = None
    clear_override: bool = False

