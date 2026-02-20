"""
Shared FastAPI dependencies (Depends-injectable).

Each function here returns a pre-initialised client or validated
resource that route handlers and services can depend on.
"""

from fastapi import Request
from supabase import Client


def get_supabase(request: Request) -> Client:
    """Return the Supabase client stored on app state at startup."""
    return request.app.state.supabase
