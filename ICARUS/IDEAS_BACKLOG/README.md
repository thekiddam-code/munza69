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
