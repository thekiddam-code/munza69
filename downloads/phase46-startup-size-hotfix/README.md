# ICARUS 4.6 — Startup Size Hotfix Lite

[**Download the corrected ZIP**](https://raw.githubusercontent.com/thekiddam-code/munza69/codex/phase46-startup-size-hotfix/downloads/phase46-startup-size-hotfix/ICARUS_Phase4_6_Startup_Size_Hotfix_Lite.zip) · [SHA-256](SHA256SUMS.txt) · [Verification](package_verification.json)

Fixes the reproduced “Too large” startup failure using the actual Episode 2 voyage backup. The failing operation was Remote Deck `POST /api/icarus/host/publish`: 132,753 bytes in the first trace, above the unchanged 131,072-byte server limit. Final restored-world packets measure 109,918–109,920 bytes and return HTTP 200. Your world was already restoring successfully; the oversized outgoing preview caused the bridge failure.

The patch bounds disposable outgoing previews, preserves archive images, and retrieves local recording frames on selection. Boot remains until explicit ENTER. Writer protections, saves, clock, exploration and installed Android functionality remain. This is a separate download/branch; prior downloads and main are unchanged.

[Review pull request #12](https://github.com/thekiddam-code/munza69/pull/12) · [Verified published download](published_download_verification.json)

## Install safely

Keep your complete backup and original application folder. Stop the old server and close host tabs. Extract this ZIP into a separate folder and run `Start_Remote_Deck.bat`, keeping the same Windows Python environment, browser profile, hostname and port. Refresh updated assets with Ctrl+F5 if necessary. **Do not clear site data/IndexedDB or select New Voyage.** Wait for actual initialization and writer ownership, then select ENTER ICARUS. The ZIP includes `README_STARTUP_SIZE_FIX.md` with installation, configuration transfer, backup and rollback instructions.

## Actual verification

- 509 source case executions passed: 413 JavaScript, 18 service, 49 remote, 8 boot, 7 drone, 6 visual, 4 clock and 4 actual-backup checks. Suites have inherited overlap.
- 12 additional checks passed against this extracted ZIP: 4 actual-backup checks and 8 boot checks.
- All 221 ZIP entries/220 source-file hashes and 138 runtime hashes verified. Runtime matches frozen `20001c00ffaf6538cf7bb3dbbcf3c1b2dad69a06`; package source is `6884b7594c391cf2c4677ea8d2a9b0cc12432a74`.
- Original crew, knowledge, explored world, received recordings and every original history record preserved. All 98 state frames/74 PNGs present in the supplied backup remain; no absent footage was fabricated. Original private backup unchanged and excluded from distribution/reports.
- Physical Windows, installed Samsung APK, physical TV, Tailscale and antivirus validation were unavailable. Linux Chromium/real local server tests are not hardware certification. Native Android build remains pending source recovery.

[Detailed investigation and changelog](../../ICARUS/STARTUP_SIZE_REPORT.md) · [Source results](../../ICARUS/reports/startup_size/accepted_summary.json) · [Sanitized reproduction](../../ICARUS/reports/startup_size/reproduction.json)

SHA-256: `bd8ddb8a14cdd370dc3c3c52ece22fdbf721716293223a6b304b58533dea8abf`
