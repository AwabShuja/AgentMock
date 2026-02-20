"""
Supabase client initialisation.

Called once during app startup via the lifespan hook.
"""

from supabase import Client, create_client

from app.config import settings


def init_supabase_client() -> Client:
    """Create and return a Supabase client instance."""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
