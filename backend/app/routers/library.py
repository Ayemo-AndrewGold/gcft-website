from fastapi import APIRouter, Depends, Query
from app.dependencies import get_library_service
from app.schemas.library import LibraryFeaturedResponse
from app.services.library_service import LibraryService

router = APIRouter(prefix="/library", tags=["Media Library"])


@router.get("/featured", response_model=LibraryFeaturedResponse)
def get_featured_media(
    limit: int = Query(3, ge=1, le=10, description="Number of items to return per media tab"),
    service: LibraryService = Depends(get_library_service),
):
    """
    Get unified featured media feed across Audio Books, E-Books, and YouTube Videos in a single request.
    Powers the 3-tab 'Nourishment for the Spiritual Mind' media library section on the frontend.
    """
    return service.get_featured(limit=limit)
