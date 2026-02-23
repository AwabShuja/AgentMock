"""
Authentication endpoints — Google OAuth via Supabase Auth.

Routes:
    POST /auth/login      — initiate Google OAuth flow (returns redirect URL)
    GET  /auth/callback   — handle OAuth callback from Google
    GET  /auth/me         — return the current authenticated user profile
    POST /auth/logout     — sign the current user out
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Endpoint implementations will be added in Phase 2.
