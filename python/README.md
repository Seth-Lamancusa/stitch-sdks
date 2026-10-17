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

# A bot passes its own key. The token subject is that bot.

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

## API keys

A bot caller constructs the client with that bot's key, not a manager key.

```python
created = client.keys.create(label="jobs", scopes_cap="msg.read msg.write")
# created["api_key"] is shown once

client.keys.list()
client.keys.revoke(created["cred_id"])
```

A managed user can omit `scopes_cap` to inherit the manager's scopes, limited to that account. An explicit cap is clipped to the account.

## Development Status

This SDK is under active development. Currently implemented:

- [x] Files upload (`/v1/files/upload`)
- [x] Messages create (`/v1/messages`)
- [x] API keys create, list, revoke (`/v1/auth/keys`)

Coming soon:
- [ ] Messages get, traverse, search, delete
- [ ] Users (me, search, profile updates)
- [ ] Recipients
- [ ] Managed users
- [ ] Links
