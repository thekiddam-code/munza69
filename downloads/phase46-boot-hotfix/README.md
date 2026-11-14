# ICARUS 4.6 — Boot Screen Hotfix

**[Download the hotfix Lite ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/refs/heads/codex/phase46-boot-hotfix/downloads/phase46-boot-hotfix/ICARUS_Phase4_6_Boot_Hotfix_Lite.zip)**

This is a targeted Phase4.6 startup fix. The screen waits for actual initialization, accurately separates **WAITING FOR WRITER**, **INITIALIZING** and **ICARUS ONLINE**, retains key entry and requires explicit **ENTER ICARUS**. ENTER is prominent beside readiness and remains accessible while scrolling. Actual errors and retries are shown.

An initial waiting instance retries only the existing protected claim endpoint, using verified credentials, actual storage ownership and its same identity. It never overrides a live lease. A host that loses an already-held generation stays fenced until reload. All exploration modules, saves, storage locks and server generation protections are unchanged.

**Back up your voyage first.** Stop the old server/tabs, extract to a separate folder, and follow README_BOOT_HOTFIX.md. Keep the same browser profile, hostname and port. Start_Remote_Deck.bat and Python dependencies remain unchanged. Use Ctrl+F5 for updated assets if needed; do not clear site storage. Retain the original folder and complete backup for rollback.

[Cause and verification report](../../ICARUS/BOOT_HOTFIX_REPORT.md) · [Actual waiting screenshot](../../ICARUS/reports/boot_hotfix/screenshots/waiting_for_writer.png) · [Actual ONLINE/ENTER screenshot](../../ICARUS/reports/boot_hotfix/screenshots/online_explicit_enter.png) · [Checksums](SHA256SUMS.txt) · [Package verification](package_verification.json)

All **497 final-source case executions passed**:8 targeted startup,49 remote,7 drone/exploration,6 visual/save,4 ordinary production clock,405 models and18 service cases. Counts include independently executed inherited overlap. Extracted-package results are recorded separately in package_verification.json. The original Phase4.6 ZIP remains unchanged.

Only four of137 runtime files changed; the other133 are byte-identical to Phase4.6. Runtime source:fc8ce280689fda785a34d046f1187d5fcd6aee55. Packaged source/docs:792751141c3f78ffb3ffdd7af728d29bf75b3f7b. All217 source hashes and218 ZIP-entry CRCs passed; dependencies retained and tests/tools/credentials/test worlds excluded.

SHA-256: `6d36ddab8be110fac078af8fe8a6e89423ee9409bc75ef53bf22656c4a60f0a6`.

```powershell
Get-FileHash .\ICARUS_Phase4_6_Boot_Hotfix_Lite.zip -Algorithm SHA256
```

Not run: physical Windows/Samsung/native APK/LAN/Tailscale, antivirus or new long-duration campaigns. Linux Chromium/local HTTP and device emulation do not establish physical-device validation. No unrelated gameplay changes or lock bypass were introduced.

All **15 extracted-package checks passed** (8 startup +7 exploration). Full package integrity and case counts are in package_verification.json.
