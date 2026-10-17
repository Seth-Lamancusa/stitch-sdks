# Stitch JS SDK (minimal)

API key exchange, one-time delegation for minting a bot key, and quote/message import.

## Usage

```js
import {
  mintAccessToken,
  importQuoteMessages,
  buildQuoteMessageInput,
  createMessages,
  buildMessageInput
} from 'stitch-js-sdk';

const apiBaseUrl = process.env.STITCH_API_URL;
const apiKey = process.env.STITCH_API_KEY;

// Exchange the bot's own key. The token subject is the bot.
const { access_token: accessToken } = await mintAccessToken({
  apiBaseUrl,
  apiKey,
  requestedScopes: 'msg.read msg.write',
  aud: 'public-v1',
});

const displayName = 'alice';
const msg = buildQuoteMessageInput({
  content: 'Hello world',
  public: true,
  importInfo: {
    display_name: displayName,
    original_timestamp: new Date().toISOString(),
    source_platform: 'slack',
    source_url: 'https://example.com/message/123',
  },
});

await importQuoteMessages({
  apiBaseUrl,
  accessToken,
  messages: [msg],
});

const realMsg = buildMessageInput({ content: 'Hello real', public: true });
await createMessages({ apiBaseUrl, accessToken, messages: [realMsg] });
```

`delegatedAccessToken` is still accepted on the message helpers.

## First key

A bot with no key yet still uses one delegated session, then `createOwnApiKey`. `mintManagerToken` and `delegateToManaged` stay for that mint.
