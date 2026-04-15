"""Recipients resource - stub implementation."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


class Recipients:
    """Sync recipients resource (stub)."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def add(self, *args, **kwargs):
        """Add recipients to a message. Not yet implemented."""
        raise NotImplementedError("Recipients.add() is not yet implemented")

    def remove(self, *args, **kwargs):
        """Remove a recipient from a message. Not yet implemented."""
        raise NotImplementedError("Recipients.remove() is not yet implemented")


class AsyncRecipients:
    """Async recipients resource (stub)."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def add(self, *args, **kwargs):
        """Add recipients to a message. Not yet implemented."""
        raise NotImplementedError("AsyncRecipients.add() is not yet implemented")

    async def remove(self, *args, **kwargs):
        """Remove a recipient from a message. Not yet implemented."""
        raise NotImplementedError("AsyncRecipients.remove() is not yet implemented")

