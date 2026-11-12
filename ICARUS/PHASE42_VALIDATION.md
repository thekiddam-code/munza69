# Phase 4.2 executed validation

**Automated integrated build verified; physical/human final-release sign-off remains open.** Frozen tested runtime: `6707616a454d8aa6dd36923e1d2bfa3378bf3502`. All 106 runtime files were tested in an independent Lite ZIP extraction. Final documentation packaging uses a later source commit but must retain these exact 106 hashes; release_verification.json records that comparison.

## Final package tests

| Execution | Result |
|---|---:|
| Node deterministic unit/regression cases | 311 passed, 0 failed/skipped |
| Full Living Ship/legacy/knowledge/calendar browser suite | 55 passed |
| Authoritative host/UMBRA/command bridge browser+HTTP suite | 31 passed |
| Ordinary production clock, without soak hooks | 2 passed |
| Bridge and TV service unit cases | 15 passed |
| Phone touch/mobile functional checks | 15 passed |
| Tablet landscape/touch functional checks | 11 passed |

414 case executions plus 26 separate functional emulation checks. Inherited cases repeat across suites; this is not a count of unique requirements. Linux Chromium and Node v24.22.1; physical desktop/game input and television transport are stubbed in protocol tests. A prior 2dc5266 candidate also passed 71 cinematic/reliability browser executions; that is development evidence, not included in the final totals above.

The final 55-case suite includes full genuine Phase 4.1 backup import, legacy migrations, private social memory, optional private preferences without invented events, 100-registered/20-active continuity, performed cleanup, uncertain claim publication/correction, medical/containment/fire/sealed-route adverse cases, real Monday transitions, writer protection and exact reload. Original crew/routines, source history, resources and navigation survive. No live user save was accessed.

## Actual accelerated campaigns

| Seed/scenario | Real days | Ship days | Alive / dead | Arrivals | Conversations | Paid repairs / inspections | Help requests | Sunday films |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| compound_4807 | 7 | 25.0 | 20 / 0 | 5 | 420 | 198 / 92 | 14 | 1 |
| normal_1001 | 30 | 111.75 | 20 / 0 | 5 | 1924 | 869 / 409 | 34 | 4 |

Both campaigns have **zero simulation errors and zero independent source/resource/knowledge/creature/chronicle/activity audit errors**. Actual travel, work, social interaction, research and operational recovery occurred; survival alone is not the acceptance test. All original 20 identities remain accounted for. Normal checkpoints at real days 7/14/21/28/30 and adverse day 7 reload exactly. Clock is the unchanged 4× normal / synchronized 1× holiday implementation, real Monday–Sunday episodes; Halloween and later holidays explain the non-4× totals. The separately reported 20× issue is untouched.

Adverse seed 4807 starts with an explicitly labeled injury and damaged surveillance, life support and distribution—not a claimed natural opening event. It recorded two native equipment faults, two emergency completions, two critical recoveries, one critical escalation and three released assignments. Normal recorded one critical escalation/recovery and twelve released assignments. Final research cases: adverse 21, normal 22. No guaranteed Lazarus breakthrough was added.

The source audit checks retained full-history sources for private leakage into SOL, public chronicles or film highlights/awards; interaction and social memories retain valid history/experience sources. Both final runs had zero retained hearsay claims and no consent/romance or cleanup source events; these branches were exercised using explicit deterministic unit/browser fixtures, not fabricated campaign outcomes. No extraordinary lethal encounter was required or manufactured.

The driver disables per-step autosave, while exercising real controllers and explicit durable checkpoints. This is accelerated validation, not a claim of 30 days of physical-device observation or every production save cycle.

## Scale, growth and provenance

A synthetic 100-registered/20-active personnel fixture persists across real Monday and exact reload; dormant profiles gain no active body, knowledge inbox or scheduler. The separate component benchmark runs 10,000 physical-minute updates per sample with 20 and 100 registered profiles (20 active in both); it audits bounded histories and identical save continuation. It is not a full-voyage or GPU/FPS benchmark.

- 20 registered / 20 active: 302.05 ms for 10,000 component updates; 21,987 UTF-8 serialized bytes.
- 100 registered / 20 active: 215.47 ms for 10,000 component updates; 32,916 UTF-8 serialized bytes.
- 20 registered / 20 active: 222.00 ms for 10,000 component updates; 21,987 UTF-8 serialized bytes.
- 100 registered / 20 active: 200.31 ms for 10,000 component updates; 32,916 UTF-8 serialized bytes.

Measured retained recent-list bounds: social memories ≤32/person, activity history ≤16/person, existing conversation memories ≤24/person; registry ≤128. Historical source facts/archives deliberately remain persistent. The normal run ended with 38,128 history rows, 640 retained social memories, 378 directed bonds and 320 retained activity-history entries. Snapshot JSON grew from 2,041,781 to 14,117,422 characters; adverse from 2,035,663 to 5,076,362. The legacy metric is named snapshot_bytes but records JavaScript string length, not UTF-8 byte size. Growth includes legitimate retained world/history data; this is not proof of infinite-duration storage stability.

Static review verified all 106 extracted hashes, 92 runtime files byte-identical to Phase 4.1, ten intentional changed files and four new modules. Calendar/rate/pause handlers, host lease, pairing/server, UMBRA, workspace, durable storage, Knowledge authority and film/evidence capture remain unchanged. New modules add no network/process execution, package installation or system-security modifications. Existing launcher dependency installation, paired desktop input and TV network behavior remain documented in SECURITY_PHASE41.md. No antivirus was disabled.

## Regressions repaired and unavailable checks

Fixed during development: strong relationships truncated to ±20; disabled actors showing stale work/talk; instantaneous cleanup overwriting meaningful work; repair completion losing activity provenance; legacy innerHTML replacing editor handlers; and claim correction failing when an independent existing channel delivered the original. Failed development reports and corrected reruns are retained separately. Wrong harness paths/navigation and a missing test PYTHONPATH were corrected without changing product behavior. A cleanup fixture was isolated from other legitimate cleaners and distinguishes an observation from its delivered publication.

**Not run:** physical Windows, Android/Tab S5e, native APK rebuild (original Android Studio source still pending recovery), physical Samsung TV, real Wi-Fi/Tailscale, antivirus certification, human accessibility/usability and native GPU/FPS. No 365-real-day Phase 4.2 campaign or 100-active-actor test. Existing installed Android capability is retained; native work is not permanently unsupported. See PHASE42_LIMITATIONS.md and PHASE42_ACCEPTANCE.md.

Machine-readable evidence and source hashes: repository ICARUS/reports/phase42/accepted and the separate verification ZIP. Tests/reports/development tools are intentionally excluded from the Lite runtime.

## Reproduce from source

Run `node --test test_*.js` from ICARUS. Browser tests require Python Playwright/Chromium; set ICARUS_CHROMIUM if using an existing executable. Run `python -m unittest test_living_ship_integration.LivingShipIntegration -v`. Supply ICARUS_PHASE41_BACKUP to the complete historical donor if not using the original validation workspace; report that case unavailable if no genuine donor exists. The source suites retain historical fixture/report-path conventions; the executed external harnesses are included in evidence.

For the actual extracted Lite use the recorded run_suite.py adapter with ICARUS_LITE_ROOT. Accelerated campaigns use unified_soak.py with ICARUS_RUNTIME_ROOT pointing to the extraction, seed 1001/normal/30 days and seed 4807/compound/7 days. `summarize_phase42.py` independently audits full-history outputs; `verify_phase42.py` verifies hashes and the preserved Phase 4.1 boundary; `collect_phase42.py` refuses missing/failed required evidence. See the retained executed commands/harnesses for environment paths. Follow README_PHASE42.md and PHASE41_DEVICE_TESTING.md for installation, backup, migration, rollback and physical checks.
