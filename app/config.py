"""
Application configuration via pydantic-settings.

All settings are loaded from environment variables (or a .env file).
Each config group is a separate class for clarity; they are composed
into a single ``Settings`` object that the rest of the app imports.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """General application settings."""

    APP_NAME: str = "CareerFit AI"
    APP_VERSION: str = "0.1.0"
    APP_ENV: str = "development"  # development | staging | production
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class SupabaseSettings(BaseSettings):
    """Supabase connection settings."""

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""  # anon / public key

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GroqSettings(BaseSettings):
    """Groq API settings."""

    GROQ_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GoogleOAuthSettings(BaseSettings):
    """Google OAuth credentials (used by Supabase Auth)."""

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Settings(
    AppSettings,
    SupabaseSettings,
    GroqSettings,
    GoogleOAuthSettings,
):
    """
    Unified settings object.

    Inherits every config group so the app only needs a single import::

        from app.config import settings
        print(settings.SUPABASE_URL)
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# ── Singleton instance ───────────────────────────────────────────────
settings = Settings()
