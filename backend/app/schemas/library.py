from typing import List
from pydantic import BaseModel, ConfigDict
from app.schemas.audio_resource import AudioResourceRead
from app.schemas.ebook import EBookRead
from app.schemas.video import VideoRead


class LibraryFeaturedResponse(BaseModel):
    """
    Unified 3-in-1 media response for the frontend Archives & Media Library section.
    Delivers the top featured items for Audio Books, E-Books, and YouTube Videos in a single call.
    """
    audio: List[AudioResourceRead]
    ebooks: List[EBookRead]
    videos: List[VideoRead]

    model_config = ConfigDict(from_attributes=True)
