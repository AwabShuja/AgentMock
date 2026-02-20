"""
Setup router — JD upload & persona retrieval.

Endpoints:
- POST /setup/jd         — submit a Job Description for parsing
- GET  /setup/persona/{session_id} — retrieve generated persona
"""

from fastapi import APIRouter

router = APIRouter(prefix="/setup", tags=["Setup"])
