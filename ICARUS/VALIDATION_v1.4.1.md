# ICARUS v1.4.1 — measured validation

Runtime tested: `2152b53fc03cddc78e9e6673485f376e7398b9f1`. Baseline: `602b4a2`. Targeted stabilization acceptance verified: **True**. Final-release readiness remains **false**; depth, interface, hardware and human-play review still have open roadmap gates.

## Reproduction and causal recovery

The original seed-1001 profile reloads at days 30 and 90. All twenty death names, ticks and causes match the published v1.4 report (498840–499170 elapsed minutes, life-support resource shortage). The uninterrupted same-seed baseline survives; seed, initial world and external checkpoint profile must be specified together. This is documented rather than concealed as a failed reproduction.

An unchanged day-339 world is then imported into both versions, with exact initial crew/inventory checks and SHA `b87ee10fa58f1153e6c7f0217f8c169f482bc07cf89a9b6d941442eac62aa690`. After twelve days: old mechanics **0 survivors**, final repaired mechanics **20 survivors**. Real paid work: `{"criticalEscalations": 1, "criticalRecoveries": 1, "emergencyCompleted": 1, "emergencyWork": 100, "hatchWork": 200.00000000000014, "hatchesCleared": 2, "maintenanceWork": 5952.000000000358, "preventiveCompleted": 82, "preventiveStarted": 90, "releasedAssignments": 10}`.

The jam/dispatch deadlock is a confirmed defect and poor response policy; wear, hazardous access, finite production dependencies, resource depletion and permanent deaths remain intended consequences. ROOT_CAUSE_v1.4.1.md contains the physical state and causal timeline.

## Automated checks

| Check | Actual result |
| --- | --- |
| unit | 117/117 passed; 0 failed; 0 skipped |
| stability_integration.json | 30 passed |
| compatibility.json | 44 passed |
| bridge.json | 3 passed |
| backup_roundtrip.json | Passed: full file import, exact reload, source history, resumed simulation |
| syntax.json | Passed: 31 JavaScript files, 4 inline script blocks, 26 Python AST checks |

The 30-case core suite includes 19 inherited core cases; the 44 compatibility cases include Extended Universe test-lane and older continuity coverage. These are overlapping behavior suites, not a claim of 74 independent new regressions. Original baseline unit suite: 101/101. Four focused queue cases fail against untouched v1.4 and pass the corrections. No skipped unit cases are accepted.

## Continuous campaigns

Three separate year-long campaigns use seeds 1001, 2026 and 7331 at normal anthology frequency. The table contains cumulative observations from each campaign at actual day-30/90/180/365 milestones, not twelve independent restarts. Every milestone saves and reloads; every day audits the continuous clock, crew census, inventory, destinations, mission IDs and chronicle sources.

| Seed | Days | Living / dead | Native faults / completed repairs | Preventive assigned / completed | Dispatches | Hatch clearances | Low-reserve day-end samples | Arrivals | Stories |
| ---: | ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1001 | 30 | 20 / 0 | 0 / 0 | 211 / 193 | 0 | 0 | 0 | 5 | 104 |
| 1001 | 90 | 20 / 0 | 0 / 0 | 641 / 581 | 0 | 0 | 0 | 5 | 270 |
| 1001 | 180 | 20 / 0 | 0 / 0 | 1315 / 1174 | 0 | 0 | 0 | 5 | 511 |
| 1001 | 365 | 20 / 0 | 0 / 0 | 2757 / 2419 | 0 | 0 | 0 | 8 | 1018 |
| 2026 | 30 | 20 / 0 | 0 / 0 | 218 / 195 | 0 | 0 | 0 | 5 | 109 |
| 2026 | 90 | 20 / 0 | 0 / 0 | 666 / 591 | 0 | 0 | 0 | 5 | 268 |
| 2026 | 180 | 20 / 0 | 0 / 0 | 1329 / 1176 | 0 | 0 | 0 | 5 | 502 |
| 2026 | 365 | 20 / 0 | 0 / 0 | 2741 / 2399 | 0 | 0 | 0 | 8 | 981 |
| 7331 | 30 | 20 / 0 | 0 / 0 | 201 / 192 | 0 | 0 | 0 | 5 | 105 |
| 7331 | 90 | 20 / 0 | 0 / 0 | 623 / 581 | 0 | 0 | 0 | 5 | 264 |
| 7331 | 180 | 20 / 0 | 0 / 0 | 1304 / 1167 | 0 | 0 | 0 | 5 | 500 |
| 7331 | 365 | 20 / 0 | 0 / 0 | 2718 / 2394 | 0 | 0 | 0 | 8 | 981 |

Low-reserve samples mean any day-end food <10, water <5, oxygen <5 or energy <10; this is not a count of every minute of shortage. The full daily rows, source histories, policy counters, forecasts and major decision examples remain in reports. Native fault/dispatch/work metrics do not silently include expedition injury or containment incidents. Avoid summing cumulative milestone counts.

## Year-end activity and persistence

| Seed | Living / dead | Field completed / failed | Frontier ore / fuel credited | Fuel burned in travel | Min crew health | Snapshot MB | Reload seconds |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: |
| 1001 | 20 / 0 | 155 / 6 | 196.330 / 0.000 | 3.469 | 95.00 | 13.71 | 43.81 |
| 2026 | 20 / 0 | 88 / 6 | 116.286 / 0.000 | 3.469 | 93.82 | 13.32 | 28.72 |
| 7331 | 20 / 0 | 98 / 7 | 125.633 / 0.000 | 3.469 | 95.00 | 13.44 | 36.18 |

Fuel use here is ship travel only; reactor consumption and all feedstock totals are separately accounted in resource_balances.csv. Frontier credits are external field returns; feedstockImported additionally includes existing process-scrap recycling and legacy bulk recovery, so it must not be presented as fresh mining. Resource-conservation checks reconcile each aggregated source/consumption/loss against the actual inventory and acquisition ledger (tolerance 1e-5). Paid repairs do not create resources. Complete source histories permit inspection of individual decisions.

The core remains two bounded context records with six known ship/local venues; there is no procedural planetary growth. Exhausted-objective route selection has focused regression tests; navigation_review.json contains actual trips, fuel, attempt failures and final explanations. A hold after finite objectives is a coherent outcome.

## Adverse scenarios

These are explicitly installed starting worlds, never represented as naturally occurring encounters. Every fixture verifies the exact installed inventory/hardware before advancing nine days, crosses a week and verifies exact save/reload.

| Scenario | Living / dead | Outcome checks |
| --- | --- | --- |
| funded_black_start | 20 / 0 | passed |
| unfunded_sealed_life_support | 0 / 20 | passed |
| injured_repair_crew | 20 / 0 | passed |
| unsafe_pressure_and_jam | 0 / 20 | passed |

The funded blackout must complete actual distribution work and recover hardware. Inaccessible sealed life support without tools/parts must not be automatically rescued. Unsafe fire/pressure access is retained. Death/memorial, medical assignment, interrupted activity and captain seal continuity are covered by both scenario reloads and targeted regressions.

## Anthology, crew and research preservation

| Seed | External encounters / categories | Shared-moment outcomes | Personal memory records | Science cases | Experiment status counts |
| ---: | --- | ---: | ---: | ---: | --- |
| 1001 | 416 / 9 | 102 | 1827 | 19 | {'complete': 64, 'no_result': 13, 'failed': 3} |
| 2026 | 378 / 9 | 95 | 1611 | 29 | {'complete': 82, 'no_result': 31, 'failed': 4} |
| 7331 | 378 / 9 | 86 | 1632 | 19 | {'no_result': 10, 'complete': 65, 'failed': 5} |

The source audit compares every story transition and Sunday card to its actual recorded text, checks weekly/arc source IDs and memory provenance, and reconciles persistent actor inventories. Research questions, experimental failures/inconclusive results, conclusions and the actual Lazarus program state are retained in science_lazarus.json. No discoveries, footage or deaths are added for presentation. Legendary lethal selection retains its existing documented-evidence predicates. Automated variety counts do not prove engaging prose or believable characters; human review remains necessary.

## Errors, superseded attempts and interpretation

Final audit errors: `[]`. Review cautions: `[]`.

Development attempts are preserved in development_attempts.json. An early introduced reservation-release bug canceled boarding and failed the 30-day meaningful-activity check; it was fixed with a regression. Later completed diagnostic years exposed wasteful travel between exhausted objectives despite mechanical passes; these were rejected as final acceptance and rerun after correction. An initial adverse setup was overwritten by pagehide persistence, so that fixture was invalidated, corrected and verified before rerunning. These are not silently relabeled passes.

## Limits and next batch

Linux Chromium, real IndexedDB, desktop/tablet viewport checks and loopback bridge command validation were run. Physical Windows/Android/TV, Firefox/Safari, real network interruptions, hostile concurrent-tab writers and sustained human content/usability review could not be run in this environment. No requested simulation duration is claimed unless its artifact is present.

Three seeds and selected adverse combinations do not establish universal survival or exhaustive failure coverage. Long runs can still fail coherently; existing deaths remain permanent on upgrade. Large JSON backups/history consume memory and storage; forecast horizons use measured recent rates rather than predicting random future faults. See KNOWN_LIMITATIONS_v1.4.1.md.

Next: review these real stories and operational explanations for specificity/repetition, widen compound-failure and seed coverage, test physical target devices, improve existing navigation/accessibility and large-save handling. Preserve anthology depth and core/Extended Universe separation; no new galaxy/economy scope is recommended.
