# Phase 4.4 validation record

## Scope and provenance

Baseline67399a5096d92530057645eba80e4f74af75b604 / verified runtime13ab447 was inspected;346 inherited Node cases passed before implementation. Main6a67441 contributed two approved backlog policies, not a replacement engine. Full brief: PHASE44_EXPEDITION_PLAN.md. Milestones7451f80 (baseline/merge/plan),3fed45f (physical field/evidence integration),ccb14c0 (equipment/communications/recovery refinements),34fd122 (navigation regression and passive wreck correction).

**Corrected runtime34fd122280a9ffd91330bb0fa3e2d702c886ad57** is an immutable128-file export. Final test/campaign/watch reports identify that commit. Documentation/packaging commits must retain all128 hashes; the Lite BUILD_MANIFEST identifies its own exact committed source. No late runtime changes may be substituted without retesting.

## Investigation of failed candidate

Candidateccb14c0 passed367 Node,39 remote,4 clock,19 legacy and18 services, but the full86-browser suite had one real regression: `test_completed_delivered_surveys_allow_autonomous_navigation_without_a_mission_quota` recorded zero arrivals. Normal1001 and explicit-adverse4807 each completed three asteroid sorties, including paid utility repair, and had empty conservation/source audits with20 living crew, but that did **not** satisfy acceptance.

Causal state: survey returns supplied reachable unexplored routes; the director properly prioritized a received lift fault; repair returned with zero new sectors; generic debrief cleared pendingSurvey/pendingLead; the ship could neither survey remaining known routes nor depart HOME while those routes remained. Corrected debrief preserves unrelated frontier evidence for non-survey work. The original assertion was kept and independently passed before freeze. Failed repair proposals now require changed observed equipment measurements; partial work reports real condition. No fixed mission quota was added.

Further-route review found the inherited wreck observation callback could randomly power an interlock or expose eggs. New physical expedition observations are passive: they record actual wreck rooms without those side effects. A deterministic zero-random test verifies unchanged sealed containment, reserve power and dormant biology. Older already-active legacy missions preserve their controller; this is a declared migration boundary.

The first actual-time watch requested the asteroid after derelict autonomy had reserved the shared transport; its missing field sample is preserved as a driver failure. Revised driver makes a normal authorized request at startup and otherwise uses actual wall time/UI; no fake discoveries, needs, incidents or relationships. A revised candidate watch passed, but final claims use the repeated corrected-runtime watch separately below.

## Coverage

New deterministic cases cover additive25-room migration/unchanged seals, actor-known routes/hidden hazards, paid devices/suits and condition, exact-once ticks, pressure/finite oxygen, real segment durations and blockage reversal, carrying/reserve decisions, actual repair/finite charge/post-test, lost-link/local custody, received source vs broken channel, no shuttle surface footage, body camera excludes wearer, immutable historical appearance, same-node recovery, powered dock buffering/ingestion, corrupt save rejection, quiet bounded buffers and passive wreck observation.

Actual browser coverage walks the entire C04/C01/C02/flight/foot/return sequence, exact mid-segment save/reload, successive industrial+cavern sorties, actual kit reuse, receiver failure, dropped device recovery and buffered dock ingestion, true paid industrial repair and powered post-test, and queued recall until actual source delivery. Inherited ship systems/zero-g/rest/emergency, social/privacy/lift/follow/calendar/save/research/memorial/navigation assertions remain. Adverse fixture modifications are labeled and are never reported as naturally occurring events.

Remote cases use actual HTTP pairing/commands/host acknowledgment, invalid/unpaired rejection and duplicate suppression. A phone Chromium context has no simulation module and shows received BODY feeds, delayed recall and labeled record playback. These are protocol/emulation checks, not a physical Android or LAN test.

Final executed counts, campaign/source statistics, actual-time performance and extracted-ZIP checks are appended after completion. A pending run is not a pass.

## Unavailable checks and release boundary

Physical Windows laptop, Samsung phone/Tab S5e/TV, original installed APK/native rebuild, real LAN/Tailscale, human accessibility/visual/GPU and antivirus tests cannot run in this Linux environment. Desktop/TV I/O is stubbed in remote browser tests. Native Android remains compatible in architecture and pending source recovery/build validation. No antivirus was disabled. No physical success is inferred from emulation.

No365-day campaign or full physics/rescue/FOV/video/final-game certification is claimed for this batch. PHASE44_LIMITATIONS.md lists incomplete capabilities and Phase4.5 work. Source-grounded evidence captures are reconstructions, not recorded footage. Lite excludes test suites/reports/tools/raw campaign worlds; the separate evidence ZIP contains isolated fictional test worlds and must never replace a user's voyage.

## Acceptance mapping and honest boundaries

| Brief acceptance | Evidence and boundary |
| --- | --- |
| 1–3 valid objective, qualified crew, real equipment | Existing director/Teams gates plus validated source-backed request; paid kit/suit rejection and actual browser launch tests. Qualified buddy profile is complete; no fabricated specialist expertise. |
| 4–6 physical departure/protection/connection | Browser records actual C04/C01/C02 visits, pressure stages, timed shuttle and foot edge progress. Mid-segment reload matches exactly. Vestibule is a finite-gas compartment abstraction. |
| 7–9 connected industrial/natural, actual discovery and fog | Two-sortie browser test and campaign actual visited IDs; known-route model tests and receiver-outage tests. Graph is coarse and persistent, not collision-level geometry. |
| 10–12 hazards/abort/consumption | Reported hazard route weighting, reserve/carrying/equipment withdrawal, dynamic blocked-edge reversal, delayed radio recall, safe return hatch holds and Economy/utility oxygen conservation. Independent second-team casualty rescue remains deferred. |
| 13 field camera | Actual body source/peers, no flight surface view, Follow Crew continuity and technical pixel examples; actual-time watch is separate. FOV/occlusion remains coarse. |
| 14–16 authentic bounded evidence/local custody | Source-state pre/post reconstruction, quiet ring/clip limits, channel+receipt gating, actual dropped-device recovery and powered return dock ingestion. **No original video capture.** |
| 17–18 real reports/save | Mission history records actual visited/new IDs/decisions, full-history independent source audit, genuine older-save imports, exact checkpoint and in-progress reload tests. |
| 19 desktop/Android same host | Actual paired HTTP + Chromium phone/tablet projection/controls; no remote simulation. **Physical installed Android APK remains unverified.** |
| 20 Phase4.3 preservation | Inherited Node/browser/remote engineering, gravity, physical repair, zero-g/rest/emergency and save regressions. Hardware is separate. |
| 21–22 dormant threats/unforced operation | Explicit passive-wreck zero-random regression and campaign dormant/sealed audit; normal worlds have no injected incidents/discoveries. Adverse worlds explicitly declare initial technical damage/injury fixtures. No guarantee of quiet or survival. |

This mapping verifies a bounded working implementation. Outstanding independent rescue, fine optics/art, actual-video and hardware gates are not disguised as completed acceptance tests.

## Corrected campaign results

Both independent full-history audits pass: real sources/public privacy,20 unique persistent crew identities, daily world/knowledge/creature/social/transit/engineering/gravity/economy checks, finite utility power, bounded field working sets and exact final checkpoint reload. Audits explicitly reject zero navigation arrivals or no connected field activity, rather than accepting survival alone.

| Campaign | Real / ship days | Alive / deaths | Arrivals | Asteroid sorties | Surveyed cells | Received records / frames | Science cases | Conversations | Sunday films |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| normal1001 | 7 /25 | 20 /0 | 5 | 9 | 20 | 46 /212 | 21 | 474 | 1 |
| adverse4807 | 7 /25 | 20 /0 | 5 | 7 | 20 | 40 /186 | 21 | 440 | 1 |

Normal:2 survey,1 repair,6 sampling sorties; all9 completed their actual objective. Adverse:2 survey,1 repair,4 sampling;5 objective-met,1 carrying-capacity withdrawal and1 observed-frontier-exhausted return. No duplicated new-cell claims. No active field mission remains at checkpoint and dormant/sealed military conditions remain intact. Science-case counts are investigations, not confirmed breakthroughs. Seven real days correctly yield25 ship days because Halloween remains synchronized1×; no clock was changed to force28.

The adverse campaign explicitly imports B07 condition10%,C09=32%,C07=45% and a45-point injury to crew0 through the actual backup interface. This validated initial fixture is not claimed as an organic disaster. Normal campaign changes only seed/start clock. Neither injects specimens, discoveries, relationship outcomes or threat activation.

Each campaign autonomously repairs utility5 from25% to86%, transfers exactly1 carried energy unit to its battery and performs the powered post-test. The final battery remains1 with0 lift-draw: **repair is verified; these campaigns do not claim an actual lift ride**. Utility6/7 remain25%/unpowered. Final body cameras are the same2 stored devices, at99.512% normal/99.6215% adverse, rather than freshly recreated equipment. Source-receipted recovered bulk totals36 ore/18 waterIce normal and32 ore/16 waterIce adverse across existing field missions; every recovery retains its specimen source and existing finite economy accounting. These totals include derelict as well as asteroid missions.

Snapshot growth is2,796,454→8,295,416 bytes normal and2,583,436→7,955,364 adverse over these25 ship days. Full actual source histories contain12,456/12,237 records. New field limits stay bounded; genuine full-history growth is not called solved. Linux headless campaign wall times527.80/503.62 seconds include concurrent verification load and checkpoint persistence, not physical Windows benchmarks. Raw final inventories, ledger source totals, utilities, suit/device conditions and source audits are in campaign_summary.json and the evidence bundle.

Technical visual examples were captured from actual deterministic controller execution using an ordinary authorized mission request (other autonomy disabled in that isolated technical example). Surface, industrial and irregular cavern screenshots retain their source DTOs and tick. They were visually inspected; these are procedural observed-state scenes, not original recorded video or final-art certification.

## Actual elapsed watch and performance

Corrected runtime watch uses actual monotonic/wall time, normal UI, the real companion server and one legitimate captain asteroid request at startup. No soak/fake-clock API, incident/need/relationship injections or assigned adult/romance outcomes. The phone is Chromium emulation and desktop/TV I/O is stubbed. It passes reconnect, no remote simulation, unique source IDs, zero discarded wall time and reload continuity.

Normal phase123.434 seconds advances0→8 ticks, measured3.8887×; selected20× phase541.719 seconds advances8→189, measured20.0473×. The latter reloads at tick99 and resumes tick99 with20× retained. Five sampled intervals have actual BODY feeds; unavailable travel/range intervals remain unavailable. All20 crew remain alive,4 actual conversations occur and15 ship lift trips complete. The harness took684.879 seconds including setup/teardown.

Final post-reload draw counters:2420 main+4216 preview frames,5830.7ms cumulative drawing (~0.879ms/count). Largest sampled draw176.4ms under concurrent verification is retained as a limitation; this is not a claim of perfectly smooth rendering or a physical Windows/GPU benchmark. Simulation pacing is measured independently rather than inferred from drawing FPS.

An additional actual-browser regression places a legitimately launched ops44 team one minute into a real foot segment, then crosses UTC Sunday23:59:30→Monday00:00:00 through the production calendar pump. Exactly2 simulated minutes advance: the same mission/device IDs persist, edge elapsed increases by2, airlock/suit counts remain unchanged, visited knowledge persists and exact reload matches. This separately executed case supplements the full86-case run; it does not replace the inherited weekly assertion.

## Final automated results

The corrected immutable runtime passes **536 main case executions with zero final failures or skips**:369 Node (346 inherited+23 expedition),86 full inherited/expedition browser,1 additional active-ops44 real-Monday browser,39 actual-HTTP remote browser,4 production-clock,19 legacy-continuity and18 bridge/TV/classified service cases. Counts are executions; separately run inherited suites overlap. Focused development reruns are not counted again. The full86 run took990.626s under concurrent verification; remote39 took403.715s, legacy19 took155.735s and clock4 took49.928s. Raw logs and machine-readable per-case results are retained. Python compilation passes for server and new verification/campaign/capture/audit/package tools.

No runtime file changed after corrected34fd122. The old failed candidate/browser/watch and zero-arrival summaries remain clearly labeled diagnostics. The new positive lift test executes a real modeled segment for its computed visibility-adjusted duration, consumes.05 from a paid.2 battery, rejects a spent lift and proves same-tick re-entry cannot double-charge. Its initial fixture's assumed2-minute trip was corrected to the actual computed duration; the controller was not shortened to satisfy it.

## Distribution verification

The Lite ZIP is created from a committed Git source tree, retaining all128 host/web runtime files and necessary docs/licenses. BUILD_MANIFEST records the exact source commit and SHA-256 for every retained file. Tests/reports/development tools/packaging scripts/generated credentials/test worlds are excluded. All128 runtime hashes must match corrected34fd122; ZIP CRC and every manifest file hash are checked. Adjacent package_verification.json and delivery reports contain the actual ZIP checksum, source/hash equality and extracted-package test results. No silently patched runtime is substituted after final testing.

The evidence ZIP contains full final isolated campaign backups/snapshots/history, reports/watch/technical screenshots, failed-candidate diagnostics and clearly labeled old migration fixtures. **Do not import those fictional test worlds as your voyage.** Your own full backup is required for upgrade and rollback. SHA-256 files accompany downloads. Source changes and artifacts remain on codex/expedition-operations-phase4-4; main, existing releases and the installed native APK are not modified.
