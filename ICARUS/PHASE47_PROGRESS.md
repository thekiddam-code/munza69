# Phase 4.7 progress

Baseline: `31b9ccb` (includes the verified startup-size and boot hotfixes). Authoritative request: PHASE47_IMPLEMENTATION_BRIEF.md. No simulation reset, gym, new universe, second clock or renderer-driven simulation.

## Internal milestones

1. Audit and baseline: inspect actual ship/field topology, persisted domains, camera provenance, packet budget and recording custody. Run the existing Node baseline.
2. Vehicle foundation: additive original-equipment registration, real C03 parking view and physical engineering inspection using existing crew routing. Audit vehicle-sized departure feasibility before transport/camp activation.
3. Surveillance: recover access to retained historical records without renumbering; genuine captured-sequence playback controls; source-limited Sectors/Facilities/Drones categories; animated live received drone views and terrain differentiation. Preserve the 110,000-byte wire budget.
4. Autonomous escort: use actual team location, known connected routes and paid batteries; replacement rendezvous before outgoing return, explicit gaps when infeasible; preserve radio outages and save/load.
5. Integrated verification: schema migration, old voyage, browser/server regression, actual-renderer screenshots, final limitations and independently reviewable commits.

Vehicle transport, persistent field camp, camp power/maintenance, ATV logistics and camp-based rotations must remain explicitly incomplete until physically implemented and tested. A crew shuttle abstraction or personnel hatch must not silently become a truck carrier. Do not declare Phase 4.7 complete based on partial milestones.

## Audit findings

- ExpeditionWorld is the existing 25-cell graph. ExpeditionOps performs C04 collection, C01 staging, C02 pressure cycling, 50-minute shuttle travel, connected field traversal and return. Field crew positions exist only after actual arrival; a request/proposal alone is not an arrival.
- C03 is Cargo Bay; C04 is Equipment Storage. Existing ship corridors are abstract travel nodes, with a four-person lift. There is no metric truck clearance or freight-carrier payload model. A large vehicle cannot be assumed to pass a personnel hatch or unmanned drone port.
- The supplied Episode 2 backup retains DRONE-1-RECORD-1 through -20, nextRecord21, no local pending clips. The local UI selected only archive.slice(-8), explaining a visible list beginning at Record13. Records1–12 are retained data, not lost footage. All98 states and74 PNG images present in that backup must be preserved; absent pixels are not recoverable from state alone.
- Older local/host retention is8/24 clips. Missing future/older records outside actual retained storage cannot be fabricated. The remote preview has a separate size budget.
- DroneUI forces paused/reduced rendering; FieldArt has no drone motion overlay. Existing ObservationUI animates received ship states without advancing the simulation. Extend those established boundaries.
- Existing catch-up is bounded to120 minute steps per pump and6 real hours retained. Rendering/PNG sampling costs are candidates for measurement, but meaningful steps and original clock rules must remain.

## Implemented checkpoint

- Persistent original FOC-01 registration/stock/restraints, C03 exterior establishing camera, paid service charging and physical eight-minute engineering inspection. Actual browser travel/inspection/reload test passed. Truck departure and camp remain unimplemented; no cosmetic deploy action is offered.
- Every retained received record is listed locally, recovering access to Records1–12 in the supplied backup. Compact remote metadata retains every ID. Playback has play/pause/replay, actual image/state availability counts, source labels and empty-preview clearing. Future host retention removals retain bounded metadata; pre-existing absent pixels are not invented.
- Live drone panel honors actual traversal, pause, signal, light/damage and visual preferences, with visible-only render updates and source-relative framing. Received Sectors/Facilities/Drones filters and limited architectural distinctions are implemented. This is not full remote high-rate video or a new static camera network.
- Source-informed ship-dock escort controller performs physical replacement launch/rendezvous/return, conservative route/energy forecasting and bounded truthful gaps. Deterministic overlap/outage/unavailable/reload tests pass. Camp-based rotations remain unimplemented.
- Production catch-up yields between completed simulation minutes; deterministic yielding vs uninterrupted clock comparison passes. Existing rates/holiday/week/recovery cap remain.
- Supplied snapshot has no active crew expeditions, no modern expedition-operation completion entries and no currently field-assigned crew. It cannot establish the cause of an earlier attempted assignment. Existing staging/travel/field/return and blocked-mission reporting are preserved and must pass regressions; no crew are inserted into cameras to satisfy visibility.

Pre-freeze milestone:427/427 Node cases passed; three real renderer/engine feature cases passed before final freeze. Final exact-runtime regression and private-backup verification follow. Phase4.7's truck-deployment and camp acceptance gates remain open; do not publish this as a completed Phase4.7 release.
