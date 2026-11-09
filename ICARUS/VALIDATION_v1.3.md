# ICARUS v1.3 measured validation

## Baseline and automated checks

Baseline: v1.2 commit 55aff16794a797d5fd34fce63c072948e6eebb48; 71 unit cases and its real-browser seven-day voyage passed before implementation. Final source identity and runtime hashes are in reports/validation_summary.json and BUILD_MANIFEST.json.

Final verification passed 91 deterministic unit cases, 44 real Chromium integration cases, three authenticated bridge cases, genuine archived-v1.2 upgrade, the legacy seven-day runner, four explicit 14-day adverse campaigns, and year-end backup import/reload/resumption. A supplemental unavailable-database export check passed. JavaScript, inline HTML scripts and Python syntax passed. No tests in these suites were skipped. Individual machine-readable reports contain the actual assertions and errors.

## Continuing voyages

Each seed continued through all milestones in one world, saving/reloading with exact world equality at each milestone. Daily audits covered 730 combined daily checkpoints. No survival supplies, contacts, discoveries or rescues were injected into these normal campaigns.

| Seed | Days | Arrivals | Frontier jobs | Science cases | Memories | Survivors | Logical snapshot MB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1001 | 7 | 6 | 7 | 29 | 14 | 20 | 1.30 |
| 1001 | 30 | 34 | 48 | 60 | 133 | 20 | 3.51 |
| 1001 | 90 | 111 | 168 | 132 | 427 | 20 | 7.41 |
| 1001 | 180 | 219 | 347 | 231 | 899 | 20 | 12.10 |
| 1001 | 365 | 443 | 725 | 446 | 1890 | 20 | 22.39 |
| 2026 | 7 | 6 | 8 | 20 | 19 | 20 | 1.27 |
| 2026 | 30 | 34 | 48 | 54 | 122 | 20 | 3.69 |
| 2026 | 90 | 107 | 157 | 124 | 398 | 20 | 7.26 |
| 2026 | 180 | 213 | 343 | 229 | 938 | 20 | 12.21 |
| 2026 | 365 | 444 | 706 | 445 | 1921 | 20 | 22.09 |

At year end seed 1001 had 658 completed / 67 failed frontier jobs; seed 2026 had 642 completed / 63 failed / one active. Failures persisted without unlimited repeated attempts. All twenty founders remained accounted for. Injuries, fatigue, low morale and incomplete healing occurred; survival is not guaranteed for every seed.

## Observed living activity

| Year-end measure | Seed 1001 | Seed 2026 |
| --- | ---: | ---: |
| Persistent entities | 135 | 146 |
| Trades / refusals / misunderstandings | 23 / 8 / 8 | 21 / 11 / 9 |
| Cooperations | 4 | 1 |
| Stranding incidents | 9 | 12 |
| Field repairs | 4 | 2 |
| EVA attempts / successful interventions | 4 / 4 | 11 / 10 |
| External rescue assistance | 1 | 0 |
| Completed stage records | 1666 | 1632 |
| Teams of 2 / 3 / 4 | 454 / 247 / 24 | 422 / 263 / 21 |
| Personal memories | 1890 | 1921 |
| Indexed history rows | 219358 | 219693 |
| IndexedDB bytes | 125104128 | 125173760 |
| Year-end reload seconds | 24.61 | 60.66 |

Both voyages encountered all modeled actor types, including four unidentified contacts each. Normal routes did not revisit destinations; natural repeated-contact activity is not claimed. Persistence, reputation and repeat-interaction restrictions are also directly tested. Rare encounters were not guaranteed. One natural EVA attempt failed. No cinematic footage was invented or lethal sequence forced.

## Conservation, science and source integrity

All milestone inventory balances and source-ledger aggregates agree. Ship stock, feedstock, loans, cargo, finite deposits and bilateral actor transfers are separately audited. Year-end actor stock equals initial plus received minus spent. No unexplained creation, negative inventory, duplicate mission IDs, missing destination references, orphan assignments or missing recap sources were found. See conservation_audit.json, resource_balances.csv and living_frontier_audit.json for quantities and provenance.

Seed 1001 consumed 1723.55 travel fuel, extracted 1465.47 and ended with 83.05; seed 2026 consumed 1717.55, extracted 1508.55 and ended with 96.01. Extraction totals exclude bilateral trade, which is separately recorded in the complete source ledger. Science reached 446 / 445 cases. Seed 1001 recorded 1333 complete, 399 inconclusive/no-result and 89 failed experiments; both full distributions, programs and unresolved Lazarus questions are in research_outcomes.json. Experiment completion does not automatically mean confirmed science or Lazarus success.

Memory sources, staged objectives, incident outcomes, weekly source IDs and recap card text were checked against actual stored source records. Stories are reconstructions of those records, not fabricated footage.

## Adverse conditions and recovery

Explicit 14-day variants cover zero initial fuel, dense contacts, zero contacts and captain-held position. Focused tests additionally cover failed repair, rescue range/availability, full-team loss/unavailable pod, interrupted rescue/travel/research/treatment at a weekly boundary, containment injury, ship damage, exhausted reserves, cargo saturation, extinction and recovery caches. Fixture injections are labeled and do not count as natural voyage evidence.

Durable tests abort writes, corrupt the newest snapshot, create orphan uncommitted revisions, remove cache, preserve historical future events after rollback, and reject incomplete modern imports before replacing the world. Complete off-device export works during write failure; unavailable storage warns and retains pending history. The accepted seed-2026 year-end backup imported with no mismatched domains in 22.81 s, reloaded in 34.84 s, preserved all historical IDs and resumed from minute 525600 to 525720. The verifier's per-operation limit is explicitly 120 seconds.

## Failed runs and coverage boundaries

The first distance-integrated seed 1001 lost a field team, then collapsed by day 200. Its actual history exposed a ship repair assignment given to an off-ship engineer. Assignment reconciliation, physical-presence checks, responder rotation and critical-ship launch restraint fixed the defect with direct regression coverage. failure_investigation.json retains the evidence; this run remains a failure. Later 30-second large-save reload timeouts also remain failures. Hydration and validation transport were optimized; fresh campaigns passed bounded 120-second reload checks. Interrupted exploratory runs are not acceptance results.

The accepted voyages used repaired physics and storage. Subsequent boundary hardening (modern import validation, unrecovered-pod guard, unknown-contact display and backup-failure export) received unit/browser/migration/backup checks; both full years were not rerun for those boundary changes. Neither accepted voyage lost its primary pod. Final runtime hashes identify the packaged source explicitly.

Year-end logical snapshots were 22.39 / 22.09 MB, below the 64 MB budget; IndexedDB was about 125 MB, below 512 MB. Significant history grows with activity; storage is not unlimited and large saves load slowly. No physical Windows/Android/TV, Firefox/Safari, real LAN-interruption or hostile multi-tab certification was run. Detailed model limits and the next recommended batch are in KNOWN_LIMITATIONS_v1.3.md.
