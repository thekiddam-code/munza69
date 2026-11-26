# Individual sound-volume hotfix verification

Date: 2026-11-26. Source base: `005e9c294922e0cb9c6adedf6b03154210f30329` (`main`, recovered UMBRA + bulk-import companion update). This change is isolated on `codex/umbra-individual-sound-volume`; no existing release or ICARUS runtime ZIP is replaced.

## Investigation and reproduced cause

The user reports build 4.9, bulk-imported sounds, and a save error resembling “signal aborted”. In the current bulk-import source, `payload/web/umbra/soundboard.js` gives `edit` requests a **10,000 ms AbortController deadline**. Meanwhile `SoundService.post` calls `preserve_existing()` under the library lock before the first import/edit/delete/reorder/output mutation after a companion restart. That operation creates and verifies a complete library backup before metadata changes. The larger bulk library permits 512 sounds / 256 MiB. Backup hashes source files, compresses them, checks the archive, and compares the source again; host/disk latency can exceed the browser's edit deadline.

Using the actual paired HTTP handler, real library and backup implementation, generated bulk-imported WAVs and a controlled **11-second backup delay**, the unmodified bulk script failed exactly with **“signal is aborted without reason”**. See `results/before.json`: one deliberately failing pre-fix regression. The delay is injected to reproduce the ordering/deadline problem; it is not a measurement of the user's Windows disk or a naturally slow three-clip library. The user's actual PC logs/library were unavailable, so the exact duration/cause of their host's backup remains unmeasured.

A cancelled browser request does not cancel a server mutation already in progress. It can finish after the UI reports failure, leaving the client with an old revision. Automatically replaying that edit or claiming it never saved would be incorrect. The fault is the mismatched client deadline and opaque error reporting; there is no demonstrated lost or corrupt clip.

## Implemented repair

- Only the installed `web/umbra/soundboard.js` changes. No server/library schema, capacity, voice routing, playback engine, save engine or Android source change.
- Backup-dependent calls (`backup`, `import`, `edit`, `delete`, `reorder`, `output`) get a bounded 180-second deadline. Catalog/play/stop retain 10 seconds; link retrieval retains 25 seconds.
- Saving displays an explicit waiting message. The button remains disabled while its request is pending; draft and existing server errors are retained on failure.
- A genuine deadline expiry reports an **unconfirmed** save, possible server completion, and a refresh-before-retry instruction. There is no automatic mutation replay.
- The installer accepts only the exact known bulk-import backend and before/after web script, normalizing CRLF/BOM. It creates a private code backup and requires the existing validated helper to create a verified populated library backup before atomically replacing one script. Refused paths, failed backup or mismatching code leave existing files intact.
- Code-only rollback retains the larger-library backend and current private data, including libraries over 64 sounds.

## Executed results

Linux, Python 3.12, headless Chromium `/usr/bin/chromium`, Playwright, temporary libraries and fake Windows render output. No real microphone, Windows defaults, Sonar configuration or user voyage is opened.

| Suite | Result | Main checks |
|---|---:|---|
| Pre-fix reproduction | 1 expected failure | Exact AbortError with 11s verified-backup wait and old 10s edit deadline |
| New volume browser regressions | 3/3 passed | Delayed successful save; only chosen volume changes; audio/output/profile retained; service restart, browser reload, second mobile-sized client; saved gain reaches host-play; failed backup preserves draft/data; true timeout preserves draft, server may finish, no replay |
| Existing sound/bulk browser regressions | 10/10 passed | 70 new imports + existing clip; duplicates/errors; conflicts/cancel/permission; browser edit/reorder/delete/restart; authenticated limits; mobile layout; cache/offline; tap vs private hold isolation |
| Existing services/audio/bulk regressions | 42/42 passed | Persistence, limits, metadata validation, revision conflicts, verified backup, output selection, profile processing and safe import boundaries |
| New installer regressions | 5/5 passed | Real verified backup of 65-sound library; identical private bytes; check/no-op/rollback; live-server refusal; unknown source; missing/corrupt library; backup failure; linked path refusal; tampered backup; atomic-write rollback |

**60 post-fix tests passed, zero failures/errors/skips in those suites.** Raw case-level reports are in `results/`. Browser bulk suite: 77.224 seconds; services: 5.388 seconds; installer source run: 1.031 seconds. The original and fixed runs use equivalent controlled backup delays; this verifies correctness across the old deadline, not improved server backup performance.

## Preservation and static review

`CHANGES.patch` shows the focused web diff. `manifest.json` pins all required source hashes. The library remains schema 1; no data migration or volume defaults are rewritten. Tests compare all original sound metadata except the selected volume, immutable IDs, WAV bytes, selected output and profile bytes, including across restart. The original Phase 4.9 runtime ZIP and existing bulk release ZIP remain unchanged.

Runtime network behavior remains same-origin authenticated `/api/sounds/` calls. No new external host, telemetry endpoint, process, microphone access, driver or background service is introduced. The installer calls only the known local Python backup helper and checks local port 8765; it writes code/library backups and replaces the single web script. It does not kill processes, clear browser storage, change Windows defaults, edit Sonar/VoiceMeeter, download executables, or modify antivirus. Backups must stay private; the package contains no imported clips, pairing secrets or voyage data.

## Not verified / remaining limitations

- Actual Windows installation, user's private sound library, audible headphone output, Fortnite/Sonar injection, Samsung tablet/phone hardware, native APK operation and Windows `.bat` execution were not accessible/tested. Mobile-sized Chromium is emulation, not physical-device validation.
- Backup time on the user's PC is unknown. Operations exceeding 180 seconds still report an unconfirmed result; the synchronous server backup has not been redesigned. Network interruptions unrelated to the deadline can still show their actual browser error.
- Applying this source patch does not remotely deploy it. The PC-side installer must successfully back up the existing populated library and verify matching hashes. Unknown 4.9 variants need a matching patch rather than a forced overwrite.
- No full ICARUS multi-day simulation was rerun: the world engine is unchanged and this is an isolated soundboard hotfix. Private preview isolation is validated at the API/test endpoint level, not the physical Windows audio graph.

The README contains installation, verification, developer test commands and code-only rollback instructions. Packaging checks and distribution SHA-256 are recorded separately beside the ZIP.

## Distribution verification

ZIP: `UMBRA_Phase49_Volume_Fix.zip` (23,157 bytes). Source commit: `3dbf4f65e670b10862fe40e69c0517372a244eb4`.

SHA-256: `2de0a81bbd4aa62517bc2d4b5755ba2efc25d5cce46fbee872a612711b27693b`.

The 8-entry ZIP passed CRC validation and every source entry was compared byte-for-byte with the pinned Git commit. It includes only the web payload, installer, hashes and user/review documentation. No test fixture, audio library, backup, cache, native binary or user save is included.

After extraction, all 5 installer safety tests were rerun against the **packaged installer and payload** and passed. This is an additional artifact check of the same 5 cases, not 5 newly distinct mechanics; the 60 distinct post-fix regression cases remain the main result. See `results/packaged-installer.json`.

Published branch: `codex/umbra-individual-sound-volume`. Main and prior release artifacts are not modified. Windows launch/hardware checks and installation against the actual private library remain for the host PC.
