# ICARUS v1.2 — The Expanding Frontier

## Audit and milestones

The source baseline is completed v1.1 `e8c7069` (runtime `48d37c3`). AGENTS.md, CODEX_START_HERE.md, prior engineering documents, simulation initialization/reset paths, research/custody, crew work, expedition manifests, economy, weekly archive, backup/recovery, server bridge and both interfaces were inspected. An isolated v1.1 archive checkout passed 51 unit tests and its real seven-day browser baseline. Historical handoff text referencing v0.94.8 is retained as history, not treated as a replacement for the user's v1.2 assignment.

The audit found two fixed field locations, no ship travel or off-ship bulk acquisition, bounded recent economic history without a lifetime source ledger, and synchronous JSON saves nearing browser storage limits. Existing continuous clock, physical ship work, clinical treatment, two-person teams, custody/research and event-grounded recaps were retained.

Implementation milestones:

1. Deterministic sector generation and persistent contacts, with finite deposits and legacy origin orbit.
2. Metered navigation, observed frontier jobs, extraction/cache/refining, and nonmodal map.
3. Regression repairs, finite oxygen makeup, lifetime provenance aggregates, lossless save storage and paired tablet navigation.
4. Adverse/browser verification, continuing multi-seed campaigns, conservation/diversity reports and packaging.

Source commits are in Git history; generated results are packaged separately. The machine-readable validation summary in `reports/` controls the acceptance claim.

## Module boundaries

| Module | Responsibility |
| --- | --- |
| universe.js | Keyed seed/sector hash, persistent sensor catalogue, destination descriptors/deposits, daily hazards, deposit audit |
| navigation.js | Actual ship coordinates, route eligibility/cost/duration, incremental burn, drift and exactly-once arrival |
| logistics.js | Cargo capacity, reserve deficits, finite extraction, failed-operation caches, offload receipts, ice refining, reconciliation |
| frontier.js | Observed opportunities, shared team launch/staging/field/return, actual sampling/custody callbacks, weather and contact events |
| frontier-ui.js | Interactive full star map, contact intelligence, opportunities, navigation controls and provenance |
| tablet-frontier.js | Paired telemetry map and commands; no simulation engine |
| save-store.js | Transparent lossless encoding of the three existing core/recovery/checkpoint storage slots |
| vendor/lz-string.min.js | Local, pinned lz-string 1.5.0 codec, MIT license included |

Existing voyage/discovery/research/teams/economy/living/operations/story modules remain authoritative in their domains. `icarus.html` adapts these interfaces to established physical work, logs, research intake, captain controls and rendering. The large legacy HTML has not been rewritten. New simulation modules use explicit dependencies and do not make network calls. The existing bridge alone transports bounded PC telemetry and captain commands.

## Universe and navigation

The universe uses deterministic integer sectors in a two-dimensional abstract coordinate lattice. Sector/body identities derive from the universe seed and coordinates, independent of generation order. Bodies include planets, moons, asteroid fields, derelicts, anomalies and rare installations. Empty sectors, barren systems, cold/warm environments, dangerous contacts, low-interest sites and false sensor resource hints are possible. Descriptors exist conceptually before a mission: sensor scans reveal a fixed surrounding sector window, never fill a quota or respawn exhausted deposits.

Only discovered sectors are materialized in saves. Each body retains identity, position, temperature, hazard, composition, resource hints, initial/remaining/extracted deposits, survey transects, findings, caches and signal resolution. The original derelict and asteroid retain their original maps/missions and share HOME staging. Autonomous departure waits for their existing finite survey objectives. Captains may depart earlier once any team has returned.

One route leg stores origin coordinate, target coordinate, duration, elapsed time, fuel budget and actual burn. Routes require known contacts, working propulsion, sufficient power, no outstanding expedition and finite fuel. Distance costs five fuel units per coordinate unit; duration is at least 90 minutes or distance × 800 minutes. Fuel burns per minute. Arrival increments once for that leg and records the destination. Midcourse overrides start at the current coordinate; consumed fuel is never refunded. Damage/fuel exhaustion causes drift at the actual position. Repair can permit a fresh remaining route. Hold means hold at current orbit or after a current leg; it does not freeze the clock or teleport the ship.

SOL ranks observed contacts by interest, unresolved telemetry, distance, hazard and projected feedstock deficits. Low-fuel navigation filters for fuel evidence, retaining a reserve. Local reserve acquisition takes precedence over spending more travel fuel. Poor intelligence, exhausted deposits and compound failures can still strand a voyage; there is no guarantee of survival or generated rescue fuel. The map and decision field expose the measured status/reason. Captain course/hold/release/recall remains optional.

## Mission and evidence lifecycle

New frontier operations share existing transport, two-person team selection, six suits, paid food/water/oxygen/energy cargo and physical staging. Roles, fit availability, health, fatigue, morale, skills and relationships influence team eligibility, cohesion, decisions and work rate. Expedition members retain actual field condition and recovery records. Faulty equipment, short cargo, injuries and adverse environmental rolls can cause safety return, failed objectives, injury and recoverable caches.

Opportunities come from unsurveyed observed contacts, unresolved distress carriers, recorded abandoned cargo, and actual reserve deficits at known deposits. They carry objectives, reasons, requirements, risk, finite duration and outcome records. Survey completion exhausts three distinct transects; resolved beacons do not recur. Failed operations have at most two attempts of each kind per destination. Resource missions may recur only while a real reserve deficit and finite material remain. Existing onboard maintenance and emergency systems remain responsible for damaged hardware and ship threats.

Survey specimens use the existing deterministic Discovery path and custody intake, not test injections. Actual returned evidence enters hypotheses, paid experiments, replication and uncertain conclusions. Distress operations recover modeled beacon telemetry cartridges: they do not invent rescued people. Remote contacts are newly resolved pre-existing sectors. Daily weather can damage actual power-distribution hardware; rare consequences are probabilistic. Events flow through the existing journal and source-linked Sunday recap. There is no new combat or fabricated cinematic footage; existing extraordinary documented lethal-event eligibility is preserved.

## Resource provenance and conservation

Quantities are normalized gameplay units. Dry bulk capacity includes ore, fuel, nutrients, water ice and currently held raw expedition cargo. Habitable stores, installed equipment and compact scientific samples are separate; this is not a full ship mass/volume model.

Extraction atomically removes finite material from a destination and places it in a held cargo lot. Successful return credits that exact lot once and records destination/mission receipts. Failed return leaves a finite cache; total team loss records actual loss. Recovery transfers cache contents and cannot create another copy. Ice conversion consumes real ice and energy with working fabrication hardware. Oxygen makeup consumes water and energy through working life-support/fabrication equipment: one normalized water mass yields .88 oxygen with .12 hydrogen explicitly vented. Existing recycling, galley/fabricator inputs, solar energy and reactor fuel remain finite/source-backed.

The recent 200-entry ledger view is supplemented with persistent aggregate rows by kind/resource/source, storing amount, count and first/last tick. Transfers, metabolic recovery, conversion inputs/outputs and losses remain auditable after the recent view rolls over. Individual frontier job/receipt sources identify material provenance. Legacy saves retain prior cumulative totals; source aggregates begin at upgrade and cannot reconstruct previously unrecorded historic transactions. Recent offload view is bounded to 300 receipts; cumulative extraction/credit/loss totals remain.

Audits enforce separately:

- stock: initial + production + imports − consumption − loss = actual stores/buffers/cargo;
- feedstock: initial + imports/recovery − used = inventory;
- destination: initial deposit = remaining + extracted;
- extraction: extracted = credited + lost + held + cached;
- six suits = stored + loaned + lost, with no negative compartments;
- held plus stored dry bulk remains within capacity.

These are normalized inventory equations, not a chemical/thermodynamic proof. Different resource conversions use documented gameplay ratios. An explicit injected initial condition in an adverse test is not reported as natural acquisition.

## Persistence, determinism and regression repairs

The v1.1 monotonic clock and weekly archive-only transitions remain. New state domains initialize only when absent; old research, crew, fields, equipment, incidents and in-flight legacy manifests are retained. Universe/navigation/logistics/frontier objects travel through the existing save/import/recovery paths. Active frontier work and ship travel are never reset on Sunday. The retained latest four full episode presentations and older compact factual summaries preserve world data separately from presentation history.

Large core JSON is losslessly encoded physically in browser storage; application readers and portable exports still receive ordinary JSON. Small/raw legacy saves remain readable. Compression affects only the three ICARUS core slots, not paired-device tokens/preferences. Corruption exercises the existing verified recovery snapshot. LZ source/license is local; no runtime package or network dependency was introduced. Older application binaries cannot read compressed physical slots; export a JSON backup before downgrading.

Long campaign debugging exposed and fixed: perpetual morale decay despite rest/health; mismatched meal activity labels that prevented satiation; low-fuel curiosity travel; departing while a local fuel job awaited staffing; early expedition return lacking the readiness dictionary; oxygen attrition that eventually prohibited launches; uncompressed browser quota failure; and naive cumulative energy rounding at days 328/330. Economic/source cumulative amounts now use persisted compensated sums, verified by one million micro-flow cycles across a JSON reload; the original strict audit tolerance is unchanged. Morale now responds to actual rest, nutrition, stress, health and relationships. Meal relief requires paid food and working galley activity. No morale reset, generated resources or scripted survival exemption was added.

Fixed seed plus controlled actions is deterministic. Browser/UI wall time and archive metadata are not a universal cross-browser replay guarantee. Campaigns execute normal minute steps in accelerated batches, without quota missions, forced supplies or synthetic specimens.

## Validation and reproduction

```
node --test test_*.js
python test_frontier_integration.py --report frontier_integration.json
python test_frontier_bridge.py --output bridge_results.json
python frontier_soak.py --seed 1001 --output campaign_1001
python frontier_soak.py --seed 2026 --output campaign_2026
python test_v11_upgrade.py --baseline /path/to/v1.1/ICARUS --report v11_upgrade.json
python verify_frontier_backup.py /path/to/voyage_seed_2026.json --report backup_roundtrip.json
python summarize_frontier_reports.py /path/to/assembled/reports
```

Use Playwright plus Chromium; `ICARUS_CHROMIUM=/usr/bin/chromium` was used for these runs. A same-origin upgrade test also loads a save produced by the actual v1.1 engine, compares every legacy domain before stepping, then advances, saves and reloads v1.2. The bridge tests stub desktop input and exercise the real local HTTP handler and two independent browser contexts. No real keyboard/mouse/TV action is invoked.

The packaged year-end portable save is additionally imported through the normal file UI in a fresh browser, compared by domain, saved/reloaded and resumed for two hours. Final identity-graph audits check duplicate journal/mission/destination IDs and orphaned mission targets. Campaign reports at 7/30/90/180/365 are milestones of one continuing voyage per seed, including exact extended snapshot equality after each reload. Daily checks cover monotonic time, founding-identity census including deaths, retained destinations/research/jobs, condition bounds, inventories, suits, cargo, active-job ages and domain audits. Acceptance additionally requires actual travel, multiple destinations, acquired material, and travel in the final thirty days. This catches a stable idle world that a simple uptime test would pass. Storage sizes, mission types, fuel/receipts, discoveries, experiments and actual event diversity are recorded. Save growth is measured and budgeted, not assumed bounded for an infinite voyage.

See `reports/validation_summary.json`, `reports/campaign_statistics.csv`, `reports/resource_balances.csv` and `reports/conservation_audit.json` for final measured results. Failed development runs and the corrections they motivated are documented separately; they are not acceptance passes.

## Packaged acceptance result

All ten multi-seed milestones pass on the corrected simulation. Final arrivals are 498 / 472, frontier jobs 747 / 754, and both voyages continue actual travel in their final thirty days. All resource equations and cumulative source-ledger checks reconcile. VALIDATION_v1.2.md provides the measured table and scope; reports retain exact data, failed development diagnostics and year-end portable saves. Physical device and non-Chromium testing remains explicitly unverified.
