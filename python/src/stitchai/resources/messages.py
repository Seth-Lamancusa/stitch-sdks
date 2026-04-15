"""Messages resource."""

from typing import TYPE_CHECKING, List, Optional, Dict, Any, Union

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


class Messages:
    """Sync messages resource."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def create(
        self,
        recipients: List[Union[str, Dict[str, Any]]],
        *,
        content: str,
        parent_id: Optional[str] = None,
        public: bool = True,
        files: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a message.

        Args:
            recipients: List of recipient user UIDs/user_tags (str) or dicts with 'uid' and optional 'public' (required)
            content: Message content (required, min length 1)
            parent_id: Optional parent message ID for replies
            public: Whether the message is public (default: True). Used for string recipients.
            files: Optional list of file metadata dicts from files.upload()
            tags: Optional list of tag strings

        Returns:
            Dict containing the created message result with 'success', 'message', and 'error' keys.
            If successful, 'message' contains the MessageResponse dict.

        Example:
            >>> result = client.messages.create(
            ...     recipients=["user123", "user456"],
            ...     content="Hello, world!",
            ...     public=True
            ... )
            >>> if result["success"]:
            ...     print(f"Created message: {result['message']['id']}")
        """
        # Normalize recipients to the format expected by the API
        # The API accepts either strings or dicts with 'uid' and 'public' keys
        normalized_recipients = []
        for recipient in recipients:
            if isinstance(recipient, dict):
                # Already in dict format - ensure it has 'uid'
                if "uid" not in recipient:
                    raise ValueError(f"Recipient dict must have 'uid' key: {recipient}")
                # Use recipient's own 'public' if provided, otherwise use message's public
                normalized_recipients.append({
                    "uid": recipient["uid"],
                    "public": recipient.get("public", public)
                })
            elif isinstance(recipient, str):
                # String format - convert to dict using message's public value
                normalized_recipients.append({"uid": recipient, "public": public})
            else:
                raise ValueError(f"Invalid recipient format: {recipient}. Expected str or dict.")

        # Build request payload
        payload = {
            "content": content,
            "public": public,
            "recipients": normalized_recipients,
        }

        if parent_id is not None:
            payload["parent_id"] = parent_id

        if files is not None:
            payload["files"] = files

        if tags is not None:
            payload["tags"] = tags

        # The API returns a list of MessageCreateResult objects
        # For single message creation, we'll get a list with one result
        results = self._client._request("POST", "/v1/messages", json=payload)

        # Return the first result (for single message creation)
        if isinstance(results, list) and len(results) > 0:
            result = results[0]
            # Convert Pydantic model to dict if needed
            if hasattr(result, "dict"):
                return result.dict()
            return result
        elif isinstance(results, dict):
            return results
        else:
            # Fallback: wrap in expected format
            return {"success": True, "message": results, "error": None}

    def get(self, message_id: str, *args, **kwargs):
        """Get a message by ID. Not yet implemented."""
        raise NotImplementedError("Messages.get() is not yet implemented")

    def delete(self, message_id: str, *args, **kwargs):
        """Delete a message. Not yet implemented."""
        raise NotImplementedError("Messages.delete() is not yet implemented")

    def traverse(self, message_id: str, *args, **kwargs):
        """Traverse a message thread. Not yet implemented."""
        raise NotImplementedError("Messages.traverse() is not yet implemented")

    def search(self, *args, **kwargs):
        """Search messages. Not yet implemented."""
        raise NotImplementedError("Messages.search() is not yet implemented")

    def list_inbox(self, *args, **kwargs):
        """List inbox messages. Not yet implemented."""
        raise NotImplementedError("Messages.list_inbox() is not yet implemented")

    def list_public(self, *args, **kwargs):
        """List public messages. Not yet implemented."""
        raise NotImplementedError("Messages.list_public() is not yet implemented")


class AsyncMessages:
    """Async messages resource."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def create(
        self,
        recipients: List[Union[str, Dict[str, Any]]],
        *,
        content: str,
        parent_id: Optional[str] = None,
        public: bool = True,
        files: Optional[List[Dict[str, Any]]] = None,
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a message (async).

        Args:
            recipients: List of recipient user UIDs/user_tags (str) or dicts with 'uid' and optional 'public' (required)
            content: Message content (required, min length 1)
            parent_id: Optional parent message ID for replies
            public: Whether the message is public (default: True). Used for string recipients.
            files: Optional list of file metadata dicts from files.upload()
            tags: Optional list of tag strings

        Returns:
            Dict containing the created message result with 'success', 'message', and 'error' keys.
            If successful, 'message' contains the MessageResponse dict.

        Example:
            >>> result = await client.messages.create(
            ...     recipients=["user123", "user456"],
            ...     content="Hello, world!",
            ...     public=True
            ... )
            >>> if result["success"]:
            ...     print(f"Created message: {result['message']['id']}")
        """
        # Normalize recipients to the format expected by the API
        # The API accepts either strings or dicts with 'uid' and 'public' keys
        normalized_recipients = []
        for recipient in recipients:
            if isinstance(recipient, dict):
                # Already in dict format - ensure it has 'uid'
                if "uid" not in recipient:
                    raise ValueError(f"Recipient dict must have 'uid' key: {recipient}")
                # Use recipient's own 'public' if provided, otherwise use message's public
                normalized_recipients.append({
                    "uid": recipient["uid"],
                    "public": recipient.get("public", public)
                })
            elif isinstance(recipient, str):
                # String format - convert to dict using message's public value
                normalized_recipients.append({"uid": recipient, "public": public})
            else:
                raise ValueError(f"Invalid recipient format: {recipient}. Expected str or dict.")

        # Build request payload
        payload = {
            "content": content,
            "public": public,
            "recipients": normalized_recipients,
        }

        if parent_id is not None:
            payload["parent_id"] = parent_id

        if files is not None:
            payload["files"] = files

        if tags is not None:
            payload["tags"] = tags

        # The API returns a list of MessageCreateResult objects
        # For single message creation, we'll get a list with one result
        results = await self._client._request("POST", "/v1/messages", json=payload)

        # Return the first result (for single message creation)
        if isinstance(results, list) and len(results) > 0:
            result = results[0]
            # Convert Pydantic model to dict if needed
            if hasattr(result, "dict"):
                return result.dict()
            return result
        elif isinstance(results, dict):
            return results
        else:
            # Fallback: wrap in expected format
            return {"success": True, "message": results, "error": None}

    async def get(self, message_id: str, *args, **kwargs):
        """Get a message by ID. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.get() is not yet implemented")

    async def delete(self, message_id: str, *args, **kwargs):
        """Delete a message. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.delete() is not yet implemented")

    async def traverse(self, message_id: str, *args, **kwargs):
        """Traverse a message thread. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.traverse() is not yet implemented")

    async def search(self, *args, **kwargs):
        """Search messages. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.search() is not yet implemented")

    async def list_inbox(self, *args, **kwargs):
        """List inbox messages. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.list_inbox() is not yet implemented")

    async def list_public(self, *args, **kwargs):
        """List public messages. Not yet implemented."""
        raise NotImplementedError("AsyncMessages.list_public() is not yet implemented")

