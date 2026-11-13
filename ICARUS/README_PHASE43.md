# ICARUS / UMBRA: Phase 4.3 Living Ship Operations

This build extends the existing Phase 4.2B voyage with operational gravity, local electrical dependencies and physical engineering work. It does not create a new voyage, change calendar pacing or replace UMBRA.

## Install and preserve your voyage

1. In the working installation, pause and export a complete backup, including history, through the existing backup interface. Keep an untouched copy of that installation and backup outside the new folder.
2. Close all old ICARUS host tabs and stop the previous companion server. Old versions do not share the current writer fence; never run competing hosts.
3. Extract the Lite ZIP into a new folder. Keep its complete `web` folder and all six root host/runtime files together. Do not open `icarus.html` on the phone as a second host.
4. On the Windows laptop run `Start_Remote_Deck.bat`. Python 3 and the listed requirements remain necessary; install them from this folder with `py -m pip install -r requirements.txt` if needed. See README_PHASE41.md for the existing launcher, configuration, pairing and Tailscale procedure. The launcher is unchanged by this update.
5. Open the same laptop browser/profile and server origin used for the voyage. Browser data is origin-specific. If it shows a new world, stop and import your exported backup through the normal interface; do not overwrite the old backup with that new world.
6. A legacy save receives additive gravity hardware at its first load. Existing crew/history/resources/calendar remain. Confirm identity, date and incidents before resuming; export a new separately named backup after confirming migration.
7. Open the UMBRA web address on the paired phone/tablet. It remains a terminal for laptop telemetry/commands. The installed native app is not replaced or rebuilt.

## Use engineering

On the host or paired UMBRA, choose **Ship → Systems**. The compact engineering section shows generator condition, actual measured/target gravity, local power, warnings, queued work and recent source-backed diagnostics. Select a zone before operating it.

Gravity targets range 0–1.2g and take real simulation time to settle. Gravity isolation switches the local field; circuit isolation also affects connected lights, machinery, doors and life support. Restore normally uses a gradual ramp. Explicit rapid restoration warns of falling unsecured bodies/objects; it is a consequential control, not an effect preview. Restoring gravity does not automatically restore an electrically isolated circuit.

Inspect/maintain requests enter the existing crew workflow. Informed available engineers must collect tools/parts, travel, diagnose, safely isolate, repair and test actual components. Watch actual C07 work with the detailed camera when the security receiver/feed is available. Zero-g crew use floating/handhold poses and must secure themselves for work. A successful command changes the authorized target/request, not a promise that damaged/unpowered equipment can produce it.

A stale engineering measurement is labeled with its original tick. Restore real upstream power to obtain fresh readings; reconnecting a phone cannot manufacture a new measurement. Connection loss does not replace or reset host state.

## Roll back

Pause, export the new voyage separately, close all new/old host tabs and stop the server. Restart the preserved previous installation at its previous origin and import the untouched pre-upgrade backup if necessary. Do not expect older code to advance new gravity/repair fields correctly. Keep both backup generations until the rollback is confirmed.

## Reproduce verification from full source

Lite omits development tests/reports/tools; the development branch retains them. From the repository root run `node --test ICARUS/test_*.js`. From ICARUS run the OperationsIntegration, OperationsRemote and PersonalitiesClock unittest classes with Playwright/Chromium installed, plus the bridge/TV/service tests. `operations_campaign.py` drives real-calendar accelerated isolated campaigns and records source commit/hashes, explicit fixtures, daily audits and exact checkpoint reloads. Test output and unavailable hardware checks are detailed in PHASE43_VALIDATION.md.

See PHASE43_ARCHITECTURE.md for migration/authority boundaries and PHASE43_LIMITATIONS.md for approximations and pending hardware checks. Passing automated tests does not declare the final game finished.

For portable full-source verification use `python verify_operations.py --suite focused --runtime PATH_TO_EXTRACTED_LITE --report focused.json` from ICARUS. Use suites `browser`, `remote`, `clock` or `legacy` for the broader checks. For archived migration cases provide `--v13-web EVIDENCE/fixtures/v13_web`, `--phase41-backup EVIDENCE/fixtures/phase41_backup.json` and `--phase4-backup EVIDENCE/fixtures/phase4_backup.json`. Install development Playwright/Chromium separately; `--chromium PATH` selects a local browser. Missing fixtures produce explicit failures rather than invented pass results. These tools remain in full source, not Lite.
