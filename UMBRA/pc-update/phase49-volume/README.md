# UMBRA 4.9 individual-volume save hotfix

This fixes the reproduced **“signal is aborted without reason”** error when Customize → Volume → Save waits for the companion's verified sound-library backup. It is a small **web-script update for the Phase 4.9 bulk-import companion**, not a replacement ICARUS installation. No APK, driver or new Python package is required.

## Install on the Windows host

1. Export a voyage backup through the existing ICARUS UI as a precaution. Save and close the authoritative simulation tab and stop the companion normally. Keep the original installation and browser profile.
2. Extract this ZIP into a **separate folder**. Do not extract over ICARUS or copy another `soundboard_data` folder over your library.
3. Double-click **apply_volume_fix.bat**, then enter the original ICARUS folder containing `server.py`. Alternatively run:

   ```bat
   py -3 apply_volume_fix.py "C:\path\to\ICARUS"
   ```

4. The installer verifies the original bulk-import backend and web-script hashes, saves the old web script in `umbra_volume_code_backups`, and invokes your existing backup tool. It requires a verified, populated audio-library backup in `soundboard_backups` before changing the script. This can take time for a large library; allow it to finish. It stops if source hashes, library integrity, disk writes or backup verification fail. Keep both backup folders private.
5. Restart the **same installation** through its existing launcher. Hard-refresh the UMBRA browser page on each terminal (Ctrl+F5 on PC; reload on phone/tablet, restarting the browser if necessary). **Do not clear site data, IndexedDB or storage.**
6. Open Soundboard → Customize beside a sound, adjust Volume, then Save sound. Wait for confirmation. The first save after a companion restart can wait for a library backup. Reopen Customize and verify the saved percentage; refresh another terminal to verify the shared value.

The installation directory must already contain the verified bulk-import update. If the installer reports unrecognized source, **stop and retain the original folder**; do not force it or overwrite files manually. Supply that error and the build details for a matching patch. A missing populated library means the wrong installation may have been selected; this installer intentionally has no empty-library bypass.

Read-only compatibility check (does not back up or change anything):

```bat
py -3 apply_volume_fix.py "C:\path\to\ICARUS" --check
```

## Changes and preservation

Only `web/umbra/soundboard.js` is installed. Operations that may wait for the verified library backup now allow **180 seconds**, instead of 10 seconds for edits (the explicit backup previously allowed 120). Ordinary catalog/play/stop requests still use 10 seconds; link retrieval remains 25 seconds. The editor shows a saving message and keeps the draft on errors. True timeout errors explicitly say the result is unconfirmed and instruct a refresh before retrying. No write is automatically repeated.

A timeout does not prove that the server rejected the save. Close the edit, **Refresh library**, and check the stored value before retrying. If the server is still backing up, allow it to finish before refreshing again. Repeated failures need the companion's actual error investigated, not repeated blind saves.

The patch does not change the library format, clip bytes, sound IDs, button order, categories, favorites, other sounds' volumes, playback-output selection, audio profile, microphone routing, Sonar preset, VoiceMeeter, pairing or ICARUS voyage. It retains the larger-library backend and existing authenticated/revision-checked API. It does not remotely deploy to your PC or back up files inaccessible to this build environment. The installer creates the actual backup when run on your PC.

## Code-only rollback

Stop the companion normally and run:

```bat
py -3 apply_volume_fix.py "C:\path\to\ICARUS" --restore-code "C:\path\to\ICARUS\umbra_volume_code_backups\YOUR-BACKUP-FOLDER"
```

This restores only the previous bulk-import web script. It retains the 512-sound backend, all current sounds and settings, including libraries larger than 64 sounds. Restart normally and refresh UMBRA. The original timeout behavior will return. Do not downgrade the backend or replace your expanded library as part of this code-only rollback.

## Verification and limitations

See the source-folder `VERIFICATION.md` and `results/` for executed tests. Tests use generated audio, the real HTTP handler/library/backup implementation, Chromium and a fake Windows playback endpoint. Physical Windows, Samsung, Sonar/Fortnite, the Windows batch launcher and the user's private installed library cannot be tested from this environment. No claim of deployment or a backup of the user's actual library is made.

The 180-second deadline is bounded; a slower or failed host can still produce an unconfirmed result. This patch does not redesign the synchronous server backup as a background job. Native Android code and routing remain unchanged; browser saves update the same host metadata used for playback.

## Developer reproduction

Use a disposable Phase 4.9 Lite runtime from source commit `780108d56646982c323b3a4b82c74a2268a0bd60`, overlay the four `../phase49/payload` bulk-import files, then overlay this hotfix payload. Obtain the original `ICARUS/` test harness from that same commit separately. Never use a live installation or private data as the runtime fixture.

```sh
ICARUS_CHROMIUM=/usr/bin/chromium python run_tests.py --runtime /path/to/disposable/runtime --tests /path/to/historical/ICARUS --suite volume --report volume.json
python run_tests.py --runtime /path/to/disposable/runtime --tests /path/to/historical/ICARUS --suite installer --report installer.json
python run_tests.py --runtime /path/to/disposable/runtime --tests /path/to/historical/ICARUS --suite services --report services.json
ICARUS_CHROMIUM=/usr/bin/chromium python run_tests.py --runtime /path/to/disposable/runtime --tests /path/to/historical/ICARUS --suite bulk --report bulk.json
```

Playwright and Chromium are development test dependencies, not runtime additions. To reproduce the original failure, overlay the original bulk `soundboard.js` instead of the fixed script and run the slow-backup volume test only; it should fail with the original AbortError. All installer tests create their own temporary fixtures and real verified backups; no user audio is included in the package or test results.
