"""
Shared FastAPI dependencies (Depends-injectable).

Each function here returns a pre-initialised client or validated
resource that route handlers and services can depend on.
"""

from typing import Optional

from fastapi import Request
from groq import Groq
from supabase import Client


def get_supabase(request: Request) -> Optional[Client]:
    """Return the Supabase client stored on app state at startup."""
    return request.app.state.supabase


def get_groq(request: Request) -> Optional[Groq]:
    """Return the Groq client stored on app state at startup."""
    return request.app.state.groq
