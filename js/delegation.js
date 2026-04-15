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
