# Phase 4.8C local headphone routing correction — not full C completion

[Download ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/codex/umbra-sonar-phase4-8c/downloads/phase48c-routing/UMBRA_Phase4_8C_Headphone_Routing_Checkpoint_Lite.zip)

[Backup Tool — run in OLD installation first](https://raw.githubusercontent.com/thekiddam-code/munza69/codex/umbra-sonar-phase4-8c/downloads/phase48c/Backup_Existing_Soundboard_Tool.zip)

## Protect the existing installation before upgrade

The developer cannot access the actual Windows sound library; it has NOT been backed up or verified here. Stop the old server. Copy only the backup .py/.bat helpers beside OLD server.py and soundboard_data, run the batch file, require created=true, verified=true, expected nonzero source.sounds and empty source.errors. Keep original installation/folder and verified ZIP. Never clear IndexedDB or reset the voyage. Sound backups are separate from voyage backups.

Extract the new package separately; while stopped copy the entire soundboard_data and private configurations from the old installation. Preserve hostname/port/browser profile. Follow README_PHASE48C.md and PHASE48C_ROUTING_CORRECTION.md in the ZIP for installation/rollback. No schema migration or original deletion. Backups/private sounds/credentials/tests/reports/development packaging tools are intentionally excluded; runtime dependencies retained.

## Implemented

Instant Buttons → Audio calibration / Sonar / verified backup → Restore PC headphone playback. Explicitly select the Windows playback/render endpoint feeding headphones, save, then tap an existing sound. The Arctis Nova microphone is a capture endpoint, not a speaker output. No guessed default or physical mic selection. Server validates the render identity, revision and backup before modifying only UMBRA's output preference. Existing original sound files and button metadata remain. Aux has an explicit warning: it replaces local clip output, needs Personal Mix for local hearing, and is not Sonar Microphone injection.

## Routing finding — consequential decision outstanding

SteelSeries documents Mic + Aux through Sonar Stream Mix with games using Sonar - Stream. This needs no extra cable, but requires intentional mix membership/game-input changes. No supported direct injection API into unchanged Sonar - Microphone was identified. A downstream virtual mixer could combine Sonar-processed voice and clips, but also needs its own combined game input and adds a software/driver dependency. A cable alone does not provide that mix inlet. Upstream replacement of the physical Sonar mic input is excluded.

No Sonar/default/game-input setting, external mixer or new driver was applied. Physical Arctis selection/voice processing are untouched. Microphone-stream injection remains **unimplemented and unverified** pending that routing choice and real Windows testing. Full Phase 4.8C is not complete.

## Actual verification

56 source case executions + 4 Node gesture executions + 22 extracted-package executions = **82 selected passing executions**, with overlapping coverage; zero final failures/errors/skips. Actual HTTP/Chromium software tests; native audio endpoints are controlled fixtures. Source report: ICARUS/reports/phase48c_routing/source_tests.json. Package report: package_tests.json. Both modified JS files passed syntax checks. All 280 source-file hashes and ZIP CRC validated, with 169 runtime files. Only two runtime files changed; other 167 match the prior C checkpoint, including simulation/save code, native audio code and Easter egg assets/palettes. Both earlier B/C ZIPs are unchanged.

The tests check Aux→headphone selection/persistence, byte-identical sound files/assignments, pre-write verified snapshot, backup-failure preservation, rejection of input-only devices, explicit selection and draft retention, separate private holds without host-play, B imports/edits/reorder/restart, consent/cancellation/DSP/cache guards, and individual Easter colors/trigger continuity.

**Not run:** audible physical Windows headphone playback; actual Sonar/game combined voice+effects; physical private/OBS/loopback/acoustic isolation; close/force-kill voice continuity; Samsung/native APK/TV/antivirus validation. Full historical/long-duration suites were not rerun. A browser preview uses that terminal's current output: if the browser itself is routed into a future broadcast mix, software host-play separation alone cannot ensure privacy. Verify the actual receiving mix before using any broadcast route. Level detection alone is not proof that both sources reached it.

Source commit: `4d0be2d9cbdba5ddb2a2030ecf83ee69f2a69a6d`.

ZIP SHA-256: `351f0f0f9ae163aa10f6bb110acd931e7a04ffdd0d8b9ff0aaaafe6d1054a7ed`.

See SHA256SUMS.txt and verification.json. Published download transport verification is recorded separately after upload.
