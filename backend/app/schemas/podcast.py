from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.common import PaginatedResponse, TimestampRead


class PodcastEpisodeBase(BaseModel):
    guid: str
    recording_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    audio_url: str
    embed_url: Optional[str] = None
    image_url: Optional[str] = None
    recording_page_url: Optional[str] = None
    file_size_bytes: Optional[int] = None
    duration: Optional[int] = None
    published_at: Optional[datetime] = None



class PodcastEpisodeCreate(PodcastEpisodeBase):
    pass


class PodcastEpisodeRead(PodcastEpisodeBase, TimestampRead):
    pass


# Backwards-compatible alias; new code should use PaginatedResponse[PodcastEpisodeRead].
class PodcastListResponse(PaginatedResponse["PodcastEpisodeRead"]):
    pass

