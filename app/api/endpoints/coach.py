"""
Coach endpoints — post-interview feedback.

Routes:
    POST /coach/analyse/{session_id}   — trigger the Coach Agent to analyse
                                         a completed session's transcript
    GET  /coach/feedback/{session_id}  — retrieve the structured JSON feedback
                                         report for a given session
"""

from fastapi import APIRouter

router = APIRouter(prefix="/coach", tags=["Coach"])

# Endpoint implementations will be added in Phase 5.
