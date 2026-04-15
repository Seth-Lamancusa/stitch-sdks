"""Custom exceptions for Stitch SDK."""

from typing import Any, Optional


class StitchError(Exception):
    """Base exception for Stitch SDK."""

    pass


class AuthenticationError(StitchError):
    """Authentication failed."""

    pass


class APIError(StitchError):
    """API request failed."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response: Optional[dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

