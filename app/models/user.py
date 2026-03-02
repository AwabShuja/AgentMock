"""
User-related Pydantic schemas.

Covers the data returned by Supabase Auth and the ``profiles`` table.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ── Response schemas ─────────────────────────────────────────────────


class UserProfile(BaseModel):
    """Public-facing user profile (from the ``profiles`` table)."""

    id: str                         # UUID as string
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime


class AuthUserResponse(BaseModel):
    """Returned by GET /auth/me — the authenticated user's profile."""

    id: str
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


# ── OAuth response ───────────────────────────────────────────────────


class OAuthURLResponse(BaseModel):
    """Returned by POST /auth/login — the Google OAuth redirect URL."""

    url: str
