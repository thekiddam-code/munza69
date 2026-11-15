# ICARUS PHASE 4.7
## FORWARD OPERATIONS, FUC MOBILE & DRONE SURVEILLANCE

### Mission

Expand the existing Phase 4.6 simulation into a fully functioning autonomous expedition support system.

Implement:

1. FOC-01, the FUC Mobile
2. Expanded cargo bay camera coverage
3. Deployable asteroid field camp
4. Autonomous drone charging and escort rotations
5. Live, animated drone cameras
6. Improved asteroid and facility visuals
7. Event-triggered video recordings and historical archive
8. Reorganized Surveillance interface
9. Crew expedition integration
10. Persistent field logistics and autonomous operations

**Important:** Phase 4.6 is complete. Inspect and extend the actual existing systems. Do not rebuild working functionality unnecessarily.

Preserve existing voyage saves, world history, crew autonomy, ship systems, asteroid geography, and simulation canon.

---

## PART 1 — FOC-01: THE FUC MOBILE

### Vehicle identity

Official designation: FOC-01 Mobile Field Operations Center.

Crew nickname: The FUC Mobile.

The vehicle is approximately the size of a box truck, substantially larger than an ordinary van.

Visual appearance:

- Rugged, industrial, utilitarian
- Slightly improvised and battered
- Mismatched panels and field repairs
- Functional exterior storage racks
- Foldout equipment compartments
- External lighting and communications equipment
- Appropriate wheels, suspension, and terrain clearance

The vehicle should look questionable but be surprisingly capable.

### Starting condition

FOC-01 begins aboard ICARUS as original expedition equipment.

It is:

- Operational
- Stocked with basic field supplies
- Fueled or charged
- Equipped with medical, survival, and reconnaissance equipment
- Ready for deployment

It must not begin already deployed.

The crew may autonomously deploy it when mission requirements justify establishing a field camp.

FOC-01 is a persistent physical vehicle, not a menu action or instantly spawning structure.

Its condition, location, supplies, cargo, and deployment state must survive save/reload.

---

## PART 2 — CARGO BAY & VEHICLE PARKING

Inspect the existing ship topology and cargo bay dimensions.

The cargo bay should already be one of the larger ship compartments.

Create a dedicated parking position for FOC-01 within that existing space.

Include:

- Appropriate vehicle clearance
- Marked parking area
- Wheel restraints or docking fixtures
- Charging or service connections
- Loading space
- Nearby supply storage
- Physically valid departure route

Do not shrink the vehicle or stretch the room artwork to create the illusion of space.

If the current room geometry cannot accommodate the vehicle, adjust the actual geometry and related navigation consistently, preserving existing room connections and save compatibility.

### Cargo bay surveillance

Improve camera coverage for the room's actual dimensions.

Implement:

- Wide cargo bay establishing camera
- Optional loading/service camera
- Accurate vehicle scale
- Visible crew loading and preparation
- Consistent character positions between camera views
- Empty parking position when FOC-01 is deployed

Use the Phase 4.5 visual improvements as the baseline.

---

## PART 3 — DEPLOYABLE FIELD CAMP

FOC-01 transports equipment to a physically reachable asteroid location.

The crew must select a viable site, travel there, and establish the camp through simulated activity.

### Camp equipment

Include:

**Medical station**
- Deployable medical tent
- Emergency treatment equipment
- Medical supplies
- Patient stabilization capability

**Living and survival**
- Sleeping tents
- Environmental shelter
- Camping equipment
- Food and water
- Oxygen and life-support supplies appropriate to the asteroid environment

**Transportation**
- Four-wheelers or compact all-terrain vehicles
- Cargo transport equipment
- Vehicle charging or fuel supplies
- Maintenance tools

**Drone operations**
- Charging and docking stations
- Drone maintenance equipment
- Spare parts
- Local mission scheduling
- Communications relay

**Security**
- Deployable perimeter sensors
- Surveillance cameras
- Floodlights
- Alarm equipment
- Autonomous security patrol coordination

**Logistics**
- Supply storage
- Portable power
- Repair equipment
- Geological sample storage
- Communications equipment

All deployed equipment must exist as persistent world objects with relevant location, condition, resource, and operating states.

### Camp setup

Crew should physically perform appropriate setup activities.

Deployment consumes simulated time and available resources.

Allow camp operation, maintenance, resupply, packing, relocation, and recovery.

Do not teleport equipment or instantly establish a complete camp.

---

## PART 4 — EXTERIOR-ONLY CAMP VISUALS

Do not create interior camera views for the FUC Mobile or any tents.

Show occupancy and activity through exterior effects.

Examples:

- Medical tent fabric illuminated while treatment is underway
- Actual crew silhouettes moving behind tent walls
- Sleeping tent lights dimming as occupants settle down
- Command tent equipment glow
- FUC Mobile cabin and dashboard lights when occupied
- Exterior work lights when equipment is being used
- Security beacons and perimeter lighting at night

These visual effects must reflect actual simulation states.

Do not generate silhouettes for nonexistent occupants.

Respect power failures, damaged equipment, and visibility conditions.

The simulation should track interior tasks and occupancy without requiring rendered interior geometry.

---

## PART 5 — AUTONOMOUS DRONE OPERATIONS

The FUC Mobile functions as a forward drone operations center.

When deployed, drones should be able to:

- Launch directly from the field camp
- Return for charging
- Undergo maintenance
- Conduct reconnaissance missions
- Escort crew expeditions
- Patrol the camp perimeter
- Investigate reported anomalies
- Support search-and-rescue operations when feasible

The FUC Mobile should coordinate with SOL and existing expedition systems.

Local drone operations must respect actual power, battery, signal, maintenance, and supply constraints.

### Automatic escort rotation

When an escort drone approaches its safe battery reserve:

1. Calculate whether a charged replacement is available.
2. Verify that the replacement can reach the expedition.
3. Launch the replacement from the field camp.
4. Navigate to the crew's actual location.
5. Establish overlapping camera coverage where feasible.
6. Transfer escort responsibility.
7. Return the outgoing drone to the nearest viable charging station.

If a safe handoff is impossible, report the coverage gap and allow appropriate autonomous safety decisions.

Never teleport replacement drones or fabricate continuous surveillance.

---

## PART 6 — LIVE DRONE CAMERAS

This is a required Phase 4.7 deliverable.

Extend the existing Phase 4.6 drone camera implementation into continuously updating, animated surveillance views.

### Camera requirements

- Show the drone's actual current location.
- Update as the drone physically moves.
- Display nearby crew and equipment when visible.
- Use the existing authoritative world state.
- Support moving camera framing.
- Display real battery and signal status.
- Reflect lighting, obstructions, and environmental conditions.
- Show camera damage or signal interruption accurately.
- Support switching between active drones.

Do not substitute static procedural screenshots for live feeds.

Do not fabricate crew, movement, discoveries, or camera footage.

### Visual improvements

Different locations must look meaningfully different.

Natural caverns should not resemble industrial corridors.

Mining infrastructure should reflect its actual equipment and construction.

Military vessel interiors should have a distinct architectural identity.

Weyland-Yutani facilities should have their own recognizable visual characteristics.

Use actual environment geometry, room purpose, lighting, damage, and equipment placement.

Preserve the existing 2D side-view pixel-art surveillance style and Phase 4.5 improvements.

---

## PART 7 — DRONE EVENT RECORDINGS

Repair the existing event recording implementation.

Current reported problems:

- DRONE-1 recording list begins around Record 13.
- Earlier Records 1–12 are not visible.
- Selecting available recordings displays a procedural still image rather than a playable event clip.

### Investigation

Determine whether missing records were:

- Filtered out
- Archived
- Overwritten
- Deleted by retention rules
- Stored locally on the drone
- Never captured as footage
- Lost through persistence or indexing errors

Recover existing data where possible.

Do not invent missing recordings or silently renumber historical events.

### Playable event recordings

Implement short, genuine event-triggered clips using actual captured simulation frames.

Include:

- Pre-event buffer when technically feasible
- Event timestamp
- Camera source
- Location
- Event classification
- Play/pause/replay controls
- Clear footage availability status

Use bounded recording duration, frame rate, and storage to avoid uncontrolled database growth.

Record meaningful events rather than continuously saving all video.

A disconnected drone may retain footage locally until communication or physical recovery makes it accessible.

Do not misrepresent reconstructed imagery as authentic captured footage.

---

## PART 8 — SURVEILLANCE INTERFACE

Rename the overarching camera interface:

**UMBRA // SURVEILLANCE**

Organize it into three primary categories.

### Sectors

Cameras covering geographic exploration areas:

- Mining tunnels
- Natural caverns
- Surface regions
- Geological formations
- Deep borehole approaches

### Facilities

Cameras associated with actual discovered structures:

- Mining installations
- Weyland-Yutani facilities
- Military vessel
- Other established structures

Do not reveal undiscovered locations.

### Drones

Mobile surveillance:

- Active drone feeds
- Drone battery and signal
- Current assignments
- Escort status
- Recording archive
- Unavailable or lost drones

Integrate FUC Mobile perimeter cameras into the appropriate location and surveillance hierarchy.

Do not create fictional camera feeds merely to populate the interface.

---

## PART 9 — CREW EXPEDITION INTEGRATION

An expedition was previously assigned in Phase 4.6, but crew were not visibly observed on the asteroid or inside the derelict.

Investigate the actual expedition implementation before integrating the field camp.

Verify:

1. Mission assignment
2. Crew selection
3. Equipment preparation
4. Departure
5. Physical travel
6. Arrival
7. Exploration
8. Return

Crew must move through valid connected routes.

The FUC Mobile can support expedition preparation, transport, staging, medical response, and resupply.

Do not simply change crew location labels or teleport characters to destinations.

Show meaningful expedition progress and explain blocked missions.

---

## PART 10 — PERSISTENCE AND SIMULATION PERFORMANCE

All new systems must integrate with the existing authoritative simulation.

Persist:

- FUC Mobile location and condition
- Camp deployment state
- Crew assignments and occupancy
- Equipment and supplies
- Drone locations and battery levels
- Drone missions and rotations
- Camera and recording metadata
- Exploration discoveries
- Damage and repairs

Preserve authoritative-writer exclusivity.

### Catch-up performance

Phase 4.6 previously showed a backlog of approximately 16,000 real seconds at 20× pacing, taking several minutes to process.

Inspect the existing catch-up implementation.

Optimize unnecessary rendering and redundant processing where safe.

Do not skip meaningful events, fabricate outcomes, or advance the clock without simulation.

Keep the browser responsive and report genuine catch-up progress.

---

## PART 11 — DEVELOPMENT STAGES

### Phase 4.7A — Vehicle and cargo bay

- Persistent FUC Mobile
- Dedicated parking location
- Improved cargo bay cameras
- Vehicle preparation and deployment
- Deployable field camp

### Phase 4.7B — Autonomous field operations

- Drone charging and maintenance
- Automatic escort rotation
- Camp security and patrols
- ATV transportation
- Medical and logistical support
- Autonomous expedition coordination

### Phase 4.7C — Surveillance and recording overhaul

- Live animated drone feeds
- Improved sector and facility visuals
- Surveillance interface organization
- Event video recording and playback
- Missing recording investigation
- Expedition camera integration

Implement incrementally, with regression tests between stages.

---

## PART 12 — ACCEPTANCE TESTS

Before reporting completion, verify:

1. FUC Mobile begins aboard ICARUS in its dedicated cargo bay parking position.
2. The vehicle is visible at an appropriate scale on the cargo bay camera.
3. Crew can physically prepare and deploy it.
4. The camp appears in a reachable asteroid sector.
5. Camp occupancy is visible through exterior lighting and silhouettes.
6. Drones can launch, return, recharge, and resume missions from the camp.
7. A low-battery escort drone can be relieved by another drone when feasible.
8. Live drone camera feeds visibly update as drones move.
9. Different sectors and facilities have visually distinct environments.
10. Event recordings can be played as actual captured sequences.
11. The fate of missing Records 1–12 is investigated and reported.
12. Crew expeditions visibly progress through valid physical locations.
13. All major states survive save/reload.
14. Existing ship cameras, world history, and Phase 4.6 systems continue functioning.
15. The application remains usable during catch-up processing.

Provide screenshots from the actual running implementation, not conceptual mockups.

Report confirmed fixes, test results, remaining limitations, and deferred functionality.

**Do not mark Phase 4.7 complete until the live drone camera, autonomous drone rotation, FUC Mobile deployment, and persistent field camp have been verified working.**

---

## CANON AND DESIGN CONSTRAINTS

- Preserve asteroid 8847-A and established ship/derelict geography.
- Preserve existing Xenomorph starting conditions and causal prerequisites.
- No forced disasters or guaranteed discoveries.
- No invented camera footage.
- No teleportation disguised as physical movement.
- Preserve the established 2D surveillance visual style.
- Maintain Spectator and Management modes.
- Keep the gym in the future-development backlog.
- Do not introduce unrelated features or redesign working systems without necessity.

The goal is a functioning, autonomous expedition ecosystem, not merely a collection of new screens.