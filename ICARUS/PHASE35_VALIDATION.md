# Phase 3.5 measured validation

Status: substantial working increment verified within the explicit limits below. **Full Phase 3.5/final audiovisual production is not declared complete.** See PHASE35_LIMITATIONS.md and FINAL_RELEASE_ROADMAP.md.

Runtime tested from **9da612e810ea6706c3f1fa829bdf5b5d4e92a228** through an independently extracted source-based Lite ZIP, with **63 runtime files**. Final packaging may update documentation; runtime hashes must stay identical. All accepted campaign runtime hashes match this independent extraction exactly. Final packaging may update documentation only; runtime identity is checked again before publishing.

## Final extracted Lite automated results

| Suite | Actual result |
| --- | --- |
| Node deterministic cases | 257 passed, 0 failed, 0 skipped |
| cinematic Chromium suite | 70 passed |
| stability Chromium suite | 30 passed |
| compatibility Chromium suite | 44 passed |
| production Chromium suite | 2 passed |
| bridge Chromium suite | 3 passed |
| Pixel 5 touch/mobile flow | 15 checks passed; actual HTTP, stubbed host input/TV |
| Static/dependency/manifest | 55 syntax files; 53 local script dependencies; all retained hashes verified |

Browser suites overlap inherited cases; counts are executions, not distinct scenarios. Tests run outside Lite against extracted assets. Positive extraordinary-lethal tests use explicitly authored fixtures, not claimed natural campaign clips.

## Real backup migration

| Backup | History records in receiving browser | Tick resumed | Result |
| --- | --- | --- | --- |
| migrate_phase1 | 10659 | 36000 → 36120 | Original compared domains, full history IDs and exact reload preserved |
| migrate_phase2 | 50170 | 160920 → 161040 | Original compared domains, full history IDs and exact reload preserved |
| migrate_phase3 | 48137 | 160920 → 161040 | Original compared domains, full history IDs and exact reload preserved |
| migrate_phase3_loss | 45870 | 160920 → 161040 | Original compared domains, full history IDs and exact reload preserved |
| migrate_phase35 | 45515 | 160920 → 161040 | Original compared domains, full history IDs and exact reload preserved |

Legacy Phase 1/2/3 and new Phase 3.5 complete backups preserve the compared original domains, all supplied history IDs and exact reload/resume. The verified new empty source-frame field is the only allowed cinema migration difference for old saves. Save-only v1.3 imports preserve available records and explicitly label incomplete older archives; Core/Extended isolation is retained. Initial two-minute harness timeouts and the reproduced late-cancel failure are retained as diagnostics, excluded from accepted results.

## Continuous campaigns

Fixed start 2026-10-28 00:00 UTC, America/Chicago. Production physical/calendar controllers process hourly real intervals; test-driver per-step autosave is disabled, actual saves/checkpoint reloads asserted. Thirty real days equal 111.75 simulated days due to synchronized 1× holidays; seven equal 25.0. Adverse initial states use asserted normal backup-import fixtures, not natural-event claims.

| Profile | Real / simulated days | Alive / dead | Arrivals | Field / local jobs | Conversations | Films / awards |
| --- | --- | --- | --- | --- | --- | --- |
| chamber_4807 | 7 / 25.0 | 20 / 0 | 5 | 12 / 5 | 385 | 1 / 3 |
| compound_1001 | 7 / 25.0 | 20 / 0 | 5 | 9 / 6 | 402 | 1 / 3 |
| normal_1001 | 30 / 111.75 | 20 / 0 | 5 | 8 / 5 | 2032 | 4 / 3 |
| normal_4807 | 30 / 111.75 | 20 / 0 | 5 | 8 / 5 | 2097 | 4 / 3 |

Daily resource/frontier/chronicle/knowledge/creature/cinematic audits pass, all original crew identities remain accounted for, wall time is not discarded/rewound and checkpoint reloads match. Independent full-history audits find no private/missing public film/SOL sources or invalid snapshot provenance. Real travel/objectives are required; survival alone is insufficient.

Deaths and their actual causes, if any, are listed in campaign_summary.json. Survival is not manufactured or treated as the sole acceptance gate. Legendary positive-path tests use retained raw-evidence fixtures; ordinary deaths, insufficient samples and missing imagery are excluded.

## Sources, science, resources and growth

- **chamber_4807:** 10558 full history records; 27 science cases; experiment statuses {"complete": 81, "failed": 5, "no_result": 26}; 2004 actual captured state frames, 120 retained; 3 sourced recorded film segments, 0 Legendary segments. Film durations: [268] seconds. Primary compressed cache: 365334 → 695624 bytes. Travel fuel: 1.9624515496596866.
- **compound_1001:** 10230 full history records; 17 science cases; experiment statuses {"complete": 55, "failed": 5, "no_result": 10}; 1972 actual captured state frames, 120 retained; 3 sourced recorded film segments, 0 Legendary segments. Film durations: [268] seconds. Primary compressed cache: 366638 → 670108 bytes. Travel fuel: 1.9624515496596866.
- **normal_1001:** 45514 full history records; 24 science cases; experiment statuses {"complete": 72, "failed": 4, "no_result": 25}; 8587 actual captured state frames, 120 retained; 3 sourced recorded film segments, 0 Legendary segments. Film durations: [268, 208, 218, 218] seconds. Primary compressed cache: 350360 → 1454184 bytes. Travel fuel: 1.9624515496596866.
- **normal_4807:** 46211 full history records; 20 science cases; experiment statuses {"complete": 63, "failed": 3, "no_result": 17}; 8378 actual captured state frames, 120 retained; 3 sourced recorded film segments, 0 Legendary segments. Film durations: [268, 228, 218, 238] seconds. Primary compressed cache: 349120 → 1497290 bytes. Travel fuel: 1.9624515496596866.

## Editorial and streamed-history evidence

The baseline ordinary runs repeated the same unchanged HR follow-up 300/301 times. New actual counts: chamber_4807 16, compound_1001 9, normal_1001 81, normal_4807 95. This measures recurrence, not human literary quality. Actual excerpts/source IDs and top repeated text are retained for human review.

Actual streamed roundtrip: 45515 history records, 22306975 bytes; cursor export 32.73 seconds, staged NDJSON import 110.49 seconds. The history getAll method was forbidden; real OPFS writable-file APIs and exact source/world/reload equality were checked. Native OS chooser behavior was not claimed. API cancellation, corrupt/truncated chunks, transaction abort, writer collisions/fencing, LAN lease fallback, late cancellation and future-schema protection are exercised separately by the refinement suite.


Complete resource balances/acquisition, source-kind diversity, repeated social text counts, checkpoints, fatality causal windows and runtime/backup SHA-256 values are in reports/phase35/campaign_summary.json and accepted_summary.json. Resource audits retain finite production/conversion/consumption/transfer identities; Phase 3.5 adds no free-resource source. Sparse frames mean reconstruction cards are common. Short quiet archives are intentional, not filled with invented scenes.

## Performance and unavailable gates

1000 paused synchronous camera refreshes: mean 0.606 ms, p95 1.200 ms, max 40.900 ms. Actor rebuild counter 2 → 2; world snapshot unchanged. Heap samples and Linux campaign RSS series are retained separately. Timings under concurrent headless load are not native GPU/compositor FPS or a proof of no multi-year leak.

Linux campaign process-tree RSS peaks (MiB): normal_4807 1523.8, normal_1001 1400.5, compound_1001 1154.8, chamber_4807 1056.0. This includes Python harness, browser and shared pages counted more than once; it is not retained game JS heap or Android thin-client memory. Full timestamp samples are retained.


Source frames 24, routine memories 24/person, choices 12/person, snapshots 120, SOL notes 48 and films 12 weeks are bounded; full history/knowledge still grow. Live-state growth, legacy-format memory use and wider platform/human review remain open.

Not run: Native Windows BAT/input; Physical Android/Wi-Fi and Galaxy Tab S5e/Samsung TV; Firefox/Safari; Antivirus engine/penetration testing; Human long-form story quality, final art/audio and accessibility review. No antivirus bypass or native-hardware certification is implied.

Superseded diagnostic failures/campaigns are identified in engineering notes and excluded from accepted totals. Procedural motion, optional source-backed awards, conservative automatic lethal classification, staged streaming transfers and single-writer protection are implemented and tested. Native hardware/antivirus and sustained human cinematic review remain blocked by unavailable facilities. No final-release or full-phase completion is declared. Next batch: execute native/human gates, review story examples and retained-heap performance, and improve live-state/legacy JSON scaling before additional scope.
