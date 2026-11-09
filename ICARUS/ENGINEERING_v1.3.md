# ICARUS v1.3 — The Living Frontier

## Audit and implementation history

Base: verified v1.2 source 55aff16794a797d5fd34fce63c072948e6eebb48. Read AGENTS.md, CODEX_START_HERE.md, v1.2 engineering/validation/limitations, initialization and weekly transitions, field/custody/research, team and gear lifecycle, economy ledgers, browser save/import/recovery, local bridge and both interfaces. Historical v0.94 prompts remain historical; the current user assignment is the eight-phase v1.3 batch.

The baseline passed 71 unit tests and its seven-day real-browser simulation. An isolated git-archive checkout was retained for a genuine v1.2 save-upgrade test. The audit found a useful separation between world clock, voyage, fields, crew and science, but fixed two-person teams, scalar field work, no non-crew registry or independent rescue lifecycle, a 4000-entry hot event window, and compressed localStorage as the primary store.

Milestones in Git history:

1. Persistent contacts/organizations, staged variable teams, individual experiences, local rescue, transactional snapshots and source-linked chronicle cards.
2. Rescue/resource regression repairs, cache-versus-commit protocol, full indexed mission/memory/contact history, fork-safe future event IDs, real local distance and objective loadouts.
3. Full regression/adverse verification, actual v1.2 migration, continuing multi-seed campaigns and packaged backup resumption.
4. Measured reports, limitations, architecture and release package.

Candidate campaigns interrupted for integration/source freezes are diagnostic, not acceptance. The first extended browser pass found asynchronous startup assumptions and old cache-precedence assertions; tests now wait for readiness and require the newer verified IndexedDB revision. Later fixtures caught borrowed field resources, repeated rescue allocation, responder return after team loss, and collapsed playback panels. No conservation threshold was relaxed. A pre-repair natural seed exposed a native off-ship emergency dispatch and exhausted-responder deadlock; actual history and the failed run are retained. Presence/fitness reconciliation and critical-ship hold/recall were added, then the same seeds rerun. Large-history tests also exposed the 30-second harness deadline and object-transport memory overhead. Startup now validates only as many snapshots as needed, avoids redundant mirror writes and keeps plain JSON in IndexedDB. The harness uses a declared 120-second bound, plain JSON transport, read-only daily metrics checked against full snapshots, and recoverable milestone artifacts; actual timings are reported.

## Architecture

| Module | Responsibility |
| --- | --- |
| entities.js | Seeded persistent actors/organizations, finite inventories, encounter/reputation history, communication/refusal/misunderstanding/trade/cooperation |
| expeditions.js | Objective-dependent loadouts, two-to-four-person profile, field stages, actual local range, kit wear and accumulated exposure |
| emergency-ops.js | Persistent field incidents, shelter, carried-kit repair, capability-gated EVA rescue, deadlines, withdrawal, failed intervention and independent responder return |
| experiences.js | Actual-event personal memory, bounded confidence/caution, relationship changes and SOL willingness assessments |
| world-schema.js | Nonmutating legacy-compatible structural checks; incomplete modern histories and invalid inventories are rejected before replacement |
| durable-store.js | Versioned IndexedDB snapshots/transaction head, checksum verification, compatible compressed cache, indexed significant history, recovery and quota warnings |
| chronicles.js | Weekly event-source index, reconstructed event cards and stricter documented extraordinary encounter eligibility |
| living-frontier-ui.js | Nonmodal registry, emergency controls, personal history, chronicle playback and durable save status |
| Existing modules | Navigation, finite deposits/logistics, scientific custody/uncertainty/Lazarus, physical ship work, crew survival, maintenance and weekly continuous clock remain authoritative |

The HTML is the integration adapter and established NIGHTGRID/Remote Deck interface. It waits for durable hydration before initializing the engine. Independent layout scripts can load while storage opens. This avoids reconstructing or overwriting a world before its authoritative save is available. New modules remain local; no simulated agent executes commands or makes network requests. The existing authenticated bridge transports bounded telemetry/captain commands only.

## Persistent entities and exchange

Contacts are descriptors keyed by the universe seed and destination identity. A destination can expose a derelict hull record, station, trader, prospector, independent research ship, stranded traveler or uncertain contact. Four small organizations carry distinct goals/attitude biases. Materialization occurs at an actually visited orbit, without quotas. The registry has a hard ceiling of 256 actors; leaving a location does not delete an actor.

Each actor retains location, crew identities, finite starting cargo, received/spent totals, condition, organization, goal/activity, rapport, reputation and encounter IDs. Off-screen provisions are consumed, and depleted actors conserve resources. Derelict histories are damaged registry fragments; abandonment cause remains explicitly unverified. Unidentified contacts remain uncertain.

Local communications need a real orbit and functioning ship power. Attempt IDs prevent replaying a conversation/payment every tick. A refusal or protocol mismatch transfers no cargo. Reputation and rapport persist; later encounters can use that state. SOL exchanges actual deficits only when the other inventory, affordability, cargo room and reserve policy permit it. Fuel costs mineral feedstock, with bilateral debits/credits. Cooperative patch stock has an actual finite source. NPC EVA assistance requires a capable local known actor with crew and expendable patching stock; no interstellar rescue is asserted.

Independent actors are orbital residents, not a separately navigated fleet. This complete local encounter loop is intentionally smaller than faction economics, combat or full NPC interior simulation.

## Advanced expeditions

New frontier jobs choose two, three or four fit complementary people according to objective and measured hazard. Existing/legacy active manifests retain their original form. Health, fatigue, stress, experience, role, relationships and memory-based willingness influence suitability. Staging crew are reserved; field/rescue personnel are unavailable to ship work and science. The last available medical/engineering specialist is retained through the existing team policy.

Objective-specific kits are transferred from real aboard inventory into expedition cargo: tools/repair parts, survey assay allocations, or a clinical allocation. Loaned supplies count toward conservation but are unavailable to another launch/rescue. Unused material returns to its real store, including clinical cartridges. Field assays consume actual lab allocation even when no specimen is found. Kit wear influences work rate. Damage can destroy carried repair material.

New plans progress through assessment, objective work and securing the return. Jobs preserve stage thresholds and completed stage/time history, debrief conditions, equipment/exposure and full/partial/withdrawn outcome. Seeded destination landing range controls pod flight duration; legacy bodies without that property use a 25-unit range. The pod speed is .5 normalized range units/minute. EVA responders travel at .6 units/minute and cannot service ranges over 40. These are abstract local distances, not orbital mechanics. A primary pod left with a fully lost field team is marked unrecovered and blocks free replacement launches; retrieval/replacement is outside this batch.

Environment and actual elapsed exposure influence harm; existing accident/supply/safety checks remain. Scientific specimens still use the existing field probability, source-cell identity, custody and paid uncertain research system. A completed transect never guarantees a finding. Partial withdrawal does not create full-objective success or replay an exhausted sample parcel.

## Emergency response

Measured seeded transport/EVA faults create one persistent incident per affected mission. A stranded team shelters at its actual location and continues consuming carried food, water and oxygen. With a fit field engineer and a real carried repair allocation, repair takes 90 work minutes and consumes those parts. Without it, SOL evaluates an aboard fit engineer, spare suit, preparation energy, ship condition/survival reserve, repair tools/parts, provisions, range and target locality.

A rescue is a separate manifest with physical staging, outbound travel, timed repair and return. At most one responder mission may exist; at most two EVA attempts are allowed per incident. A paid repair can fail and withdraw. A responder returns even if the original team has died. A staging cancellation refunds unused carried provisions/gear without moving the person through blocked access. Clinical helpers and already reserved crews cannot be allocated to EVA simultaneously. Patching, clinical triage, lost cargo and lost suits all use the same finite resource accounting. Carried clinical aid buys a limited health improvement; it cannot assert survival.

Insufficient capabilities or communications do not teleport a crew home. Resource exhaustion/deadline exposure can kill real crew through the existing injury/death system. Deaths retain memorials, grief and mission consequences. Existing onboard hull, atmosphere, power, clinical and resource emergencies remain in their original physical-response systems; the new registry specializes in field rescue rather than replacing them.

Captain controls request assessment/rescue or shelter and retain normal recall. Recall cannot repair a stranded transport. No guaranteed success, rescue-fuel spawn or mandatory incident schedule is introduced.

## Individual memory and medical consequences

Each experience has a stable memory ID, actual source event/mission/incident, person, time, peers and individual confidence change. A seen-key prevents duplicate reactions on reload. Reactions differ with the person's state; established names, role and personality are retained. Shared success, failure and rescue alter the participating relationships, rather than applying identical global morale changes.

Confidence/caution affect willingness, selection ranking and required readiness. SOL assessments cite the count of recorded experiences. Existing stress, morale, nutrition, fatigue and relationship systems continue. Significant injuries can receive a deterministic individual recovery rate and lasting health ceiling; treatment needs actual staff, safe conditions, power and clinical supply. Reaching a personal ceiling completes treatment without repeatedly consuming cartridges. Outcomes remain limited by actual capability and conditions, not a promised cure.

## Durable persistence and migration

The new IndexedDB database is `icarus-voyage`, schema version 1. Stores:

- `saves`: three rolling versioned complete envelopes, plain JSON payload, checksum, revision and world tick (old encoded envelopes remain readable);
- `meta`: the authoritative committed transaction head;
- `history`: significant source events and full mission/memory/contact records, with actor, episode and mission indexes.

Snapshot and head advance in one read/write transaction. Interrupted transactions cannot publish a partial head. Startup selects a complete, checksum-valid envelope no newer than the committed head. Corrupt latest payloads fall back to a prior verified revision; orphan records without a committed head are rejected. Checksums detect accidental corruption; they are not cryptographic authentication.

The compressed v1.2 core/recovery keys remain a compatible cache/fallback. Metadata distinguishes a committed mirror from a queued uncommitted mirror, so an interrupted write cannot be mistaken for an intentional cache edit. Local quota failure leaves IndexedDB authoritative with a visible warning. A missing cache can be rebuilt from the database. If IndexedDB is unavailable, fallback is explicit and warned; it does not masquerade as a verified durable commit.

The engine initializes only after hydration. App-generated v1.3 backups require all modern history groups; a partial modern structure is rejected before replacement, while legacy states with those domains wholly absent remain migratable. New Voyage creates a complete fresh schema before its first commit. Large snapshots are validated newest-first until a usable committed record is found; identical cache payloads are not recompressed on hydration. Full history transport in validation uses JSON strings rather than expanding every nested object through the browser protocol. Old v1.2 fields are preserved; missing domains/crew careers initialize separately. Available old journal records migrate into history; records already pruned by v1.2 cannot be invented or reconstructed. Continuous clock, research, expeditions, navigation, inventory, crew and incidents remain independent of weekly presentation.

High-volume recent UI telemetry stays bounded. Important source, personal, mission and encounter history is retained in indexed storage and full backups. History batches commit separately; an acknowledged commit waits for snapshot and history queues. Existing actor/mission histories are collected at snapshots as well as the journal's streaming archive. Queries support actor, mission and episode rather than scanning only the UI window.

Future journal IDs include a stable namespace while existing IDs remain unchanged. Automatic rollback recovery reserves a distinct namespace for the next actual event without changing the recovered snapshot itself. Restoring an older backup gives subsequent events a distinct rollback namespace, preserving old indexed source records instead of silently overwriting them. Portable backups contain an immutable world snapshot plus indexed historical records. Import restores both, performs migration, and commits the result. Backup export merges readable indexed and pending history even after a failed write. Integrity metadata distinguishes durable commit from complete historical coverage, and partial rescue exports are labeled. Browser-origin deletion still removes local databases; export is necessary for off-device durability.

## Sunday chronicles and interface

Weekly cards select recorded research, mission, encounter, emergency, medical, death and relationship events. Each card retains its source ID, people, time and reconstruction label. Unresolved incidents become factual cliffhanger references. Existing anthology options, memorials and Sunday recaps remain. Playback can pause/skip and runs independently of simulation pause; expanding or using a card does not require an operational decision.

No camera footage is manufactured. Extraordinary lethal selection requires a real incident recording reference, existing causal event IDs, lethal/encounter/extraordinary flags and measured danger, disadvantage, ingenuity and rarity. Environmental deaths alone do not qualify. There is no new kill generator or guaranteed weekly lethal segment.

The PC view exposes actors, encounters/reputation, stages/assignments, incident assessment/controls, crew memory/conditions, chronicle cards and durable save/backup controls. The paired tablet remains a thin telemetry/controller view: recent contacts/memories, emergency buttons, save status and the existing navigation. It does not run another world. New commands use the existing host-key/paired-token boundary and a restricted command grammar.

## Reproduction and evidence

```
node --test test_*.js
python test_living_frontier_integration.py --report living_integration.json
python test_frontier_bridge.py --output bridge_results.json
python test_v12_upgrade.py --baseline /path/to/v1.2/ICARUS --report v12_upgrade.json
python living_adverse_soak.py --report adverse_campaigns.json
python living_soak.py --seed 1001 --output reports
python living_soak.py --seed 2026 --output reports
python verify_frontier_backup.py reports/voyage_seed_2026.json --report backup_roundtrip.json
```

Playwright and Chromium are required for browser checks. Linux Chromium at `/usr/bin/chromium` is used through `ICARUS_CHROMIUM`. Tests use isolated browser contexts and never touch the user's browser profile. Physical input is stubbed in bridge tests; only simulation HTTP paths are exercised.

Long campaigns are continuous per seed, with milestones at 7/30/90/180/365 and exact snapshot equality after each reload. Daily checks use lightweight read-only metrics with the same full domain audits; all milestone comparisons still use complete extended snapshots. Daily checks cover clock, founding-identity census, resources/suits/cargo, actor inventories, mission/incident age, stored destinations/research, memory and recap sources. New-system activity is measured, not inferred from uptime. Source-ledger aggregates and bilateral exchange are audited separately. Storage size, IndexedDB usage/history count, performance, crew/encounter/rescue/science statistics and JavaScript errors are reported.

See the packaged `reports/validation_summary.json` and VALIDATION_v1.3.md for final acceptance and measured values. A pending, interrupted or failed report is not a pass. Known limitations and explicitly untested platforms are in KNOWN_LIMITATIONS_v1.3.md.
