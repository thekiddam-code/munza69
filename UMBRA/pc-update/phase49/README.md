# PC UMBRA Phase 4.9 bulk-sound update

This package adds **Soundboard → Add many sounds** to the existing Phase 4.9 website on its existing port 8765. It is prepared source, not a claim that your private PC site was deployed remotely. The build environment could not reach that LAN address.

The update changes only four existing soundboard files. It reuses the same library, PCM conversion, authenticated import API, playback, verified backups, output routing and audio profile. No simulation/world engine, clock, IndexedDB save, Windows/Sonar default, microphone, driver, pairing file or TV integration is replaced.

## Apply on your PC

1. Export your current voyage backup through the existing UI. Keep the original installation. Save and close its authoritative simulation tab; stop the companion normally.
2. Extract this update ZIP into a separate folder. Do not extract it over ICARUS, replace your installation, clear browser site data, or copy an empty soundboard_data folder over your sounds.
3. Run **apply_bulk_update.bat** and enter the original ICARUS folder containing `server.py`. Alternatively: `py apply_bulk_update.py "C:\path\to\ICARUS"`. Standard Python only; no new packages/drivers.
4. The installer requires matching Phase 4.9 source hashes (Windows CRLF/BOM differences are accepted), checks the companion is stopped, saves the original four code files, and runs your existing sound-backup helper with `--require-existing`. A missing/corrupt/unverified library or changed code stops the update. It never guesses an original sound count or calls an empty folder a verified backup.
5. Restart the same installation through its existing launcher. Keep the same browser profile, hostname and port. Hard-refresh the UMBRA Remote Deck page to load the new script; do not clear IndexedDB or site data. Install the matching UMBRA Mobile 3.1 APK for larger native catalogs.

For a genuinely new/empty library only: `py apply_bulk_update.py "C:\path\to\ICARUS" --new-library`. Do not use this option to work around a missing previously populated folder. It refuses a populated library. If an empty `library.json` already exists, this explicit mode still backs it and its output/profile metadata up, without claiming any previously imported sounds were found.

`--check` verifies code without modifying anything and can be run before stopping. An already fully applied update is a no-op. Code backups are in the selected installation's `umbra_bulk_code_backups`; verified audio archives remain in its existing `soundboard_backups`. Keep both privately. Never upload them to public GitHub.

## Use the bulk uploader

Open the existing Soundboard and choose **Add many sounds**. Select multiple files or an audio folder, category and per-clip volume, confirm permission, then start. Up to 512 files can be queued; the total library is bounded to **512 sounds / 256 MiB**. Each source remains at most 8 MiB and 30 seconds. Browser-supported formats are converted one at a time through the original converter to 24 kHz mono PCM16 WAV. Unsupported or long files receive individual errors. Audio originals are not stored separately; keep your originals.

Existing sounds, immutable IDs, labels, favorites, output and audio_profile.json are retained. Imported labels come from filenames and can be edited through the existing Customize action. Duplicate canonical audio is skipped by the server by default; Allow duplicates explicitly creates separate mappings. This works on HTTP LAN sites without depending on browser HTTPS-only Web Crypto.

Progress counts only acknowledged saves and duplicate responses. Cancel stops remaining files; a request already received by the server can finish. Saved clips are retained, never rolled back/deleted because another file fails. A timeout, authorization/revision conflict or unconfirmed save stops the queue, refreshes the catalog and does not automatically replay uploads. Reselecting files with default duplicate skipping can resume safely. Import does not play audio or change outputs.

The server preserves schema-1 storage, exact legacy import payloads and per-sound size/permission/revision checks. It adds an optional boolean `skip_duplicate` to the same import method and advertises capacity in the catalog. There is no parallel library or playback engine. The standalone backup bound rises to 384 MiB so the 256 MiB library and metadata remain preservable. Old 64-sound server builds cannot read a library expanded beyond 64: retain the verified pre-import archive before rollback.

## Rollback and verification

Stop normally. To restore the old code: `py apply_bulk_update.py "C:\path\to\ICARUS" --restore-code "C:\path\to\code-backup"`. This refuses if the current library exceeds the old 64 sounds / 64 MiB limit or checksums do not match. Restore a verified pre-import library separately first if downgrading; keep the current expanded library safe. No automatic data deletion/reset is provided.

`manifest.json` identifies the exact Phase 4.9 baseline and all original/new code hashes. `CHANGES.patch` is the reviewable diff. Browser tests use the real handler and isolated generated sounds/fake Windows render output; they do not prove your private library backup, audible PC output, live deployment or voice/Sonar isolation. Regression tests in this package require the full Phase 4.9 source test harness. Windows batch execution and your actual PC installation remain manual checks.

Developer reproduction: in an isolated checkout of the manifest baseline, copy `test_bulk_services.py`, `test_bulk_soundboard.py` and `test_sound_services.py` into `ICARUS/`, apply the four payload files there, then run `python -m unittest -v test_sound_services test_audio_foundation test_bulk_services` and `python test_bulk_soundboard.py` from `ICARUS/`. The browser suite needs the original Playwright/Chromium harness; use its documented browser setup. The included legacy service test uses the advertised new `MAX_SOUNDS` constant instead of its historical hardcoded 64; the capacity assertion remains strict. Set `ICARUS_CHROMIUM` to an installed Chromium executable if the Playwright browser bundle is unavailable. For installer tests, set `ICARUS_PHASE49_REFERENCE` to that isolated checkout root (whose HEAD remains the original baseline), then run `python test_bulk_installer.py` from this package. It creates temporary fixture installations and reads original code via `git show`; never target the live PC data.
