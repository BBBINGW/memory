# BOOT GitHub Notes OAuth connectivity audit and self-healing

Date: 2026-10-31
Track: BOOT
Code commit: df37c0b

## Verified incident

ChatGPT plugin settings showed GitHub Notes in DEVELOPMENT mode at `https://folic-unseemly-sanitary.ngrok-free.dev/mcp` with “authentication update required”. A connector-native `list_repo_files("")` call returned reauthentication-required before repair.

The MCP protected-resource metadata advertises Auth0 issuer `https://dev-xlcmo1d4ew08nl6k.us.auth0.com/` and only `notes:read notes:write` resource scopes. Auth0 discovery advertises authorization-code, refresh-token grants, PKCE S256, revocation, and `offline_access`. The server/provider can support refresh, but the currently observable MCP resource metadata does not advertise/request `offline_access`; no evidence proves that ChatGPT received a refresh token. Access-token TTL and refresh rotation settings are not publicly exposed by discovery.

After an explicit safe-boundary reconnect, ChatGPT settings reported “Primary connected” and the native sentinel successfully listed `AGENT.md`, `STATE.md`, and `findings/`.

## Orchestrator repair

- Added a configurable 30-minute `GITHUB_NOTES_CONNECTIVITY_WATCHDOG`.
- Added states HEALTHY, TOKEN_REFRESHING, REAUTH_REQUIRED, TOOL_REGISTRATION_PENDING, and UNAVAILABLE_WITH_LOCAL_FALLBACK.
- Reauthentication is conditional, idempotent per conversation, and deferred while Research GPT or a connector tool call is active.
- No blind scheduled reconnect was added.
- Local Git remains the research authority while the connector is unavailable; no Research Turn is consumed or fabricated.
- Dashboard now shows OAuth refresh-token status, last probe/refresh, and next probe.
- Added nine OAuth/connectivity continuity regressions; full suite passed 103/103 plus TypeScript build.

## Remaining provider-side requirement

To prove persistent refresh end-to-end, the provider owner must ensure the authorization request includes `offline_access`, Auth0 issues a refresh token to the ChatGPT client, rotation is enabled, and a short-TTL canary demonstrates access expiry followed by refresh without user action. Until that evidence exists, Dashboard must report refresh-token capability as UNKNOWN rather than claim success.
