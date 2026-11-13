# Living Ship Operations architecture

ICARUS remains one browser-authoritative simulation backed by the existing fenced Windows companion bridge. Phase 4.3 adds systems inside the existing fixed-minute world step; rendering and paired UMBRA clients never advance a second world. The approved continuation to the brief is recorded in PHASE43_LIVING_SHIP_OPERATIONS_PLAN.md.

## Authorities and interfaces

- `ship-systems.js` owns additive `state.shipSystems`, its seven installed components, six zones, circuit controls, measured field ramps, condition/wear, diagnostics and bounded recent hardware history. Existing `equipment.C07/C08/C09`, finite Economy, atmosphere and maintenance remain authoritative. Existing equipment appears through read-only adapters rather than duplicate health values.
- `gravity-motion.js` owns persistent per-character/object gravity motion and one-minute updates guarded by the last simulation tick. Existing Spatial/Transit graph remains the only travel topology. The motion multiplier changes actual travel duration; secured-work delays/factors change actual repair/research/task progress.
- `systems-maintenance.js` extends `maintenance.systemOrders`, because multiple components can occupy the same existing room. It uses existing engineer selection, task completion, physical C04 supply collection, finite inventory, Knowledge and safe-air rules. It does not create another crew scheduler.
- `engineering-ui.js` is a read-only renderer plus command sender. The local and paired Engineering panels share it. The remote loads this UI module, not ship-system or gravity simulation modules.
- `icarus.html` connects these modules to the established single fixed-minute step, save/restore, source-backed reports, local command validation and modern host telemetry. `server.py` adds only a bounded command whitelist to the existing paired/deduplicated/fenced route.

The root pump, production clock, calendar, durable writer fence, backup format, Android project and television service are unchanged. Selected 20× pacing remains supported; ordinary Auto remains 4×, synchronized holidays 1× and episodes real local Monday–Sunday. New operational progression uses elapsed simulation minutes, never render frames.

## Physical registry and dependencies

The gravity generator is physically installed at accessible existing C07 engineering, not at an invented room. Engineering repair scenes use its actual console position. Distribution consoles use A02, A08, B08, C04, C02 and C07 respectively.

| Zone | Actual rooms |
| --- | --- |
| Habitation | A01–A07, A09–A10 |
| Medical | A08 |
| Science | B01–B10 |
| Cargo/storage | C03, C04, C10 |
| Hangar/airlock | C01, C02 |
| Engineering | C05–C09, plus existing shared lift cabin supply |

Corridors use the existing Transit station adjacency, with deck-default selection at shared boundaries. No additional map exists. The registry audit requires exactly thirty unique ship rooms.

The upstream bus depends on actual global power, existing C07/C08 condition and paid finite electrical inventory. Generation retains its existing fuel/solar source; it is deliberately not gated behind downstream circuit power, allowing legitimate black starts. Local circuits then gate gravity, powered hatches/lift, lights/cameras, lab availability and downstream production. Bridge/drive circuits gate departure and thrust progression; actual coordinates/fuel remain intact during interruption. Hangar power/very low gravity can withhold launches. Existing core-edition travel boundaries remain unchanged.

Life support extends existing oxygen/pressure/temperature progression, respects closed hatches and local electrical regulation. It does not implement a calibrated CO2 concentration model. Engineering telemetry says unavailable for that sensor; no synthetic ppm reading exists.

## Gravity and consequences

Healthy installed components default to 1g. Targets are bounded to 0–1.2g. Power and condition limit output; local isolation does not automatically disable independent neighboring circuits. Gravity isolation and electrical isolation are distinct. Fields descend at at most 0.2g per minute; ordinary restoration ramps at 0.05g, explicit rapid restoration at 0.25g. Current gravity can differ from target.

Reduced gravity uses lighter-step movement and modified work. Zero-g uses actual handhold travel, visible floating and an anchoring delay before work. Actors retain their graph node/routes; they never teleport between rooms. Character and object camera heights/horizontal coordinates use the same lightweight motion state as consequence checks. Only real discovered loose containers/samples in the existing room-object collection participate; decorative objects are not invented. Secured objects stay secured.

Fall energy accumulates during actual descent. Harm requires real height, an unsecured actor/object, a sufficiently energetic rapid restoration/nearby impact and the existing injury pathway. Grounded/secured actors are not injured merely because a target changed. A normalized default object mass is an explicit approximation where old objects lack mass metadata. This is deterministic compartment physics, not a rigid-body engine.

## Knowledge, maintenance and authority

Actual instrumented fault reports create source records and Knowledge facts. Engineers require qualifications plus received information or physical presence, a feasible route and tools. Operator inspection requests use the same source-backed workflow. The sequence is supply collection/travel, diagnosis, service isolation, physical spare collection, condition-dependent paid repair, release of service isolation, powered post-test and recorded outcome. Work depends on energy/experience, gravity support, breathable atmosphere and finite tools/parts/electricity. Missing supplies/power or higher duties can block or release it. Operator electrical isolation is never silently undone by a repair.

A dead/missing/preempted assigned worker releases the reservation. Partial condition/progress and paid receipt flags persist, preventing duplicated parts after reload. Component histories retain the most recent sixteen repairs; equipment summary/history and fault presentation are bounded. Genuine source history retains the existing durable archive policy.

New hardware controls, automatic safeguards and human engineer work do not require a SOL object, and reports do not grant Knowledge to a terminated SOL. This phase does not implement or claim to validate the separate proposed AI symbiotic takeover/lifecycle design.

## Telemetry and observation

Engineering instrumentation is explicitly on the upstream control bus. When unavailable it returns the last actual measurement with its original tick and a stale label, or no measurement if never powered. Local circuit damage cannot magically reveal a new reading through an unpowered instrument. The security-camera receiver remains physically dependent on B07 power; losing its science circuit can take the network offline even while engineering controls remain reachable.

Ordinary telemetry contains observed engineering status and bounded diagnostics; private thought/quarters/classified payload boundaries remain unchanged. Detailed pixel cameras extend existing scenes with actual gravity poses, generator work, drifting objects and lighting. Existing privacy, receiver availability, room/lift transitions and Follow Crew projection remain in place. No video recording or invented footage is introduced.

## Migration

Old saves retain their existing version/envelope and all world data. On first load, absent `shipSystems` installs healthy baseline gravity hardware at 1g and adds an empty component-order dictionary alongside the existing ledger. Initial available bus is derived from existing equipment/power/energy; an empty-energy save cannot claim live instrumentation. No historical gravity failures or repairs are retrospectively fabricated. Once present, installed state, motion, faults, targets, isolation, measurements and ongoing jobs serialize through the existing durable save pipeline.

Back up before migration. Older builds do not simulate the new fields; rollback requires the pre-upgrade backup, not silently loading a new operational world into an old build.
