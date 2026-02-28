"""
Authentication endpoints — Google OAuth via Supabase Auth.

Routes:
    POST /auth/login      — returns the Google OAuth consent URL
    GET  /auth/callback   — exchanges the OAuth code for a session
    GET  /auth/me         — returns the current user's profile
    POST /auth/logout     — signs the user out
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from supabase import Client

from app.core.security import get_current_user
from app.dependencies import get_supabase
from app.models.common import MessageResponse
from app.models.user import AuthUserResponse, OAuthURLResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ── Helpers ──────────────────────────────────────────────────────────


def _auth_service(supabase: Client = Depends(get_supabase)) -> AuthService:
    """Provide an AuthService instance via dependency injection."""
    return AuthService(supabase)


# ── Endpoints ────────────────────────────────────────────────────────


@router.post(
    "/login",
    response_model=OAuthURLResponse,
    summary="Start Google OAuth login",
)
async def login(
    redirect_to: Optional[str] = Query(
        None,
        description="Frontend URL to redirect to after Google auth.",
    ),
    auth_service: AuthService = Depends(_auth_service),
):
    """Return the Google OAuth consent URL.

    The frontend should redirect the user to the returned ``url``.
    After the user authenticates with Google, Supabase redirects
    back to ``redirect_to`` (or the default ``FRONTEND_URL/auth/callback``)
    with a ``code`` query parameter.
    """
    url = auth_service.get_google_oauth_url(redirect_to)
    return OAuthURLResponse(url=url)


@router.get(
    "/callback",
    summary="OAuth callback — exchange code for session",
)
async def callback(
    code: str = Query(..., description="Authorization code from Google OAuth"),
    auth_service: AuthService = Depends(_auth_service),
):
    """Exchange the OAuth authorization code for a Supabase session.

    Returns the ``access_token``, ``refresh_token``, and basic user info.
    The frontend should store the access token and include it as
    ``Authorization: Bearer <token>`` in subsequent requests.
    """
    session_data = auth_service.exchange_code_for_session(code)
    return session_data


@router.get(
    "/me",
    response_model=AuthUserResponse,
    summary="Get current user profile",
)
async def me(
    current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(_auth_service),
):
    """Return the authenticated user's profile.

    Attempts to fetch from the ``profiles`` table first. Falls back
    to the JWT-embedded metadata if the profile row is not yet created.
    """
    profile = auth_service.get_profile(current_user["id"])

    if profile:
        return AuthUserResponse(
            id=str(profile["id"]),
            email=profile.get("email", current_user["email"]),
            full_name=profile.get("full_name"),
            avatar_url=profile.get("avatar_url"),
        )

    # Fallback to JWT-embedded data
    return AuthUserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        avatar_url=current_user.get("avatar_url"),
    )


@router.post(
    "/logout",
    response_model=MessageResponse,
    summary="Sign out the current user",
)
async def logout(
    _current_user: dict = Depends(get_current_user),
    auth_service: AuthService = Depends(_auth_service),
):
    """Sign the current user out of Supabase Auth."""
    auth_service.sign_out()
    return MessageResponse(message="Successfully signed out.")
