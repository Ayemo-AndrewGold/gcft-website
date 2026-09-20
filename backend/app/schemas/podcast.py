from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


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


class PodcastEpisodeRead(PodcastEpisodeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PodcastListResponse(BaseModel):
    total: int
    count: Optional[int] = None
    items: List[PodcastEpisodeRead]

