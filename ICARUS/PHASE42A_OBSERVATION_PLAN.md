# ICARUS / UMBRA
# PHASE 4.2A — OBSERVATION PROTOCOL
## Living Crew, Detailed Pixel-Art Surveillance & Ship Systems

**Development status:** Approved for implementation  
**Repository:** `thekiddam-code/munza69`  
**Target:** Existing ICARUS / UMBRA application  
**Priority:** Watchable simulation  
**Visual reference:** Aliens: Infestation (Nintendo DS), Alien vs. Predator (SNES), Prometheus and Alien: Covenant interfaces

---

# 0. MISSION DIRECTIVE

Implement Phase 4.2A as a complete, testable upgrade to the existing ICARUS simulation.

This is not a new project, a standalone graphics demonstration, or a replacement for the existing application.

**The goal is to transform ICARUS into a visually observable, autonomous, persistent spaceship simulation.**

A user should be able to:

1. Launch ICARUS on the Windows host.
2. Open the existing UMBRA command bridge.
3. Select a security camera.
4. Watch crew members move, work, converse, rest, and respond to events.
5. Switch between multiple live camera feeds.
6. Inspect rooms through an interactive ship cutaway.
7. Examine crew profiles and activities.
8. Leave the simulation operating autonomously.
9. Return later and find that the world has continued consistently.

Prioritize observable behavior over additional simulation complexity.

**Do not add new world regions, large story systems, or unrelated features during this phase.**

---

# 1. REPOSITORY INSPECTION AND SAFETY

Before modifying code:

- Inspect the repository and identify the newest relevant ICARUS development branch.
- Do not assume older Phase 4 or Phase 4.1 branches represent the current build.
- Identify the authoritative simulation engine.
- Locate crew behavior, pathfinding, rendering, camera, cutaway, and dashboard code.
- Identify save/load mechanisms and schema versions.
- Identify the UMBRA remote telemetry and command architecture.
- Identify Bridge Mode and Creator Mode restrictions.
- Identify existing animation and performance settings.
- Inspect the current GitHub ideas backlog.

Backlog location:

`ICARUS/IDEAS_BACKLOG/README.md`

Create a dedicated Phase 4.2A development branch from the correct current baseline.

Preserve existing functionality and saved voyages.

Do not replace the entire application or reorganize unrelated modules unnecessarily.

Create a baseline build and record current behavior before changing rendering systems.

Where implementation details differ from this specification, adapt to the existing architecture and document the decision.

---

# 2. AUTHORITATIVE SIMULATION ARCHITECTURE

The Windows host remains the authoritative simulation.

UMBRA is a remote observation and control interface.

There must never be separate independently evolving worlds for:

- Windows ICARUS.
- Browser-based ICARUS.
- UMBRA on Android.
- Security camera previews.
- Cutaway displays.

All views must derive their information from the same world state.

Use a consistent identity for:

- Crew members.
- Rooms.
- Equipment.
- Cameras.
- Activities.
- Biological entities.
- Ship systems.
- Simulation timestamps.

Where interpolation is needed for smooth animation, interpolation may alter presentation but not authoritative positions or outcomes.

If the remote device disconnects, display a stale/disconnected state rather than silently creating another simulation.

Reconnection should restore the current world state without resetting the simulation.

Keep simulation time independent from display frame rate.

---

# 3. DETAILED 16-BIT PIXEL-ART CAMERA GRAPHICS

## 3.1 Approved visual direction

Use detailed, 16-bit-era pixel art for security camera scenes.

Primary artistic references:

**Aliens: Infestation — Nintendo DS**
- Industrial spaceship corridors.
- Detailed environmental tiles.
- Compact, readable character sprites.
- Layered backgrounds.
- Atmospheric lighting.
- Machinery and environmental animation.

**Alien vs. Predator — Super Nintendo**
- Readable character silhouettes.
- Creature proportions and poses.
- Expressive motion.
- Animation timing.
- Distinct character states.

These games are visual and technical references only.

Create original ICARUS graphics, sprite sheets, animations, and environments.

Do not copy or distribute proprietary game sprites, extracted backgrounds, ROM data, or copyrighted source code without appropriate permission.

## 3.2 Rendering style

Implement:

- Crisp pixel-art scaling.
- Nearest-neighbor filtering.
- Consistent pixel density.
- Layered room backgrounds.
- Animated equipment.
- Distinct foreground and background elements.
- Appropriate occlusion.
- Directional lighting.
- Restrained atmospheric effects.

Avoid blurry textures and inconsistent sprite scaling.

Use a logical internal rendering resolution appropriate to the camera aspect ratio, then scale cleanly.

Do not force the entire application to run at a retro resolution.

Only the simulated camera scenes should use pixel art.

## 3.3 Character sprite specifications

Initial target sprite dimensions:

- Standard crew: approximately 32×48 to 48×64 pixels.
- Larger characters and creatures: variable dimensions appropriate to their actual proportions.

These are starting guidelines, not fixed constraints.

Each character should support reusable animation states:

| State | Visual requirement |
|---|---|
| Idle | Breathing, subtle posture changes |
| Walking | Directional movement cycle |
| Turning | Orientation change |
| Searching | Looking around, scanning surroundings |
| Talking | Gestures, facing conversation partner |
| Listening | Attention and response gestures |
| Working | Equipment-specific interaction |
| Repairing | Tool-use animation |
| Examining | Inspection gestures |
| Sitting | Seated pose |
| Eating | Dining gestures |
| Resting | Rest or sleep pose |
| Alert | Increased attention |
| Fear | Contextual defensive reaction |
| Injured | Appropriate reduced mobility |
| Emergency | Urgent task-driven movement |

Not every character requires unique animation artwork.

Use shared animation sets with character-specific appearances and optional personality variations.

Character identity must remain visually recognizable.

## 3.4 Character appearance

Use original visual variations for:

- Uniforms.
- Clothing.
- Hairstyles.
- Equipment.
- Role identification.
- Character proportions.
- Posture and movement.

Characters should not all appear identical.

Avoid generating hundreds of unique sprite sheets immediately.

Start with a reusable sprite architecture that can support additional character variations later.

---

# 4. CREW MOVEMENT AND ACTIVITY ANIMATION

## 4.1 Core principle

**The animation must reflect what the character is actually doing.**

The simulation should not report an activity that has no understandable visual representation when that character is visible.

If a character is repairing equipment, they should move toward the equipment and interact with it.

If a character is looking for someone to talk to, they should behave accordingly.

Do not use unrelated random animations to create the illusion of activity.

## 4.2 Movement

Improve existing navigation and rendering to support:

- Movement between rooms.
- Movement toward specific interaction points.
- Turning toward targets.
- Approaching other characters.
- Avoiding obvious overlapping.
- Waiting for occupied interaction points.
- Navigating around furniture.
- Handling blocked routes.
- Interrupting and resuming tasks.

Movement must remain synchronized with authoritative crew locations.

If the existing simulation uses room-level rather than coordinate-level movement, introduce a compatible visual position layer without inventing independent crew behavior.

## 4.3 Interaction anchors

Rooms should define logical interaction locations.

Examples:

- Engineering workstations.
- Medical beds.
- Dining tables.
- Bridge consoles.
- Research equipment.
- Storage shelves.
- Doors and access panels.
- Conversation areas.

Characters should approach these locations before performing corresponding animations.

## 4.4 Conversation behavior

Implement a visible social interaction sequence.

A crew member searching for conversation should:

1. Determine whether suitable conversation partners exist.
2. Look around or move toward an appropriate location.
3. Approach an available character.
4. Face that character.
5. Initiate the interaction if permitted by both characters' actual states.
6. Display talking and listening animations.
7. Respond to interruptions.
8. Return to an appropriate activity afterward.

A failed attempt should also be observable.

For example, the character might wait, look around, and move elsewhere.

Do not fabricate a successful conversation.

## 4.5 Iris Bell regression scenario

During user testing, Iris Bell was reported as searching for a conversation while standing motionless.

Treat this as a specific regression test.

The upgraded simulation must visibly distinguish:

- Looking for conversation.
- Approaching someone.
- Waiting for an available partner.
- Actively conversing.
- Giving up or changing activities.

The activity log and visible state must agree.

## 4.6 Work animations

Prioritize existing crew activities:

- Engineering repairs.
- Equipment inspection.
- Console operation.
- Research.
- Medical examination.
- Cleaning.
- Inventory handling.
- Eating.
- Resting.
- Patrols.
- Emergency response.

Connect animations to real task states and task completion.

---

# 5. ROOM GRAPHICS AND ENVIRONMENTS

Build reusable pixel-art room components.

Prioritize existing rooms rather than creating new areas.

## 5.1 Engineering

Include recognizable:

- Machinery.
- Consoles.
- Pipes.
- Cables.
- Diagnostic displays.
- Tool stations.
- Maintenance access points.

Equipment activity should correspond to actual system state.

## 5.2 Medical

Include:

- Examination beds.
- Medical monitors.
- Diagnostic equipment.
- Storage.
- Workstations.

## 5.3 Bridge

Include:

- Navigation stations.
- Command consoles.
- Crew workstations.
- Operational displays.

## 5.4 Mess hall

Include:

- Tables.
- Seating.
- Food stations.
- Common areas.

## 5.5 Corridors

Include:

- Doors.
- Bulkheads.
- Signage.
- Lighting.
- Access panels.
- Environmental details.

## 5.6 Environmental effects

Where supported by simulation state:

- Lights switch on and off.
- Consoles display activity.
- Emergency lighting activates.
- Equipment displays fault indicators.
- Smoke or atmospheric effects appear during relevant incidents.

Avoid fake emergencies or unrelated visual effects.

---

# 6. OPEN-SOURCE RENDERING RESEARCH

Before selecting a new rendering library, evaluate the existing renderer.

Investigate:

**LittleJS**
https://github.com/KilledByAPixel/LittleJS

Potential uses:
- Sprite rendering.
- Tile layers.
- Pixel scaling.
- Lightweight browser graphics.
- Animation handling.

**Phaser**
https://github.com/phaserjs/phaser

**Phaser examples**
https://github.com/phaserjs/examples

Potential uses:
- Sprite-sheet animation.
- Tilemaps.
- Camera systems.
- Scene composition.
- Performance optimization.

**Excalibur.js**
https://github.com/excaliburjs/Excalibur

Potential uses:
- Character actors.
- Animation state organization.
- Scene and entity management.

**Pixelorama**
https://github.com/Orama-Interactive/Pixelorama

Potential uses:
- Creating original sprite sheets.
- Animation frames.
- Palette management.
- Asset export.

## 6.1 Decision rules

Do not automatically install every library.

Compare:

- Compatibility with the existing application.
- Rendering performance.
- Dependency footprint.
- Mobile support.
- Animation flexibility.
- Integration complexity.
- Maintenance burden.
- License compatibility.

Prefer improving the current renderer if it can meet the requirements.

If adopting another library, use it as a rendering component rather than replacing the authoritative simulation.

Preserve required license notices and review the licensing of every imported file.

Do not assume that open-source example artwork is freely reusable.

## 6.2 Prototype requirement

Before converting the entire ship:

Create one detailed room with:

- Two recognizable crew members.
- Walking animations.
- Conversation behavior.
- One equipment interaction.
- Environmental lighting.
- Working camera rendering.

Test it using actual simulation events.

Once validated, extend the reusable system to the rest of the ship.

---

# 7. LIVE CAMERA SURVEILLANCE ARRAY

## 7.1 Main monitor

Preserve the existing primary camera display.

It should remain the largest monitor.

Display the currently selected camera and relevant metadata.

## 7.2 Four rotating preview monitors

Add four smaller camera monitors.

On narrow screens, use a responsive arrangement.

The preview monitors should rotate through authorized available cameras.

Default rotation interval: **12 seconds**.

Provide:

- Automatic rotation.
- Pause/resume rotation.
- Next camera bank.
- Previous camera bank.
- Camera labels.
- Connection and availability indicators.

## 7.3 Click-to-promote

Selecting any preview switches the main monitor to that camera.

The main monitor remains on the selected camera until changed by the user.

Preview rotation must not automatically replace the primary feed.

## 7.4 Preview pinning

If practical, allow individual preview monitors to be pinned.

Pinned previews remain fixed while other previews continue rotating.

This is secondary to basic camera operation and performance.

## 7.5 Rendering consistency

All monitors must show the same authoritative world.

Camera previews may use:

- Reduced internal resolution.
- Lower frame rate.
- Simplified visual effects.
- Shared scene assets.

Do not spawn separate world simulations.

Do not fabricate camera footage.

## 7.6 Camera metadata

Where supported, display:

- Camera ID.
- Room name.
- Coverage status.
- Connection status.
- Recording status, only if recording actually exists.
- Relevant alerts.

Avoid displaying REC indicators if no recording mechanism is active.

## 7.7 Privacy

Ordinary security cameras must not cover crew quarters.

Private quarters must not appear in standard camera selection or preview rotation.

Keep covert surveillance separate from ordinary security functionality.

---

# 8. SHIP CUTAWAY REDESIGN

## 8.1 Purpose

The cutaway is an interactive **ship systems schematic**, not a live video feed.

It should display the physical layout of ICARUS and the operational status of its rooms.

Use the existing ship geometry and room data.

Maintain a visually distinct separation between:

- Security cameras: visual observation.
- Cutaway: sensors, systems, controls, and telemetry.

## 8.2 Cutaway display

Show room-level information where available:

- Room name.
- Room designation.
- Lighting state.
- Ambient temperature.
- Atmospheric condition.
- Power state.
- Biological detection.
- Door/access status.
- Hazard warnings.
- Camera coverage indicator.

Use compact technical overlays.

Allow room selection, zooming, and panning.

## 8.3 Quick controls

Include a small set of room controls directly on the cutaway.

Prioritize:

- Room focus.
- Lighting on/off.
- Brightness where supported.
- Alert inspection.
- Advanced room controls.

Do not display working-looking controls that cannot actually affect the simulation.

## 8.4 Focused room interface

Selecting a room opens a more detailed systems panel.

Potential controls and telemetry:

**Lighting**
- Brightness.
- Lighting presets.
- Emergency lighting.

**Environment**
- Current temperature.
- Target temperature.
- Atmospheric pressure.
- Oxygen.
- Carbon dioxide.
- Ventilation.
- Contamination.

**Power**
- Equipment status.
- Power consumption.
- Circuit state.

**Security**
- Door status.
- Access controls.
- Access history.
- Camera availability.

**Safety**
- Fire suppression.
- Emergency isolation.
- Environmental hazards.

Only implement systems that have genuine backing state.

Unsupported features should be read-only, clearly unavailable, or deferred.

## 8.5 Biological detection

The cutaway should distinguish between:

- Registered crew.
- Detected biological signatures.
- Unknown or unclassified signatures.
- Sensor uncertainty.

Example:

Engineering:
- Registered crew: 2.
- Biological returns: 3.
- Unclassified returns: 1.

This must be derived from real simulation state and sensor capabilities.

Do not automatically identify unknown creatures.

Allow for sensor limitations, false readings, and environmental interference only where these behaviors are modeled.

SOL must not become omniscient through this feature.

## 8.6 Crew quarters privacy

Crew quarters should appear as private rooms in the schematic.

They may display appropriate environmental and occupancy readings.

They must not provide standard security-camera footage.

---

# 9. CREW LOCATION QUICK-ACTION MENU

Add a three-dot menu to crew entries in the Crew Location panel.

The menu should offer shortcuts to existing relevant features.

Include where available:

- Locate crew member.
- Open available live camera.
- Psychological profile.
- Biography.
- Current assignment.
- Activity history.
- Relationships.
- Relevant personnel records.

Do not expose restricted information merely because a menu exists.

Respect Bridge Mode, Creator Mode, and in-universe access permissions.

If a crew member is in an area without camera coverage, show an appropriate unavailable state.

Menus must work with mouse, touch, and keyboard.

---

# 10. HOME DASHBOARD REPAIRS

## 10.1 Collapsible widgets

Remove separate collapse buttons from Home widgets.

Clicking a widget header should collapse or expand it.

Preserve:

- Widget layout.
- Widget state.
- Custom positioning.
- Keyboard accessibility.
- Touch interaction.

Header controls must not accidentally trigger collapse.

## 10.2 Locked Autonomous overlay

Investigate the Locked Autonomous header obstructing the Focus button.

Remove the unnecessary blocking overlay or relocate essential status information.

The Focus button must remain accessible.

A screenshot may be provided later to reproduce the exact issue.

## 10.3 Custom scrollbars

Restore themed UMBRA scrollbars.

Use:

- Dark tracks.
- Slim cyan/teal thumbs.
- Subtle hover feedback.
- Adequate contrast.
- Consistent behavior across supported browsers.

Avoid breaking normal scrolling.

Resolve nested scrolling problems where practical.

Do not allow panels to jump unexpectedly when interacting with crew profiles or controls.

---

# 11. UMBRA VISUAL IDENTITY

Preserve the approved dark science-fiction interface.

Primary design references:

- Prometheus.
- Alien: Covenant.
- Weyland-Yutani industrial systems.
- Existing UMBRA visual language.

Suggested colors:

| Element | Hex |
|---|---|
| Main background | #080D10 |
| Dark panel | #12313A |
| Cyan instrumentation | #25DCCB |
| Mint highlights | #7CE9A9 |
| Amber warnings | #FFAC48 |
| Primary text | #D9F4F1 |

Use sharp geometric panels, restrained illumination, compact technical labels, and functional instrumentation.

Keep the detailed 16-bit graphics inside the security camera scenes.

Do not turn the entire dashboard into pixel art.

Preserve animation controls, including reduced-motion options.

---

# 12. BRIDGE MODE, CREATOR MODE, AND SOL

Preserve the existing separation between Bridge Mode and Creator Mode.

**Bridge Mode**
- Normal ship operations.
- Cameras.
- Cutaway.
- Crew observation.
- Authorized room controls.
- SOL interactions.

**Creator Mode**
- Debugging.
- Simulation overrides.
- Forced testing scenarios.
- Administrative controls.
- Development tools.

Ensure Pause/Resume and the ship clock remain visible in their intended locations.

Do not accidentally hide normal bridge controls behind Creator Mode restrictions.

Preserve SOL's limited knowledge.

SOL should only know information available through its actual sensors, records, communications, and observations.

---

# 13. DEFERRED: CLASSIFIED SOL OPERATIONS

Preserve the idea of restoring the earlier Linux-style secret menu as a classified SOL Operations interface.

Potential future functions:

- Secret corporate missions.
- Covert surveillance.
- Hidden investigations.
- Restricted sensors.
- Unauthorized observations.
- Classified directives.
- Detection and consequences.

This should be an in-universe system, not a replacement for Creator Mode.

Do not implement it during Phase 4.2A if doing so would delay the watchable simulation.

Record any further ideas in the GitHub backlog.

---

# 14. SIMULATION PERFORMANCE

Target approximately 20 active crew members.

The system should support:

- One primary camera.
- Four rotating camera previews.
- Autonomous crew activity.
- Detailed pixel-art environments.
- Ship cutaway telemetry.
- Remote UMBRA access.

Use performance-conscious techniques:

- Sprite batching or equivalent optimizations.
- Shared assets.
- Efficient animation updates.
- Lower preview update rates.
- Visibility-aware rendering.
- Avoiding unnecessary offscreen work.
- Separating simulation ticks from rendering frames.

Measure:

- Main camera frame rate.
- Preview rendering cost.
- Simulation tick performance.
- Memory usage.
- Mobile responsiveness.
- Remote bandwidth where applicable.

Do not silently reduce simulation correctness to improve graphics performance.

---

# 15. SAVE COMPATIBILITY AND REMOTE ACCESS

Preserve existing saves.

Do not reset the crew roster, relationships, history, world state, or persistent consequences.

Keep the existing Windows companion server and UMBRA connectivity functioning.

Test both local-network and Tailscale access where the test environment supports them.

The phone must not create a second simulation.

If remote testing cannot be completed without physical devices, report that limitation rather than claiming success.

---

# 16. DEVELOPMENT EXECUTION ORDER

Complete the work in the following sequence.

## PASS 1 — Foundation and Pixel-Art Prototype

1. Inspect current code and establish baseline.
2. Evaluate current renderer and open-source alternatives.
3. Choose the least disruptive rendering approach.
4. Build one detailed room.
5. Add two recognizable animated crew members.
6. Connect walking and interaction animations to actual simulation states.
7. Demonstrate a conversation and equipment interaction.
8. Verify save and rendering compatibility.

**Checkpoint:** A working, watchable room with real crew behavior.

## PASS 2 — Camera Array

1. Integrate detailed pixel-art rendering into the existing camera system.
2. Add four rotating previews.
3. Implement click-to-promote.
4. Preserve primary camera selection.
5. Add preview rotation controls.
6. Enforce private-room camera restrictions.
7. Optimize multi-camera rendering.

**Checkpoint:** A functional surveillance wall displaying consistent live simulation activity.

## PASS 3 — Interactive Cutaway

1. Convert cutaway presentation to a ship systems schematic.
2. Connect rooms to real telemetry.
3. Add room focus.
4. Add supported lighting controls.
5. Add advanced room panels.
6. Add biological sensing where the simulation supports it.
7. Verify privacy and sensor knowledge limitations.

**Checkpoint:** A usable deck-management interface, not a simulated video wall.

## PASS 4 — Interface Repairs

1. Implement header-click widget collapsing.
2. Fix the Locked Autonomous overlay.
3. Restore themed scrollbars.
4. Add crew quick-action menus.
5. Resolve relevant navigation and scrolling issues.
6. Test desktop and mobile layouts.

**Checkpoint:** Existing UMBRA functionality remains usable and visually consistent.

## PASS 5 — Integration and Observation Testing

1. Test all systems together.
2. Run extended autonomous simulation.
3. Observe crew movement and interactions.
4. Verify camera switching.
5. Verify cutaway data.
6. Test persistence and reconnection.
7. Measure performance.
8. Fix critical defects.

**Checkpoint:** A stable observation build ready for user testing.

Do not continue expanding scope while core acceptance criteria remain broken.

---

# 17. REQUIRED ACCEPTANCE TESTS

## Test A — Iris Bell conversation

Start a real conversation-seeking activity.

Verify:

- Visible search behavior.
- Movement or meaningful orientation.
- Approach to another character when appropriate.
- Conversation animation if interaction begins.
- Correct handling of failure or interruption.
- Accurate activity records.

## Test B — Engineering repair

Assign or observe a genuine engineering repair.

Verify:

- Character travels to equipment.
- Character faces equipment.
- Appropriate tool or repair animation occurs.
- Activity state changes correspond to task progress.
- Equipment condition updates correctly.

## Test C — Camera rotation

Verify:

- Four previews are available at supported screen widths.
- Preview rotation works.
- Pause/resume works.
- Selecting a preview changes the main monitor.
- Main monitor remains selected.
- Camera footage remains synchronized.

## Test D — Private quarters

Verify:

- Crew quarters are excluded from normal security cameras.
- Private-room feeds do not appear in preview rotation.
- Cutaway displays only permitted telemetry.
- No hidden video access is exposed through ordinary UI.

## Test E — Room controls

Verify:

- Room focus works.
- Real temperature and lighting data are displayed where available.
- Working controls modify actual ship state.
- Unsupported controls are not falsely presented as operational.

## Test F — Crew navigation

Verify:

- Three-dot menu opens.
- Psychological profile shortcut works.
- Live camera shortcut works where coverage exists.
- Unavailable feeds are correctly indicated.
- No accidental scroll jumps occur.

## Test G — Dashboard

Verify:

- Header-click collapse works.
- Separate collapse buttons are removed.
- Focus remains accessible.
- Themed scrollbars work.
- Mobile layout remains usable.

## Test H — Persistence

Verify:

- Save succeeds.
- Reload restores world state.
- Crew identities remain stable.
- Activities resume consistently.
- No duplicate worlds appear.

---

# 18. FINAL MILESTONE — THE WATCHABLE SHIFT

Perform an extended observation test targeting 30–60 minutes of real elapsed time.

Use normal autonomous behavior.

Do not script a fake demonstration.

Observe:

- Crew traveling between locations.
- Work activities.
- At least one genuine social interaction, if naturally available.
- Routine equipment operations.
- Rest or downtime.
- Camera switching.
- Room telemetry.
- Persistence after restart.

Do not force disasters to create excitement.

A quiet shift is acceptable.

If the session cannot be completed automatically, provide a reproducible manual test procedure and report the actual duration tested.

Record defects and remaining limitations.

---

# 19. DELIVERABLES

Provide:

1. Working Phase 4.2A code.
2. Updated camera rendering and animation systems.
3. Updated surveillance interface.
4. Updated cutaway interface.
5. Dashboard repairs.
6. Test results.
7. Performance observations.
8. Save compatibility results.
9. List of incomplete features.
10. Updated GitHub backlog entries.
11. Clear instructions for running the build.

Where appropriate, create a pull request for review.

Do not claim completion for untested functionality.

Do not substitute screenshots or mockups for functioning simulation features.

---

# FINAL DEVELOPMENT RULE

**Build a world we can watch before expanding the world we can imagine.**

Phase 4.2A succeeds when the user can observe believable crew behavior, switch between real camera feeds, inspect functioning ship systems, and return to a persistent simulation that continues to make sense.

Prioritize reliability, animation readability, authentic behavior, and observable results over additional features.