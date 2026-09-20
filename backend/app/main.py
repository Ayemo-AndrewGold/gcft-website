from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.jobs import start_scheduler, stop_scheduler
from app.routers import videos_router, live_router, podcasts_router, gallery_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup lifecycle: ensure DB tables are created and start scheduler
    try:
        from app.database import Base, engine
        import app.models  # noqa: F401
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        import logging
        logging.getLogger("gcft_api").warning(f"Database initialization warning: {e}")
    start_scheduler()
    yield
    # Shutdown lifecycle
    stop_scheduler()


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend REST API for Church Content, Media, Live Streaming, and Gallery Management.",
    lifespan=lifespan,
    debug=settings.debug,
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(videos_router)
app.include_router(live_router)
app.include_router(podcasts_router)
app.include_router(gallery_router)


@app.get("/", tags=["Health"])
def health_check():
    """Root health check endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.environment,
    }
