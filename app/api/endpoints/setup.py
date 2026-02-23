"""
Setup endpoints — Job Description parsing & persona management.

Routes:
    POST /setup/jd                        — submit a Job Description for AI parsing
    GET  /setup/persona/{session_id}      — retrieve the generated interviewer persona
"""

from fastapi import APIRouter

router = APIRouter(prefix="/setup", tags=["Setup"])

# Endpoint implementations will be added in Phase 3.
