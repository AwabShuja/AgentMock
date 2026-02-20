"""
Authentication router — Google OAuth via Supabase Auth.

Endpoints:
- POST /auth/login   — initiate Google OAuth flow
- GET  /auth/callback — handle OAuth callback
- GET  /auth/me       — return current authenticated user
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])
