import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.config import get_settings
from app.database import SessionLocal
from app.services.podcast_service import PodcastService
from app.services.youtube_service import YouTubeService

logger = logging.getLogger("gcft_api.jobs")
settings = get_settings()

scheduler = AsyncIOScheduler()


async def sync_podcasts_job():
    """Background task: latest podcast episodes from Mixlr recordings API and RSS feed."""
    logger.info("Executing scheduled job: sync_podcasts_job")
    try:
        # SessionLocal is sync — keep blocking DB work off the event loop.
        stats = await asyncio.to_thread(_run_sync_podcasts)
        logger.info(f"sync_podcasts_job completed: {stats}")
    except Exception as e:
        logger.error(f"Error executing sync_podcasts_job: {e}")


def _run_sync_podcasts() -> dict:
    db = SessionLocal()
    try:
        service = PodcastService(db)
        # service.sync_all is async; this thread has no running loop, so run it here.
        import asyncio as _asyncio

        return _asyncio.run(service.sync_all())
    finally:
        db.close()


async def sync_youtube_videos_job():
    """Background task to fetch latest videos from YouTube API."""
    logger.info("Executing scheduled job: sync_youtube_videos_job")
    try:
        count = await asyncio.to_thread(_run_sync_youtube)
        logger.info(f"sync_youtube_videos_job completed: {count} videos")
    except Exception as e:
        logger.error(f"Error executing sync_youtube_videos_job: {e}")


def _run_sync_youtube() -> int:
    db = SessionLocal()
    try:
        service = YouTubeService(db)
        import asyncio as _asyncio

        return _asyncio.run(service.fetch_and_upsert_videos())
    finally:
        db.close()


def start_scheduler():
    if not scheduler.running:
        scheduler.add_job(
            sync_youtube_videos_job,
            "interval",
            minutes=settings.job_sync_interval_minutes,
            id="sync_youtube_videos",
            replace_existing=True,
        )
        scheduler.add_job(
            sync_podcasts_job,
            "interval",
            minutes=settings.job_sync_interval_minutes,
            id="sync_podcasts",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("APScheduler (async) started successfully.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")
