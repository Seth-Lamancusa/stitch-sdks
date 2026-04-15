"""Users resource - stub implementation."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


class Users:
    """Sync users resource (stub)."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def me(self, *args, **kwargs):
        """Get current user profile. Not yet implemented."""
        raise NotImplementedError("Users.me() is not yet implemented")

    def get(self, user_id: str, *args, **kwargs):
        """Get a user by ID. Not yet implemented."""
        raise NotImplementedError("Users.get() is not yet implemented")

    def search(self, *args, **kwargs):
        """Search users. Not yet implemented."""
        raise NotImplementedError("Users.search() is not yet implemented")

    def update_profile(self, *args, **kwargs):
        """Update current user profile. Not yet implemented."""
        raise NotImplementedError("Users.update_profile() is not yet implemented")


class AsyncUsers:
    """Async users resource (stub)."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def me(self, *args, **kwargs):
        """Get current user profile. Not yet implemented."""
        raise NotImplementedError("AsyncUsers.me() is not yet implemented")

    async def get(self, user_id: str, *args, **kwargs):
        """Get a user by ID. Not yet implemented."""
        raise NotImplementedError("AsyncUsers.get() is not yet implemented")

    async def search(self, *args, **kwargs):
        """Search users. Not yet implemented."""
        raise NotImplementedError("AsyncUsers.search() is not yet implemented")

    async def update_profile(self, *args, **kwargs):
        """Update current user profile. Not yet implemented."""
        raise NotImplementedError("AsyncUsers.update_profile() is not yet implemented")

