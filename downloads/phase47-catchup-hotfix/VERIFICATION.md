# Phase 4.7A Catch-up Hotfix Lite

This is a focused catch-up/telemetry repair to the existing development checkpoint. The unfinished Phase 4.7 vehicle departure, forward camp and camp-based rotations remain unfinished.

Download `ICARUS_Phase4_7A_Catchup_Hotfix_Lite.zip` and read `README_CATCHUP_HOTFIX.md` inside. Export a complete backup first. Stop the old server and close its host tabs; keep the same browser profile, hostname and port. Never clear IndexedDB or bypass writer locks. `Start_Remote_Deck.bat` is unchanged. Installation and rollback details are included.

## Verification

- ZIP: 989,164 bytes; 235 committed source files plus build manifest.
- Source commit: `cb4f8bbf52fd31e6ed1a271cad1d6fd558d1fcb0`.
- Tested runtime commit: `ef4f12d4e745aa29de96f0fd6c6b6a6d6cc3bcc8`.
- All 145 runtime hashes match the frozen tested runtime. All 235 packaged source hashes match the source commit. ZIP CRC verification passed.
- SHA-256: `a8df639823dd00927ad19403ca30d6f3a03a44286afe71cf93c6d82f22e52230`.
- 551 selected source/frozen-runtime case executions passed. Another **14 tests passed against the extracted ZIP** (eight complete boot tests and six durability/telemetry regressions): **565 passing case executions**, with inherited overlap.
- Existing private Episode 2 backup retained original crew, maps, history and recordings across reload; all 16,954 original indexed history rows were verified. The private backup remains excluded and unchanged.
- Matched 120-tick canonical completion: **31.656 → 1.778 seconds**, same full initial/final world hashes, unchanged selected 20× rate. Including compatibility mirror completion: **31.656 → 4.916 seconds**.
- Full 16,000-wall-second backlog drained in **117.986 seconds**, plus 0.046 seconds of outstanding canonical writes; 5,333 physical minutes, zero remaining backlog, writer retained. All original received recordings remained unchanged. Largest observed telemetry publication: **109,990 bytes**; all returned HTTP 200.

The full report is [CATCHUP_VALIDATION.md](../../ICARUS/CATCHUP_VALIDATION.md), with [root cause and architecture](../../ICARUS/CATCHUP_INVESTIGATION.md) and [machine-readable evidence](../../ICARUS/reports/catchup_fix/validation_summary.json). The entire historical Python/campaign matrix was not rerun. Results are Linux Chromium tests on isolated imported copies, not physical Windows/Samsung/TV/Tailscale/antivirus verification. Native Android rebuilding remains pending source recovery. No world reset, extra speed multiplier, raised payload cap, antivirus modification or writer-lock bypass was used.
