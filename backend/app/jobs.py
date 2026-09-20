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
        return asyncio.run(service.sync_all())
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
        return asyncio.run(service.fetch_and_upsert_videos())
    finally:
        db.close()


async def check_youtube_live_job():
    """Background task to check YouTube live streaming status during service windows."""
    logger.info("Executing scheduled job: check_youtube_live_job")
    try:
        status = await asyncio.to_thread(_run_check_youtube_live)
        logger.info(f"check_youtube_live_job completed: is_live={status.is_live}")
    except Exception as e:
        logger.error(f"Error executing check_youtube_live_job: {e}")


def _run_check_youtube_live():
    db = SessionLocal()
    try:
        service = YouTubeService(db)
        return asyncio.run(service.fetch_live_status(force_refresh=True))
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
        # Sunday service window live check (Africa/Lagos, every 15 min).
        # Costs ~100 quota units per call → ~400 units per Sunday, well within quota.
        scheduler.add_job(
            check_youtube_live_job,
            "cron",
            day_of_week="sun",
            hour="9",
            minute="*/15",
            timezone="Africa/Lagos",
            id="check_youtube_live",
            replace_existing=True,
        )
        scheduler.start()
        logger.info("APScheduler (async) started successfully.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")
