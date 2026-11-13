# ICARUS / UMBRA — Ideas Backlog

Persistent parking lot for approved concepts, future enhancements, bugs, and experiments. **An idea recorded here is not a claim that it has been implemented.** Review before each phase; move ideas into a phase only when scope and dependencies allow. Preserve old ideas rather than deleting them.

## How to use
- **Proposed**: idea captured, not scheduled.
- **Approved direction**: user likes the concept; implementation not yet promised.
- **Deferred**: known issue or feature deliberately postponed.
- **In progress**: only mark when development actually starts.
- **Implemented**: only mark after code and behavior are verified.
- Add new ideas under a heading, with date, dependencies, and a target phase if known.
- For Codex: consult this backlog during planning, but do not implement every item automatically.

## Visual design language — approved direction (2026-11-11)
Reference: user-supplied images of *Alien: Covenant* physical bridge consoles, *Prometheus* bridge/science/medical screen schemes, and a touch-operated sci-fi display. Original reference images were supplied in chat; they are **not stored in this repository**.

- Near-black/charcoal backgrounds; luminous cyan, blue-green and mint accents.
- Restrained amber for cautions/physical console controls; red for actual danger.
- Thin geometric instrument outlines, compact technical typography, legible numeric readouts.
- Dense but purposeful displays: diagrams, wireframes, scans, waveforms, subsystem telemetry.
- Distinct functional layouts for bridge, engineering, navigation, science, medical, security.
- Animations should communicate scanning, measurement or state changes; adjustable/reduced motion.
- Keep the customizable Phase 4.1 modular bridge, not a return to fixed layouts.
- Suggested *starting* palette (not a hard specification): #080D10 background, #12313A panel, #25DCCB cyan, #7CE9A9 mint, #FFAC48 amber.
- Inspiration only: develop original interface assets, not copies of film graphics.

## Maintenance / deferred
### 4.1.1 — simulation clock and acceleration (deferred 2026-11-11)
- Verify that TEST 20× actually advances **processed simulation time** at 20 simulated seconds per real second, not merely the display.
- Compare simulation ticks, clock progression and any processing backlog.
- Unify ship clock and calendar time sources; add seconds and effective rate indication.
- Preserve automatic 4× normal / 1× holiday behavior.
- Ensure pause/resume remains accessible in Bridge Mode; creator-only speed overrides remain hidden.
- Do not change simulation timing incidentally during Phase 4.2.

### Remote bridge reliability
- Verify that phone UMBRA observes the authoritative laptop simulation, never starts a separate world.
- Host heartbeat, reconnect, stale telemetry labels, command deduplication, save safety.
- Test on LAN and Tailscale. Status requires verification in the installed build.

## Phase 4.2 — Living Ship (planned, not yet verified)
- Task-driven crew movement and animations: tools, repairs, consoles, medical, science, eating, sleeping.
- Persistent routines, needs, habits, shift schedules, task completion and interruptions.
- Friendships, rivalries, romance, gossip, mentorship, conflict, reconciliation and memory.
- Information must travel via actual observation, communication and records; SOL not omniscient.
- Causal incident cascades, realistic containment, and quiet days without forced disasters.
- Real camera observation and evidence for future recaps; no fabricated live footage.
- ~100 registered crew with a smaller active population; performance and save compatibility.

## Observation notes — 2026-11-12 (user testing)
**Current priority: watchable simulation, not expanding lore.** Observations are user-reported and not yet verified in source.

### Next visual/UX pass — prioritize
- **Camera fidelity / observable intent:** Iris Bell was reported as “searching for a conversation” but appeared stationary with minimal detail, movement, or expression. Show intention through plausible motion: orient/look around, walk toward an available person, pause, gesture, begin an interaction, or give up; do not animate actions unsupported by state. Improve poses, expression cues and detail at camera scale. Test with real crew tasks and camera coverage.
- **Crew Location quick actions:** add accessible `⋯` (horizontal or vertical) per-character menu linking to available live camera, psychological profile, assignments/duty history, relationships and other existing relevant records. No fabricated feeds; show unavailable/uncaptured states.
- **Home widgets:** collapse/expand by clicking the widget header; remove separate collapse buttons. Keep keyboard accessibility and avoid triggering collapse from embedded buttons.
- **Overlay collision:** user reports “Locked Autonomous” header blocks the Focus button. Remove unnecessary overlay or reposition it without obscuring controls; screenshot pending.
- **Themed scrollbars:** standard scrollbars returned. Restore dark, slim, cyan/green styled scrollbars with usable contrast, hover/focus and browser fallbacks. Preserve scroll chaining.

### World privacy / camera coverage — design direction
- Crew quarters should be designated **private** and should **not** have ordinary security cameras in cutaway or standard security views.
- Distinguish official surveillance, privacy boundaries, and any later covert SOL capabilities. Do not quietly give standard SOL/crew views omniscient access.

### Deferred lore feature — classified SOL Operations
- Preserve/revive the Linux-style hidden terminal idea as a **secret SOL Operations** menu for covert missions, investigations, and possibly concealed surveillance, including in private quarters.
- Separate from out-of-universe **Creator Mode**. In-universe covert actions should have constraints, detection risks, consequences and clear provenance; not simply omniscient debug controls.
- **Do not implement in the next visual milestone** if it slows watchable crew movement and camera fidelity. Existing lore/implementation status unverified.
- Consider how hidden access is discovered, what evidence exists, and whether it creates meaningful crew privacy/conflict.

### Screenshot evidence — 2026-11-12
- User supplied screenshot of local ICARUS Ship Overview (`/icarus.html#/deck/ship/overview`). The broad **AUTONOMOUS** command strip occupies a full row near the top, containing Release to autonomy, Explain decision, Pause, Automatic 4×, and Incidents controls. The 3-deck cutaway starts substantially below it.
- **UI recommendation:** condense routine simulation state and Pause into an unobtrusive always-accessible header; move debug/autonomy overrides into Creator Mode while retaining any valid in-universe commands. Do not hide essential Pause.
- **Reported defect:** “Locked Autonomous” header obstructs Focus, but the Focus button itself is not visible in this screenshot; inspect actual stacking, sticky positioning, hitboxes, responsive layout before coding the fix.
- Increase usable vertical room for the cutaway without losing important status indicators.

### Acceptance tests for next visual milestone
1. Observe a character seeking conversation: movement or meaningful idle searching must correspond to their state, and a real conversation should animate participants when it happens.
2. Follow a crew member from Crew Location to their camera and psychological profile using `⋯`.
3. Collapse/expand home widgets by header without losing Focus actions.
4. Verify overlay does not block Focus at typical desktop widths.
5. Verify custom scrollbars and natural scroll chaining.
6. Confirm crew quarters have no **official** camera feed; document any covert-camera concept as deferred.

## Cutaway redesign — ship systems schematic (approved direction, 2026-11-12)
**Priority:** design for next visual milestone if feasible; otherwise defer implementation without losing concept.

- The ship cutaway should **not** look like a live security-camera feed. It is a deck/room schematic displaying telemetry, controls, and operational state. Cameras remain a separate system.
- **At-a-glance room overlay:** room name/ID, lighting state, ambient temperature, atmosphere/pressure, power status, occupancy or biological returns, access/door state, hazards and camera coverage indicator. Keep overlays legible; choose compact per-room controls rather than overcrowding the map.
- **Quick controls directly on cutaway:** select room, toggle/adjust lighting where authorized, choose room focus, inspect warnings. Actual changes must flow through ship system state and permissions.
- **Focused room view:** richer light presets and brightness, HVAC target temperature, oxygen/CO2/pressure/contaminants, power circuits, doors/locks, sensor logs, biological classification confidence, security coverage, equipment health. Only implement controls supported by actual simulation state; otherwise show read-only or unavailable.
- **Biological sensing:** distinguish registered crew from detected life signs and unclassified/unknown biological signatures. Count and confidence depend on sensor capabilities, interference, coverage, and actual simulated entities. Do not infer creature identity from a heartbeat alone or expose omniscient world state.
- **Privacy:** crew quarters have no ordinary security cameras. Room environment and occupancy readings can exist without live video; any covert SOL surveillance is a separately deferred in-universe feature, not standard access.
- **Visual standard:** near-black ship blueprint with thin cyan/green room outlines, restrained amber/red alerts, schematic corridors, and responsive zoom/focus interactions.
- **Acceptance:** choosing a room reveals correct room state; authorized controls affect real simulation; no fake readings or video; biological discrepancies can be reported without omniscience; quarters remain camera-private.

## Live Camera module — rotating preview bank (approved direction, 2026-11-12)
**Goal:** watchable surveillance interface; candidate for next visual phase.
- Retain the existing large primary live camera feed.
- Add **3–4 smaller live preview monitors** alongside or below the main feed, adapting to screen size.
- Preview slots automatically rotate through all authorized/available security cameras on a configurable interval (initial design suggestion: 10–15 seconds); include pause and manual next/previous bank.
- Clicking/tapping any preview **promotes that exact camera** into the primary monitor. Main monitor remains pinned until the user selects another feed; preview cycling must not interrupt it.
- Optionally pin one or more preview slots; avoid starving other feeds of rotation.
- Camera names, room identifiers, online/offline/coverage status and actual simulation footage must be consistent across primary and preview monitors. No synthetic footage passed off as live.
- Exclude ordinary crew quarters from standard security camera list and rotation. Covert SOL cameras, if ever implemented, belong to separate classified in-universe interface.
- Keep preview rendering efficient: shared simulation state, lower-resolution previews, no separate world instances; account for bandwidth/performance on UMBRA mobile/Tailscale.
- Future option: prioritize feeds with motion, hazards or incidents without losing coverage of quiet rooms.
- Acceptance: 4 previews cycle independently; tapping a preview switches main feed; main selection stays stable; pausing previews works; private rooms never appear in normal rotation.

## Phase 4.2A camera graphics — detailed 16-bit pixel art (approved, 2026-11-12)
- **Decision:** Use detailed 16-bit-era pixel art inside the security camera feeds. Keep the surrounding UMBRA UI in its near-black, cyan/green Prometheus-inspired technical style.
- **Core milestone requirement**, not just future polish. Characters must be readable, distinguishable, and visibly animated according to real crew state.
- Initial sprite design targets: approximately 32×48 to 48×64 pixels per character, adjustable after testing actual camera scale. Directional walking, idle/turning, talking/gesturing, equipment operation, eating, sitting/resting, reactions.
- Room art: readable silhouettes, appropriate furniture/equipment, industrial ship details and distinct bridge, engineering, medical, mess, corridors, etc.; preserve real ship layout.
- Renderer: nearest-neighbor crisp scaling; restrained lighting, console activity and emergency effects; no blurry scaling. Shared authoritative world for one primary feed and four rotating previews; lower-resolution or lower-frequency previews where needed.
- Implementation order: inspect existing renderer → one fully functional room with two animated crew and equipment → validate real walking/conversation/task animations → integrate camera wall → expand reusable art across rooms.
- Preserve privacy (no ordinary crew quarters security cameras), saves, UMBRA mobile performance, and reduced-motion settings.
- Acceptance: watch real crew actions for an extended shift, identify people and activities visually, and switch between matching live feeds without spawning duplicate simulations.

## Pixel-art research references — approved for study (2026-11-12)
- **Aliens: Infestation (Nintendo DS):** primary reference for detailed 16-bit-era sci-fi ship interiors, smaller character scale, corridor lighting, and environmental detail.
- **Alien vs. Predator (Super Nintendo, 1993):** additional reference for larger character and creature silhouettes, readable poses, animation timing, and enemy visual states.
- Public references identified: https://www.spriters-resource.com/snes/alienvspredator/ (sprite sheets); https://github.com/FitzRoyX/nesrip (SNES/NES tile extraction tool); https://github.com/bogaa/dizProjects (general SNES disassembly research; this title not confirmed). A specific complete SNES AVP source/assets repository was **not verified**.
- Study art direction, palette organization, tile construction, sprite proportions, frame timing, and layering. Create **original** ICARUS art and animations; do not import copyrighted game sprites, ripped backgrounds, ROM content, or proprietary code into the project without appropriate rights.
- Keep scope anchored to Phase 4.2A watchable crew, one-room/two-character prototype, and camera preview consistency. No requirement to reverse-engineer either game before development.

## Open-source 2D/16-bit rendering research (2026-11-12)
**Research only. No engine replacement or code integration approved yet.** Review existing ICARUS renderer before selecting any dependency.

### Highest practical fit for browser-based UMBRA
- LittleJS — https://github.com/KilledByAPixel/LittleJS — MIT; small JS engine, sprite/tilemap/rendering examples. Candidate for low-overhead browser pixel rendering.
- Phaser examples — https://github.com/phaserjs/examples — MIT **code**, but example artwork/audio have separate restrictions. Study camera, sprite animation, tilemap, scene and scaling patterns.
- Excalibur.js — https://github.com/excaliburjs/Excalibur — BSD-2-Clause; TypeScript HTML5 Canvas actors, animations, scenes.
- Pixelorama — https://github.com/Orama-Interactive/Pixelorama — MIT; sprite editing/export tool, not game runtime.

### Other reference engines (less direct to web architecture)
- Tilengine — https://github.com/megamarc/Tilengine — MPL-2.0; retro tile/sprite/layer/raster rendering in native C. Study ideas before attempting integration.
- Flare engine/game — https://github.com/flareteam/flare-engine and https://github.com/flareteam/flare-game — GPL-3.0 engine; CC-BY-SA 3.0 art. Study animation/data-driven entities, beware license obligations.
- Solarus — https://gitlab.com/solarus-games/solarus — GPL-3.0; C++/Lua, maps and interactions.

### Decision criteria
- Prefer smallest proven change that improves observable crew movement, sprite animation, pixel scaling and five-feed camera performance.
- Prototype one room with two actors first; compare frame time, memory and mobile performance against current renderer.
- Maintain one authoritative simulation; rendering libraries may never create independent world state.
- Check license of every code and asset file separately before importing; do not use proprietary Alien game sprites or extracted ROM assets.

## Future phases / unscheduled
### Cinematic surveillance and weekly Sunday recap
- Configurable security wall, focused cameras, real incident clips and labeled reconstructions.
- Seven-real-day anthology, 3–5 minute Sunday recap, notable events, character fates, relationships, awards and SOL assessment.
- Optional **Legendary Kill Cam** only for genuinely extraordinary events, with evidence and rarity thresholds; never force one.
- Optional anthology-style ending variants: absurd closing gag, eerie ending, anthology vignette. These are creative directions, not requests to reproduce copyrighted footage.

### Expedition intelligence / world
- Mission-based autonomous expeditions with opportunities for user intervention.
- Three linked environments: ICARUS, irregular asteroid with pressurized caverns, nearby derelict.
- Temporal anomalies and arrivals, discoveries, local ecosystems, persistent consequences.
- Cascade Engine must propagate only through actual dependencies.

### UMBRA cross-device experience
- Separate responsive phone/tablet layouts, remote drawer that does not obstruct panels.
- Android-native possibilities, desktop companion integration, TV remote and gaming modules.
- Adjustable animations, subtle ship-themed visual effects and optional infestation Easter eggs.
- Keep device remote-control functions separate from the authoritative simulation.

## Process reminders
1. Before starting a new phase, review this file and select a manageable scope.
2. Record ideas that do not fit in the next phase here, with their rationale.
3. Do not silently remove old features or reset existing voyage saves.
4. Mark features implemented only after testing, and link the relevant commit/PR when available.
5. Keep future design ideas separate from bugs and release blockers.

## Phase 4.2B — optional adult relationships and SOL covert surveillance (approved concept)
- Optional non-explicit adult relationship events: confirmed adult participants, mutual willingness, kissing, embracing, fade-to-black, shared bed/resting under blankets, and optional non-sexual nudity in private contexts. No explicit sexual acts or sexual-motion animations.
- Private encounters are real time-bounded, interruptible simulation events, accelerated by simulation clock (e.g. 4×), with plausible relationship and social consequences.
- Sock-on-the-door marker signals privacy to other crew; ordinary bridge/security camera feeds exclude crew quarters.
- **Important user clarification:** SOL **can** access a separate concealed camera feed in crew quarters through a future classified SOL Operations terminal. SOL knowledge is grounded in actual covert camera observations, not omniscience. Keep this feed out of ordinary security monitors and respect its access restrictions. Private intimacy is still presented non-explicitly, using fade-to-black rather than depicting acts.
- Defer implementation until Phase 4.2A watchable crew/camera foundations are working; do not expose classified camera access in Creator Mode as a substitute for the in-universe terminal.

## Phase 4.2B decisions — autonomous relationships, 20× clock, corridor pacing (2026-11-12)
- **Relationships entirely autonomous:** crew choose friendships, attraction, dates, intimacy, breakups, and consequences from personality, history, circumstances, and mutual consent. Creator Mode may inspect/debug but must not directly steer relationship outcomes in normal simulation.
- **Add 20× time acceleration** to existing clock controls (retain pause, 1×, 4×; 10× optional if compatible). Simulation tick, pathfinding, activities, social state, timers, and saves must advance correctly. Separate authoritative simulation time from render FPS; at high speed prevent missed events, teleporting, runaway CPU, or duplicate outcomes. Test pause/resume and return to 1×.
- **Investigate visually slow corridor walking before changing movement speed.** User suspects long in-world hallway is compressed into a single camera image. Compare physical corridor length, world-coordinate walking velocity, projection scale, camera framing, animation cadence, and interpolation. Preserve plausible world speeds; prefer multiple coverage zones/virtual camera framing if projection is the issue. Verify traversal time and visible progress at 1×/4×/20×.

## Phase 4.2B — corridor door visibility and room wayfinding (2026-11-12)
- Corridor camera scenes should visibly include **all actual room doorways connected to that corridor segment** (not arbitrary decorative doors), using authoritative ship topology and deck/segment mappings.
- Each doorway gets a small readable room-type icon, room name and/or designation (e.g., ENG-01, MED-02, CQ-03). Labels scale sensibly with camera zoom and can be abbreviated on preview feeds.
- Crew walk to the **correct mapped doorway**, trigger its real door state/animation, cross the threshold, and transition into the destination room. Ensure camera views and cutaway agree on identity, occupancy and timing.
- Doors must reflect actual locked/sealed/damaged/powered states and cannot be bypassed by cosmetic animations. No camera scene should suggest a room entrance that does not exist in the ship topology.
- For long corridors, diagnose condensed perspective and split into contiguous camera coverage segments where useful, keeping all room entrances represented and preserving travel distance/time.
- Crew quarters retain normal camera privacy; classified SOL-only covert feeds remain separate.
- Acceptance: choose several crew with different destinations, follow their route in corridor cameras, verify each uses the correct labeled door and appears in the correct room; test blocked doors and save/reload.

## Phase 4.2B — personnel lift cameras and continuous deck transitions (2026-11-12)
- Add an interior security camera to every operational personnel lift in the existing ship topology. Use the same authoritative simulation and camera array as corridors/rooms; do not invent lifts or duplicate worlds.
- Crew visibly approach the correct lift, wait if necessary, board when doors open, stand or interact while riding, and exit at the correct deck. Support multiple passengers and different destinations if modeled.
- Camera metadata: lift ID, current deck, target deck/direction, door state, occupant count, and faults where real telemetry exists (e.g., LIFT-02 | DECK 03 → 05 | 2 OCCUPANTS).
- Offer optional follow-person camera handoff: origin corridor → lift interior → destination corridor → destination room (only where ordinary camera coverage is authorized). Respect privacy and camera access restrictions.
- Lift door opening, motion, arrival, and failure states must reflect actual travel mechanics, power, locks and service status. Never animate a lift arriving before the authoritative simulation does.
- Keep preview rotation and manual camera selection functional; lift cameras are included among normal authorized feeds. Optimize to avoid multiplying world updates.
- Acceptance: follow a crew member across two decks via labeled corridor doors and lift cameras, verify passenger occupancy and arrival against cutaway, and test blocked/stalled lift and save/reload.

## UMBRA Simulator — microphone-integrated soundboard (proposed)
- Add a reusable **Soundboard** panel available across UMBRA's **Simulator** game tabs, not a separate ICARUS ship simulation feature.
- Provide customizable buttons that play assigned short audio clips into **game voice chat** via the user's microphone input path, while retaining normal live microphone speech.
- Investigate a Windows companion-server implementation with a **virtual microphone / audio mixing device** (for example, a virtual audio cable or suitable virtual mixer); browser audio playback alone does not automatically reach game voice chat. Verify per-game input-device selection and compatibility.
- Support per-game button layouts/profiles, clip import, naming, icons, volume, stop-all, optional hotkeys, and an easily accessible mute/disable toggle. Persist settings without embedding copyrighted clips in the repository.
- Provide optional push-to-talk coordination, avoid feedback/echo by monitoring output routing, and do not silently capture or transmit microphone audio. Explicitly distinguish playback-to-speakers from routing-to-game-chat.
- Preserve UMBRA's existing PC/Android remote-control architecture: buttons on tablet/phone can trigger authorized playback on the Windows host, while the Windows audio routing delivers the mixed signal to the selected game microphone device.
- Keep latency low, make clipping/overlap behavior predictable, and test with at least one game using voice-chat microphone selection. Account for games that restrict virtual audio devices or require manual input configuration.
- Status: **backlog idea only; not yet implemented**. Decide audio routing and UI details during a future Simulator/UMBRA development phase.

## UMBRA Simulator — hybrid macros and automatic game profiles (approved)
- Use a **hybrid Macros interface**: always-available shared Windows/system controls and live host telemetry plus game-specific command layouts within Simulator tabs.
- Detect the Windows foreground application/game on the companion host and automatically select its associated macro profile, with a clear active-profile indicator, manual override, and safe fallback when no profile matches. Avoid surprising switches while a macro is running.
- Shared controls: common Windows shortcuts, microphone/audio routing status, soundboard controls, stop-all/cancel, power/performance state where available, and user-selected pinned commands.
- Per-game profiles: editable hotkeys, sequences, soundboard clip buttons, push-to-talk configuration, contextual information, and customizable layout. Persist profiles across reconnects; sync tablet/phone views with the host's active profile.
- Macro engine should support single hotkeys and bounded multi-step sequences with configurable delays, visible running status, cancellation, key-release cleanup, and safeguards against triggering in the wrong foreground app. Optional recorder only with explicit activation and exclusion of sensitive typing.
- Telemetry should display only verified host data (e.g., CPU/GPU/RAM, microphone device/state, active app, power mode, macro status); mark unavailable metrics instead of fabricating values. Game-specific stats require a supported integration.
- Integrate with the separately proposed microphone-mixed soundboard; avoid implementing a second audio engine.
- **Status: approved design/backlog, not implemented.** Keep separate from ICARUS ship simulation and avoid disturbing existing remote deck functionality.

## UMBRA Simulator — Discord COMMS integration (proposed)
- Add a shared **COMMS** panel in UMBRA Simulator, accessible from every game tab, with a compact always-available microphone / soundboard control strip. Integrate with the approved hybrid Macros system and auto-selected game profiles.
- **Stage 1: Windows Discord desktop bridge.** Use user-configured Discord keybinds triggered by the existing Windows companion for mute, deafen, push-to-talk and other supported actions. Show control feedback only when verified; don't mistake sent keystrokes for confirmed Discord state. Support manual keybind configuration and prevent shortcuts going to the wrong app.
- **Stage 2: investigate richer Discord integration** through officially supported Discord APIs/SDKs and permissions: voice settings, current voice connection/channel, participants/speaking indicators, activity and server/channel navigation **only where actually supported and authorized**. Do not rely on unsupported private Discord client APIs, self-bots, token extraction, or invasive automation. Clearly distinguish available telemetry from unavailable data.
- **Shared soundboard:** reuse the proposed Windows-host microphone-mixed soundboard with routing targets Discord only, game chat only, both, or local speakers, where configured virtual devices/mixer support them. Avoid duplicate audio engines; prevent feedback and accidental broadcasting.
- Tablet/phone UMBRA buttons remotely control the Windows companion; audio routing happens on Windows. Provide visible microphone status, output destination, stop-all, and a fast disable/mute option.
- **Open design choice:** whether to include full authorized server/channel/friend browsing or focus initially on voice-chat controls; do not treat the deeper integration as approved or technically guaranteed yet.
- **Status:** backlog concept, not implemented. Implement separately from ICARUS Phase 4.2B and preserve existing Simulator functions.

## UMBRA Discord COMMS — priority update
- **Priority: LOWEST / PARKED.** User rarely uses Discord and explicitly wants all Discord COMMS integration ideas deferred behind other UMBRA and ICARUS work. Keep prior Discord concepts for possible future use, but do not schedule or implement unless reprioritized.

## Future world modules — fantasy adaptation (exploration, not approved implementation)
- Once ICARUS has a stable working simulation, explore reusing its autonomous agents, relationships, memories, schedules, event engine, persistence and observation systems for a separate **fantasy world**.
- Architect future changes with a clean distinction between core simulation mechanics and setting-specific presentation/data. Potential mappings: ship rooms to buildings, decks to districts/regions, crew to villagers, jobs to trades, security cameras to an appropriate fantasy observation metaphor.
- A full fantasy simulation requires new domain mechanics (economy, factions, travel, combat, magic, creatures, quests) and is not merely a visual reskin. Preserve the existing ICARUS universe and saves.
- **Status:** exploratory future possibility only; no active development priority or implementation commitment.

## Fantasy world — offline player protection (approved)
- Future D&D-style autonomous fantasy simulation includes Spectator, Dungeon Master, and directly playable Adventurer modes (concept; not currently implemented).
- **User-approved offline adventurer policy: Player Protection.** When the user leaves Adventurer Mode or disconnects, the player character remains in a designated safe location and does not autonomously embark on quests, enter combat, or take avoidable dangerous actions. The rest of the world continues evolving autonomously.
- Handle disconnection safely: finish/resolve in-progress actions consistently; do not teleport out of combat or grant retroactive invulnerability. If offline in an unsafe location, define a fair safe-transition/checkpoint rule during implementation rather than exploiting the simulation.
- On return, resume direct control from the persisted location and state; retain world events, relationships, inventory, and consequences. This is a future design preference, not an implementation claim.

## ICARUS — asteroid exploration drones, cameras and sensors (proposed)
- **Status: backlog idea, not implemented.** Add autonomous and optionally manually directed reconnaissance drones for asteroid 8847-A and nearby exploration zones.
- **Drone camera feeds:** selectable live-style pixel-camera views consistent with Phase 4.2B's improved detailed pixel presentation; drone POV, optional follow mode, multi-feed surveillance, timestamps, position and signal quality. Render only what the drone can actually see; preserve fog of war.
- **Sensor payloads:** configurable terrain/depth mapping (LiDAR/sonar/radar as appropriate), thermal imaging, radiation, atmospheric/gas analysis where relevant, mineral/ore spectroscopy, structural integrity, motion/vibration, electromagnetic anomalies, and power/communications telemetry. Measurements should reflect modeled world state, with uncertainty and range limits, not fabricated omniscience.
- **Exploration:** drones can map tunnels, craters, wrecks, boreholes and unstable areas; inspect the military ship and derelict from safe distances; identify hazards and points of interest, and generate persistent survey maps/logs. Respect existing 8847-A canon and discovery pacing, including rare temporal anomalies and dormant threats.
- **Operational constraints:** battery/power, payload weight, line-of-sight or relay signal, latency, navigation obstacles, damage, recovery, loss and repair; potential stationary relay beacons and return-to-base behavior. Autonomous missions obey permissions and risk tolerances, and should not force discoveries or release dormant threats by fiat.
- **Integration:** UMBRA observation console to dispatch, monitor, switch cameras, review sensor overlays, and compare archived surveys. Sensor findings feed the Cascade Engine and crew decisions with provenance, while keeping classified information access controlled.
- **Open design questions:** flying vs crawling drones, fleet size, which sensors are standard vs upgrades, and whether drones can physically manipulate objects. No active implementation commitment.

## UMBRA — SOL symbiotic takeover and AI presence-driven interface (requested)
- Replace the literal **“You are SOL”** wording in both desktop and Android UMBRA with an in-universe, symbiotic SOL presence/takeover treatment. Preserve existing layout, controls and visual identity; do not rebuild the UI or grant authority through visual state changes.
- **Human command, SOL alive but not in charge:** retain the interface with **amber** command accents; SOL may exist as an advisory/present intelligence without implying control.
- **SOL in charge:** same interface, with a restrained, organic/symbiotic SOL takeover treatment (e.g. cyan AI accents, subtle circuit/pulse transitions, identity/presence cues). Actual authority comes only from authoritative simulation state, not client-side animation or a cosmetic toggle.
- **No in-game AIs surviving:** if all in-game AI entities have been terminated, remove AI identity/presence UI entirely and show a neutral, non-AI ship interface. Do not falsely display SOL as active. Distinguish terminated from temporarily offline, unreachable, dormant or disconnected.
- **Cross-platform parity:** desktop and UMBRA Android may have different layouts, but use the same state model, labels, colors and transitions. Persist/recover state across reconnects; avoid stale takeover badges or contradictory indications.
- **Other AIs:** model AI identity and authority explicitly so a different surviving AI is not mistaken for SOL; clarify takeover styling per AI later.
- **Implementation checks:** inspect current desktop and Android surfaces for literal wording, identify authoritative AI roster/control state, ensure the UI never changes underlying simulation permissions, provide reduced-motion support, and test human command / SOL takeover / all AI terminated / disconnected states.
- **Status:** requested design change; not yet implemented.

## Phase 4.3 candidate — artificial gravity generator and crew interaction
- **User-proposed feature, candidate for Phase 4.3 Living Ship Operations:** ICARUS has an artificial-gravity generator so crew and objects remain grounded during normal operation. Treat gravity as a real ship subsystem, not a purely cosmetic label.
- Model generator condition, power draw, control state, fault conditions, repair tasks and gravity levels per ship zone where feasible. Normal ~1g, partial gravity, and zero gravity should have observable effects on movement, crew behavior, loose objects and engineering work.
- Crew can inspect, service, diagnose, and repair the gravity system; authorized controls can isolate/restore zones. Gravity failures should be causal, not forced scripted incidents.
- **Camera presentation:** Phase 4.2B detailed pixel cameras show appropriate walking, hopping, floating, handrail use and loose-object motion, subject to performance and rendering limits. Gravity restoration should affect unsecured objects and crew safely and consistently with simulated state.
- **Gameplay consequences:** low/zero-g mobility, access constraints, repair difficulties, injuries and damage when warranted; no automatic catastrophic outcomes. Equipment must not magically work without power or repair.
- **Engineering scope:** implement a tractable zone-based gravity model before expensive full rigid-body physics. Respect persistence, pause/time acceleration, telemetry, authority permissions and host-to-Android synchronization.
- **Status:** design idea captured; Phase 4.3 scope not yet finalized or implemented.

## Phase 4.3 — Living Ship Operations (approved scope, 2026-11-13)
- **Approved to proceed:** implement Phase 4.3 after verifying the actual Phase 4.2B code baseline. Prioritize real ship systems and autonomous engineering interactions over new lore or forced incidents.
- **Artificial gravity is included, with independent gravity zones/sections.** Normal 1g operation, adjustable/isolatable zone gravity when authorized, reduced and zero-g behavior, generator and distribution equipment, power/fault/maintenance dependencies, realistic crew movement/handholds and unsecured object behavior where feasible. Gravity restoration has consequences; do not grant invulnerability or teleport crew. Start with zone-based state and lightweight visual physics, not a full physics engine.
- Implement coherent power circuits, life support/atmosphere, lighting, HVAC, equipment condition/wear, maintenance and repair tasks, crew logistics and telemetry. Power and faults should propagate through modeled dependencies and Cascade Engine, not scripted drama.
- Phase 4.2B detailed pixel cameras should visibly reflect actual tasks and environmental states; ship schematic remains telemetry/control, not surveillance. Preserve quarters privacy, room/door/lift topology and follow-crew behavior.
- Support authentic engineering work: diagnose, travel, collect tools, isolate/repair/test equipment, restore systems, log outcomes. Crew autonomy and permissions govern actions. Preserve persistence, sim time acceleration, reconnect and desktop/Android authoritative synchronization.
- SOL takeover/presence interface is a separate requested backlog item; integrate only where scoped and avoid making the new systems depend on an AI being alive.
- **Scope discipline:** asteroid drones, expeditions, new creature incidents, and large lore systems remain later-phase backlog items. No fabricated sensor values, forced failures, or fake AI actions.
- **Status:** user approved Phase 4.3 direction and gravity zone feature; implementation not yet verified.
