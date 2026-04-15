"""File models."""

from pydantic import BaseModel, Field


class FileMetadata(BaseModel):
    """Metadata for an uploaded file."""

    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type")
    size: int = Field(..., description="File size in bytes")
    url: str = Field(..., description="Signed URL for access")
    gcs_path: str = Field(..., description="Cloud storage path")

    class Config:
        extra = "allow"

