# Native Instant Buttons and supported ICARUS outputs

The inspected baseline is the existing repository's `ICARUS/server.py`, `ICARUS/config.json`, and Remote Deck `web/index.html` at commit `5c08c9e`. Phase 2.1 only embedded a read-only catalog and truncated compact widgets with `take(6)`; it had no dedicated native Instant Buttons route or full output editor. Phase 2.3 adds that native page and removes the truncation. It does not require a new server endpoint or modify the Windows server, simulation, TV integration, or web deck.

Open **DECK → Instant Buttons**. Long-press its title for Create, Select buttons, Save, Load, and Restore. Long-press a button for configure/resize/duplicate/remove or drag to arrange. Each widget can select an independent catalog subset. The complete selected set wraps across grid rows and scrolls within the configured size. The selection editor supports search, Select all, and Deselect all; there is no six-button cap.

Local buttons support create, edit, rename, delete, icon selection, typed output parameters, persistent save/load, explicit command testing, and placement in widgets. Configuring a discovered server reference saves an explicit UMBRA override and preserves its placement; PC mappings remain unchanged. Native pairing is required for execution, separately from browser login. Tailscale remains managed by its own app.

## Inspected contracts

All calls reuse the server-bound Keystore-encrypted token, bounded responses, configured timeouts, cancellation, and refusal to follow redirects. No arbitrary URL, shell/script, host key, or unprotected control endpoint is accepted from a button file.

| Editor output | Existing endpoint and body | Relevant parameters / behavior |
| --- | --- | --- |
| QuickChat | `POST /api/action`, `action: quick` | Exact current `name`; server resolves current key array at execution |
| Macro | Same endpoint, `action: macro` | Exact configured `name`; server's existing combination limits apply |
| Text | Same endpoint, `action: text` | `text` 1–120 non-control characters; `channel` match/team; `speed` fast/balanced/safe |
| FortniteEmote | Same endpoint, `action: fortnite_emote` | `index` 0–8; eight slots plus existing repeat slot; labels read from status |
| MineToggle | Same endpoint, `action: mine_toggle` | Toggle held mining input; existing server safety release after 60 seconds |
| ForwardMine | Same endpoint, `action: forward_mine` | `seconds` 0.2–10; existing forward + mining timed hold/release |
| Stop | Same endpoint, `action: stop` | Release inputs held by the existing server |
| TvKey (legacy) | Blocked | Retained only for migration/export; hidden from the native catalog and editor |
| Simulation | `POST /api/icarus/command` | `command`: pause, resume, speed1, speed5, speed20, save; asynchronous queue acknowledgment |

Phase 3 removes native TV controls. Existing shared server TV components are preserved for other integrations.

Generic arbitrary key-down/key-up/hold, arbitrary scripts, and invented output protocols are **unsupported** and are identified as such in the editor. Timed holds are exposed only where the server implements them. Text typing inherits the server's PyAutoGUI limitations; arbitrary Unicode input is not promised. A missing macro/quick-chat name or unavailable emote is reported rather than replaced with another command.

The current checked-in Rocket League quick-chat mappings remain Nice shot! → 2,1; Great pass! → 2,2; Thanks! → 2,3; What a save! → 2,4. These are inspection findings, not copied mobile key arrays. Sync reads the current names and saved message text/channels from authenticated `/api/status`; quick/macro keys remain server-resolved at execution. Saved-message references follow the latest synchronized snapshot, with a visible timestamp. UMBRA never writes `/api/custom_messages`, `/api/fortnite_emotes`, or PC configuration files during local editing.

## Execution and feedback

A tap executes; a long-press enters editing and consumes release so it does not also execute. Commands share the existing one-in-flight gate: repeated in-flight taps are dropped instead of queued or retried automatically. Feedback appears only after the response. Simulation says “Queued … PC execution pending,” not “executed.” HTTP acknowledgment does not verify game focus, downstream PC behavior. Cancellation cannot undo a command already received by the server.

File import and configuration changes never test or execute commands automatically. The Test command button is explicit. Unknown output enums, malformed types, illegal ranges, unsafe paths, and oversized files are rejected. Imports preserve current settings on validation failure. Credentials and private connection settings are excluded from button-only files; full configuration exports still exclude pairing secrets.

Automated coverage uses the real native UI and local MockWebServer contracts, including payloads, authentication, duplicate suppression, failures, and queued feedback. Live private Tailscale, PC/game focus, phone Keystore behavior require physical testing; they are not asserted from host tests.
