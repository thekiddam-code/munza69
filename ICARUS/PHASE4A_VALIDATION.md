# Phase 4A measured validation

Runtime frozen at `3b6d986f5e26c3fa33c42c61abc3f0e830b286c6`. Tests use an independent extraction of the source-built Lite ZIP; external harnesses retain source tests and point runtime roots/imports to that extraction. Final documentation/package metadata may identify a later commit; all 90 runtime bytes/hashes must remain identical. Evidence is under `reports/phase4a` and the separate verification archive, excluded from Lite.

## Executed checks

All 183 browser/server regression cases and seven TV-service unit cases pass (190 unittest cases total), alongside 276 Node tests and 26 additional phone/tablet functional checks. All five full-history migrations pass. Final regression and migration totals are recorded in `reports/phase4a/accepted_summary.json`; individual JSON/text outputs identify every executed case and failure. No native/device result is inferred from browser execution.

- 276 Node tests pass against extracted runtime modules: original regressions plus individual-knowledge camera projection and bounded layout/profile cases.
- 16 UMBRA browser/server tests pass: responsive retained departments, real HTTP pairing/TV protocol and timer cancellation, layout edit/save/cancel/undo/resize/remap/reload/overlap validation, right-hand remote stability, actual source-grounded camera/follow and style sharing, stale/unknown/offline handling, expand/Escape, default-off cosmetics, manual archive/reduced motion, touch drag/orientation draft continuity, disconnected playback, bounded repeat/cancel, unavailable renderer, timer auth/Origin/owner/target guards, idle-only cosmetics, genuine 30-day donor telemetry within the existing payload limit, and exact legacy Android response shapes.
- 7 deterministic TV-service tests pass: cache/reconnect, strict timer values, replacement/cancellation/config/owner invalidation, one-shot failure behavior and late-wake expiration. No physical TV is used.
- Phone functional checks: 15 pass; tablet touch checks: 11 pass. Chromium viewport/touch emulation with real local HTTP; desktop keyboard and Samsung socket are stubbed.
- Full cinematic (71), stability (30), compatibility (44), command-interface (17), production-clock (2) and bridge (3) suites pass; outputs are retained separately. They preserve Monday boundaries, synchronized holiday 1× / normal 4× / explicit 1/5/20× testing, source history, private knowledge, crew continuity, physical field state, backup integrity and single-writer behavior.
- Five historical full-history migrations pass: 10,659 / 50,170 / 48,137 / 45,870 / 45,515 retained source rows respectively, with no import/reload domain mismatches. They are exercised (Phase 1, Phase 2, Phase 3, Phase 3 with Nadia's existing memorial, Phase 3.5). Reports compare import/reload domains and resume 120 minutes without replacing crew/history. Original donors remain external fixtures; hashes and counts are retained.

## Real-calendar accelerated campaigns

Fixed start 2026-10-28 UTC, America/Chicago, production step/field controllers advanced in hourly real intervals. Per-step autosave is disabled in the test driver; actual checkpoint save/reload and full source-history export remain enabled. Synchronized holidays explain the difference from a simple 4× multiplication. These are freshly executed results, not copied earlier campaigns.

| Scenario | Seed | Real / simulated days | Living / dead | Arrivals | Field missions | Science cases | Conversations | Weekly films | History rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Compound adverse | 4807 | 7 / 25 | 20 / 0 | 5 | 12 | 21 | 417 | 1 | 10,463 |
| Normal | 1001 | 30 / 111.75 | 20 / 0 | 5 | 8 | 24 | 2,032 | 4 | 45,514 |

Compound starts equipment B07=10, C09=32, C07=45 and one crew member at health 55, explicitly marked as adverse fixture setup. Subsequent events come from simulation. Research statuses: adverse 62 complete / 26 no-result / 3 failed, four confirmed conclusions; normal 72 / 25 / 4, three confirmed conclusions. Neither campaign produced a Legendary segment. Surviving crew alone is not the acceptance test.

No reported resource, frontier, chronicle, knowledge, creature or cinematic audit errors; no crew identity loss, real-clock rollback/discard or missing/private public sources. Checkpoints are byte-exact at day 7 for both and day 30 for normal. Original mission, travel, research, conversation and Sunday systems actually run. Five local jobs each; recorded resource-acquisition statistic is empty in both, so these campaigns do not establish fresh extraction diversity. Travel fuel consumed 1.9624515496596866 each. Full resource balances and source-kind statistics are in campaign_summary.json. End snapshot diagnostics grow to 4,014,121 / 9,922,484 bytes; compressed primary+fallback storage 1,363,274 / 2,878,002 bytes. Long-history growth remains a pre-release limitation, not a new unboundedness claim from only these runs.

The campaign driver records 89 existing host/web hashes, all matching the extracted package. The newly required `tv_service.py` is independently included in the 90-file runtime identity/static audit and executed service/server tests. No runtime source was changed during campaigns.

## Static/package review

64 standalone JS/Python syntax files checked, inline scripts checked, 63 local script references resolved; every selected file verified against its committed source and manifest. Old config/dependencies/launcher, TV key allowlist and nine existing server primitives remain unchanged. Six GIFs match supplied source bytes, each 12 frames at 240 ms per frame (2.88 s); reduced-motion previews derive from original first frames. Private pairing/TV-token files, tests, packaging tools and replacement APK are absent from Lite. SECURITY_PHASE4A.md documents LAN HTTP, inherited optional TV certificate omission, authenticated desktop input and timer power-off effects.

Development diagnostics were corrected without weakening runtime assertions: Playwright option state uses the actual disabled DOM property; fake clock is installed before interval creation; resize assertions await the responsive mode. Independent asset verifier initially mistook 240 ms per frame for total duration; corrected to 2,880 ms. An audit attempted before campaigns finished correctly rejected incomplete runs; final audit ran only after completion. Prior successful core Phase 4 evidence remains historical, separate from these fresh results.

## Not run / remaining acceptance

Native APK build/update is **pending recovery of the existing Android Studio project**. The installed app is preserved; protocol compatibility is exercised, but its binary/WebView/packaged assets are not validated. Physical Windows installation/input, Samsung Tab S5e/Android/Wi-Fi, Samsung TV model/firmware/permission/power behavior, antivirus scanning, screen reader/native GPU/FPS, sustained ergonomics and human content review are NOT RUN here. Actual streaming, advanced native TV functions and recorded Kill Cam capture remain deferred. Native/human gates prevent declaring the entire phase/final release complete; they do not block the independently implemented browser/server distribution.
