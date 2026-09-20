from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GCFT API"
    environment: str = "development"
    debug: bool = True
    api_key: Optional[str] = "your-secret-api-key-here"

    # Database Settings
    database_url: str

    # YouTube API
    youtube_api_key: Optional[str] = None
    youtube_channel_id: Optional[str] = None
    youtube_live_cache_seconds: int = 180
    youtube_recordings_sync_limit: int = 25

    # Cloudinary Integration
    cloudinary_url: Optional[str] = None
    cloudinary_cloud_name: Optional[str] = None
    cloudinary_api_key: Optional[str] = None
    cloudinary_api_secret: Optional[str] = None
    cloudinary_folder: str = "gcft_gallery"

    # Mixlr & Audio Streaming
    mixlr_channel_name: Optional[str] = None
    mixlr_channel_id: Optional[str] = None
    podcast_rss_url: Optional[str] = None
    mixlr_live_cache_seconds: int = 60

    # Scheduled Jobs
    job_sync_interval_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
