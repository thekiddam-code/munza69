# Phase 4.7C Lite checkpoint verification

[Download ZIP](ICARUS_Phase4_7C_Surveillance_Checkpoint_Lite.zip) · [SHA-256](SHA256SUMS.txt)

Source commit `4a07ffb4491628dc1edd6c145b350c78263af5e5`; final runtime `c3670d0fdb623415202b7888b0cd2dcbce6ac9a8`. ZIP: 1,031,431 bytes, 246 source files plus BUILD_MANIFEST.json, 149 runtime hashes verified, CRC and all manifest hashes passed. Runtime dependencies retained. Tests, raw reports, development tools, packaging scripts, credentials and private voyage data excluded from Lite.

SHA-256: `6a985089dae7e29d2933cf0b0dddfb54306fae438239a0b3f1355cf678ea932c`.

**592 selected case executions passed**: 580 source/runtime checks plus 12 extracted-ZIP checks (8 boot, 3 dispatch/render/media, 1 paired original-record HTTP playback path). Inherited cases overlap; this is not 592 unique tests. See package JSONs here and [full validation](../../ICARUS/PHASE47C_VALIDATION.md), [reports](../../ICARUS/reports/phase47c) and [actual rover screenshot](../../ICARUS/reports/phase47c/screenshots/futuristic_rover.png). Original supplied backup hash remains unchanged.

## Scope and compatibility warning

This is a tested checkpoint, not a complete Phase 4.7 release. No separate Phase 4.7B source was found in available GitHub branches. **Do not overwrite an installation containing unpublished B changes.** Merge/retest against that source first. High-rate image sequences are foreground/event-based best-effort captures, not encoded audiovisual recordings. Original PNGs and source-state reconstructions retain explicit provenance. Remote originals above 512KiB remain available on the host.

Physical Windows, Android/Samsung tablet, TV, Tailscale routing, antivirus and native APK rebuild tests were unavailable. Existing web/native/TV paths are retained. Full historical campaigns and 30/90/365-day soaks were not repeated. Package/source tests ran in Linux Chromium, including isolated copies of the supplied voyage; they did not modify the live Windows world.

## Safe install and rollback

1. Export a full voyage backup; retain the previous installation folder and private pairing configuration.
2. Stop its server and close authoritative tabs. Extract separately. For the supported repository baseline, use the same browser profile, hostname and port; saves are origin-bound.
3. Run `Start_Remote_Deck.bat`. Wait for actual readiness and explicitly select ENTER ICARUS; do not bypass writer ownership or clear IndexedDB. Pair UMBRA through the existing model.
4. Open Missions → Destinations → Asteroid/Derelict → Expedition. Choose a crew member, wait for refresh and confirm selection persists. Dispatch must show acceptance/queued blocker/error; accepted crew physically collect gear and transit. A paused or unsafe mission need not leave immediately.
5. Test available live feeds/received records from the paired remote. Report-only locations are not live cameras. Open Load original record when needed, then play/scrub. Reconnect without creating a second simulation.
6. For rollback, export a post-update backup, restore the pre-update backup in this version, close its tabs/server, then use the retained prior build. Older validators do not understand new optional motion fields; retain both backups.

No antivirus protection, operating-system settings or installed Windows files were altered by development. New media service uses Python standard-library code and existing local/Tailscale pairing/host lease; no new external dependency or public cloud service.
