# ICARUS / UMBRA
# PHASE 4.5 — VISUAL OVERHAUL 2.0 & SYSTEM BOOT
**Implementation instructions for Codex**

## PRIMARY OBJECTIVE

Deliver a substantial, immediately noticeable improvement to the existing ICARUS simulation's visual presentation and startup experience.

Phase 4.4 introduced some visual improvements, but the completed simulation still looks almost identical to earlier versions.

This phase must address that directly.

**Primary goals:**

1. Redesign spacecraft rooms so their functions are immediately recognizable.
2. Improve character anatomy with slightly taller, more naturally proportioned pixel sprites.
3. Rebuild the wheelchair representation and its animations.
4. Convert one of the two existing recreation rooms into a gym.
5. Improve furniture interactions and character movement.
6. Introduce a dedicated ICARUS boot screen with actual initialization progress.
7. Preserve the existing simulation, world state, camera system, and autonomous behavior.

This must be an actual upgrade to the running application, not a separate visual demonstration.

---

## 0. MANDATORY BASELINE AUDIT

Before implementing changes:

1. Inspect the actual repository, current branch, and completed Phase 4.4 implementation.
2. Identify the exact renderer used by the running surveillance cameras.
3. Inspect room definitions, character sprite functions, animations, collision geometry, and camera transforms.
4. Determine whether Phase 4.4's visual changes are active or whether the application is using older rendering code.
5. Check for stale assets, browser caching, duplicate rendering paths, and unused visual components.
6. Verify the current number and identities of recreation rooms.
7. Inspect the startup and authoritative-writer authorization architecture.
8. Capture baseline screenshots of the existing recreation room, corridor, engineering room, and wheelchair character.

Report what was actually found.

Do not claim that an existing feature is implemented unless it can be verified.

Do not build another disconnected renderer.

## 1. VISUAL DESIGN DIRECTION

Preserve the existing detailed side-view pixel-art style.

Maintain the industrial, retro-futuristic science-fiction aesthetic established for ICARUS and UMBRA.

Use a cohesive visual language featuring:

- Dark industrial metals
- Structural wall panels
- Exposed mechanical systems
- Functional lighting
- Industrial flooring
- Distinct room-specific furnishings
- Restrained cyan, amber, and red system indicators
- Visible signs of habitation and equipment use

Avoid generic repeated backgrounds.

The objective is to make the spacecraft feel physically constructed, inhabited, and operational.

Do not change the simulation into a top-down, isometric, or fully 3D game.

## 2. REDESIGN ROOM ARCHITECTURE

Every major room category must have a distinctive visual identity.

Do not accomplish this through color changes alone.

### Engineering

Use substantial machinery, generator housings, conduits, industrial platforms, repair stations, tool storage, and appropriate work lighting.

The room should look mechanically dense and immediately recognizable as engineering.

### Medical

Use examination beds, diagnostic equipment, treatment stations, medical storage, overhead examination lighting, and cleaner architectural finishes.

### Science

Use laboratory benches, specimen storage, analytical instruments, research displays, and scientific equipment.

### Bridge

Use recognizable command stations, navigation consoles, communications equipment, operational displays, and command-oriented architecture.

### Crew quarters

Use bunks, lockers, storage compartments, personal belongings, and variations reflecting the occupants.

Preserve existing privacy restrictions.

### Cargo

Use cargo containers, storage racks, handling equipment, industrial markings, and appropriate open floor space.

### Corridors

Introduce structural variation through intersections, bulkheads, maintenance access, lighting, signage, and utility panels.

Keep corridors physically navigable.

### Security

Use appropriate monitoring stations, equipment storage, controlled-access features, and security workspaces.

All room visuals must correspond to the actual room registry and ship topology.

Do not invent additional rooms solely to showcase artwork.

## 3. RECREATION ROOM CONVERSION

The user believes ICARUS currently has two recreation rooms.

First, inspect the authoritative room registry and confirm this.

If two recreation rooms exist:

**Recreation Room A becomes the Crew Lounge.**

Include:

- Sofas and seating
- Communal tables
- Food and beverage dispensers
- Entertainment displays
- Games or leisure equipment
- Personal relaxation areas
- Warmer, softer lighting

**Recreation Room B becomes the Fitness Center / Gym.**

Include:

- Resistance equipment
- Weight-training equipment
- Exercise bikes or compact cardio equipment
- Training mats
- Lockers
- Hydration station
- Accessible circulation space
- Suitable equipment for characters with different mobility needs

The two rooms must look substantially different.

Do not simply rename one room or recolor its walls.

Preserve existing room identifiers, doors, connectivity, camera assignments, and save compatibility.

If the registry does not contain two suitable recreation rooms, report the discrepancy before changing the layout.

## 4. GYM FUNCTIONALITY

The gym should be more than decorative where the existing simulation supports meaningful activity.

Add appropriate autonomous activities such as:

- Exercise
- Stretching
- Resistance training
- Cardio training
- Recovery or rehabilitation activities where appropriate

Characters should physically approach and use available equipment.

Exercise animations must correspond to actual task states.

If the existing simulation has fatigue, conditioning, morale, or wellness systems, integrate with those systems.

Do not invent unsupported numerical fitness benefits.

If advanced fitness mechanics are outside the scope of this phase, implement the room and basic grounded interactions while clearly documenting the deferred mechanics.

Characters should not perform fake exercise animations simply because a camera is watching.

## 5. CHARACTER PROPORTION OVERHAUL

Redesign the existing crew sprite system.

**Target approximately 10–15% taller characters as an initial prototype**, subject to testing.

Do not merely stretch existing sprites vertically.

Improve:

- Head-to-body proportions
- Torso length
- Leg length
- Shoulder structure
- Arm articulation
- Hands and feet
- Seated anatomy
- Clothing construction
- Hair and facial variation

Maintain recognizable pixel-art proportions and readable silhouettes.

Characters should appear slightly more mature and anatomically natural without becoming photorealistic.

### Individuality

Introduce persistent variations in:

- Height
- Build
- Hairstyle
- Hair color
- Clothing
- Uniform details
- Accessories
- Posture
- Movement characteristics

Preserve character identity across cameras and save files.

Do not randomize appearances every time the simulation loads.

## 6. CHARACTER ANIMATION OVERHAUL

Improve movement through articulated sprite animation.

Required states:

- Standing idle
- Walking
- Turning
- Sitting
- Standing up
- Working at consoles
- Carrying equipment
- Using tools
- Repairing machinery
- Eating or drinking where supported
- Exercising
- Entering and exiting rooms
- Using lifts
- Low-gravity movement where supported

Animations should be smoother and less rigid.

Avoid characters sliding across the floor without meaningful leg movement.

Keep animation speed consistent with actual simulation movement.

Respect pause and accelerated simulation time.

Do not fabricate activities for visual effect.

## 7. WHEELCHAIR CHARACTER REDESIGN

The existing wheelchair representation is insufficient.

The character currently appears positioned over two wheels without a convincing wheelchair structure.

Rebuild the representation as a coherent character-and-wheelchair assembly.

### Required geometry

Include:

- Proper seat
- Backrest
- Supporting frame
- Large rear wheels
- Smaller front casters
- Footrests
- Appropriate arm supports
- Correctly positioned seated legs
- Proper hand placement

The character should visibly sit inside the chair.

### Movement

Implement:

- Stationary seated posture
- Wheel rotation
- Propulsion animation
- Turning
- Stopping
- Approaching workstations
- Appropriate seated interactions

Do not reuse standing or walking animations while the character is using the wheelchair.

### Accessibility

Ensure wheelchair navigation respects:

- Door widths
- Corridor clearance
- Lift access
- Turning space
- Workstation approach positions
- Accessible gym equipment

Preserve the character's autonomy and role within the simulation.

Do not remove wheelchair users or automatically teleport them through inaccessible routes.

## 8. ROOM DEPTH AND COMPOSITION

Improve the existing side-view renderer through layered visual composition.

Use:

1. Background structural layer
2. Wall equipment and fixtures
3. Furniture and machinery layer
4. Character and interaction layer
5. Foreground architectural layer
6. Lighting and environmental effects

Use foreground elements selectively to create depth.

Avoid obscuring characters or important activity.

Increase the visual variety of room silhouettes.

Not every room should use the same flat wall, overhead pipe arrangement, and floor tiles.

Preserve accurate collision geometry and camera framing.

## 9. FUNCTIONAL FURNITURE

Connect furniture visuals to actual interaction points.

Characters should:

- Approach seats correctly
- Sit at believable positions
- Face consoles while working
- Stand near machinery during repairs
- Use exercise equipment from appropriate positions
- Navigate around furniture
- Avoid clipping through solid objects

Decorative furniture must not create invisible obstacles.

Functional furniture must remain consistent with actual simulation behavior.

## 10. LIGHTING AND ENVIRONMENTAL DETAIL

Improve room-specific lighting.

Examples:

- Engineering: industrial work lighting
- Medical: clean examination lighting
- Lounge: softer ambient lighting
- Gym: brighter functional lighting
- Corridors: overhead utility lighting
- Bridge: restrained console illumination

Lighting must respect existing ship power and emergency systems.

Do not show fully illuminated equipment when its actual power state should prevent it.

Introduce restrained environmental details such as wear, personal belongings, and maintenance equipment.

Do not fabricate damage or incidents merely for atmosphere.

## 11. ICARUS BOOT SCREEN

Implement a dedicated full-screen startup interface.

The user currently experiences a delay where the Authoritative Writer banner initially displays READ ONLY and the authorization-code interface takes too long to become usable.

Replace this ambiguous startup experience with a proper ICARUS boot sequence.

### Visual design

Use an industrial spacecraft-computer presentation.

Include:

**ICARUS**

UNIFIED WORLD CONTROL SYSTEM

System initialization status

Actual startup stages

Connection status

Authorization status

A progress indicator based on real initialization events

### Startup stages

Where supported by actual host initialization, display:

1. Establishing host connection
2. Initializing simulation kernel
3. Restoring persistent world state
4. Synchronizing ship systems
5. Establishing command authorization
6. Preparing surveillance network

Do not simulate progress using arbitrary delays.

Do not claim systems are initialized before the host confirms readiness.

### Early authorization

Allow the user to enter the authorization code as soon as the authentication service is available.

Do not require all cameras or world graphics to finish loading before showing the authorization interface.

### Completion

When the required simulation systems are operational, display:

**ICARUS ONLINE**

If command authorization is still pending, clearly indicate that separately.

Transition to the main simulation interface automatically when ready.

Do not grant writer access without server verification.

### Failure handling

Provide clear states for:

- Connecting
- Loading
- Authorization required
- Read-only access
- Ready
- Disconnected
- Initialization failed

Show meaningful errors and retry options.

Avoid indefinite loading animations without diagnostic information.

### Compatibility

Support:

- Windows host
- Desktop browser
- Android UMBRA
- Remote connections through Tailscale

Preserve existing security and single-authoritative-writer protections.

## 12. CAMERA SYSTEM PRESERVATION

Maintain:

- Existing detailed pixel cameras
- Camera identities
- Follow Crew
- Manual camera selection
- Surveillance arrays
- Character tracking
- Camera privacy rules
- Actual room geometry
- Consistent world state

The visual overhaul must appear in the cameras currently used by the simulation.

Do not create a separate showcase renderer that is disconnected from live gameplay.

## 13. PERFORMANCE

Improve visual quality without excessive rendering overhead.

Use reusable rendering primitives and cached static layers where appropriate.

Avoid unnecessary redraws of static backgrounds.

Keep multiple simultaneous camera feeds functional.

Maintain acceptable performance on the existing Windows host and Android clients.

Support reduced animation settings where practical.

## 14. REQUIRED IMPLEMENTATION ORDER

### Pass A: Verify active rendering pipeline

Identify the live renderer, inspect previous changes, and eliminate stale or disconnected visual code.

### Pass B: One-room visual prototype

Redesign the existing recreation room into a clearly recognizable crew lounge.

Demonstrate a meaningful difference using the same camera position and zoom as the original.

### Pass C: Character prototype

Implement the slightly taller character design and improved movement.

Demonstrate it beside the original character proportions.

### Pass D: Wheelchair prototype

Implement proper wheelchair geometry, seated posture, and movement.

### Pass E: Complete room redesign

Extend the visual system to engineering, medical, science, bridge, quarters, cargo, security, and corridors.

### Pass F: Gym conversion

Confirm both recreation rooms and convert one into a distinct gym with grounded interactions.

### Pass G: Boot experience

Implement the ICARUS boot screen, real readiness reporting, and early authorization.

### Pass H: Regression testing

Verify simulation functionality, persistence, camera consistency, navigation, and performance.

## 15. MANDATORY VISUAL ACCEPTANCE TESTS

Provide before-and-after comparisons using identical camera positions and zoom levels.

Required comparisons:

1. Recreation room before vs. new crew lounge
2. Second recreation room before vs. gym
3. Engineering before vs. after
4. Medical before vs. after
5. Corridor before vs. after
6. Original character vs. taller redesigned character
7. Original wheelchair vs. redesigned wheelchair
8. Wheelchair idle vs. moving vs. turning
9. Original startup experience vs. new boot screen

**The visual changes must be clearly noticeable at normal camera viewing size.**

Minor color changes, additional wall lines, or small decorative props are not sufficient.

If a room still looks nearly identical to the previous version, it does not pass visual acceptance.

## 16. FUNCTIONAL ACCEPTANCE TESTS

Verify that:

1. Existing rooms retain correct identities and connectivity.
2. Furniture does not obstruct required navigation.
3. Character appearance persists across saves.
4. Characters use appropriate animations for actual activities.
5. Wheelchair movement and accessibility work correctly.
6. Gym equipment is usable where implemented.
7. Room lighting respects power states.
8. Camera feeds display the new renderer.
9. Multiple camera feeds remain performant.
10. Boot status reflects actual host readiness.
11. Authorization becomes available without waiting for nonessential rendering.
12. No unauthorized writer access is granted.
13. Existing Phase 4.3 and 4.4 functionality remains operational.
14. Simulation saves and autonomous behavior are preserved.

## 17. DELIVERY REQUIREMENTS

Provide:

- Implementation summary
- Modified file list
- Renderer architecture changes
- Before-and-after screenshots
- Character and wheelchair demonstrations
- Gym conversion confirmation
- Boot-screen demonstration
- Test results
- Performance observations
- Known limitations
- Deferred functionality

Do not claim completion if the active simulation still uses the previous visuals.

Do not substitute screenshots of a prototype for screenshots from the running application.

## FINAL DIRECTIVE

Phase 4.5 must deliver a genuinely noticeable visual evolution.

ICARUS should look like a functioning spacecraft with distinct rooms, recognizable crew, believable mobility, and meaningful daily activities.

The new boot experience should make startup clear and intentional.

**Preserve the living simulation while substantially improving how it looks and feels.**

## User clarification (supersedes gym conversion)

Registry has A09 Recreation and A03 Observation Lounge. User explicitly chose: **Keep A03; defer gym conversion**. Preserve Observation Lounge, redesign A09 as Crew Lounge, and do not convert another room to manufacture a gym.
