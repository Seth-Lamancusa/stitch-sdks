# Stitch Python SDK - Internal Docs

Quick reference for SDK development.

## Adding Methods

```python
# In resources/messages.py

class Messages:
    def new_method(self, param: str) -> Dict[str, Any]:
        return self._client._request("POST", "/v1/endpoint", json={"param": param})

class AsyncMessages:
    async def new_method(self, param: str) -> Dict[str, Any]:
        return await self._client._request("POST", "/v1/endpoint", json={"param": param})
```

## Common Patterns

**Normalize inputs:**
```python
normalized = []
for item in items:
    if isinstance(item, str):
        normalized.append({"uid": item, "public": public})
    elif isinstance(item, dict):
        normalized.append(item)
```

**Handle optional params:**
```python
payload = {"required": value}
if optional is not None:
    payload["optional"] = optional
```

**Parse responses:**
```python
results = self._client._request(...)
if isinstance(results, list) and len(results) > 0:
    return results[0]
return results
```

