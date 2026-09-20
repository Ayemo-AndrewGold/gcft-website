from app.routers.videos import router as videos_router
from app.routers.live import router as live_router
from app.routers.podcasts import router as podcasts_router
from app.routers.gallery import router as gallery_router

__all__ = ["videos_router", "live_router", "podcasts_router", "gallery_router"]
