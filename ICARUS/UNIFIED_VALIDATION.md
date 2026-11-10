# Unified World Phase 1 — actual validation

**Verified implemented scope: True. Complete uploaded specification: false. Final release ready: false.**

Campaign runtime: `ada3da90cca08823216a478a72702afba633e372`. Baseline: v1.4.1 `a363799`. All delivered web files are checked against the tested runtime hashes. Tests do not certify the unfinished design areas listed in UNIFIED_LIMITATIONS.md.

## Automated results

| Suite | Result |
| --- | --- |
| unit | 158/158 passed; 0 failed; 0 skipped |
| unified_browser_frozen.json | 27 passed |
| stability_browser.json | 30 passed |
| compatibility.json | 44 passed |
| adverse.json | Passed |
| bridge.json | 3 passed |
| production_clock.json | 2 passed |
| syntax.json | Passed |
| backup_roundtrip.json | Passed |

The 27 unified browser cases include inherited core checks plus the new calendar/spatial/lore cases. The 30 stability and 44 compatibility cases overlap in inherited behavior; these counts are not independent new tests. Two ordinary-page production timer cases run without soak hooks and verify actual 4× and holiday 1×, legacy-speed refusal and pause/resume. The real-Monday adverse test preserves a live expedition, experiment, medical treatment and fire across both boundary and reload.

Unit coverage includes all nine synchronized dates, eight recognized 4× observances, Gregorian Easter, Christmas 24/25 continuity, actual rather than federal observed dates, fractional accumulation, 23/25-hour DST, full 25-hour holiday, unique holiday IDs across reload/timezone changes, bounded backlog, rollback, overlapping presentation flags and personal observances without global slowdown. Spatial tests check room/corridor/field distinction and physical accessibility. World tests check initial concealed adult/eggs, creator/public separation, source validation, ownership, finite local power, host incubation/development, android ineligibility and memorial retention.

## Real-calendar campaigns

These are two separate campaigns of **30 elapsed real-time days**, advanced in explicit hourly wall-clock intervals from 2026-10-28 00:00 UTC, configured for America/Chicago. They are accelerated test replays, not claims that the application was left running for thirty actual days. Per-step autosave is suppressed only in deterministic test pumping; daily and milestone saves are explicit. Production timer behavior is separately exercised.

The interval includes full Halloween and Veterans Day and eighteen local hours of Thanksgiving. Its correct physical advancement is `(720 - 66) × 4 + 66 = 2682` game hours: **160920 minutes / 111.75 simulated days**. Monday transitions occur four times. There is no holiday event quota or generated crew history before initialization.

| Seed | Real days | Sim days | Living / dead | Episodes | Stories | History records | Preventive completed | Military rooms visited | Remaining wreck battery |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- | ---: |
| 1001 | 30 | 111.75 | 20 / 0 | 5 | 331 | 48048 | 735 | [23, 22, 21, 24] | 15 |
| 2026 | 30 | 111.75 | 20 / 0 | 5 | 333 | 48338 | 728 | [23, 22, 21, 24] | 15 |

Both day-7 checkpoints reach 25 simulated days. Day-7 and day-30 checkpoints save and reload the exact full snapshot, including calendar, biological state, personal objects and existing world groups. Daily crew census, inventory, navigation, chronicle and suspension audits pass. Both crews physically explore the existing military region and consume five units from its twenty-unit finite local battery. The initial adult and eggs remain dormant in these two campaigns: no release or host exposure was forced to demonstrate danger. Host development is verified through explicitly synthetic unit scenarios, not falsely reported as a natural campaign event.

The source audit checks every anthology transition and Sunday card against the recorded source text, validates acquired lore and object-transfer sources, prohibits unexplained new adults, and checks the current runtime hashes. It reports no errors. Campaigns preserve positive, humorous, mysterious, ordinary and dangerous categories; actual distributions and policy decisions are in reports/validation_summary.json and the full saved snapshots/history.

## Adverse recovery and complete backup

The four inherited nine-day adverse scenarios are explicit fixtures: funded blackout (20 survive), unfunded sealed life support (0 survive), injured engineers (20 survive), and unsafe fire/pressure access (0 survive). Exact installed inventory/hardware and save/reload are verified. They retain genuine fatal outcomes; new biology and calendar work does not introduce artificial survival guarantees. These use fixed physical steps and supplement the new real-calendar boundary test.

A real 30-day campaign file is imported through the normal backup UI. It retains all checked world domains, including calendar and unified state, and 48049 indexed history records. It reloads exactly and resumes from tick 160920 to 161040. Measured import: 2.04 seconds; reload: 4.49 seconds.

## Development failures and scope limits

Earlier attempts are kept in the report folder and clearly named. The initial calendar test hook inherited the paused soak flag; that test path was corrected. A corridor renderer removed its own actor container and failed reloads; the renderer now preserves the container. An accessibility fixture tried to modify an uninitialized navSystem; the verified fixture initializes the system and demonstrates actual route refusal. A first military integration was replaced by actual asteroid-region references after the deeper map audit found existing wreck rooms. None of these failed or superseded attempts is counted as final acceptance.

The complete specification remains incomplete. Full creature AI/ecology, natural character/body/prop animation, verified astronomical lunar dates, authored individual cultural content and automatic religious calendar conversion, radio-delivery/individual-knowledge consolidation, complete prop physics and cross-environment geometry consolidation remain open. Paused UI state is inherited session behavior rather than persisted captain state. See UNIFIED_ARCHITECTURE.md and UNIFIED_LIMITATIONS.md.

Physical Windows/Android/TV, Firefox/Safari, actual desktop-input devices, hostile concurrent tabs, real network interruptions and sustained human content/usability review could not be run here. No new 365-day campaign is claimed. The earlier v1.4.1 year reports are historical evidence only; this build’s actual long campaigns are the durations above.

Recommended next batch: complete the existing foundations and their visual/knowledge/creature limitations, then widen adversarial/device/human testing. Keep the bounded four-environment anthology and source-grounded chronicles; do not add unrelated galaxy or economy scope.
