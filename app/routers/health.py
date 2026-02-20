"""
Health-check router.

Provides a lightweight endpoint for uptime monitoring and
deployment readiness probes.
"""

from fastapi import APIRouter

from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Return basic application health status."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
