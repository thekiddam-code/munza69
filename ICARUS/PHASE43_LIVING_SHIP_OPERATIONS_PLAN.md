# ICARUS / UMBRA
# PHASE 4.3 — LIVING SHIP OPERATIONS
**Implementation brief for Codex**

## Mission

Build on the working Phase 4.2B simulation to make ICARUS function as a persistent spacecraft with meaningful operational systems.

The ship must no longer be merely a visual environment containing autonomous characters. Its systems must influence crew behavior, navigation, environmental conditions, maintenance, equipment availability, and the consequences of events.

**The central new feature is a functioning artificial-gravity system with independently controlled ship zones.**

Preserve all working Phase 4.2B features, especially the improved detailed pixel cameras, autonomous personalities, room transitions, lift cameras, and Follow Crew functionality.

Do not redesign the existing interface.

## 0. Baseline inspection and safeguards

Before modifying code:

1. Inspect the actual repository, active branch, current Phase 4.2B implementation, and existing test infrastructure.
2. Read `ICARUS/IDEAS_BACKLOG/README.md`, particularly the approved Phase 4.3 scope.
3. Identify the authoritative simulation clock, world-state model, persistence layer, ship topology, crew task scheduler, camera renderer, and desktop/Android communication paths.
4. Identify existing ship systems and extend them rather than creating parallel simulations.
5. Preserve existing save compatibility, with migrations where necessary.
6. Create a clear implementation plan and execute it in manageable passes.

Do not claim functionality is complete unless it is implemented and verified.

## 1. Ship systems framework

Introduce or extend a unified ship-systems model.

Systems should have meaningful state, including:

- Operational status
- Health and wear
- Available power
- Current load
- Environmental dependencies
- Faults and diagnostic information
- Maintenance requirements
- Repair history
- Location and affected zones

Primary systems:

- Electrical generation and distribution
- Artificial gravity
- Atmosphere and life support
- Lighting
- Environmental temperature control
- Doors and lift dependencies
- Engineering machinery and equipment

Changes must propagate through modeled dependencies.

For example, a damaged electrical distribution circuit might affect lighting, gravity, or equipment in its connected sections.

Do not trigger unrelated failures merely to create drama.

## 2. Artificial-gravity generator

Create a functional artificial-gravity subsystem.

### Generator and distribution

Model a primary gravity generator and distribution to independently controlled ship zones.

Each zone should track:

- Gravity level, measured in g
- Target gravity
- Available generator power
- Distribution condition
- Control authority
- Active faults
- Connected rooms and corridors

Normal shipboard gravity should default to approximately 1.0g.

Support reduced gravity and zero gravity, with reasonable configurable operational limits.

Do not assume every zone must lose gravity when one distribution component fails.

### Gravity zones

Derive zones from the existing ship topology rather than inventing a second, disconnected floor plan.

Where practical, allow independent gravity settings for:

- Engineering
- Habitation
- Medical
- Science
- Cargo and storage
- Hangar or docking areas

Use the actual ship's existing rooms and deck structure. These are examples, not mandatory new compartments.

Allow authorized personnel to isolate or restore gravity in individual zones.

### Physical generator location

The generator must exist as an actual ship component associated with an accessible engineering location.

Crew should be able to:

- Travel to its location
- Inspect its status
- Operate its console
- Diagnose faults
- Perform maintenance
- Repair damaged components
- Test the system after repairs

Use existing locations if possible. Avoid unnecessarily rebuilding the ship.

## 3. Gravity-dependent crew behavior

Gravity must affect simulated behavior, not just a number on a dashboard.

### Normal gravity

- Standard walking and work animations
- Normal floor contact
- Ordinary equipment handling

### Reduced gravity

- Modified movement speed and animation
- Longer or lighter steps
- Adjusted object handling
- Appropriate use of handrails or support structures
- Task difficulty changes where relevant

### Zero gravity

- Floating crew and unsecured objects
- Movement using handholds, walls, or available propulsion
- Appropriate navigation constraints
- Difficulty performing tasks requiring stable positioning
- Increased risk when gravity returns unexpectedly

Use a practical, deterministic movement model. Full rigid-body physics is not required.

Crew must not simply continue ordinary walking animations while gravity is zero.

Characters should remain connected to the actual world topology.

Do not teleport crew between rooms to simulate floating.

### Gravity restoration

When gravity returns:

- Floating characters must transition appropriately.
- Unsecured objects may fall.
- Injuries or equipment damage may occur when justified by actual conditions.
- Secured objects remain secured.
- The simulation must handle partial and gradual restoration consistently.

Do not manufacture injuries merely because a gravity transition occurred.

## 4. Power and environmental dependencies

Extend the existing power system so connected equipment responds to real power availability.

Examples:

- Lighting dims or fails when circuits lose power.
- Gravity distribution may degrade when its supply is insufficient.
- Environmental equipment may stop regulating temperature.
- Powered doors and lifts respond according to their actual operating and backup systems.

Life support should track meaningful environmental values such as oxygen, carbon dioxide, pressure, and temperature where supported by the simulation.

Changes should progress over simulated time rather than instantly producing catastrophic results.

Respect compartments, doors, isolation, and any existing backup systems.

Avoid creating fake readings for sensors that have no modeled data source.

## 5. Autonomous engineering and maintenance

Crew must respond to ship conditions through the existing autonomy system.

A typical repair sequence should be:

1. Detect a fault through available sensors, observation, or reports.
2. Determine whether the character has the necessary information and qualifications.
3. Evaluate urgency and competing duties.
4. Obtain required tools or supplies.
5. Navigate to the correct equipment.
6. Diagnose the fault.
7. Perform any necessary isolation or safety procedure.
8. Attempt repairs.
9. Test the equipment.
10. Return it to service when appropriate.
11. Record the outcome.

Repair success should depend on relevant conditions, not a guaranteed completion timer.

Crew should be able to fail, discover that they lack parts, request assistance, or postpone nonurgent work.

Use existing personality, experience, skill, and task systems where available.

Do not invent expertise or equipment inventories merely to make repairs succeed.

## 6. Detailed pixel camera integration

Preserve the Phase 4.2B camera quality and presentation.

Make operational changes visibly observable.

Examples:

- An engineer arrives at a gravity control station.
- A technician carries tools to a damaged power unit.
- Corridor lights dim after a circuit failure.
- Crew float in a zero-gravity compartment.
- Objects drift when unsecured.
- An engineer secures themselves before working in low gravity.
- A repaired generator resumes operation.

Animations must correspond to actual simulated actions.

Do not display repair animations for characters who are merely idle or traveling.

Maintain correct room doors, corridors, lift transitions, and Follow Crew camera handoffs.

Respect the established privacy rules for crew quarters.

Keep the ship schematic distinct from security-camera views.

## 7. UMBRA engineering controls

Extend the existing Engineering interface rather than replacing it.

Add a gravity overview showing:

- Generator condition
- Current power availability
- Shipwide gravity summary
- Individual gravity-zone values
- Active warnings
- Fault history
- Maintenance activity

Provide an appropriate zone-selection interface.

Authorized controls may include:

- Adjust gravity target
- Isolate a zone
- Restore normal gravity
- Request inspection
- Request maintenance
- View diagnostics

Control changes must be validated by the authoritative simulation and its permission model. Do not make a cosmetic slider directly rewrite world state without validation. If a command is unavailable, explain why.

### SOL and AI authority
Respect the separately approved SOL symbiotic takeover design. Engineering systems must continue if SOL is absent or all in-game AIs are terminated. Human-operated controls, authorized crew actions and equipment safeguards must not depend on SOL being alive. Do not implement a second AI authority system.

## 8. Equipment wear and failures
Measured persistent wear can depend on operating duration, load, environment, maintenance quality, previous damage and component design. Faults have identifiable causes/consequences. Quiet periods are valid. Integrate causal failures with existing Cascade Engine; no forced emergencies. Routine maintenance can prevent failures.

## 9. Persistence and synchronization
Persist component condition, gravity settings, faults, repair progress, environments, history, relevant object/crew motion. Respect pause/1×/4×/acceleration; use simulated elapsed time. Windows host authoritative; desktop/Android displays agree. Reconnect without duplicate commands or invented telemetry.

## 10. Performance and boundaries
Zone-based gravity, lightweight objects, event-driven updates, efficient cameras and bounded task processing. No rigid-body replacement, map rebuilding, decorative-object microphysics, scripted disasters, drones, major expeditions, new creature incidents or unrelated lore.

## 11. Passes
A baseline/framework/compatibility. B generator/distribution/zones/controls/power. C movement/objects/environment. D physical crew diagnosis/logistics/repair/testing. E existing camera and Engineering controls. F save/load/acceleration/host sync/recovery/performance/failure testing.

## 12. Acceptance tests
1. Healthy zone ~1g. 2. Authorized target affects actual state. 3. Independent neighbor unaffected. 4. Connected power dependencies. 5. Zero-g crew do not ordinary-walk. 6. Real unsecured objects react. 7. Engineer detects/responds to fault. 8. Physical travel to equipment. 9. Source-backed visible repairs. 10. Actual repair outcome. 11. Consistent restoration. 12. Accurate telemetry. 13. Save ongoing work. 14. Acceleration preserves events. 15. Desktop/Android agree (physical versus emulated reported). 16. Existing cameras/personality/transitions/follow retained. 17. No SOL dependency for operations. 18. Extended unforced operation.

## 13. Delivery
Implemented features/files/architecture/migration/tests/results/limitations/performance/run and test instructions; list remaining hardware/manual checks. Report incomplete work instead of decorative mockups. Final objective: a functioning inhabited spacecraft with observable, controllable, maintainable gravity.

The original upload above is verbatim through its truncation. This continuation records the full user-supplied follow-up requirements in condensed form; the complete follow-up in the conversation remains authoritative.
