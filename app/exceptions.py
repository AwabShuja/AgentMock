"""
Custom exception classes for CareerFit AI.

All domain-specific exceptions live here. They are caught by the
global exception handlers registered in ``app.middleware``.
"""


class CareerFitException(Exception):
    """Base exception for the application."""

    def __init__(self, detail: str = "An unexpected error occurred."):
        self.detail = detail
        super().__init__(self.detail)


class AuthenticationError(CareerFitException):
    """Raised when authentication fails (invalid/expired token, etc.)."""

    def __init__(self, detail: str = "Authentication failed."):
        super().__init__(detail)


class AuthorizationError(CareerFitException):
    """Raised when a user lacks permission for a resource."""

    def __init__(self, detail: str = "You do not have access to this resource."):
        super().__init__(detail)


class SessionNotFoundError(CareerFitException):
    """Raised when a requested interview session does not exist."""

    def __init__(self, detail: str = "Interview session not found."):
        super().__init__(detail)


class AgentError(CareerFitException):
    """Raised when an AI agent encounters an error."""

    def __init__(self, detail: str = "The AI agent encountered an error."):
        super().__init__(detail)
