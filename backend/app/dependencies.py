from typing import Optional
from fastapi import Header, HTTPException, status, Query
from pydantic import BaseModel
from app.config import get_settings

settings = get_settings()


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 20


def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of records to return"),
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)


def get_podcast_pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(3, ge=1, le=100, description="Number of records to return (defaults to rolling latest 3)"),
) -> PaginationParams:
    return PaginationParams(skip=skip, limit=limit)



def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Optional/Mandatory API key validation dependency for protected administrative endpoints.
    """
    if not settings.api_key:
        return x_api_key or ""
    
    if x_api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return x_api_key
