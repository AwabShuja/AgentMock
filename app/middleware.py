"""
Application middleware — CORS, global exception handlers, request logging.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.exceptions import (
    AuthenticationError,
    AuthorizationError,
    CareerFitException,
)


def register_middleware(app: FastAPI) -> None:
    """Attach all middleware and exception handlers to the app."""

    # ── CORS ─────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: lock down in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Global Exception Handlers ────────────────────────────────────
    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(
        _request: Request, exc: AuthenticationError
    ) -> JSONResponse:
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(AuthorizationError)
    async def authorization_error_handler(
        _request: Request, exc: AuthorizationError
    ) -> JSONResponse:
        return JSONResponse(status_code=403, content={"detail": exc.detail})

    @app.exception_handler(CareerFitException)
    async def careerfit_error_handler(
        _request: Request, exc: CareerFitException
    ) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": exc.detail})
