"""
Interview session endpoints.

Routes:
    POST /sessions             — create a new interview session
    GET  /sessions             — list all sessions for the authenticated user
    GET  /sessions/{id}        — get details of a specific session
    PATCH /sessions/{id}       — update session metadata (e.g., status)
    DELETE /sessions/{id}      — delete a session and its transcript
"""

from fastapi import APIRouter

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# Endpoint implementations will be added in Phase 3.
