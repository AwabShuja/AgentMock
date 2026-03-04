"""
Security utilities — JWT verification and ``get_current_user`` dependency.

Supabase issues JWTs signed with the project's JWT secret (HS256).
This module verifies those tokens and extracts the authenticated
user's ID + metadata so route handlers can use ``Depends(get_current_user)``.
"""

import logging

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import settings
from app.exceptions import AuthenticationError

logger = logging.getLogger(__name__)

# FastAPI security scheme — expects ``Authorization: Bearer <token>``
_bearer_scheme = HTTPBearer(auto_error=False)


def _decode_supabase_jwt(token: str) -> dict:
    """Decode and verify a Supabase-issued JWT.

    Raises ``AuthenticationError`` if the token is invalid, expired,
    or the JWT secret is not configured.
    """
    secret = settings.SUPABASE_JWT_SECRET
    if not secret:
        raise AuthenticationError("Server JWT secret is not configured.")

    try:
        payload = jwt.decode(
            token,
            secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Token has expired.")
    except jwt.InvalidTokenError as exc:
        raise AuthenticationError(f"Invalid token: {exc}")


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
) -> dict:
    """FastAPI dependency — resolve the authenticated user from the JWT.

    Returns a dict with at least ``{"id": "<uuid>", "email": "..."}``.

    Usage::

        @router.get("/me")
        async def me(user: dict = Depends(get_current_user)):
            return user
    """
    if credentials is None:
        raise AuthenticationError("Missing authorization header.")

    payload = _decode_supabase_jwt(credentials.credentials)

    user_id: str | None = payload.get("sub")
    email: str | None = payload.get("email")

    if not user_id:
        raise AuthenticationError("Token does not contain a valid user ID.")

    user_metadata = payload.get("user_metadata", {})

    return {
        "id": user_id,
        "email": email or "",
        "full_name": user_metadata.get("full_name", user_metadata.get("name", "")),
        "avatar_url": user_metadata.get("avatar_url", user_metadata.get("picture", "")),
    }
