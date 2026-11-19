# UMBRA Phase 4.8C preservation/audio foundation checkpoint

**FIRST: [Download the standalone existing-library Backup Tool](Backup_Existing_Soundboard_Tool.zip).** Stop the OLD server and copy only its .py/.bat helpers beside the OLD server.py and soundboard_data. Run the batch helper there. Require created=true, verified=true, your expected nonzero sound count and no source.errors. Keep the originals and ZIP. Empty/wrong folder fails; it is never claimed as your existing backup. The tool is self-contained standard Python and does not upload/remove originals.

**Your actual Windows sounds were not accessible and have NOT been backed up/verified by this cloud task.** Their safety check must run on the PC before upgrade. No schema migration, original removal or live Windows configuration change occurred. Code/fixtures are not proof of your real folder's state.

[Download optional C foundation Lite ZIP](UMBRA_Phase4_8C_Audio_Foundation_Checkpoint_Lite.zip) · [SHA-256 checksums for both ZIPs](SHA256SUMS.txt)

The library was already authoritative on the Windows server: soundboard_data/*.wav and library.json (IDs/order/name/category/icon/favorite/volume/output). Browsers are caches. This build adds verified backups before writes and blocks missing/older-server sync from deleting populated terminal caches. Keep/copy the whole private folder while stopped; voyage backups do not contain it. The optional audio_profile.json holds only owned metrics/settings, no voice audio. Originals and old IDs stay unchanged.

## Implemented / verified software

Read-only endpoint diagnostics, host-local consent-only five-second input sampling, separate mix-level measurement without changing calibration, K-weighted gated loudness/relative offset, bounded boost/sample peak protection, transient clip processing shared by host/private preview, explicit Sonar Aux clip-output selection and Emergency Reset. No serial UMBRA mic route or automatic Windows/Sonar/default/per-app setting change. Normal shutdown preserves owned preferences; reset disables DSP. Processing defaults OFF. Raw voice samples are never saved or transmitted.

Source `93064e50783786e7630e003c64fdeedda46801da`, runtime `12988bcc080ea50b7f7598d486ad41b6a83dd807`. **664 selected case executions passed**: 627 source/regression plus 37 extracted-package checks (including two actual standalone helper CLI checks). Inherited overlap; not 664 unique tests. ZIP 1,125,774 bytes, 278 source files + manifest, 169 runtime hashes/all source hashes/CRC/SHA verified. Helper shares the same verified code hashes. Private data/backups/credentials/tests/tools/reports excluded; existing runtime dependencies retained, no new pip dependency.

Lite SHA-256 `e0a6b0abf4a0ee877a5659d09ec2799ed872b24855a1f3f5716530953f4e47ea`. Helper SHA-256 `da5860f23c5dac0ad95cf0522187516ec53a5c123bf93dbc57a58e775edd19a5`.

[Full test report and exact source lineage](../../ICARUS/PHASE48C_VALIDATION.md) · [Installation/backup/rollback](../../ICARUS/README_PHASE48C.md) · [Architecture/security](../../ICARUS/PHASE48C_ARCHITECTURE.md) · [Sonar route/hardware checklist](../../ICARUS/SONAR_ROUTING_AND_VALIDATION.md) · [Separate palette restoration report](../../ICARUS/EASTER_PALETTE_RESTORATION.md)

## Palette fidelity

Original amber corporate tag/hazard stripes, mint readout, green panel edges/background and undimmed individual colors are restored from historical CSS in a scoped stylesheet. Two before-fix failures and passing restored tests prove the regression. The global UMBRA theme, trigger JavaScript, client preferences and all 13 original arcade files remain unchanged. Source reports contain actual before/after UI captures, not fabricated game footage.

## Full Phase 4.8C remains incomplete

Actual Windows/Sonar endpoints, both physical microphones, real private headphone/loopback isolation, combined game-chat delivery, normal-close/force-kill voice continuity, native Samsung/TV/Tailscale/antivirus and sustained gaming performance were unavailable. No physical result is claimed. Source tests use named input/output fixtures and owned generated sound clips. Actual imported-library backup/count verification is pending on the PC. Full historical/campaign matrix was not rerun.

SteelSeries' documented optional Mic+Aux route uses Sonar Stream Mix and a receiving app's Sonar Stream input, different from the reported Sonar Microphone input. This build does not apply those external persistent changes. Aux selection changes only UMBRA's clip output after explicit confirmation; microphone selection inside Sonar stays manual. Do not assume a level meter or render playback proves mixing into your unchanged chat input. `injection_verified` stays false until real review/testing; no unsafe serial mixer is substituted.

Use the manual checklist before any external routing decision. No new virtual driver, microphone default, power/fan setting or antivirus change. The C profile is opt-in and sample-peak/short-clip limitations are documented. Keep the old installation, all private library data and verified backups. Do not overwrite/delete the old folder to resolve missing sounds.
