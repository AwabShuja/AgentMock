"""
Supabase client initialisation.

Called once during app startup via the lifespan hook.
"""

import logging
from typing import Optional

from supabase import Client, create_client

from app.config import settings

logger = logging.getLogger(__name__)


def init_supabase_client() -> Optional[Client]:
    """Create and return a Supabase client instance.

    Returns ``None`` with a warning if credentials are missing or
    invalid, allowing the app to boot during early development.
    """
    url = settings.SUPABASE_URL
    key = settings.SUPABASE_KEY

    if not url or not key or "placeholder" in key.lower():
        logger.warning(
            "Supabase credentials not configured — client is disabled. "
            "Set SUPABASE_URL and SUPABASE_KEY in your .env file."
        )
        return None

    try:
        return create_client(url, key)
    except Exception as exc:
        logger.warning("Failed to initialise Supabase client: %s", exc)
        return None
