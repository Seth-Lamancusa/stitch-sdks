export async function httpJsonFetch({ url, method = 'GET', headers = {}, body, signal }) {
  const res = await fetch(url, {
    method,
    headers: {
      ...headers,
      ...(body !== undefined && !headers['Content-Type'] ? { 'Content-Type': 'application/json' } : {}),
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal,
  });

  // Attempt to parse JSON error bodies; fall back to text.
  const contentType = res.headers.get('content-type') || '';
  let parsed;
  if (contentType.includes('application/json')) {
    parsed = await res.json().catch(() => undefined);
  } else {
    parsed = await res.text().catch(() => undefined);
  }

  if (!res.ok) {
    const detail =
      parsed && typeof parsed === 'object'
        ? parsed.detail || parsed.error || parsed.message
        : parsed;
    const msg = `HTTP ${res.status} ${res.statusText}${detail ? `: ${detail}` : ''}`;
    const err = new Error(msg);
    err.status = res.status;
    err.body = parsed;
    throw err;
  }

  return parsed;
}
