"""
Health-check endpoint.

Provides a lightweight route for uptime monitoring and
deployment readiness probes.
"""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(prefix="", tags=["Health"])


@router.get("/health", summary="Health check")
async def health_check():
    """Return application health status."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
