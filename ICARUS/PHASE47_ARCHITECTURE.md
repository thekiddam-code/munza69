# Phase 4.7 checkpoint architecture

**This is an implementation checkpoint, not a completed Phase 4.7 release.** The deployment/camp acceptance gates are not met.

## Existing authorities retained

The authoritative browser minute controller still owns movement and decisions. Windows companion authentication, lease generations, durable writer fencing, save namespace, explicit ENTER boot and backup transactions are unchanged. Crew, Knowledge, Economy, ExpeditionWorld, ExpeditionOps, cameras and calendar remain the existing systems. No new universe, clock, gym or camera-side world advancement is introduced.

## Original vehicle and cargo view

`forward-ops.js` adds optional `state.forwardOperations`. Legacy absence migrates once during normal initialization and backup restore. It registers the author-approved original FOC-01 at C03, operational, restrained, with a named initial charge/load and stocked equipment inventory. It does not rewrite voyage history or infer previous deployment. Initial field stores are a separate original-equipment asset, not a replenishment of ship Economy; no ship/field resource-transfer capability is claimed yet.

An available engineer can take the queued inspection through the existing task selector and physical navigator, reach C03 and perform eight work minutes. Emergencies/qualifications/access/power gate work. Service charging consumes actual ship electrical inventory and tracks initialCharge + charged − used = battery; repeats at the same tick do nothing. Structural validation rejects negative/unaccounted charge and unsupported locations. The bounded service history persists.

`forward-art.js` is the actual C03 establishing camera. A 6.2×2.5×3.1m box-truck asset and 8×4m parking declaration are projected at20px/m, with the existing crew rigs scaled consistently in this wide view. Different panel colors, racks, restraints, service cable, loading lane, wheels and communications fittings are drawn from the registered exterior. The camera DTO contains exterior identity/restraint/dimension data, not an omniscient inventory dump. UMBRA loads the same renderer. This is a new visual scale declaration in an abstract topology, not proof of physical truck clearance through existing doors. No interior vehicle/tent camera is created.

The actual departure route, payload-rated carrier, camp deployment work, deployed equipment objects, resupply, ATVs and medical camp remain unimplemented. The interface states that explicitly instead of offering a teleport/deploy button. Those are engineering work still to do; no extra approval requirement is inferred.

## Escort controller

`drone-escort.js` extends the existing DroneOps missions with `escortId`, rather than a second movement engine. It runs once per minute before DroneOps. A current DIRECT/RELAYED expedition report and a SOL-received location are required. Replacement launch uses actual charged/serviceable chassis, the existing paid dock and a connected observed route. A conservative round-trip forecast rejects routes beyond the battery budget.

Replacement drones traverse existing50-minute approaches and graph segments. A handoff requires a stationary co-located team/replacement; overlap is recorded only if the outgoing drone is also actually present. The outgoing then returns through existing reserve/recovery logic. No replacement, radio loss, blocked path, degraded equipment or insufficient power can produce a truthful bounded coverage-gap record. No continuous surveillance is invented. Loss of a current report requests return only through a working drone radio; disconnected drones retain their onboard policy and battery safeguards.

**These are ship-dock rotations. There is no functioning field camp/dock yet.** Maintenance/charging at the ship reuses Phase4.6. This checkpoint does not claim camp maintenance, camp patrols, ATVs or independent search-and-rescue dispatch. Only the existing single asteroid crew expedition can be escorted.

## Surveillance and recordings

The local UI now lists every retained received host recording, rather than the latest eight. In the supplied backup, Records1–20 exist and nextRecord21; no clips remain pending onboard. Records1–12 were hidden by the presentation slice. They are exposed under their original IDs. There are98 retained state frames and74 PNGs; the24 state frames without PNGs are not invented/recovered as pictures. Their absence alone does not establish whether capture was unavailable or an earlier mutation removed pixels.

Host24-record and drone8-clip retention bounds remain. Future host evictions retain up to64 small removal notices; this cannot reconstruct records already missing before installation. Onboard/unreceived state remains private until actual radio/dock receipt. A source-state reconstruction is never labeled captured imagery.

Playback offers play, pause and replay of actual retained frames. Source, tick, location, receipt, event ID and image/state counts remain visible. Empty metadata previews clear the old canvas rather than display a different record's image. Old recordings may look static if their retained frames depict the same scene. This does not create historical motion. New captures remain low-cadence bounded PNG/state sequences at simulated-minute cadence; high-frame-rate encoded video/audio is **not** implemented.

The drone panel renders current received state repeatedly when visible and running, honors reduced/minimal motion and pause, and stops background/closed-detail animation work. Travel framing follows actual graph progress; cosmetic HUD animation never advances a drone or predicts an unseen arrival. Co-located crew in a passage are filtered by actual proximity. FieldArt distinguishes natural/surface/industrial architecture and uses actual visible facility names to distinguish military/corporate structures. It never reveals an undiscovered destination as a menu filler.

Sectors/Facilities/Drones are filters over received intelligence, not newly invented installed static feeds. A full unified geographic camera tree and remote on-demand full media service remain work. The remote receives all retained recording IDs with compact metadata and the latest bounded frame preview; older full playback currently requires the host.

## Wire and catch-up reliability

The110,000-byte complete-envelope UTF-8 budget and131,072-byte server guard are preserved. Historical metadata is compacted before transmission; complete host archives are unchanged. Optional histories/handoff previews are bounded. An irreducibly oversized packet still reports a preview error without losing writer authority or truncating saves.

Calendar.advance accepts an optional cooperative yield predicate only after a completed physical minute. Production requests yield after roughly24ms and resume backlog in16ms tasks, keeping existing minute steps, Monday–Sunday boundaries, selected rates and synchronized holidays. Tests can drain deterministically with fixed inputs. The inherited six-real-hour recovery cap remains unchanged and reports any older omitted wall interval; this patch does not claim unlimited suspension recovery. A single expensive step still cannot be preempted internally.
