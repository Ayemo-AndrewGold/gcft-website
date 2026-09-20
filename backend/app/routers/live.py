from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_api_key
from app.schemas.live import LiveStatusRead, LiveStatusUpdate
from app.services.mixlr_service import MixlrService

router = APIRouter(prefix="/live", tags=["Live Stream"])


@router.get("", response_model=LiveStatusRead)
async def get_live_status(
    force_refresh: bool = Query(False, description="Bypass in-memory cache and fetch directly from sources"),
    db: Session = Depends(get_db),
):
    """
    Get unified live stream status for Mixlr (audio) and YouTube (video).
    Returns real-time broadcasting state, listener count, metadata, and ready-to-embed iframe URLs.
    """
    service = MixlrService(db)
    if force_refresh:
        await service.fetch_live_status(force_refresh=True)
    return await service.get_combined_live_status()


@router.put("/status", response_model=LiveStatusRead)
async def update_live_status(
    payload: LiveStatusUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_api_key),
):
    """
    Manually update/override live stream status (protected endpoint for church media admins).
    """
    service = MixlrService(db)
    service.update_manual_status(
        platform=payload.platform,
        is_live=payload.is_live,
        title=payload.stream_title,
        stream_url=payload.stream_url,
        embed_url=payload.embed_url,
    )
    return await service.get_combined_live_status()
