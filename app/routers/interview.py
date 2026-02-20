"""
Interview router — WebSocket endpoint for the live voice interview.

Endpoints:
- WS /interview/{session_id} — real-time turn-based interview
"""

from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["Interview"])
