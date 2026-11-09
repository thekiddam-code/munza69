# Verified v1.2 validation

Final acceptance uses two continuing campaigns from fresh initial state, without injected specimens, supplies or forced mission quotas. Each campaign saves/reloads at all five milestones. Older failed development runs are recorded separately in reports/development_failures.json.

| Seed | Days | Arrivals | Visited bodies | Frontier complete / failed | Samples | Science cases | Experiments | Crew alive | Logical save MB |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1001 | 7 | 7 | 8 | 7 / 0 | 6 | 30 | 87 | 20 | 1.059 |
| 1001 | 30 | 37 | 38 | 48 / 1 | 40 | 64 | 271 | 20 | 2.419 |
| 1001 | 90 | 120 | 121 | 169 / 9 | 134 | 158 | 652 | 20 | 4.435 |
| 1001 | 180 | 242 | 243 | 341 / 22 | 272 | 296 | 1217 | 20 | 6.185 |
| 1001 | 365 | 498 | 499 | 701 / 46 | 524 | 548 | 2255 | 20 | 9.502 |
| 2026 | 7 | 6 | 7 | 8 / 0 | 7 | 20 | 84 | 20 | 1.071 |
| 2026 | 30 | 36 | 37 | 51 / 1 | 39 | 52 | 215 | 20 | 2.795 |
| 2026 | 90 | 116 | 117 | 161 / 9 | 112 | 125 | 511 | 20 | 4.116 |
| 2026 | 180 | 231 | 232 | 333 / 31 | 227 | 240 | 991 | 20 | 5.646 |
| 2026 | 365 | 472 | 473 | 682 / 72 | 468 | 481 | 1979 | 20 | 9.168 |

All ten milestone reports pass. Across 730 daily checkpoints, the founding crew census, continuous clock, research/destination retention, active-job age and resource/domain audits pass. Every milestone reload has zero extended-snapshot differences. Final identity-graph checks find no duplicate journal/mission/destination IDs or orphaned frontier targets.

The automated suite passes 71 unit tests, 29 browser regressions and 3 paired-bridge tests. An additional real v1.1 same-origin save upgrade passes, as does normal file-UI import/save/reload/resumption of the packaged seed-2026 year-end voyage. All 26 Python/JavaScript syntax checks pass. The retained legacy seven-day runner also passes on this build.

| Seed / year end | Fuel used in travel | Fuel acquired | Ice acquired | Travel in final 30 days | Physical core slots MB |
| --- | --- | --- | --- | --- | --- |
| 1001 | 1881.348 | 1882.264 | 734.000 | 42 arrivals | 3.352 |
| 2026 | 1851.286 | 1827.285 | 714.000 | 39 arrivals | 3.221 |

Normal campaigns needed fuel salvage and ice replenishment; they did not need to manufacture ore/nutrient missions while initial reserves remained sufficient. Finite ore/nutrient extraction, capacity saturation and ice refining are covered by focused deterministic tests. Adverse browser scenarios cover fuel denial, drive failure, failed mining/cache retention, ship damage, clinical work, containment injury, interrupted research, complete team loss and weekly/in-flight continuity.

Seed 1001: mission types {"distress": 64, "extract_fuel": 121, "extract_waterIce": 27, "recovery": 2, "survey": 533}. Recorded frontier event kinds/counts: {"arrival": 498, "departure": 499, "environmental_damage": 4, "injury": 41, "medical": 2, "mission": 18, "mission_authorized": 747, "mission_completed": 701, "mission_failed": 46, "unexpected_contact": 4}.

Seed 2026: mission types {"distress": 63, "extract_fuel": 140, "extract_waterIce": 29, "recovery": 9, "survey": 513}. Recorded frontier event kinds/counts: {"arrival": 472, "departure": 473, "environmental_damage": 4, "injury": 41, "medical": 2, "mission": 64, "mission_authorized": 754, "mission_completed": 682, "mission_failed": 72, "unexpected_contact": 3}.

Resource equations and lifetime source-ledger aggregates reconcile at all milestones. See reports/resource_balances.csv, conservation_audit.json, research_outcomes.json and campaign_statistics.csv for exact quantities, differences, evidence outcomes and mission diversity. These checks establish normalized inventory consistency, not physical chemistry.

The observed year-end save growth fits the tested 16 MB logical / 8 MB physical-core budget. Legitimate retained destinations, missions and evidence still grow with exploration; unlimited-duration storage is not certified.

Not run: real Windows input devices, physical Android tablet, Samsung TV, Safari/Firefox or real LAN-disconnection testing. Bridge tests use the real HTTP handler and separate Chromium contexts with desktop input stubbed. See KNOWN_LIMITATIONS_v1.2.md for direct-leg navigation, two-person transport, abstract surfaces, cargo scope and recommended next batch.
