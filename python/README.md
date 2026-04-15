# stitchai

Python SDK for the Stitch API.

## Installation

```bash
pip install -e .
```

## Usage

```python
from stitchai import StitchClient

client = StitchClient(api_key="sk_...")

# Upload a file
with open("document.pdf", "rb") as f:
    file_meta = client.files.upload(f)
    print(file_meta.url)

# Create a message
result = client.messages.create(
    recipients=["user123", "user456"],
    content="Hello, world!",
    public=True
)
if result["success"]:
    print(f"Created message: {result['message']['id']}")
```

## Messages

### Create Message

```python
# Basic message
result = client.messages.create(
    recipients=["user123", "user456"],
    content="Hello, world!"
)

# Reply
result = client.messages.create(
    recipients=["user123"],
    content="Reply",
    parent_id="msg_abc123"
)

# With tags/files
result = client.messages.create(
    recipients=["user123"],
    content="Message",
    tags=["important"],
    files=[file_meta]
)
```

**Parameters:** `recipients` (list), `content` (required), `parent_id`, `public` (default: True), `files`, `tags`  
**Returns:** Dict with `success`, `message`, `error` keys

## Development Status

This SDK is under active development. Currently implemented:

- [x] Files upload (`/v1/files/upload`)
- [x] Messages create (`/v1/messages`)

Coming soon:
- [ ] Messages get, traverse, search, delete
- [ ] Users (me, search, profile updates)
- [ ] Recipients
- [ ] Managed users
- [ ] Links
