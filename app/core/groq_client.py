"""
Groq client initialisation.

Provides access to both the LLM (chat completions) and Whisper STT
through the same ``Groq`` SDK client.
"""

import logging
from typing import Optional

from groq import Groq

from app.config import settings

logger = logging.getLogger(__name__)


def init_groq_client() -> Optional[Groq]:
    """Create and return a Groq client instance.

    Returns ``None`` with a warning if the API key is missing,
    allowing the app to boot during early development.
    """
    api_key = settings.GROQ_API_KEY

    if not api_key or "placeholder" in api_key.lower():
        logger.warning(
            "Groq API key not configured — client is disabled. "
            "Set GROQ_API_KEY in your .env file."
        )
        return None

    return Groq(api_key=api_key)
