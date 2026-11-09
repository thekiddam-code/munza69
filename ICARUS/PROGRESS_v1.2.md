# v1.2 progress

Base: v1.1 e8c7069. Branch codex/v1.2-expanding-frontier.

Implemented: deterministic sector/destination model; sensor discovery; navigation, per-tick fuel burn and captain commands; finite extraction/refining, provenance and cargo reconciliation; observed frontier operations using existing two-person manifests, research and events; nonmodal interactive stellar map. Legacy sites remain in HOME orbit.

Tests: baseline v1.1 and new unit tests passed. Initial integrated seven-day run passed. Full multi-seed campaign validation and adverse/browser tests are pending. Do not claim final acceptance from the development run alone.

Next steps: execute milestone-report campaign runner at 7/30/90/180/365 days for multiple seeds; repair any state, storage, resource or operational failures; finalize documentation and downloadable package. Intermediate reports live in work/v12_reports in the shared execution workspace.

Regression milestone: 70 unit tests, 29 real-browser continuity/adverse tests and 3 real paired-bridge tests pass. Added lifetime provenance and finite oxygen makeup after development campaigns exposed day-180 oxygen attrition. Two fresh continuous campaigns (seeds 1001, 2026) have passed day 90; final 180/365 milestones remain pending. Simulation physics frozen at this milestone; subsequent presentation-only changes do not change stepping. Final acceptance must use work/v12_reports/acceptance, not earlier diagnostic campaigns.

Precision milestone: previous acceptance candidates reached days 328/330 with continuous travel, then strict audit caught ~1.0e-6 accumulated energy rounding error. Cumulative economic/source amounts now use persisted compensated sums; the threshold is unchanged. Added one-million-cycle regression with a mid-run JSON reload. 71 unit tests pass. Fresh final campaigns are in work/v12_reports/final; do not use prior 180-day passes to claim year acceptance.

Final acceptance verified: final fresh campaigns for seeds 1001 and 2026 each completed 365 days and passed all 7/30/90/180/365 milestones, daily audits, exact milestone reloads, final source/identity audits and continued final-month travel. Year-end arrivals: 498 / 472; frontier jobs: 747 / 754. The seed-2026 portable year-end backup passes normal file-UI import, exact domain comparison, save/reload and 120-minute resumption. 71 unit, 29 browser and 3 bridge cases pass; real v1.1 upgrade, retained legacy seven-day runner and 26 syntax checks also pass. See VALIDATION_v1.2.md and packaged reports. Earlier pending/failed entries above are the engineering history, not unresolved final results.
