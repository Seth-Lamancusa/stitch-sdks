"""Managed users resource - stub implementation."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


class Managed:
    """Sync managed users resource (stub)."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def list(self, *args, **kwargs):
        """List managed users. Not yet implemented."""
        raise NotImplementedError("Managed.list() is not yet implemented")

    def create(self, *args, **kwargs):
        """Create a managed user. Not yet implemented."""
        raise NotImplementedError("Managed.create() is not yet implemented")

    def switch(self, *args, **kwargs):
        """Switch to a managed user session. Not yet implemented."""
        raise NotImplementedError("Managed.switch() is not yet implemented")


class AsyncManaged:
    """Async managed users resource (stub)."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def list(self, *args, **kwargs):
        """List managed users. Not yet implemented."""
        raise NotImplementedError("AsyncManaged.list() is not yet implemented")

    async def create(self, *args, **kwargs):
        """Create a managed user. Not yet implemented."""
        raise NotImplementedError("AsyncManaged.create() is not yet implemented")

    async def switch(self, *args, **kwargs):
        """Switch to a managed user session. Not yet implemented."""
        raise NotImplementedError("AsyncManaged.switch() is not yet implemented")

