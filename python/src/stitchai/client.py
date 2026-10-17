"""Stitch API client."""

from typing import Any, Optional

import httpx

from .auth import AuthManager, AsyncAuthManager
from .exceptions import APIError
from .resources import (
    Files,
    AsyncFiles,
    Messages,
    AsyncMessages,
    Users,
    AsyncUsers,
    Recipients,
    AsyncRecipients,
    Managed,
    AsyncManaged,
    Keys,
    AsyncKeys,
)

DEFAULT_BASE_URL = "https://api.stitch.lol"


class StitchClient:
    """
    Synchronous client for the Stitch API.

    Usage:
        client = StitchClient(api_key="sk_...")

        # Upload a file
        with open("doc.pdf", "rb") as f:
            file_meta = client.files.upload(f)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        requested_scopes: str = "msg.read msg.write",
    ):
        """
        Initialize the Stitch client.

        Args:
            api_key: Your Stitch API key (sk_...)
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
            requested_scopes: Space-separated scopes to request
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._auth = AuthManager(
            api_key=api_key,
            base_url=self.base_url,
            timeout=timeout,
            requested_scopes=requested_scopes,
        )
        self._client = httpx.Client(timeout=timeout)

        # Resources
        self.files = Files(self)
        self.messages = Messages(self)
        self.users = Users(self)
        self.recipients = Recipients(self)
        self.managed = Managed(self)
        self.keys = Keys(self)

    def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            path: API path (e.g., "/v1/messages")
            json: JSON body
            params: Query parameters
            files: Multipart form files

        Returns:
            Parsed JSON response

        Raises:
            APIError: On non-2xx response
        """
        url = f"{self.base_url}{path}"
        headers = self._auth.get_auth_headers(self._client)

        response = self._client.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            files=files,
        )

        if response.status_code == 401:
            # Token may have expired, try re-auth
            self._auth._access_token = None
            headers = self._auth.get_auth_headers(self._client)
            response = self._client.request(
                method,
                url,
                headers=headers,
                json=json,
                params=params,
                files=files,
            )

        if not response.is_success:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"detail": response.text}

            raise APIError(
                f"API request failed: {response.status_code}",
                status_code=response.status_code,
                response=error_body,
            )

        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "StitchClient":
        return self

    def __exit__(self, *args) -> None:
        self.close()


class AsyncStitchClient:
    """
    Asynchronous client for the Stitch API.

    Usage:
        async with AsyncStitchClient(api_key="sk_...") as client:
            with open("doc.pdf", "rb") as f:
                file_meta = await client.files.upload(f)
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        requested_scopes: str = "msg.read msg.write",
    ):
        """
        Initialize the async Stitch client.

        Args:
            api_key: Your Stitch API key (sk_...)
            base_url: API base URL (defaults to production)
            timeout: Request timeout in seconds
            requested_scopes: Space-separated scopes to request
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self._auth = AsyncAuthManager(
            api_key=api_key,
            base_url=self.base_url,
            timeout=timeout,
            requested_scopes=requested_scopes,
        )
        self._client = httpx.AsyncClient(timeout=timeout)

        # Resources
        self.files = AsyncFiles(self)
        self.messages = AsyncMessages(self)
        self.users = AsyncUsers(self)
        self.recipients = AsyncRecipients(self)
        self.managed = AsyncManaged(self)
        self.keys = AsyncKeys(self)

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Make an authenticated request to the API.

        Args:
            method: HTTP method
            path: API path (e.g., "/v1/messages")
            json: JSON body
            params: Query parameters
            files: Multipart form files

        Returns:
            Parsed JSON response

        Raises:
            APIError: On non-2xx response
        """
        url = f"{self.base_url}{path}"
        headers = await self._auth.get_auth_headers(self._client)

        response = await self._client.request(
            method,
            url,
            headers=headers,
            json=json,
            params=params,
            files=files,
        )

        if response.status_code == 401:
            # Token may have expired, try re-auth
            self._auth._access_token = None
            headers = await self._auth.get_auth_headers(self._client)
            response = await self._client.request(
                method,
                url,
                headers=headers,
                json=json,
                params=params,
                files=files,
            )

        if not response.is_success:
            try:
                error_body = response.json()
            except Exception:
                error_body = {"detail": response.text}

            raise APIError(
                f"API request failed: {response.status_code}",
                status_code=response.status_code,
                response=error_body,
            )

        return response.json()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncStitchClient":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

