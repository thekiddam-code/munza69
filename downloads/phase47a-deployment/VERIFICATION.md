# Phase 4.7A Field Deployment Checkpoint Lite

This is the next verified milestone: FOC-01 can be physically prepared, loaded, flown on the shared transport, unloaded into a persistent Landing Shelf camp, packed and recovered. The whole Phase4.7 release remains incomplete. Camp drone services, ATV driving, treatment, security/resupply/relocation and later encoded media are not complete.

## Download and installation

Download `ICARUS_Phase4_7A_Field_Deployment_Checkpoint_Lite.zip`; read `README_PHASE47A_DEPLOYMENT.md` inside. Export a complete pre-deployment backup first, retain the previous build, stop its server and close authoritative tabs, then extract separately and run `Start_Remote_Deck.bat` using the same browser profile/hostname/port. Do not clear IndexedDB or bypass locks. Boot still requires explicit ENTER. Before rolling back to an older build, pause this build and restore the pre-deployment backup here first; old validators do not understand active camp/freight state.

## Exact artifact verification

- ZIP: **1,017,373 bytes**; 240 committed source files plus manifest; all 146 runtime dependencies/assets included.
- Source commit: `c6c0e0d7dc2b6af8e4c90e81f73e16c17250a535`.
- Frozen tested runtime: `13f5ed7d17182f6923e7e19f9fdbba76564dd5bc`.
- Every packaged file hash matches its source commit, every runtime hash matches the tested freeze, and ZIP CRC verification passed.
- SHA-256: `9e7955df820b2fca0b07a657abb1bcdc4b7a099e61f1506ea123e16b772564ee`.
- **570 selected source/frozen-runtime case executions passed**, plus **23 extracted-ZIP executions**: boot 8, physical deployment/adversity 7, durable/preview 6, paired freight 1 and additional actual autonomous-decision 1. **593 passing executions**, with inherited overlap.
- The additional autonomous case completes a real physical exploration sortie, enables ordinary autonomous operations, and reaches a deployed camp without a deployment-button request or injected mission history.
- The actual supplied Episode2 backup retained original crew, maps, all 16,954 indexed history rows, recordings and exact restart state. The original file is unchanged and excluded.
- The full 16,000-wall-second catch-up backlog drained in **118.929s**; 5,333 physical minutes, unchanged 20× selection, zero remaining backlog, valid writer, no browser errors and all original received recordings unchanged. Maximum publication **109,963 bytes**, all HTTP 200. Compared with the prior hotfix's equivalent run, all final state domains matched except additive `forwardOperations`.

[Detailed validation](../../ICARUS/PHASE47A_DEPLOYMENT_VALIDATION.md), [architecture/limitations](../../ICARUS/PHASE47A_DEPLOYMENT_ARCHITECTURE.md), [machine-readable evidence](../../ICARUS/reports/phase47a/validation_summary.json), and [package results](../../ICARUS/reports/phase47a/package_verification.json).

Actual renderer screenshots: [deployed camp](../../ICARUS/reports/phase47a/screenshots/actual_camp_body_camera.png) and [empty C03 parking during transit](../../ICARUS/reports/phase47a/screenshots/actual_empty_cargo_parking.png). These are isolated technical simulation states, not the private voyage or physical recorded video.

No physical Windows/Samsung/TV/Tailscale/antivirus or native APK build result is claimed. Native source recovery remains pending; existing Android/TV paths are preserved. No new external network service, runtime dependency, system modification or antivirus bypass was added. Only the listed test suites were rerun; the full historical campaign matrix was not repeated. Runtime tests/reports/development tools/private data are excluded from Lite and remain separately in the source branch.

Published raw GitHub download verified after push: HTTP 200, 1,017,373 bytes, exact SHA-256 above. Evidence: `ICARUS/reports/phase47a/github_download_verification.json`. Review branch: `codex/phase47a-field-deployment`, draft [PR #15](https://github.com/thekiddam-code/munza69/pull/15). The existing main branch and previous downloads remain unchanged.
