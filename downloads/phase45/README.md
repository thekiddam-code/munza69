# ICARUS Phase 4.5 — Visual Overhaul & System Boot

[Download the Lite ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/refs/heads/codex/visual-overhaul-system-boot-phase4-5/downloads/phase45/ICARUS_Phase4_5_Visual_Overhaul_and_System_Boot_Lite.zip)

[Before/after camera gallery](../../ICARUS/reports/phase45/VISUAL_COMPARISONS.md) · [Verification](VERIFICATION.md) · [Checksums](SHA256SUMS.txt) · [Evidence ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/refs/heads/codex/visual-overhaul-system-boot-phase4-5/downloads/phase45/ICARUS_Phase4_5_Verification_Evidence.zip)

This increment replaces the active detailed camera art with layered, room-specific environments and articulated characters, improves ordinary seated activities and wheelchair rendering, and adds an event-backed startup/authentication screen. A09 becomes Crew Lounge; A03 remains Observation Lounge. Gym conversion is deferred by your decision.

**Before upgrading:** Export a complete backup and retain the old application folder. Close old ICARUS tabs and stop the old server. Extract the Lite ZIP to a new folder, follow `README_PHASE45.md`, and start `Start_Remote_Deck.bat`. Use the same browser profile, host and port to retain the existing voyage. Never import the isolated worlds in the evidence archive as your voyage. Installation, optional paired-configuration transfer, backup, migration and rollback instructions are included in the ZIP.

The package contains source, runtime dependencies and instructions; no tests, development tools, private credentials or test worlds. It does not include Python or an installer. Existing Android/TV interfaces are preserved. A native APK rebuild awaits original Android Studio source recovery.

Actual verification: **563 passing source case executions plus 21 checks against the extracted ZIP**, two 7-real-day/25-ship-day normal/adverse campaigns, and an actual-time reconnect/reload watch. The counts include independently executed inherited overlap. Final runtime is `4bd2dadbd6e6541ef118e04b50b30ddbf561ae19`; Lite source/documentation commit is `4592a904561e6325edd79176231f66c38312093e`.

Physical Windows, Samsung phone/Tab S5e/TV, native APK, real LAN/Tailscale, antivirus, human visual/accessibility/touch and device GPU tests were **not run**. Coarse movement, limited interaction coverage and other unfinished work remain documented in [known limitations](../../ICARUS/PHASE45_LIMITATIONS.md). This is a tested development build, not final-game certification. Do not disable antivirus protection.

Source is on `codex/visual-overhaul-system-boot-phase4-5`; main, previous downloads and existing releases are unchanged.
