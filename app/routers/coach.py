"""
Coach router — feedback retrieval.

Endpoints:
- POST /coach/analyse/{session_id} — trigger feedback generation
- GET  /coach/feedback/{session_id} — retrieve structured feedback
"""

from fastapi import APIRouter

router = APIRouter(prefix="/coach", tags=["Coach"])
