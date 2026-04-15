# Stitch JS SDK (minimal)

Programmatic delegation + quote/message import.

## Usage

```js
import {
  mintManagerToken,
  delegateToManaged,
  importQuoteMessages,
  buildQuoteMessageInput,
  createMessages,
  buildMessageInput
} from 'stitch-js-sdk';

const apiBaseUrl = process.env.STITCH_API_URL;
const managerApiKey = process.env.MANAGER_STITCH_API_KEY;

// 1) Mint manager token
const { access_token: managerAccessToken } = await mintManagerToken({
  apiBaseUrl,
  managerApiKey,
  requestedScopes: 'msg.write',
  aud: 'public-v1',
});

// 2) Delegate to managed bot/user (Annabelle)
// managedUid is Stitch's UID for the bot user (not user_tag).
const managedUid = process.env.ANNABELLE_UID;
const { access_token: delegatedAccessToken } = await delegateToManaged({
  apiBaseUrl,
  managerAccessToken,
  managedUid,
  requestedScopes: 'msg.read msg.write',
  aud: 'public-v1',
});

// 3) Import a quote message
const displayName = 'alice';
const msg = buildQuoteMessageInput({
  content: 'Hello world',
  public: true,
  importInfo: {
    display_name: displayName,
    original_timestamp: new Date().toISOString(),
    source_url: 'https://elevatecfo.ai/...',
  },
});

await importQuoteMessages({
  apiBaseUrl,
  delegatedAccessToken,
  messages: [msg],
});

// Real authored message (not quoted)
const realMsg = buildMessageInput({ content: 'Hello real', public: true });
await createMessages({ apiBaseUrl, delegatedAccessToken, messages: [realMsg] });
```
