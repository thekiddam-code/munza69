# Phase 4.4 expedition architecture

## Authority and baseline

Baseline: verified Phase4.3 delivery67399a5, runtime13ab447. Main6a67441 adds the approved mixed asteroid and significant-recording backlog policies; merge7451f80 preserves the newer engine. Implementation milestones3fed45f andccb14c0, corrected runtime34fd122. The full uploaded specification is PHASE44_EXPEDITION_PLAN.md. The Windows browser remains the single simulation authority; the companion server fences and relays paired commands. UMBRA renders received projections only. No new simulation, fleet, universe generator, mission scheduler or clock is introduced.

## Module boundaries

| Runtime module | Responsibility |
| --- | --- |
| expedition-world.js | Additive geometry on the existing25 asteroid identities, authored surface/industrial/cavern classifications, typed persistent edges, known-route pathfinding, utility energy audit. |
| expedition-ops.js | Existing manifest extension `ops44`: physical preparation, isolated EVA vestibule, shuttle/foot durations, conservative field choices, real utility work/post-test, return, inspected suit metadata, bounded history. |
| field-evidence.js | Paid physical camera/radio/light kits; source snapshots; local significant-event buffers; real transmission, loss, recovery and powered-dock ingestion. |
| field-art.js | Read-only original pixel terrain/industrial scene presentation using existing character rigs. No world advancement in drawing. |
| expedition-ui.js | Compact mission/equipment/known-route/evidence controls for host and UMBRA; no remote world mutation. |
| expedition-schema.js | Optional additive-domain validation during existing save/backup validation. Old states without new domains remain valid. |

`icarus.html` connects these modules to the existing Teams, Economy, KnowledgeRuntime, physical ship navigation, mission registry, naturalSurvey/specimen/science intake, backup and telemetry boundaries. `teams.js` retains crew selection/cohesion/field consumption; new manifests disable its generic random field accident in favor of actual environmental constraints. `spatial.js` and `knowledge.js` project actual foot nodes/edge progress. `gravity-motion.js` treats genuine preparation work as support-dependent while preserving Phase4.3 rest/emergency recovery fixes. No calendar or voyage-clock change.

## Physical expedition sequence

Available qualified Engineer + Scientist buddy team → C04 actual equipment collection and paid assembly → C01 protection/knowledge briefing → C02 → independently cycled EVA vestibule → existing shared shuttle50 simulated minutes → connected asteroid foot segments → known safe return to node0 →50-minute shuttle return → finite-oxygen repressurization and actual safe inner hatch → C02 ship navigation. Ship corridors/doors/lift remain existing Transit/Spatial routes. Field segments persist elapsed time; an interrupted closed passage requires retracing traversed distance before replanning. No direct quarter-to-cavern relocation.

The vestibule is a small extension associated with C02, separate from its occupied ship-room atmosphere. It has inner/outer states, pressure, charged/vented/breathed oxygen and paid pump energy. C02 power/air/seal gates operation. An unsafe return can wait; suit oxygen is finite and death remains possible. This is a compartment abstraction, not a fluid dynamics engine.

The25 legacy room IDs/names/visited/objects/findings remain authoritative. Geometry attaches to that same graph. A damaged lift5–10 needs real condition and transferred battery power, while alternate foot passages remain. Military containment23 stays sealed. New surveys use passive wreck observations: no automatic restoration of old isolation interlocks or random biological exposure. Existing already-active legacy missions retain their old controller until return rather than being retrofitted with invented equipment/progress.

## Knowledge and autonomy

True field conditions belong to the asteroid world. Crew map records are observations with source/tick; SOL receives only delivered Knowledge records. Path planning uses the leader's known routes and hazards; only a locally observed adjacent frontier can be entered. Instruments/lighting are real paid kits with condition and battery consumption. Dark unseen interiors do not yield hidden labels/equipment. Sensor gaps and changed passages remain possible. Creator-authored canon is not made an acquired fact.

The existing mission director still chooses real evidence/need-based opportunities. A received damaged lift can justify a repair; failed repair repeats need changed observed equipment measurements. Generic survey completion counts new sectors, not revisits. A repair debrief preserves previous reachable-frontier evidence; it cannot strand navigation by consuming an unrelated survey lead. Exhausted objectives are checked before paid launch. Source delivery can rearm actual frontier/science leads, not a timer quota. Science observations enter existing specimens/research with provenance, without guaranteed discoveries or breakthroughs.

Current complete profiles are reconnaissance/survey, inspection, utility repair, salvage, sampling, reported-anomaly inspection and dropped-device retrieval. The default qualified team is two; existing Teams can represent2–4. No new role qualifications or specialist selection UI are fabricated. Leader caution/experience, fatigue, health, cohesion and carrying limits affect actual travel/work/reserve decisions; existing social continuity remains. This is not a new dialogue/disagreement generator.

## Resources and evidence custody

Existing suit tokens receive persistent condition/assignment metadata. Legacy ungraded tokens register100% inspection baseline explicitly; past wear is unknown. Camera kits cost .25 spares/.05 tools/.5 energy each, are physically collected, reused and worn. Manifest oxygen/water/food/energy/tools/lab/medical come from the existing ledger; carrying limits and conservative return reserves constrain work. Repair consumes real tools/spares/energy, transfers finite power with receipts, then requires a3-minute powered post-test. Utility battery+drawn must equal paid transferred energy. No free working rover or replacement shuttle appears after total loss.

A camera snapshot contains its actual current location and observed peers, excluding its wearer and inaccessible rooms. Shuttle transit is never presented as a surface feed. Pixel scenes reconstruct that source snapshot; **no original video encoder or recorded video is claimed**. Significant records retain camera/mission/time/location/reason/source/signal gaps,3 pre-event minute states plus up to2 post-event states (at most6 total including the event). Local ring≤3, clips≤12/device, devices≤32, received archive≤64, event keys≤128, mission summaries≤40. Significance2/3 is configurable. Quiet walking updates only the short rolling buffer.

A delivered fact alone cannot upload a recording through a broken link. Local records stay on the device until both actual transmission and source receipt, or surviving co-located recovery and powered dock ingestion. Dock ingestion creates a real source/Knowledge receipt, preserves originalSourceId and clears transferred local clips without duplicates. Receiver outages retain unread stored devices; they are not central evidence yet. Remote previews are limited to the most recent4 records×3 retained frames; full bounded records remain in saves. This bounded working set does not eliminate growth of the existing durable full historical journal.

## Persistence and integration

New optional domains: `asteroidExploration.operationsGeometry`, per-room `field`, manifest `ops44`, `expeditionOperations`, `fieldEvidence`, `teamLog.fieldSuits`, actual crew fieldPosition/fieldMotion. Existing schema1 envelope and backups/history/writer fencing are unchanged. Domains are initialized additively and validated; malformed future/corrupt records are rejected, not silently reset. Mid-segment, receiver-outage, queued recall, airlock and utility work state are serializable.

ObservationModel/CompanionView supply source-limited body feeds to existing PixelCamera/FollowCrew. OperationalUI/index include receive-only field controls/art, and bounded expedition DTOs are removed from legacy compact telemetry branches to preserve their size contract. The server accepts only fixed paired command grammars and bounds; requests use existing deduplication and host acknowledgment. No Android/native or TV source replacement.
