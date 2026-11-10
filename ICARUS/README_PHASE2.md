# ICARUS — Phase 2 Living World

An autonomous science-fiction anthology simulation. This increment adds individual source-backed knowledge and delayed communications, local seeded organism behavior, state-driven schematic activity/mobility cues, reduced motion, and offline verified lunar markers with explicit personal observances. SOL still operates autonomously; captain intervention remains optional. Final-release polish and the boundaries in PHASE2_LIMITATIONS.md remain open.

## Updating a working Phase 1 Lite installation

1. In the existing game, export a **complete backup** and keep a copy of the working Phase 1 folder.
2. Stop the old server. Extract the entire Phase 2 Lite ZIP to a separate folder. Keep all `web` files together with `server.py` and `Start_Remote_Deck.bat`.
3. If you customized host configuration or paired devices, copy your existing `config.json`, `paired_devices.json` and `samsung_tv.json` into the new folder when present. Generated pairing/TV files are not supplied in this ZIP.
4. Run the unchanged `Start_Remote_Deck.bat`. Use the **same PC browser profile, hostname and port (8765)** as before. The folder change does not change a browser origin, but switching between localhost, an IP and another browser profile does. Do not select New Voyage to recover an existing voyage.
5. Your core save namespace is unchanged. Existing saves migrate additively; if the voyage is not visible, use the complete-backup import in the original browser/origin. Reconnect Android through the host's displayed LAN URL, using existing pairing or normal PIN pairing. Android remains a thin client of the PC simulation.

Python/runtime requirements and the launcher are unchanged from Phase 1 Lite. No new Python installation is needed for an already working installation. A new PC needs Python and the packages in `requirements.txt` (`py -m pip install -r requirements.txt`). The astronomy library is included and works offline. Do not downgrade a Phase 2 save into an older runtime; retain the original Phase 1 backup for rollback.

## Using the increment

- Operations → In-game archives: choose a knowledge perspective. Acquisition method, confidence, disclosure and tick are shown. Private actor views do not represent shared SOL knowledge. **Read available ship records** requires that actor at a real working terminal; **Send shareable report** queues an actual radio report and waits for its channel.
- Field discoveries can remain personal while radio is lost. Restoring a relay/receiver or returning with records can deliver them; dead senders do not transmit. Research still requires actual specimen custody and received evidence.
- Settings includes reduced motion, explicit individual observances and body profiles. Personal entries accept annual `MM-DD` or one-time `YYYY-MM-DD`, optional inclusive `until` and `enabled:false`. No beliefs or dates are inferred.
- Normal pacing stays 4× elapsed real time; the nine approved synchronized holidays run 1×. Episodes remain real local Monday–Sunday. Six offline real hours is the existing catch-up limit. Private canon is creator reference, not acquired scientific evidence.
- Creatures act only when actual state permits. Quiet voyages remain valid; no attack, release, discovery or Lazarus breakthrough is guaranteed. Chronicles use actual delivered sources and label reconstructions.

Development, architecture, test evidence and known limits are in the `codex/living-world-phase2` branch of https://github.com/thekiddam-code/munza69 under ICARUS. Lite excludes tests, reports, development utilities and packaging scripts, while retaining every runtime dependency and upstream license. See SECURITY_PHASE2.md and LUNAR_MODEL.md supplied here.
