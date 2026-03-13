"""
Shared / common Pydantic models.

Base models, standard response wrappers, and enums reused
across multiple domains.
"""

from datetime import datetime
from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


# ── Enums ────────────────────────────────────────────────────────────


class SessionStatus(str, Enum):
    """Allowed states for an interview session."""

    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# ── Standard response wrappers ───────────────────────────────────────


class MessageResponse(BaseModel):
    """Simple message response (e.g. for deletes, logouts)."""

    message: str


class DataResponse(BaseModel, Generic[T]):
    """Generic wrapper: ``{"data": <payload>}``."""

    data: T


class ErrorResponse(BaseModel):
    """Error payload returned by exception handlers."""

    detail: str


# ── Timestamp mixin ──────────────────────────────────────────────────


class TimestampMixin(BaseModel):
    """Provides created_at / updated_at fields for DB-backed models."""

    created_at: datetime
    updated_at: Optional[datetime] = None
