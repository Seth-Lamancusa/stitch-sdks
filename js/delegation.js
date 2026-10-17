import { httpJsonFetch } from './http.js';

/**
 * Mint a manager access token using the manager's API key.
 *
 * Stitch endpoint:
 *   POST /v1/auth/token
 *   Header: x-api-key: <manager_api_key>
 *
 * Returns:
 *   { access_token, expires_in, token_type }
 */
export async function mintManagerToken({
  apiBaseUrl,
  managerApiKey,
  requestedScopes = 'msg.write',
  aud = 'public-v1',
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!managerApiKey) throw new Error('managerApiKey is required');

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/auth/token`;
  return httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      'x-api-key': managerApiKey,
    },
    body: {
      requested_scopes: requestedScopes,
      aud,
    },
    signal,
  });
}

/**
 * Exchange an API key for an access token.
 *
 * The key's principal is the token subject. There is no act claim.
 *
 * Stitch endpoint:
 *   POST /v1/auth/token
 *   Header: x-api-key: <apiKey>
 */
export async function mintAccessToken({
  apiBaseUrl,
  apiKey,
  requestedScopes = 'msg.read msg.write',
  aud = 'public-v1',
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!apiKey) throw new Error('apiKey is required');

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/auth/token`;
  return httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      'x-api-key': apiKey,
    },
    body: {
      requested_scopes: requestedScopes,
      aud,
    },
    signal,
  });
}

/**
 * Mint an API key for the authenticated principal.
 *
 * Used once while delegated into a bot. Omit scopesCap to inherit the manager's scopes.
 * Omit expiresAt for 90 days. A YYYY-MM-DD date expires at the end of that UTC day (max 730 days).
 *
 * Stitch endpoint:
 *   POST /v1/auth/keys/self
 */
export async function createOwnApiKey({
  apiBaseUrl,
  accessToken,
  label = '',
  scopesCap,
  assurance,
  pop,
  env,
  expiresAt,
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!accessToken) throw new Error('accessToken is required');

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/auth/keys/self`;
  const body = { label };
  if (scopesCap) body.scopes_cap = scopesCap;
  if (assurance) body.assurance = assurance;
  if (pop) body.pop = pop;
  if (env) body.env = env;
  if (expiresAt) body.expires_at = expiresAt;

  return httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body,
    signal,
  });
}

/**
 * Delegate to a managed user (bot) using the manager access token.
 *
 * Stitch endpoint:
 *   POST /v1/managed/auth/delegate
 *   Authorization: Bearer <manager_access_token>
 */
export async function delegateToManaged({
  apiBaseUrl,
  managerAccessToken,
  managedUid,
  requestedScopes = 'msg.read msg.write',
  aud = 'public-v1',
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!managerAccessToken) throw new Error('managerAccessToken is required');
  if (!managedUid) throw new Error('managedUid is required');

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/managed/auth/delegate`;
  const data = await httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${managerAccessToken}`,
    },
    body: {
      managed_uid: managedUid,
      requested_scopes: requestedScopes,
      aud,
    },
    signal,
  });

  return data;
}
