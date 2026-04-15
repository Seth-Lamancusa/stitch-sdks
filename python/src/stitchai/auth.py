"""Authentication manager for Stitch API."""

import time
from typing import Any, Optional

import httpx

from .exceptions import AuthenticationError


class AuthManager:
    """Manages API key -> JWT token exchange and refresh."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 30.0,
        requested_scopes: str = "msg.read msg.write",
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.requested_scopes = requested_scopes

        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expires_at: float = 0.0

    def _is_token_valid(self) -> bool:
        """Check if current access token is still valid (with 15s buffer)."""
        return bool(self._access_token) and time.time() + 15 < self._expires_at

    def _mint_token(self, client: httpx.Client) -> None:
        """Exchange API key for JWT access token."""
        url = f"{self.base_url}/v1/auth/token"
        try:
            response = client.post(
                url,
                headers={"x-api-key": self.api_key},
                json={"requested_scopes": self.requested_scopes},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(
                f"Failed to authenticate: {e.response.status_code}"
            ) from e

        data = response.json()
        self._access_token = data["access_token"]
        self._refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in", 600)
        self._expires_at = time.time() + expires_in - 30

    def ensure_token(self, client: httpx.Client) -> str:
        """Ensure we have a valid access token, minting if necessary."""
        if not self._is_token_valid():
            self._mint_token(client)
        return self._access_token or ""

    def get_auth_headers(self, client: httpx.Client) -> dict[str, str]:
        """Get authorization headers with valid token."""
        token = self.ensure_token(client)
        return {"Authorization": f"Bearer {token}"}


class AsyncAuthManager:
    """Async version of AuthManager."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        timeout: float = 30.0,
        requested_scopes: str = "msg.read msg.write",
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.requested_scopes = requested_scopes

        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._expires_at: float = 0.0

    def _is_token_valid(self) -> bool:
        """Check if current access token is still valid (with 15s buffer)."""
        return bool(self._access_token) and time.time() + 15 < self._expires_at

    async def _mint_token(self, client: httpx.AsyncClient) -> None:
        """Exchange API key for JWT access token."""
        url = f"{self.base_url}/v1/auth/token"
        try:
            response = await client.post(
                url,
                headers={"x-api-key": self.api_key},
                json={"requested_scopes": self.requested_scopes},
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise AuthenticationError(
                f"Failed to authenticate: {e.response.status_code}"
            ) from e

        data = response.json()
        self._access_token = data["access_token"]
        self._refresh_token = data.get("refresh_token")
        expires_in = data.get("expires_in", 600)
        self._expires_at = time.time() + expires_in - 30

    async def ensure_token(self, client: httpx.AsyncClient) -> str:
        """Ensure we have a valid access token, minting if necessary."""
        if not self._is_token_valid():
            await self._mint_token(client)
        return self._access_token or ""

    async def get_auth_headers(self, client: httpx.AsyncClient) -> dict[str, str]:
        """Get authorization headers with valid token."""
        token = await self.ensure_token(client)
        return {"Authorization": f"Bearer {token}"}

