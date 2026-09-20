import logging
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import get_settings
from app.database import SessionLocal
from app.services.podcast_service import PodcastService

logger = logging.getLogger("gcft_api.jobs")
settings = get_settings()

scheduler = BackgroundScheduler()


def sync_youtube_videos_job():
    """Background task to fetch latest videos from YouTube API."""
    logger.info("Executing scheduled job: sync_youtube_videos_job")
    # YouTube sync will be implemented alongside YouTube module


def sync_podcasts_job():
    """Background task to fetch latest podcast episodes from Mixlr recordings API and RSS feed."""
    logger.info("Executing scheduled job: sync_podcasts_job")
    db = SessionLocal()
    try:
        service = PodcastService(db)
        stats = service.sync_all()
        logger.info(f"sync_podcasts_job completed: {stats}")
    except Exception as e:
        logger.error(f"Error executing sync_podcasts_job: {e}")
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
        logger.info("APScheduler started successfully.")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler stopped.")
