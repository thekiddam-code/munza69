# ICARUS v1.1 — The Continuous Voyage

## Audit and implementation milestones

Base: v1.0 commit b97e31a. Read AGENTS.md, CODEX_START_HERE.md, the v1.0 engineering/limitations documents, clock and reset paths, field/custody/research lifecycle, crew survival and treatment, supply workstations and the existing browser runner. A separate git-archive checkout of v1.0 passed its 33 unit tests and seven-day baseline simulation.

The audit identified the v1.0 weekly world reinitialization, its 480-minute deadline offset, greedy field routing, scarce natural recoveries, single-person transport, and replenishment without a production chain. Changes were made as integrated milestones and committed separately:

1. Continuous clock, one-time legacy timer migration and archive-only boundaries.
2. Seeded field observations, independent spectral support and revisable conclusions.
3. Two-person manifests, physical staging, equipment/cargo budgets, field condition and buddy-return decisions.
4. Finite stores, source-backed production/recovery, rationing, clinical hardware maintenance and conservation audits.
5. Deterministic regression, adverse browser scenarios and 7/30/90-day acceptance runs.

See reports/validation_summary.json for the final source commit, actual results and acceptance status. Intermediate reports do not establish final acceptance. One final validation process was interrupted by an environment reconnection; the complete ninety-day run was restarted.

## Architecture and boundaries

The established HTML remains the UI and integration adapter for existing ship physics, relationships, psychology, navigation, incidents and captain controls. Eight local CommonJS/browser modules now have these responsibilities:

| Module | Responsibility |
| --- | --- |
| voyage.js | Monotonic elapsed clock, versioned legacy timer migration, archive-only weekly boundaries |
| discovery.js | Once-per-cell seeded observations, nearest-unvisited routing, independent support and conclusion revision |
| research.js | Hypotheses, finite paid experiments, scientist assignment, uncertainty, disagreements and longitudinal Lazarus evidence |
| teams.js | Fit complementary teams, suits/cargo, staging, condition records, disagreement, emergency return and debrief |
| economy.js | Stores, finite conversion inputs, production dependencies, consumption, recycling, priority modes and audits |
| living.js | Seeded entropy, vitals, injuries, treatment, death, grief and crew availability |
| operations.js | Existing dispatch assessment, maintenance ranking and supply transfer policy |
| story.js | Bounded event journal, character highlights, source-linked recaps and optional factual endings |

No new module makes network calls or executes commands. Server.py and physical device controls are unchanged. NIGHTGRID layout, ship/field displays, SOL identity and explain/recall/abort/command/release controls remain.

## Continuous world and save migration

New saves store clock.version=1, elapsed simulation minutes and the next presentation boundary. state.tick is elapsed time, state.minute is 480 + elapsed, and directorClock reads elapsed. Neither resets at an automatic boundary. The first archive retains the historical midnight boundary at minute 10080; subsequent episodes are exactly 10080 minutes apart.

Rollover appends a recap/archive, increments episode and moves the next boundary. It never reconstructs state or reassigns crew. Equipment condition, ship atmosphere/damage, reserves, production, incidents, maintenance routes, clinical progress, relationships, research assignments, expedition cargo and field maps remain the same live objects.

Legacy saves use (episode-1)*9600 + minute-480 to recover explicitly advanced minutes. A one-time migration preserves the remaining time/age of director reservations, launches, research deadlines, ship timers, notices and navigation cooldowns. Historical text timestamps remain historical. Existing mission progress, analyst identity, costs, clinical counters and evidence are retained. Legacy single-person expeditions finish as imported manifests; new launches use teams. The existing version-2 save key and backup format remain.

The explicit full-scenario reset is now labeled New Voyage. It requires its existing confirmation, saves a fresh campaign, and reloads through normal initialization. This is distinct from a weekly episode archive. Downgrading to older application binaries is not supported for the new world clock; keep an exported old-version backup.

## Natural evidence and scientific work

Each newly surveyed field cell has one persisted sampling opportunity. Probability depends on location, depth/cell, carried sensor kits and previous recoveries; its seeded roll and outcome are stored. Successful observations create physical specimens with source location, cell, mission, time, measured-condition metadata and modeled material properties. There is no retry timer to manufacture new finds in exhausted cells. Preset legacy objects remain available alongside the new samples.

A nearest-unvisited route can cross visited junctions, preventing the old greedy exploration loop. Recovered specimens enter existing transfer, custody, quarantine and classification paths. Preliminary metadata classifications remain tentative. Composition assays/replications record actual model measurements; contamination can create mixed spectra. Contradictory readings revise hypotheses and can contest previously supported conclusions. Confirmed composition-family conclusions require matching measurements from at least two distinct physical source cells. They do not establish alien origin, function or safe revival.

Experiments debit real laboratory stores, require a fit scientist physically present in a lab, reserve their work time and release/reassign that work when interrupted. The shared slot prevents parallel phantom work. Failed/inconclusive runs retain costs. Prolonged blocks terminate safely; reassignment never pays again. Confirmed comparisons can prioritize a survey of genuinely unexplored sectors, but cannot create an endless follow-up loop.

Lazarus advances from evidence collection to replication requirements and, with independent positive activity measurements, independent_activity_supported. Identity continuity and safe reconstruction remain unknown. No guaranteed breakthrough or crew resurrection is introduced. Existing separately authorized specimen reconstruction remains experimental.

## Expedition teams and intervention

New launches select two complementary fit crew based on role/objective, health, fatigue, morale, experience, relationships and existing readiness reservations. The last available medical/engineering specialist is retained aboard. There is one shared transport and six reusable suits. A manifest must have suits, food, water, oxygen and preparation energy before launch; denial is atomic.

Both people physically route to shuttle/collar staging. The manifest then shares a field route while retaining each person's condition. Cohesion and experience affect work rate; field accident checks and safety withdrawals use real conditions. Relationship tension can record a disagreement and slow work. Injury, exhaustion or inadequate carried supplies causes a documented buddy return. Casualties persist, affect the debrief, and can fail a mission. Complete team loss disposes carried supplies and records lost suits; it does not silently refund them.

Captain recall during staging cancels the operation without teleporting personnel. In-flight intervention retains existing return semantics. Return transactions are idempotent, unused cargo is transferred back, suits are reconciled, all surviving members receive condition/debrief and recovery records. Legacy one-person operations can complete without re-launching or changing their progress.

## Resource economy

Resource quantities are normalized gameplay units, not a thermodynamic or clinical chemistry model. Food/lab/tools/parts include existing workstation buffers and cargo reserves. Water, oxygen and energy have explicit stores; medical stock is the existing sterile cartridge inventory. Carried expedition cargo is part of the same total inventory.

| Output | Source and dependency |
| --- | --- |
| Energy | Rate-limited incident starlight through distribution hardware; backup reactor conversion debits finite fuel |
| Water | Powered reclamation of recorded metabolic/clinical wastewater through life support |
| Oxygen | Powered regeneration from recorded metabolic CO2 through life support |
| Food | Galley conversion of organic waste or carried nutrients, with energy cost |
| Parts/tools/lab materials | Fabricator/lab conversion of finite mineral feedstock, with energy cost |
| Sterile cartridges | Nutrients, water and sterilization energy through functioning lab/fabrication hardware |

Ordinary workstations, experiments, clinical cycles, life support and expedition preparation/consumption debit actual stock. Recoverable process scrap returns 98% mineral feedstock; meals/clinical waste and metabolic output have explicit recovery sources. Finite natural bulk recoveries are credited once per recovered parcel. Water ice is catalogued reserve material; this batch's water replenishment uses reclamation rather than an ice-processing plant.

SOL changes between normal, rationing and survival modes based on measured availability. Food rationing reduces allocations/satiation, severe deficits injure crew, and survival priorities suspend optional launches/research. Wear and hardware condition constrain production. The clinical tissue unit is connected to the existing engineer maintenance/workstation system, so it can be repaired with actual crew work and parts rather than receiving a weekly reset.

The audit enforces initial + produced + imports - consumed - losses = actual inventory for every resource, with 1e-6 tolerance. It also reconciles feedstock, every physical compartment (including cargo), and six suits across stored/loaned/lost gear. Transfers and scenario reloads are not production. Buffers are production targets; existing legacy stock above a target is preserved rather than discarded.

## Tests and reproducibility

```
node --test test_*.js
python test_continuity.py --report adverse_report.json
python soak_test.py --days 7 --seed 1001 --report soak_7day.json
python soak_test.py --days 30 --seed 1001 --report soak_30day.json
python soak_test.py --days 90 --seed 1001 --report soak_90day.json
```

Install Playwright and Chromium for development tests. ICARUS_CHROMIUM can point to an existing browser; /usr/bin/chromium was used here. Browser runs use fresh contexts and never modify a user's existing save. Adverse fixtures are explicitly artificial; natural acceptance runs use no specimen injections.

Unit tests cover clock migration/idempotency, no-reset object continuity, field probability/provenance, independent/contradictory evidence, inventory conservation, source scarcity, rationing, team selection and gear/cargo return. Real-browser scenarios cover equal-seed execution, future equivalence after reload, legacy migration, a boundary during simultaneous mission/experiment/treatment/emergency, real resource deprivation, containment exposure/injury, interrupted work, complete expedition loss, staging cancellation, total crew loss and explicit New Voyage behavior.

Each long run checks daily identity census, vitals, monotonic time, retained science/history, mission age, member uniqueness, every resource balance, bounded records and late-voyage mission growth. Final save/reload compares the extended world snapshot exactly. Reports include actual discovery/experiment statistics, team outcomes, daily stores/feedstocks, production/consumption, SOL decisions, state size and bounds. Seeded simulation is reproducible under controlled actions; archive wall-clock metadata and arbitrary live UI timing are not a cross-browser replay guarantee.

## Verified results for the packaged build

51 unit tests and 19 adverse/integration browser tests passed. Syntax checks passed. All acceptance simulations used seed 1001 with no specimen injection.

| Days | Weekly archives | Natural specimens | Experiments: complete / inconclusive / failed | Confirmed families | Team missions | Surviving crew | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 7 | 1 | 13 | 39 / 14 / 3 | 3 | 8 | 20 | PASS |
| 30 | 4 | 13 | 39 / 14 / 3 | 3 | 8 | 20 | PASS |
| 90 | 12 | 13 | 39 / 14 / 3 | 3 | 8 | 20 | PASS |

The ninety-day run completed 129,600 explicit simulation minutes, ended in episode 13, retained 4000 bounded journal records and had a 1,941,722-byte extended snapshot. All daily/final conservation audits passed, all 20 founding identities were accounted for, no missions remained stuck, and the final seven days added no missions. Final save/reload had no mismatched fields. Crew health ended at 100 in this normal scenario; injuries, deprivation, containment exposure and casualties were verified separately in the adverse suite.

The normal scenario does not certify compound-failure survival or every seed. Detailed actual initial/produced/consumed/lost/final resource quantities are in reports/resource_balances.csv, and measured discovery/outcome statistics are in reports/discovery_statistics.csv.
