import { httpJsonFetch } from './http.js';

/**
 * Build a single MessageInput for quote import.
 *
 * Note: Stitch will automatically set importer_uid/importer_user_tag.
 */
export function buildQuoteMessageInput({
  content,
  public: isPublic,
  subject,
  parent_id,
  importInfo,
  extra = {},
}) {
  if (!content) throw new Error('content is required');

  const input = {
    content,
    ...(typeof isPublic === 'boolean' ? { public: isPublic } : {}),
    ...(subject ? { subject } : {}),
    ...(parent_id ? { parent_id } : {}),
    // Recipients intentionally omitted to match your requirement (empty recipients supported).
    ...(importInfo ? { import_info: importInfo } : {}),
    ...extra,
  };

  return input;
}

export function buildMessageInput({
  content,
  public: isPublic,
  subject,
  parent_id,
  extra = {},
}) {
  if (!content) throw new Error('content is required');

  return {
    content,
    ...(typeof isPublic === 'boolean' ? { public: isPublic } : {}),
    ...(subject ? { subject } : {}),
    ...(parent_id ? { parent_id } : {}),
    ...extra,
  };
}

/**
 * Import quote/ported message(s) into Stitch.
 *
 * Stitch endpoint:
 *   POST /v1/messages/import/quote
 *
 * Auth:
 *   Authorization: Bearer <delegated_access_token>
 */
export async function importQuoteMessages({
  apiBaseUrl,
  delegatedAccessToken,
  messages,
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!delegatedAccessToken) throw new Error('delegatedAccessToken is required');
  if (!Array.isArray(messages) || messages.length === 0) {
    throw new Error('messages must be a non-empty array');
  }

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/messages/import/quote`;
  const body = { messages };

  return httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${delegatedAccessToken}`,
    },
    body,
    signal,
  });
}

/**
 * Create message(s) (real authored, not quoted) in Stitch.
 *
 * Stitch endpoint:
 *   POST /v1/messages
 */
export async function createMessages({
  apiBaseUrl,
  delegatedAccessToken,
  messages,
  signal,
}) {
  if (!apiBaseUrl) throw new Error('apiBaseUrl is required');
  if (!delegatedAccessToken) throw new Error('delegatedAccessToken is required');
  if (!Array.isArray(messages) || messages.length === 0) {
    throw new Error('messages must be a non-empty array');
  }

  const url = `${apiBaseUrl.replace(/\/+$/, '')}/v1/messages`;
  const body = { messages };

  return httpJsonFetch({
    url,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${delegatedAccessToken}`,
    },
    body,
    signal,
  });
}
