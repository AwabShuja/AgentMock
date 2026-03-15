"""
Setup-domain schemas for Job Description parsing and persona retrieval.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

from app.models.common import SessionStatus


class SetupJDRequest(BaseModel):
    """Request body for POST /setup/jd."""

    job_description: str = Field(
        ..., min_length=20, description="Raw job description text."
    )
    title: Optional[str] = Field(
        None, max_length=200, description="Optional custom session title."
    )


class SetupSessionResponse(BaseModel):
    """Response for a created setup session with generated persona."""

    session_id: str
    title: Optional[str] = None
    status: SessionStatus
    persona: dict[str, Any]
    created_at: datetime


class PersonaResponse(BaseModel):
    """Response for GET /setup/persona/{session_id}."""

    session_id: str
    status: SessionStatus
    persona: dict[str, Any]
