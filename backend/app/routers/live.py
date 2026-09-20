from fastapi import APIRouter, Depends, Query
from app.dependencies import get_mixlr_service, get_youtube_service, verify_api_key
from app.schemas.live import LiveStatusRead, LiveStatusUpdate
from app.services.mixlr_service import MixlrService
from app.services.youtube_service import YouTubeService

router = APIRouter(prefix="/live", tags=["Live Stream"])


@router.get("", response_model=LiveStatusRead)
async def get_live_status(
    force_refresh: bool = Query(False, description="Bypass in-memory cache and fetch directly from sources"),
    mixlr_service: MixlrService = Depends(get_mixlr_service),
    youtube_service: YouTubeService = Depends(get_youtube_service),
):
    """
    Get unified live stream status for Mixlr (audio) and YouTube (video).
    Returns real-time broadcasting state, metadata, and ready-to-embed iframe URLs.
    """
    yt_status = await youtube_service.fetch_live_status(force_refresh=force_refresh)
    if force_refresh:
        await mixlr_service.fetch_live_status(force_refresh=True)
    return await mixlr_service.get_combined_live_status(youtube_status=yt_status)


@router.put("/status", response_model=LiveStatusRead)
async def update_live_status(
    payload: LiveStatusUpdate,
    mixlr_service: MixlrService = Depends(get_mixlr_service),
    youtube_service: YouTubeService = Depends(get_youtube_service),
    _: str = Depends(verify_api_key),
):
    """
    Manually update/override live stream status (protected endpoint for church media admins).
    """
    if payload.platform.lower() == "youtube":
        yt_status = youtube_service.update_manual_status(
            is_live=payload.is_live,
            title=payload.stream_title,
            stream_url=payload.stream_url,
            embed_url=payload.embed_url,
            video_id=payload.video_id,
            clear_override=payload.clear_override,
        )
    else:
        if payload.clear_override:
            mixlr_service.invalidate_cache()
        else:
            mixlr_service.update_manual_status(
                platform=payload.platform,
                is_live=payload.is_live,
                title=payload.stream_title,
                stream_url=payload.stream_url,
                embed_url=payload.embed_url,
            )
        yt_status = await youtube_service.fetch_live_status()

    res = await mixlr_service.get_combined_live_status(youtube_status=yt_status)
    res.manual_override = True
    return res
