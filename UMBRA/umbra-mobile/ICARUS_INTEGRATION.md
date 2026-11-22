> Phase 3: PC pairing/remote access stays in ICARUS; Engineering, Soundboard and Instant Buttons move to DECK, gaming to SIMULATOR. Native TV controls are retired. See [current architecture and limits](PHASE3_REPORT.md). Earlier endpoint descriptions below are historical compatibility notes.

# Phase 2.1 ICARUS integration

The existing repository was inspected read-only at baseline `71af46a8c6c3888b4f3514ac74c1fc999bf6fe18`. Relevant sources are sibling `ICARUS/server.py`, `ICARUS/config.json`, and the Remote Deck web client. No server, simulation, Windows, TV, or repository ICARUS files are modified by this delivery.

## Current Rocket League source

The checked-in **config**, rather than `server.py`’s older bootstrap defaults, currently defines:

| Quick chat | Configured PC key sequence |
| --- | --- |
| Nice shot! | 2 → 1 |
| Great pass! | 2 → 2 |
| Thanks! | 2 → 3 |
| What a save! | 2 → 4 |

These are inspection findings, **not hardcoded mobile mappings**. The bootstrap defaults differ and must not be copied into UMBRA. On each Sync controls, native authenticated `GET /api/status` returns the current configured `quick` names, `macros`, `custom_messages`, and Fortnite slot labels. The API does not expose quick-chat key arrays. Mobile sends `POST /api/action` with `{"action":"quick","name":"…"}`; the server reads its current config and resolves the sequence on that request. A removed name is an explicit server error. Changed key sequences require no mobile rebuild.

The current config also includes ten saved text buttons. UMBRA parses their labels/text/team-or-match channels from the server snapshot; it does not embed those personal strings. Saved-message action IDs include a content hash, so a changed text/channel cannot silently retain an old favorite identity. Refresh updates them, and missing favorites are marked absent. Text actions use the supported `speed: balanced`; chat openers and actual keyboard mappings remain server-owned (`text_chat_open`, `team_text_chat_open` with the server’s existing defaults). No `/api/custom_messages` writes occur from UMBRA.

## Existing API use

| Purpose | Existing authenticated contract |
| --- | --- |
| Pair phone | `POST /api/pair`, PIN exchange; token encrypted locally |
| Catalog / sync time | `GET /api/status`; visible-entry cache 30 seconds, explicit manual Sync bypasses cache |
| Quick chat | `POST /api/action`, `action: quick`, current name |
| Saved message | Same endpoint, `action: text`, snapshot text/channel, `speed: balanced` |
| Macro | Same endpoint, `action: macro`, current name |
| Fortnite | Same endpoint, `action: fortnite_emote`, current slot index |
| Release held input | Same endpoint, `action: stop` |

Existing Engineering simulation commands and Lounge TV controls remain in their native Phase 2 modules. No arbitrary shell command or unprotected remote endpoint is introduced. Browser Remote Deck access still uses its own session and opens immediately through Android.

## Local control behavior

Home’s ICARUS page, built-in ICARUS widgets, and native Simulator share an action controller. Favorites, local labels, and order persist in DataStore and never overwrite PC mappings. Buttons display real response messages; network/authentication errors remain explicit. A mutex drops concurrent taps instead of queuing commands; in-flight work is cancelled when its initiating view stops. Requests have existing user timeouts, bounded bodies, no redirect following, and server-bound credentials. Pairing remains in Android Keystore-encrypted no-backup storage and is excluded from export.

An acknowledgment describes what the server reported; UMBRA cannot verify the focused game processed input. A network cancellation cannot undo input already delivered to the PC. Saved text is a timestamped snapshot and updates on Sync; quick-chat/macro keys are resolved by the server on execution. There is no automatic repeat/retry. Quick-chat names/mappings unavailable from an unpaired/offline server are not replaced with sample controls.

## Verification boundary

MockWebServer tests check status synchronization, current-name requests, bearer authentication, no copied key arrays, command feedback, server-base mismatch rejection, in-flight duplicate suppression, cancellation/released gate, saved-message identity, and existing redirect/size/authorization behavior. Live private Tailscale access and PC/game focus were not available in this environment. Real ICARUS execution and phone Keystore behavior must be verified on the user’s S24+; no live execution is claimed.
