# ICARUS / UMBRA
# PHASE 4.4 — EXPEDITION OPERATIONS
**Implementation brief for Codex**

## Mission

Extend the persistent ICARUS simulation beyond the spacecraft by implementing functional, autonomous expeditions to asteroid 8847-A.

The asteroid must contain both abandoned industrial infrastructure and largely unexplored natural terrain, forming one connected environment.

Crew should physically prepare for missions, depart ICARUS, navigate the asteroid, interact with their surroundings, make discoveries, and return.

Expeditions must operate through the existing autonomous simulation, not scripted cutscenes or teleportation.

Preserve Phase 4.2B's detailed pixel-camera presentation and Phase 4.3's ship operations.

**Primary objective:** Make exploration observable, consequential, and persistent.

---

## 0. Inspect the existing implementation

Before writing code:

1. Inspect the actual repository and active development branch.
2. Read `ICARUS/IDEAS_BACKLOG/README.md`.
3. Confirm the implemented state of Phases 4.2B and 4.3.
4. Identify the authoritative world state, simulation clock, character navigation, task scheduler, equipment inventory, camera system, and save architecture.
5. Reuse existing components instead of creating duplicate systems.
6. Establish regression tests for working ship functionality.

Do not assume Phase 4.3 is complete merely because it has been launched.

If necessary, stabilize critical Phase 4.3 dependencies before extending them.

## 1. Asteroid 8847-A: Persistent exploration environment

Create or extend a spatially coherent asteroid environment with two interconnected categories.

### A. Abandoned industrial infrastructure

Include, where supported by the existing world:

- Mining tunnels and corridors
- Cargo and personnel elevators
- Maintenance shafts
- Machinery and industrial equipment
- Abandoned workstations
- Storage facilities
- Power distribution systems
- Sealed or damaged compartments
- Access points to deeper excavations

Infrastructure should show believable wear, deterioration, and environmental damage.

Functional equipment should depend on actual power, condition, and access.

### B. Natural terrain

Include:

- Natural caverns
- Geological formations
- Narrow passages
- Fissures and chasms
- Mineral deposits
- Unstable rock
- Underground voids
- Unexplored branches

Natural environments should not simply be rectangular ship rooms with different textures.

Use a practical spatial representation compatible with the current renderer and navigation system.

### Connectivity

Industrial and natural environments must connect through real navigable passages.

A mining tunnel might open into a cavern. A damaged elevator might connect upper workings to deeper excavation levels.

Crew cannot pass through sealed walls, collapsed routes, or inaccessible shafts without a supported action.

### World generation

Prefer a deterministic, seeded layout or persistent authored layout compatible with existing canon.

Once discovered or modified, locations must remain consistent across saves.

Do not regenerate explored geography differently after loading.

Preserve existing asteroid locations and established story elements.

## 2. Exploration knowledge and fog of war

Separate the true world state from what characters know.

Track:

- Explored locations
- Surveyed routes
- Known hazards
- Observed equipment
- Discovered passages
- Recorded anomalies
- Unverified reports
- Source and time of discoveries

Crew and SOL should not automatically know the entire asteroid layout.

Knowledge must originate from actual observation, communication, recovered records, or sensor measurements.

A discovered passage should remain on the map, but information may become outdated when conditions change.

Unexplored areas must not reveal hidden objects, creatures, or important story information.

## 3. Autonomous expedition planning

Implement a mission planning system integrated with existing crew autonomy.

Supported mission categories should include:

- Geological survey
- Industrial inspection
- Equipment repair
- Salvage and recovery
- Route reconnaissance
- Scientific sampling
- Investigation of reported anomalies
- Emergency retrieval

A mission should contain:

- Unique mission ID
- Objective
- Assigned personnel
- Destination or search region
- Required equipment
- Expected duration
- Known risks
- Resource budget
- Departure location
- Return plan
- Current mission status

Crew should evaluate whether a mission is feasible before departure.

They may postpone a mission because of unavailable personnel, insufficient supplies, equipment faults, environmental hazards, or competing priorities.

Allow autonomous mission selection according to the existing permission and risk systems.

User intervention should remain possible where authorized.

## 4. Expedition team assembly

Characters should be selected according to actual skills, duties, availability, and relationships.

Potential expedition roles include:

- Expedition leader
- Engineer
- Scientist
- Security specialist
- Medical specialist
- Survey technician

Do not fabricate qualifications to fill a role.

Allow smaller missions when appropriate.

Existing character personalities should influence decisions and teamwork without replacing practical mission requirements.

Characters must physically collect required equipment when available.

## 5. Equipment and supplies

Connect expedition equipment to the existing inventory and logistics systems.

Potential equipment:

- Environmental suits
- Oxygen supplies
- Communication devices
- Portable lights
- Geological scanners
- Sample containers
- Repair tools
- Medical kits
- Navigation equipment
- Portable power supplies
- Safety lines
- Weapons when authorized and available

Track meaningful resource consumption and equipment condition.

A character cannot use equipment that does not exist in inventory.

Suit oxygen, battery life, tool availability, and carrying capacity should affect mission decisions.

Use existing resource definitions where possible.

Do not introduce an unnecessarily elaborate crafting system in this phase.

## 6. Physical departure and return

Expedition members must travel through actual ship topology.

Expected sequence:

1. Receive or accept mission assignment.
2. Gather equipment.
3. Travel to preparation or staging area.
4. Check environmental protection.
5. Move to the appropriate airlock or departure point.
6. Complete supported pressure and safety procedures.
7. Transition into the asteroid environment.
8. Travel to the mission destination.

On return, reverse the appropriate process.

Do not teleport characters from ship quarters directly to a cave.

Use the existing doors, corridors, lifts, and Follow Crew architecture.

If the ship lacks an implemented airlock or surface connection, introduce the smallest coherent extension needed.

Vehicles may be represented through existing infrastructure if present. Do not invent a fully operational rover fleet without implementing its actual behavior.

## 7. Surface and underground navigation

Support navigation through:

- Industrial corridors
- Natural caves
- Uneven terrain
- Narrow passages
- Elevation changes
- Ladders or lifts where modeled
- Damaged or obstructed routes

Movement must account for actual environmental conditions.

Use a scalable navigation system suitable for the existing pixel-camera presentation.

Characters should visibly move between connected locations.

If a route becomes inaccessible, the crew must replan or abort rather than teleport through obstacles.

Navigation and movement should remain consistent at accelerated simulation speeds.

## 8. Environmental hazards

Introduce environmental hazards grounded in actual world conditions.

Potential hazards:

- Low pressure or vacuum
- Oxygen-deficient environments
- Toxic gases
- Radiation
- Extreme temperatures
- Unstable terrain
- Falling debris
- Equipment failures
- Poor visibility
- Communication interference

Hazards should have spatial locations, severity, detection requirements, and possible consequences.

Characters should respond according to their available information and equipment.

A detected hazard may cause the team to:

- Change route
- Deploy protective equipment
- Request assistance
- Continue cautiously
- Abort the mission

Avoid forced accidents and guaranteed dramatic outcomes.

Do not implement major new creature encounters during this phase.

## 9. Expedition decisions and autonomy

Expedition teams should make decisions using existing personality, knowledge, skill, and risk systems.

Examples:

- A cautious expedition leader may withdraw when oxygen reserves become low.
- An experienced engineer may recognize unsafe machinery.
- A scientist may request additional time to investigate an unusual mineral sample.
- A security specialist may recommend avoiding an unexplored passage.

Decisions must remain grounded in actual available information.

The crew should not possess knowledge from inaccessible areas or future events.

Allow disagreements and changing plans where supported by existing social behavior.

Preserve the user's ability to observe or intervene without forcing intervention.

## 10. Field cameras and observation

Extend the existing detailed pixel-camera system to expedition environments.

Support live-style observation from:

- Expedition body cameras
- Suit-mounted cameras
- Fixed cameras in accessible industrial locations, where actually installed

Drone cameras are a later-phase feature.

Each feed should have meaningful metadata:

- Camera identity
- Associated character or location
- Mission ID
- Simulated timestamp
- Communication status
- Signal quality where modeled

Show only what the camera can actually observe.

Preserve camera continuity and Follow Crew behavior when characters move between ship and asteroid locations.

If a feed becomes unavailable, show an appropriate disconnected or unavailable state.

Do not substitute omniscient views for missing video.

## 11. Important-event recording only

**User-approved policy: Save significant moments, not continuous video archives.**

Live viewing may continue where supported, but persistent recordings must be event-triggered.

Potential recording triggers:

- Significant discoveries
- Unexpected environmental hazards
- Structural collapses
- Unusual sensor readings
- Equipment failures
- Accidents or injuries
- Important mission milestones
- Encounters, when supported by the simulation
- Mission-critical decisions

Implement bounded recording with:

- Short pre-event buffer where feasible
- Post-event capture window
- Configurable significance thresholds
- Storage limits
- Duplicate-event suppression

Avoid saving long stretches of uneventful walking.

### Recording integrity

A saved clip must represent an actual observed or rendered event.

Do not generate fictional footage and present it as an original camera recording.

If video capture is not technically available, save an accurately labeled event record or still image instead.

Do not claim a text event log is recorded video.

Store:

- Camera source
- Mission ID
- Event type
- Simulated timestamp
- Location
- Recording availability
- Capture reason
- Relevant signal interruptions

### Lost recordings

When communication is interrupted, local recording may continue if the device remains operational.

Recordings stored on an inaccessible device should not automatically appear in UMBRA's central archive.

If the device is later recovered and its storage survives, its saved evidence may become available.

This will also support future drone recovery missions.

## 12. UMBRA expedition interface

Extend UMBRA with an expedition operations view consistent with the existing visual language.

Include:

- Active missions
- Mission objectives
- Assigned crew
- Current mission status
- Known route
- Equipment and supplies
- Environmental warnings
- Available camera feeds
- Significant field recordings
- Mission history

Provide authorized actions to:

- Inspect a mission
- Request or approve a mission
- Review equipment readiness
- Follow an expedition member
- View available cameras
- Recall a team
- Review mission reports

Commands must operate through the authoritative simulation.

Do not create decorative controls that falsely claim to affect the world.

Desktop and Android UMBRA must reflect the same underlying mission state, with responsive layouts appropriate to each device.

## 13. Scientific discoveries and evidence

Expeditions may discover:

- Geological formations
- Mineral deposits
- Damaged equipment
- Abandoned infrastructure
- Previously unknown passages
- Environmental anomalies
- Recoverable artifacts

Discoveries should be based on actual modeled objects and locations.

Preserve the distinction between observation and interpretation.

For example, a sensor may detect an unusual electromagnetic reading without identifying its cause.

Record provenance and uncertainty.

Recovered materials should enter the appropriate inventory or evidence system.

Detailed laboratory research can be expanded in a later phase.

## 14. Preserve established canon

Maintain the existing history of asteroid 8847-A and related locations.

Important constraints:

- The asteroid contains abandoned mining infrastructure and natural environments.
- The deep borehole and its history remain part of the world.
- The military vessel and other derelict locations retain their established roles.
- Rare temporal anomalies may exist but should not become routine scripted encounters.
- Existing dormant threat conditions remain intact.
- No active Xenomorphs should be introduced automatically.
- Do not open sealed containment areas or trigger dormant threats merely to demonstrate expedition functionality.
- Preserve established geography and causal history wherever already implemented.

Do not overwrite existing lore or world data with a newly generated generic asteroid.

## 15. Persistence and simulation timing

Persist:

- Expedition assignments
- Mission status
- Crew locations
- Equipment and supplies
- Exploration progress
- Known maps
- Environmental changes
- Discoveries
- Injuries or equipment damage
- Field recording metadata
- Recovered evidence

Maintain compatibility with existing saves where feasible.

Use the authoritative simulation clock.

Respect pause, normal time, accelerated simulation, and supported holiday/calendar rules.

Ensure missions do not complete instantly because the UI updates slowly or the simulation clock advances incorrectly.

Handle restart and reconnection without duplicating missions or inventory transactions.

## 16. Performance

Maintain reasonable performance with the existing ship crew population and detailed camera feeds.

Prefer:

- Region-based world simulation
- Active-area detail updates
- Efficient pathfinding
- Bounded event buffers
- Camera rendering based on actual observation needs
- Persistent summaries for distant or inactive regions

Do not sacrifice correct simulation state to create visually impressive but fictional activity.

## 17. Implementation passes

### Pass A: Baseline and world architecture

Verify Phase 4.3 dependencies, inspect existing asteroid geometry, and establish persistent exploration regions.

### Pass B: Connected environments

Implement or extend industrial and natural areas with navigable connections and persistent exploration knowledge.

### Pass C: Mission logistics

Implement team assembly, equipment checks, mission objectives, departure, return, and resource tracking.

### Pass D: Autonomous exploration

Implement route navigation, hazard evaluation, mission decisions, discovery, and abort behavior.

### Pass E: Camera integration

Extend detailed pixel cameras to field environments and implement event-triggered evidence capture.

### Pass F: UMBRA operations

Add expedition monitoring, controls, mission reports, and responsive desktop/Android presentation.

### Pass G: Testing and stabilization

Verify persistence, accelerated time, navigation, inventory consistency, camera provenance, and regression behavior.

## 18. Acceptance tests

Demonstrate:

1. An expedition can be created from a valid objective.
2. Crew are selected according to actual availability and qualifications.
3. Required equipment is checked against real inventory.
4. Crew physically travel to the departure point.
5. Environmental protection and departure procedures affect actual state.
6. Crew enter the asteroid without teleporting through disconnected locations.
7. Industrial and natural terrain are both navigable.
8. Crew discover new passages through actual exploration.
9. Unexplored regions remain hidden from ordinary observation.
10. Hazards influence route selection and mission decisions.
11. A mission can be aborted and the crew can attempt a return.
12. Equipment and supplies are consumed consistently.
13. Detailed field cameras show actual expedition activity.
14. Important events produce authentic saved evidence where recording is supported.
15. Ordinary uneventful activity does not create excessive saved clips.
16. Lost communication does not reveal inaccessible recordings.
17. Mission reports reflect real discoveries and outcomes.
18. Save/reload preserves expedition progress and world changes.
19. Desktop and Android UMBRA agree with the authoritative host.
20. Phase 4.3 engineering, gravity, and ship operations remain functional.
21. No active Xenomorph is introduced without the established causal prerequisites.
22. The world can operate without scripted disasters or forced discoveries.

## 19. Delivery requirements

Provide:

- Summary of completed features
- Files modified
- Architecture and data model changes
- Save migration notes
- Test results
- Performance observations
- Known limitations
- Manual testing instructions
- Features deferred to Phase 4.5

Clearly distinguish implemented functionality from prototypes and future plans.

## Final objective

**ICARUS must support believable autonomous expeditions that physically connect the ship to asteroid 8847-A.**

The crew should prepare, travel, explore, react, discover, and return through the same persistent world.

The improved pixel cameras should allow the user to witness these events, while the evidence system preserves only meaningful recorded moments.

The asteroid must feel like a real place with history, geography, operational constraints, and mysteries, not a sequence of disconnected scripted scenes.