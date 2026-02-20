"""
Sessions router — CRUD for interview sessions.

Endpoints:
- POST /sessions       — create a new interview session
- GET  /sessions       — list user's sessions
- GET  /sessions/{id}  — get session details
"""

from fastapi import APIRouter

router = APIRouter(prefix="/sessions", tags=["Sessions"])
