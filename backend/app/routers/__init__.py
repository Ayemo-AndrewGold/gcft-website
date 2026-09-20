from app.routers.videos import router as videos_router
from app.routers.live import router as live_router
from app.routers.podcasts import router as podcasts_router
from app.routers.gallery import router as gallery_router
from app.routers.ebooks import router as ebooks_router
from app.routers.audio_resources import router as audio_resources_router
from app.routers.library import router as library_router

__all__ = [
    "videos_router",
    "live_router",
    "podcasts_router",
    "gallery_router",
    "ebooks_router",
    "audio_resources_router",
    "library_router",
]
