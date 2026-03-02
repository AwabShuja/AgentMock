"""
Auth service — business logic for authentication flows.

Orchestrates Google OAuth via the Supabase SDK and profile retrieval.
All Supabase interactions for auth live here; endpoints stay thin.
"""

import logging
from typing import Optional

from supabase import Client

from app.config import settings
from app.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


class AuthService:
    """Handles authentication business logic against Supabase."""

    def __init__(self, supabase: Client):
        self._sb = supabase

    # ── Google OAuth ─────────────────────────────────────────────────

    def get_google_oauth_url(self, redirect_to: Optional[str] = None) -> str:
        """Return the Google consent-screen URL for the OAuth flow.

        ``redirect_to`` is where Supabase redirects after the user
        authenticates with Google (typically the frontend callback page).
        """
        if self._sb is None:
            raise AuthenticationError("Supabase client is not configured.")

        redirect_url = redirect_to or f"{settings.FRONTEND_URL}/auth/callback"

        response = self._sb.auth.sign_in_with_oauth(
            {
                "provider": "google",
                "options": {"redirect_to": redirect_url},
            }
        )
        return response.url

    # ── Token exchange ───────────────────────────────────────────────

    def exchange_code_for_session(self, code: str) -> dict:
        """Exchange an OAuth authorization code for a Supabase session.

        Returns the raw session dict containing ``access_token``,
        ``refresh_token``, ``user``, etc.
        """
        if self._sb is None:
            raise AuthenticationError("Supabase client is not configured.")

        try:
            response = self._sb.auth.exchange_code_for_session(
                {"auth_code": code}
            )
            session = response.session
            user = response.user

            if not session or not user:
                raise AuthenticationError("Failed to exchange code for session.")

            return {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_in": session.expires_in,
                "token_type": "bearer",
                "user": {
                    "id": str(user.id),
                    "email": user.email or "",
                    "full_name": (user.user_metadata or {}).get(
                        "full_name", (user.user_metadata or {}).get("name", "")
                    ),
                    "avatar_url": (user.user_metadata or {}).get(
                        "avatar_url", (user.user_metadata or {}).get("picture", "")
                    ),
                },
            }
        except AuthenticationError:
            raise
        except Exception as exc:
            logger.error("OAuth code exchange failed: %s", exc)
            raise AuthenticationError("Failed to exchange authorization code.")

    # ── Profile lookup ───────────────────────────────────────────────

    def get_profile(self, user_id: str) -> Optional[dict]:
        """Fetch a user profile from the ``profiles`` table by user ID."""
        if self._sb is None:
            raise AuthenticationError("Supabase client is not configured.")

        response = (
            self._sb.table("profiles")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        return response.data

    # ── Sign out ─────────────────────────────────────────────────────

    def sign_out(self) -> None:
        """Sign the current user out of Supabase Auth."""
        if self._sb is None:
            raise AuthenticationError("Supabase client is not configured.")

        self._sb.auth.sign_out()
