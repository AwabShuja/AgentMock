"""
Interview endpoint — WebSocket for the live voice interview.

Routes:
    WS /interview/{session_id}  — turn-based voice interview over WebSocket.

WebSocket message protocol:
    Client → Server:  {"type": "audio", "data": "<base64-encoded-audio>"}
    Server → Client:  {"type": "transcript", "text": "<user speech>"}
    Server → Client:  {"type": "agent_text", "text": "<interviewer response>"}
    Server → Client:  {"type": "agent_audio", "data": "<base64-encoded-audio>"}
    Server → Client:  {"type": "turn_complete", "turn_number": 1}
    Server → Client:  {"type": "session_ended"}
"""

from fastapi import APIRouter

router = APIRouter(prefix="/interview", tags=["Interview"])

# WebSocket endpoint implementation will be added in Phase 4.
