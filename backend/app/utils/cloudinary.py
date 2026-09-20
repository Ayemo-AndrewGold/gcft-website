"""Shared Cloudinary configuration for upload services."""

import cloudinary


def configure_cloudinary(settings) -> None:
    """Apply Cloudinary credentials from app settings.

    Prefers a full ``CLOUDINARY_URL``; otherwise falls back to the individual
    cloud name / API key / secret triple. No-op when nothing is configured
    (useful for tests that mock the uploader).
    """
    if settings.cloudinary_url:
        cloudinary.config(cloudinary_url=settings.cloudinary_url)
    elif (
        settings.cloudinary_cloud_name
        and settings.cloudinary_api_key
        and settings.cloudinary_api_secret
    ):
        cloudinary.config(
            cloud_name=settings.cloudinary_cloud_name,
            api_key=settings.cloudinary_api_key,
            api_secret=settings.cloudinary_api_secret,
            secure=True,
        )
