"""
Central API router.

Aggregates every endpoint router and registers them here.
``main.py`` imports only this single router — keeping the app
factory clean and preventing direct coupling to individual endpoints.
"""

from fastapi import APIRouter

from app.api.endpoints import auth, coach, health, interview, sessions, setup

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(setup.router)
api_router.include_router(sessions.router)
api_router.include_router(interview.router)
api_router.include_router(coach.router)
