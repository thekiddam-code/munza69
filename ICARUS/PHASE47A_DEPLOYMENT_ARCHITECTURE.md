# Freight and Landing Shelf camp: architecture

This milestone extends the existing Phase4.7 checkpoint and its catch-up hotfix. It is not the complete Forward Operations release.

## One controller and one transport

`forward-deployment.js` supplies bounded freight/camp hooks to the existing `ExpeditionOps` minute controller. It does not advance time or route crew. `ForwardOps` continues its existing physically assigned engineer tasks; `Teams` continues crew selection, suits, carried cargo, metabolism, casualties and return. Existing Knowledge, FieldEvidence, Economy, world graph, cameras, calendar and durable writer remain authoritative.

There is no second shuttle. `emergencyOps.transport.reservation` reserves the existing transport for the active freight manifest; `Teams.launch` rejects competing launches. Normal launch logic already permits only one active expedition. No spacecraft, suit, crew member, battery or resource is minted to make deployment work.

## Engineering dimensions and installation

The previously unspecified freight geometry is now an explicit engineering model, not an assumption that the truck fits a personnel door:

- FOC-01 retains its existing 6.2×2.5×3.1m dimensions and original cargo inventory.
- C03's freight-access record declares a 19.2×8×4.5m bay, a 9×4m loading lane and a docked 9×4×4m cargo lock.
- The freight aperture is 3.2m wide and 3.6m high. The shared carrier's usable hold is 8×3.2×3.6m, rated at 10,000kg.
- Planning includes 6,200kg vehicle dry mass, the actual remaining stock, the full original equipment kit even when erected, and a conservative 600kg allowance for crew/personal manifest. Preflight rejects dimensions/load outside these limits.

These are new declared simulation dimensions for previously abstract spaces, not historical measurements or a CAD clearance certification. Existing room IDs, personnel doors, corridors and lift capacity are preserved. The freight path is C03 → isolated cargo lock → docked shared lander, not the C02 personnel hatch or drone port. Preflight uses received site intelligence; hidden site changes are checked only on actual approach and cause a physical return without unloading when unsafe. Only Landing Shelf0 is rated in this pass; no width/terrain rating is invented for underground passages.

An available engineer must actually reach C03, inspect the vehicle and install/test the freight interlocks. Installation consumes six actual spare parts, two tools and four energy, with twelve installation minutes plus four test minutes. Paid progress persists and resumes without charging twice. A material shortage holds work; emergencies/readiness/access/power can interrupt it. `deployment.refit.condition` is the canonical freight-interface condition. Room/transport metadata refer to this component rather than maintaining another operational simulation.

## Physical lifecycle

A queued deployment becomes an ordinary asteroid expedition only after preflight. Crew physically collect paid mission equipment at C04 and navigate to C03. Loading takes eight work minutes; protection checks and a finite-oxygen pressure cycle precede the existing fifty-minute outbound flight. The vehicle's location changes to the asteroid only at actual arrival. Eight ramp minutes precede twelve setup minutes. Original equipment moves into persistent camp objects; it is not copied into another inventory.

The crew then return through the existing controller. The vehicle/camp remains at Landing Shelf0; its parking position aboard ICARUS is empty. Recovery is another ordinary expedition: actual travel, twelve packing minutes, eight loading minutes, fifty-minute return, repressurization and subsequent physical C03 re-restraint. Recall during loading preserves the actual partial lane position and releases transport only through the applicable abort/return procedure. Power loss pauses loading. Incomplete or unrecoverable work preserves equipment at its last physical location rather than returning it magically.

All crew still use the actual ship/field topology. There is no side simulation of a truck moving through imaginary tunnels. Interior truck/tent geometry and footage are not generated.

## Resources, autonomy and evidence

`deployment.equipmentBaseline` records the pre-existing original kit once. Validation checks vehicle inventory plus erected camp objects against it. Stock remains aboard the vehicle through this milestone; medical/resupply controllers are not claimed. Relay/floodlight standby draws a finite .005 charge units per simulated minute from the existing vehicle bank; `initialCharge + charged − used = battery` remains enforced. At zero charge, power stops. C03 charging still consumes ship electrical inventory.

Autonomous deployment requires an actual completed long-range expedition, a received safe Landing Shelf survey and known unfinished frontier work. The previous mission ID is the persisted justification: the same old evidence cannot repeatedly redeploy a recovered camp. Critical ship needs, fit qualified crew, launch resources, freight readiness and the shared transport gate the actual departure. Manual requests use the same validated path. Hold/release controls affect future deployment; an active mission uses the ordinary source-backed recall mechanism.

Field reports are actual crew observations. They can be recorded while radio is unavailable but do not appear in the bridge projection until SOL legitimately receives the source or the crew return/debrief. An unreported condition is labeled unreported, not filled with a guessed value. No hidden field inventory is included merely because the host owns it. The host's C03 camera shows only local parking/transfer state.

Existing suit/drone cameras at the actual site receive the exterior overlay. It draws the real truck, erected tents and power-dependent external lighting; setup/packing use existing work poses tied to actual task state. No actors or silhouettes are added for empty tents. No new omniscient static camp feed or synthetic historical footage is created. Existing event recorders may capture the new exterior state, retaining their existing provenance labels. Old frames without a captured camp DTO do not acquire today's camp during playback; the renderer uses the retained frame, not the current global world.

## Save compatibility and performance

The world version, browser storage keys, database schema, original vehicle registration, existing IDs, recordings, calendar and writer fencing are unchanged. Optional `forwardOperations.deployment` is initialized once when used/stepped. Existing saves without it remain valid. Active freight progress, transport reservation, refit costs, erected objects, remaining battery and source report IDs survive restart/week transition.

The existing worker-backed canonical-save/compatibility-cache architecture and preview budgets remain. New histories cap at64 ledger entries and24 source references; camp objects cap at24. No continuously recorded video or unbounded per-minute log was added. Full original backups remain private and outside release packages.

## Boundaries for Phase4.7B/C

Camp-based drone charging/repair/escort rotations, treatment and overnight occupancy, ATV driving, security patrols, resupply, off-shelf relocation and independent heavy recovery remain to implement. Equipment objects exist, but those services are not represented as working controls. Transit-loss recovery is not guaranteed; a lost carrier cannot be respawned. Freight-interface repair beyond existing inspection/refit is a remaining maintenance extension. High-rate encoded event media and full remote archive transport remain Phase4.7C. Current art remains a simplified exterior pixel renderer, not a final full-physics presentation. Physical Windows/Android/TV/native/antivirus validation is a separate hardware/source gate.
