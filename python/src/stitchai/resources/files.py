"""Files resource - upload files for use in messages."""

from typing import Any, BinaryIO, Optional, TYPE_CHECKING

from ..models import FileMetadata

if TYPE_CHECKING:
    from ..client import StitchClient, AsyncStitchClient


class Files:
    """Sync files resource."""

    def __init__(self, client: "StitchClient"):
        self._client = client

    def upload(
        self,
        file: BinaryIO,
        *,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> FileMetadata:
        """
        Upload a file.

        Args:
            file: File-like object to upload (opened in binary mode)
            filename: Override filename (defaults to file.name if available)
            content_type: Override MIME type (auto-detected if not provided)

        Returns:
            FileMetadata with url, gcs_path, size, etc.

        Raises:
            APIError: If upload fails (e.g., invalid file type, too large)

        Supported file types:
            - PDF documents (application/pdf)
            - Images (jpg, png, gif, webp)
            - Text files (.txt)

        Max file size: 100MB
        """
        # Determine filename
        if filename is None:
            filename = getattr(file, "name", "upload")
            # Strip path if present
            if "/" in filename:
                filename = filename.rsplit("/", 1)[-1]

        # Build multipart form data
        files = {"file": (filename, file, content_type or "application/octet-stream")}

        response = self._client._request(
            "POST",
            "/v1/files/upload",
            files=files,
        )

        return FileMetadata(**response)


class AsyncFiles:
    """Async files resource."""

    def __init__(self, client: "AsyncStitchClient"):
        self._client = client

    async def upload(
        self,
        file: BinaryIO,
        *,
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> FileMetadata:
        """
        Upload a file.

        Args:
            file: File-like object to upload (opened in binary mode)
            filename: Override filename (defaults to file.name if available)
            content_type: Override MIME type (auto-detected if not provided)

        Returns:
            FileMetadata with url, gcs_path, size, etc.

        Raises:
            APIError: If upload fails (e.g., invalid file type, too large)

        Supported file types:
            - PDF documents (application/pdf)
            - Images (jpg, png, gif, webp)
            - Text files (.txt)

        Max file size: 100MB
        """
        # Determine filename
        if filename is None:
            filename = getattr(file, "name", "upload")
            # Strip path if present
            if "/" in filename:
                filename = filename.rsplit("/", 1)[-1]

        # Build multipart form data
        files = {"file": (filename, file, content_type or "application/octet-stream")}

        response = await self._client._request(
            "POST",
            "/v1/files/upload",
            files=files,
        )

        return FileMetadata(**response)

