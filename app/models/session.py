"""
Interview session Pydantic schemas.

Request / response models for creating, listing, and retrieving
interview sessions and their transcripts.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.common import SessionStatus


# ── Request schemas ──────────────────────────────────────────────────


class SessionCreate(BaseModel):
    """Body for POST /sessions — create a new interview session."""

    job_description: str = Field(
        ..., min_length=20, description="The full Job Description text."
    )
    title: Optional[str] = Field(
        None, max_length=200, description="Short label, e.g. 'Senior React Dev'."
    )


# ── Response schemas ─────────────────────────────────────────────────


class SessionOut(BaseModel):
    """Single session returned in API responses."""

    id: str
    user_id: str
    title: Optional[str] = None
    job_description: str
    persona: Optional[dict[str, Any]] = None
    status: SessionStatus
    created_at: datetime
    updated_at: Optional[datetime] = None


class SessionListOut(BaseModel):
    """Lightweight session item for list views (no full JD)."""

    id: str
    title: Optional[str] = None
    status: SessionStatus
    created_at: datetime
