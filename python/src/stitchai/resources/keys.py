"""API key resource."""

from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


def _create_payload(
    label: str,
    scopes_cap: Optional[str],
    assurance: Optional[str],
    pop: Optional[str],
    env: Optional[str],
    expires_at: Optional[str],
) -> dict[str, Any]:
    payload: dict[str, Any] = {"label": label}
    if scopes_cap is not None:
        payload["scopes_cap"] = scopes_cap
    if assurance is not None:
        payload["assurance"] = assurance
    if pop is not None:
        payload["pop"] = pop
    if env is not None:
        payload["env"] = env
    if expires_at is not None:
        payload["expires_at"] = expires_at
    return payload


class Keys:
    """Create, list, and revoke API keys for the authenticated principal."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def create(
        self,
        *,
        label: str = "",
        scopes_cap: Optional[str] = None,
        assurance: Optional[str] = None,
        pop: Optional[str] = None,
        env: Optional[str] = None,
        expires_at: Optional[str] = None,
    ) -> dict[str, Any]:
        """Mint a key. The secret is returned once. Omit expires_at for 90 days (maximum 730). A managed user may omit scopes_cap to inherit the manager's scopes."""
        return self._client._request(
            "POST",
            "/v1/auth/keys/self",
            json=_create_payload(label, scopes_cap, assurance, pop, env, expires_at),
        )

    def list(self) -> list[dict[str, Any]]:
        data = self._client._request("GET", "/v1/auth/keys")
        keys = data.get("keys", []) if isinstance(data, dict) else []
        return list(keys)

    def revoke(self, cred_id: str) -> dict[str, Any]:
        return self._client._request("DELETE", f"/v1/auth/keys/{cred_id}")


class AsyncKeys:
    """Async create, list, and revoke for the authenticated principal."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def create(
        self,
        *,
        label: str = "",
        scopes_cap: Optional[str] = None,
        assurance: Optional[str] = None,
        pop: Optional[str] = None,
        env: Optional[str] = None,
        expires_at: Optional[str] = None,
    ) -> dict[str, Any]:
        """Mint a key. The secret is returned once. Omit expires_at for 90 days (maximum 730). A managed user may omit scopes_cap to inherit the manager's scopes."""
        return await self._client._request(
            "POST",
            "/v1/auth/keys/self",
            json=_create_payload(label, scopes_cap, assurance, pop, env, expires_at),
        )

    async def list(self) -> list[dict[str, Any]]:
        data = await self._client._request("GET", "/v1/auth/keys")
        keys = data.get("keys", []) if isinstance(data, dict) else []
        return list(keys)

    async def revoke(self, cred_id: str) -> dict[str, Any]:
        return await self._client._request("DELETE", f"/v1/auth/keys/{cred_id}")
