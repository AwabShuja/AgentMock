"""
Groq client initialisation.

Provides access to both the LLM (chat completions) and Whisper STT
through the same ``Groq`` SDK client.
"""

from groq import Groq

from app.config import settings


def init_groq_client() -> Groq:
    """Create and return a Groq client instance."""
    return Groq(api_key=settings.GROQ_API_KEY)
