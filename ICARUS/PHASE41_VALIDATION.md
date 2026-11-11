# Phase 4.1 measured validation / acceptance

Runtime frozen at **53aa62d76d356343cfb514b725de30b24fba4a06**. Tests run against an independent extraction of the source-built Lite ZIP, with test sources/harnesses outside it. All **102 runtime hashes** match the tested source and both campaign drivers. Documentation-only delivery commits can differ; the final package must retain these same runtime bytes. Thirty-two preexisting model modules are byte-identical to Phase 4A. Raw JSON/text, screenshots, source identity and actual failed/retried attempts are in reports/phase41 and the optional evidence ZIP.

## Executed automatic checks

| Suite / check | Executed result |
| --- | --- |
| Node model/presentation regressions | 279 pass, zero fail/skip |
| Phase 4.1 / inherited UMBRA HTTP-browser cases | 30 pass |
| Ordinary unpaused host during phone disconnection | 1 pass; real 4× timer, no simulation test hooks; host advanced, remote reconnected to that tick |
| Cinematic / knowledge / living-world integration | 71 pass |
| Stability and adverse emergencies | 30 pass |
| Long-term compatibility / mission/resource logic | 44 pass |
| Command interface | 17 pass |
| Ordinary production clock | 2 pass |
| Legacy authenticated Remote Deck bridge | 3 pass |
| Host service / original TV service unit cases | 8 + 7 pass |
| Phone / tablet functional checks | 15 + 11 pass; Chromium touch emulation |
| Full historical save migrations | 6 pass |

Totals are **492 automated case executions** (279 Node + 198 browser/HTTP + 15 service), plus 26 additional functional checks and six full-history migrations. Inherited tests are executed in multiple relevant suites; this is not a claim of 492 unique requirements. Exploratory/repair reruns are additional and are excluded from this final acceptance-set total.

New coverage includes automatic bootstrap without a pasted key, one active server owner across independent contexts, same-origin IDB fencing with cloned tab/session identity, unchanged native response contracts, no remote simulation bootstrap/save upload, authenticated SSE, matching host/phone tick, creator permission checks, request deduplication, retained delivery until acknowledgment, reload without reexecuting an applied-but-unacknowledged command, stale camera clearing, paused/offline distinction and genuine ordinary-clock advancement during phone disconnection. Remote disconnection is emulated with Chromium network-offline controls; it is not physical Wi-Fi/Tailscale validation.

UI cases exercise pointer/keyboard movement, real width and height resizing, collapse/focus/Escape, preset persistence, independent desktop/mobile layouts, actual observed-crew following with unchanged world, Creator restart/route behavior, profile scroll/disclosure continuity, stable select nodes, native page scroll chaining and all retained remote departments/TV/profile/fictional-archive behavior. Source privacy tests withhold raw numerical psychology/health, unseen contacts and private records, preserve received assessments and mark sensor loss as unknown. They do not fabricate a diagnosis.

## Save continuity

| Donor | Imported history rows | Living crew / retained memorial |
| --- | --- | --- |
| Phase 4A normal 30-day export | 45,515 | 20 / none |
| Phase 1 | 10,659 | 20 / none |
| Phase 2 | 50,170 | 20 / none |
| Phase 3 | 48,137 | 20 / none |
| Phase 3 adverse | 45,870 | 19 / Nadia Kline |
| Phase 3.5 | 45,515 | 20 / none |

All import/reload compared domains match, original source IDs remain and the world resumes 120 physical minutes. Reported imported totals can include explicit migration annotations; donor hashes, annotation counts and exact field checks are in each report. The original voyage/namespace/format is not replaced by a remote save. Keeping the original browser origin or explicitly importing a complete backup remains necessary.

## Fresh accelerated campaigns against the extracted runtime

Hourly real-calendar intervals use the actual production and field controllers, fixed start 2026-10-28 UTC / America/Chicago. Per-step autosave is disabled only in the test driver; explicit checkpoint saves/reloads and complete source history exports are real. Synchronized holidays explain effective duration. These campaigns test simulation continuity, not 30 days of physical network/Windows uptime.

| Scenario / seed | Real / simulated days | Living / dead | Arrivals | Field missions | Science cases | Conversations | Sunday films | History rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Compound adverse / 4807 | 7 / 25 | 20 / 0 | 5 | 12 | 21 | 417 | 1 | 10,463 |
| Normal / 1001 | 30 / 111.75 | 20 / 0 | 5 | 8 | 24 | 2,032 | 4 | 45,514 |

The adverse fixture explicitly starts B07=10, C09=32, C07=45 and one crew member at health 55; resulting events are simulated. Research outcomes are 62 complete / 26 no-result / 3 failed (four confirmed conclusions) and 72 / 25 / 4 (three conclusions). Neither produces a Legendary segment. Surviving crew alone is not the acceptance check.

Resource/frontier/knowledge/creature/chronicle/cinematic/source audits report no errors. Actual travel, autonomous mission/research decisions and social events occur. Exact reloads pass at day 7 in both and day 30 in normal. No lost/duplicated crew, wall-clock rollback/discard or missing/private public sources. Full balances, recorded decisions and all 102 runtime hashes are retained. Five local jobs each; the acquisition statistic is empty, so no fresh extraction-diversity claim is made. Travel fuel is 1.9624515496596866 each. End snapshots are 4,014,121 / 9,922,484 bytes; compressed primary+fallback storage 1,363,274 / 2,878,004 bytes. Existing history growth remains a pre-release concern. Accelerated campaign execution took about 258 / 514 seconds in this shared three-CPU environment; this is not native FPS certification.

## Package/security and diagnostics

73 standalone JS/Python files and inline scripts pass syntax checks; 72 local script references resolve. Retained files match committed source/manifest hashes. Existing config, dependencies, batch launcher, TV allowlist and nine original host primitives are unchanged. All web/runtime dependencies and bridge_service.py/tv_service.py remain; tests/reports/development tools/private tokens/replacement APK are excluded from Lite. Review SECURITY_PHASE41.md for LAN HTTP, authorized desktop input, inherited TV certificate omission, local bootstrap and webbrowser launch behavior.

Confirmed implementation fixes and their reruns are documented in PHASE41_CHANGELOG.md. Old regression drivers explicitly enter Creator Mode for creator-only operations; physical/source assertions were not removed. A responsive-profile test now waits for the actual resize event before asserting orientation. An external harness initially retained an old extraction-directory name and correctly stopped before running tests; corrected independently of runtime. The workspace later ran out of disk space: ENOSPC blocked some browser launches and the 30-day campaign startup. Failed attempts are retained in environment_failure. Generated interim/superseded diagnostics were losslessly ZIP-archived, every original hash/CRC verified, and the blocked checks rerun successfully. No live user voyage or source was discarded and no antivirus protection was disabled.

## Acceptance boundaries

Automatic browser/server verification covers matching authoritative telemetry, single-host fencing, thin remote entry, correct command target/dedup/reload, disconnection continuity, save compatibility, movable/resizable/persistent layouts, scrolling/select/profile repairs, role separation, responsive emulation and observation privacy. Six real HTTP screenshots preserve actual test-world projections; they are neither physical-device photos nor invented footage.

**NOT RUN:** physical Windows installation/input, Samsung Tab S5e/Android/WebView/Wi-Fi, Samsung TV model/firmware, actual Tailscale routing, antivirus scanning, screen reader/native GPU/FPS and sustained human usability/content review. Native APK rebuild is **pending original Android Studio source recovery**, not permanently unsupported; the installed app is preserved. Consequently the physical Windows and device/human acceptance boxes remain open: this is a verified browser/server implementation, **not a declaration of full physical release readiness**. See PHASE41_DEVICE_TESTING.md and PHASE41_LIMITATIONS.md for exact remaining work, at-most-once/crash semantics, origin handling and UI/canvas refinements.
