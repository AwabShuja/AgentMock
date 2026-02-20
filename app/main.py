"""
CareerFit AI — FastAPI application entry-point.

Creates the app with a lifespan context manager that initialises
shared clients (Supabase, Groq) and tears them down on shutdown.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.core.groq_client import init_groq_client
from app.core.supabase_client import init_supabase_client
from app.middleware import register_middleware
from app.routers import auth, coach, health, interview, sessions, setup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle hook."""

    # ── Startup ──────────────────────────────────────────────────────
    app.state.supabase = init_supabase_client()
    app.state.groq = init_groq_client()

    yield

    # ── Shutdown (cleanup if needed) ─────────────────────────────────


def create_app() -> FastAPI:
    """Application factory."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Voice-based AI interviewer & career coach.",
        lifespan=lifespan,
    )

    # Middleware & exception handlers
    register_middleware(app)

    # ── Routers ──────────────────────────────────────────────────────
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(setup.router)
    app.include_router(sessions.router)
    app.include_router(interview.router)
    app.include_router(coach.router)

    return app


app = create_app()
