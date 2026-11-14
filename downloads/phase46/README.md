# ICARUS Phase 4.6 — Autonomous Exploration & Drone Reconnaissance

**[Download Phase 4.6 Lite ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/refs/heads/codex/autonomous-exploration-phase4-6/downloads/phase46/ICARUS_Phase4_6_Autonomous_Exploration_and_Drone_Reconnaissance_Lite.zip)**

[Actual running screenshots](../../ICARUS/reports/phase46/SCREENSHOTS.md) · [Verification report](VERIFICATION.md) · [SHA-256 checksums](SHA256SUMS.txt) · [Evidence ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/refs/heads/codex/autonomous-exploration-phase4-6/downloads/phase46/ICARUS_Phase4_6_Verification_Evidence.zip)

Drones now use paid physical assembly, charging, connected asteroid surveys, real sensors and signal limits, reserve return decisions, source-backed evidence and persistent recovery/custody. Missions → Active includes received exploration controls/map/status/playback. Ship and drone cameras share the existing detailed renderer. The boot screen stays visible through actual initialization and after readiness until you press **ENTER ICARUS**; typed keys remain available, and writer ownership is separate from Bridge authorization.

**Export a complete voyage backup before upgrading.** Retain your old installation and backup. Close old host tabs/server, extract to a new folder, and follow `README_PHASE46.md` in the ZIP. Keep the same browser profile, host and port to retain the existing voyage. Run `Start_Remote_Deck.bat` on Windows; dependencies are unchanged. Phones use the laptop's printed LAN/Tailscale address and existing pairing, never a separate simulation. Rollback restores the retained pre-upgrade complete backup.

Actual tests: **595 final-source case executions and 26 extracted-ZIP checks passed**. Both normal/adverse campaigns ran seven real days /25 ship days, made five ship arrivals, and completed seven finite drone sorties each. Received20 sector observations/98 captured frames persisted through restart, with independent conservation/provenance audits. The core return-and-reload criterion is verified in actual browser execution. Public download checksums are verified separately after upload.

**Limits:** Gym remains deferred. Recordings are captured procedural frame sequences, not encoded physical video. Mid-passage salvage, independent rescue transport, dedicated autonomous relay installation and high-resolution on-demand media transfer remain deferred. Remote PNGs may fall back to explicitly labeled reconstruction to respect bandwidth limits; full bounded captures remain in the host save. Physical Windows/Samsung/native/LAN/Tailscale, antivirus and human visual/accessibility/GPU tests were not run. Native APK rebuilding awaits original Android Studio source recovery; existing functionality is preserved.

Lite source/documentation commit: `11c49af03292a5ab2dc62d8cb2c1625e69cf8aa5`. All137 runtime files match tested runtime `a22f2aca871e988a94cdd5083f8c99022da53460`. The ZIP retains runtime dependencies and instructions, excludes tests/tools/reports/credentials/test worlds, and does not bundle Python or an installer. Do not disable antivirus protection. This is a tested development increment, not final-game certification.

[Architecture](../../ICARUS/PHASE46_ARCHITECTURE.md) · [Changelog](../../ICARUS/PHASE46_CHANGELOG.md) · [Limitations](../../ICARUS/PHASE46_LIMITATIONS.md) · [Security review](../../ICARUS/SECURITY_PHASE46.md). Main, previous downloads and existing releases remain unchanged.

[Draft review PR #10](https://github.com/thekiddam-code/munza69/pull/10) · [Verified public download hashes](GITHUB_DOWNLOAD_VERIFICATION.json). Both public ZIPs returned HTTP200 and matched the published SHA-256 checksums.
