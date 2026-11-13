# ICARUS / UMBRA
# PHASE 4.2B — LIVING PERSONALITIES
## Autonomous Crew, Relationships, Connected Corridors, Lift Cameras & 20× Simulation

**Status:** Approved for development  
**Repository:** `thekiddam-code/munza69`  
**Starting point:** Latest verified Phase 4.2A build  
**Relevant branch:** `codex/observation-protocol-phase4-2a`  
**Development philosophy:** Autonomous simulation first, visual consistency second, no fabricated events.

---

# 0. PRIMARY DIRECTIVE

Implement Phase 4.2B as a continuation of the working Phase 4.2A Observation Protocol.

Phase 4.2A made the ship observable.

**Phase 4.2B must make the people aboard it feel alive.**

Crew members should independently develop routines, friendships, disagreements, attractions, romantic relationships, and personal histories.

They should travel through physically connected ship spaces, use the correct doors and lifts, and remain visible through authorized security cameras.

The user should be able to select a crew member and follow their activities without manually switching between every camera.

Add 20× time acceleration so longer-term developments can be observed efficiently.

Preserve the existing ICARUS universe, UMBRA command bridge, SOL, simulation persistence, and existing camera systems.

Do not create a new game or replace the existing simulation.

## Non-negotiable requirements

1. Relationships develop entirely autonomously.
2. Crew decisions must be grounded in their individual states and experiences.
3. Creator Mode must not directly steer relationships during normal simulation.
4. Crew movements must follow real ship topology.
5. Doors, lifts, and cameras must reflect authoritative simulation state.
6. SOL must have limited, evidence-based knowledge.
7. Normal security cameras cannot view private crew quarters.
8. SOL's classified covert camera network is separate.
9. Existing saves must remain compatible.
10. No forced disasters, relationships, or dramatic events.

---

# 1. REPOSITORY INSPECTION AND BASELINE

Before implementing:

- Identify the latest functional Phase 4.2A branch or merged commit.
- Inspect the existing crew simulation, social system, camera renderer, cutaway, ship layout, navigation, and clock.
- Inspect `ICARUS/IDEAS_BACKLOG/README.md`.
- Check existing adult confirmation, relationship preferences, trust, attraction, consent, and memory structures.
- Inspect the existing save schema and migration system.
- Identify the authoritative world clock and simulation update loop.
- Inspect current corridor dimensions and camera projection.
- Inspect the existing personnel lifts and deck connections.
- Identify current SOL access controls and the earlier terminal interface, if still available.

Do not assume that the branch named above is necessarily the latest installed build. Confirm the actual baseline.

Create a dedicated Phase 4.2B development branch.

Run existing tests and record baseline behavior.

Preserve unrelated UMBRA features, including remote controls, Android compatibility, Creator Mode, and the existing command bridge.

---

# 2. AUTONOMOUS PERSONALITY SYSTEM

## 2.1 Individual identity

Each crew member must have a persistent personality profile.

Use existing attributes where available.

Potential traits include:

- Sociability.
- Introversion or extroversion.
- Curiosity.
- Patience.
- Ambition.
- Empathy.
- Emotional stability.
- Risk tolerance.
- Humor.
- Discipline.
- Independence.
- Loyalty.
- Conflict avoidance.
- Personal boundaries.

Avoid treating these traits as rigid stereotypes.

Traits should influence choices, not predetermine every outcome.

Two characters with similar personalities should still be capable of making different decisions because of their circumstances, memories, and relationships.

## 2.2 Personal needs

Crew should respond to modeled needs such as:

- Hunger.
- Fatigue.
- Sleep.
- Stress.
- Social connection.
- Privacy.
- Recreation.
- Work obligations.
- Health.
- Safety.

Do not add dozens of decorative meters without behavior behind them.

Each need must influence real decisions or be omitted.

## 2.3 Autonomous decisions

Crew should independently decide when to:

- Work.
- Take breaks.
- Eat.
- Sleep.
- Socialize.
- Seek solitude.
- Visit recreational spaces.
- Check on friends.
- Avoid someone.
- Request help.
- Assist others.
- Respond to emergencies.

Decisions should consider:

1. Current needs.
2. Assigned responsibilities.
3. Current location.
4. Travel time.
5. Personal preferences.
6. Existing relationships.
7. Recent memories.
8. Environmental conditions.
9. Available facilities.
10. Immediate safety.

Avoid random behavior disconnected from circumstances.

## 2.4 Schedules and habits

Crew should develop recognizable routines.

For example, an engineer may usually visit the mess hall after finishing a shift.

Another crew member might prefer eating alone.

Habits may change through experience.

Do not force every character to follow an identical schedule.

## 2.5 Behavior priorities

Use a clear priority system:

- Immediate survival.
- Critical emergencies.
- Essential duties.
- Health and basic needs.
- Existing commitments.
- Social and recreational activities.

Crew should not ignore serious emergencies to continue casual conversations.

However, routine activities should not be interrupted constantly by minor status changes.

Introduce sensible hysteresis or commitment thresholds to avoid oscillating between tasks.

---

# 3. PERSISTENT MEMORIES AND PERSONAL HISTORY

Crew members should remember meaningful experiences.

Examples:

- Someone helped them repair equipment.
- A coworker repeatedly ignored them.
- A friend offered emotional support.
- A disagreement occurred.
- A shared meal went well.
- A dangerous incident happened.
- Someone broke a promise.
- A romantic interaction was accepted or declined.

## Memory structure

Each meaningful memory should contain appropriate fields such as:

- Event ID.
- Simulation timestamp.
- Participants.
- Location.
- Event category.
- Emotional significance.
- Source of knowledge.
- Confidence.
- Relationship effects.
- Persistence or decay characteristics.

Not every animation frame should create a memory.

Use meaningful events, not constant logging.

## Memory influence

Memories should affect later decisions.

A character may become more comfortable around someone who repeatedly helped them.

Another might avoid a colleague after a serious disagreement.

Memory effects should be gradual and context-sensitive.

## Knowledge restrictions

Characters must not automatically know about events they did not witness, experience, or learn through communication.

Rumors must have an actual transmission path.

SOL's knowledge follows the same evidence-based principle, with its own sensor capabilities.

---

# 4. FRIENDSHIPS, RIVALRIES, AND SOCIAL NETWORKS

Expand the existing social system rather than replacing it.

Track relationships between individual characters.

Possible relationship dimensions:

- Familiarity.
- Trust.
- Respect.
- Affection.
- Attraction.
- Resentment.
- Loyalty.
- Comfort.
- Shared history.

Relationships must evolve through actual encounters.

## Social interactions

Support:

- Casual conversation.
- Friendly greetings.
- Shared meals.
- Assistance.
- Emotional support.
- Jokes.
- Disagreements.
- Apologies.
- Avoidance.
- Reconciliation.
- Group conversations.

Interactions should have visible animation where cameras are available.

Do not display two characters talking if they are not actually interacting.

## Relationship autonomy

The user has explicitly chosen:

**Entirely autonomous relationships.**

Creator Mode may inspect profiles, inspect event histories, reproduce bugs, and configure technical test environments.

It must not provide normal gameplay commands that force two characters to become attracted to each other, fall in love, or consent to intimacy.

The crew must make these decisions themselves.

---

# 5. AUTONOMOUS ROMANTIC RELATIONSHIPS

## 5.1 Adult eligibility

Romantic intimacy features require characters to be explicitly confirmed adults.

Use the existing `adult` attribute if compatible.

Do not infer adulthood from appearance, occupation, or personality.

Characters without confirmed adult status are ineligible for mature intimacy events.

## 5.2 Attraction

Attraction may develop through:

- Repeated positive interactions.
- Shared interests.
- Personality compatibility.
- Mutual support.
- Familiarity.
- Shared experiences.
- Existing preferences.

Attraction must not guarantee reciprocation.

## 5.3 Relationship progression

Potential natural stages:

1. Acquaintances.
2. Growing familiarity.
3. Friendship or attraction.
4. Flirting.
5. Mutual romantic interest.
6. Dating.
7. Established relationship.
8. Relationship changes or separation.

These are descriptive possibilities, not a mandatory sequence.

Relationships can develop slowly, stall, remain platonic, or end.

## 5.4 Consent and boundaries

Any romantic or intimate encounter requires current mutual willingness.

Consent is:

- Specific to the interaction.
- Revocable.
- Not permanently granted by relationship status.
- Not implied by attraction or prior encounters.

If either character declines or withdraws, the encounter does not proceed.

Do not treat coercion, impaired judgment, or inability to respond as consent.

Preserve any existing explicit consent records while adding appropriate event-specific checks.

---

# 6. OPTIONAL MATURE RELATIONSHIP PRESENTATION

Implement an optional, non-explicit mature presentation mode.

The user has approved non-sexual nudity, affectionate animations, and fade-to-black intimacy.

## Supported presentation

- Flirting.
- Handholding.
- Kissing.
- Embracing.
- Affectionate conversation.
- Optional non-sexual nudity in appropriate private settings.
- Entering private quarters together.
- Closing the door.
- Fade-to-black intimacy.
- Resting or sleeping together under blankets.
- Getting dressed and resuming activities.

Do not depict explicit sexual acts or sexual-motion animations.

## Content settings

Provide a user-configurable presentation setting:

**Off**
- Friendship and non-romantic social interactions only.

**Romance**
- Dating, flirting, affection, kissing, and relationships.
- No mature private presentation.

**Mature / Implied**
- Romance plus non-explicit private encounters.
- Optional non-sexual nudity.
- Fade-to-black intimacy.
- Shared sleeping or resting scenes.

Changing the presentation setting must not rewrite character histories or fabricate events.

Separate the underlying simulation state from what is visually displayed.

If the user disables mature presentation, the simulation should remain internally consistent without showing mature scenes.

---

# 7. SOCK-ON-THE-DOOR PRIVACY SYSTEM

Add a privacy indicator for crew quarters.

When two eligible adult characters mutually choose private time:

1. They independently agree to spend time together.
2. They travel to an appropriate private room.
3. The door closes.
4. A sock or equivalent privacy marker appears on the door.
5. Other crew recognize the marker.
6. The private event proceeds off-camera or with non-explicit presentation.
7. The event concludes naturally.
8. The marker is removed.
9. Characters resume their schedules.

## Privacy behavior

Other crew should generally respect the marker.

Interruptions may occur when justified by actual circumstances, such as:

- Emergency evacuation.
- Fire.
- Medical emergency.
- Critical ship operations.
- Genuine access necessity.

Avoid random interruptions added solely for drama.

## Duration

Private events must use simulation time.

At 4× speed, a 12-minute simulated event lasts 3 real minutes.

At 20× speed, that same event lasts 36 real seconds.

Use reasonable variable durations rather than one fixed timer.

Events must be interruptible and persist correctly through saves.

## Consequences

Relationships may deepen or change depending on the participants' experiences.

Other crew should not automatically learn what happened.

Rumors require witnesses or actual communication.

---

# 8. SOL CLASSIFIED OPERATIONS TERMINAL

Implement the previously discussed classified SOL Operations interface as a separate in-universe system.

It must not replace Creator Mode.

## 8.1 Terminal identity

The terminal should resemble a restricted industrial or Linux-style command interface.

Use the existing UMBRA visual identity:

- Dark background.
- Technical text.
- Command navigation.
- Restricted-access indicators.
- Corporate classification labels.
- Minimal decorative animation.

## 8.2 Access model

The ordinary command bridge and SOL Operations must have distinct access permissions.

Do not expose classified functions through ordinary camera menus.

## 8.3 Covert cameras

SOL has access to a separate concealed camera network inside crew quarters.

This is an approved part of the ICARUS fiction.

Ordinary security cameras must continue excluding private quarters.

The classified network must:

- Use actual room state.
- Respect camera availability and power.
- Reflect actual occupants.
- Have a defined field of view.
- Avoid omniscient knowledge.
- Remain separate from the standard camera rotation.

## 8.4 Private encounters

Covert camera presentation may include non-explicit affection, non-sexual nudity where enabled, and fade-to-black transitions.

Do not render explicit sexual activity.

The underlying private event can continue as simulation state while visual presentation remains non-explicit.

## 8.5 SOL knowledge

SOL may know information obtained through its covert cameras.

However:

- SOL cannot know what happens outside its sensor coverage.
- SOL cannot read thoughts.
- SOL cannot know private intentions without evidence.
- SOL cannot identify unknown entities without sufficient information.

Information should have provenance and access restrictions.

## 8.6 Future capabilities

Prepare extensibility for:

- Classified investigations.
- Secret corporate directives.
- Covert observations.
- Restricted personnel files.
- Unauthorized surveillance consequences.
- Hidden mission assignments.

Do not build an extensive secret-mission system during this phase.

Focus on the terminal foundation and classified camera access.

---

# 9. 20× SIMULATION SPEED

Add 20× acceleration to the existing clock controls.

Retain existing supported modes, including Pause, 1×, and 4×.

If compatible, include 10× as an intermediate option.

Suggested control sequence:

`PAUSE | 1× | 4× | 10× | 20×`

## 9.1 Authoritative time

Simulation speed must affect the authoritative world clock.

All relevant systems must remain synchronized:

- Crew schedules.
- Walking and travel.
- Tasks.
- Relationships.
- Fatigue.
- Hunger.
- Social encounters.
- Private event durations.
- Equipment state.
- Door operations.
- Lift movement.
- Environmental systems.
- Event logs.
- Persistence.

## 9.2 Simulation/render separation

Do not increase display frame rate by 20 times.

Rendering must remain independent of the authoritative simulation update frequency.

Use fixed simulation steps, bounded catch-up processing, or an equivalent robust mechanism.

Do not silently discard important simulation events when the system is overloaded.

If the host cannot sustain 20× accurately, display a clear effective-speed or performance warning rather than claiming full acceleration.

## 9.3 Camera behavior

At 20×:

- Characters should not flicker between positions.
- Animations should remain understandable.
- Doors should not visibly contradict their state.
- Camera transitions should remain coherent.
- Conversations and interactions should not produce duplicate events.

A fast simulation may legitimately make crew appear to move quickly.

Do not artificially slow authoritative travel to preserve cinematic appearance.

## 9.4 Speed changes

The user must be able to return immediately from 20× to 1× or Pause.

Changing speed must not reset activities or relationships.

## 9.5 Testing

Test:

- Pause → 20×.
- 1× → 20×.
- 20× → 1×.
- 20× → Pause.
- Save and reload at accelerated speed.
- Remote reconnection while accelerated.
- Extended operation at 20×.

Compare simulated time elapsed against actual elapsed time.

Check for missed or duplicated events.

---

# 10. CORRIDOR WALKING SPEED AND CAMERA PERSPECTIVE

The user reports that walking through corridors looks unusually slow.

Do not simply increase crew movement speed without investigation.

## 10.1 Diagnose

Inspect:

- Physical corridor dimensions.
- World-coordinate walking velocity.
- Camera viewport dimensions.
- Projection scale.
- Corridor compression.
- Sprite animation cadence.
- Interpolation.
- Room transition timing.

Determine whether the issue is:

1. Incorrect world movement speed.
2. Excessive corridor length.
3. Compressed camera perspective.
4. Rendering interpolation.
5. Animation mismatch.
6. A combination of these.

## 10.2 Correct behavior

Maintain believable walking speeds.

Improve camera framing if the world is being compressed into an unusually small viewport.

Long corridors may be represented through multiple contiguous camera zones.

Preserve actual travel distances and arrival times.

Do not shorten a corridor in simulation simply because its camera view is condensed.

## 10.3 Animation synchronization

Walking animation must match movement.

Avoid:

- Sliding feet.
- Running animations during slow movement.
- Frozen sprites traveling across the screen.
- Teleportation at doorway transitions.
- Repeated walking cycles while standing still.

---

# 11. COMPLETE CORRIDOR DOOR SYSTEM

Every corridor must visibly contain the real doorways connected to its associated rooms.

These are functional world connections, not decorative background elements.

## 11.1 Topology-driven generation

Use the authoritative ship layout to determine:

- Which rooms connect to each corridor.
- Door identity.
- Door location.
- Deck.
- Access restrictions.
- Door state.
- Destination room.
- Relevant camera coverage.

Do not invent doors or rooms to fill visual space.

## 11.2 Door appearance

Each doorway should include:

- Visible door frame.
- Functional opening/closing animation.
- Small room-type icon.
- Room name.
- Room designation.
- Appropriate status indicator.

Examples:

`⚙ ENGINEERING | ENG-01`

`+ MEDICAL | MED-02`

`⌂ CREW QUARTERS | CQ-03`

`◇ RESEARCH | LAB-04`

Use original pixel-art signage consistent with the 16-bit camera environment.

Signs should be readable without overwhelming the camera image.

Use abbreviations or tooltips where necessary.

## 11.3 Functional transitions

When a crew member travels to a room:

1. Select a valid route.
2. Walk through the correct corridor.
3. Approach the correct doorway.
4. Check access and door state.
5. Open or wait for the door.
6. Cross the threshold.
7. Update the authoritative location.
8. Appear inside the correct room.

The crew member must not disappear through a wall or enter the wrong doorway.

## 11.4 Door state

Reflect actual states:

- Open.
- Closed.
- Opening.
- Closing.
- Locked.
- Sealed.
- Damaged.
- Unpowered.
- Blocked.

Do not allow crew to bypass inaccessible doors through animation alone.

## 11.5 Interactive labels

Where practical, allow clicking a room sign to focus that room in the ship cutaway.

Respect access permissions.

Do not make signs obstruct normal camera interaction.

## 11.6 Long corridors

Split long corridors into camera coverage segments when appropriate.

All actual entrances must remain represented.

A corridor split must not change the underlying ship geometry.

---

# 12. PERSONNEL LIFTS AND INTERIOR CAMERAS

Add interior security cameras to every operational personnel lift represented in the existing ship topology.

Do not create extra lifts unless necessary to repair a verified topology inconsistency.

## 12.1 Lift behavior

Crew must:

1. Approach the correct lift.
2. Request access.
3. Wait if the lift is unavailable.
4. Board when doors open.
5. Occupy an appropriate interior position.
6. Travel between actual decks.
7. Exit at the correct destination.
8. Continue along the correct route.

Support multiple passengers where the existing system allows it.

## 12.2 Interior visuals

Show:

- Lift walls.
- Door.
- Deck indicator.
- Control panel.
- Occupants.
- Subtle movement or arrival feedback.
- Emergency indicators when appropriate.

Keep the established 16-bit pixel-art style.

## 12.3 Camera metadata

Example:

`LIFT-02 | DECK 03 → DECK 05 | 2 OCCUPANTS`

Display only information supported by actual telemetry.

Potential indicators:

- Current deck.
- Destination deck.
- Travel direction.
- Door state.
- Occupancy.
- Power.
- Faults.

## 12.4 Realistic synchronization

Lift visuals must match actual lift state.

Do not show the lift arriving before the simulation records arrival.

Do not allow passengers to exit while doors are closed.

## 12.5 Lift faults

Where existing mechanics support them:

- Power loss.
- Stalled lift.
- Door malfunction.
- Unavailable destination.
- Emergency stop.

Crew must react according to actual conditions.

Do not manufacture lift failures solely to create drama.

## 12.6 Camera integration

Lift cameras belong to the ordinary authorized security network.

Include them in:

- Camera selection.
- Preview rotation.
- Follow Crew tracking.
- Camera status displays.

---

# 13. FOLLOW CREW CAMERA MODE

Implement an optional **Follow Crew** feature.

The user should be able to select one crew member and have the primary camera automatically follow them through authorized camera coverage.

## 13.1 Starting Follow Crew

Possible entry points:

- Crew Location menu.
- Personnel profile.
- Main camera controls.
- Crew search.

Provide a clear Follow Crew action.

## 13.2 Camera transitions

Example sequence:

`ENGINEERING → CORRIDOR → LIFT → DECK 03 CORRIDOR → MESS HALL`

The main monitor should automatically switch to the appropriate available camera as the selected crew member moves.

## 13.3 Camera selection rules

Choose cameras using:

- Actual crew location.
- Camera coverage.
- Visibility.
- Access permissions.
- Feed availability.
- Camera priority.

Do not infer visibility solely from room names.

Avoid rapid camera flickering when the character crosses coverage boundaries.

Use sensible handoff timing.

## 13.4 Privacy

When a crew member enters private quarters:

- Ordinary Follow Crew must stop showing them.
- Display a privacy or coverage unavailable indicator.
- Continue tracking their permitted location metadata only where authorized.
- Resume normal camera following when they return to covered areas.

SOL's covert camera network remains separate.

Do not automatically promote a classified feed into the standard camera wall.

## 13.5 User controls

Provide:

- Follow Crew on/off.
- Current followed crew member.
- Return to manual camera.
- Camera availability status.

Manual camera selection should either suspend Follow Crew or explicitly exit it, with predictable behavior.

## 13.6 Existing preview wall

Preserve the Phase 4.2A camera wall:

- One main monitor.
- Four previews.
- Automatic preview rotation.
- Pause/resume preview rotation.
- Click-to-promote.
- Camera metadata.

Follow Crew should control the main monitor without breaking preview rotation.

---

# 14. CAMERA AND CUTAWAY CONSISTENCY

The surveillance system and cutaway must agree on world state.

Examples:

- A crew member entering Engineering should appear in Engineering's occupancy data.
- A crew member boarding a lift should appear in lift occupancy.
- A closed door should not appear open in another view without a legitimate transition.
- Camera feeds should not show duplicate copies of the same character.
- A room's status should reflect its actual environmental state.

Use shared identifiers and authoritative telemetry.

All views must derive from one simulation.

Remote UMBRA clients must not run independent copies of the world.

---

# 15. VISUAL PRESENTATION

Preserve the existing UMBRA visual identity.

The command interface remains futuristic and technical.

Security camera scenes retain the detailed 16-bit pixel-art appearance established in Phase 4.2A.

## Character animation additions

Add reusable animations for:

- Greetings.
- Flirting.
- Kissing.
- Embracing.
- Disagreements.
- Apologies.
- Shared meals.
- Resting together.
- Entering and exiting doors.
- Waiting for lifts.
- Riding lifts.
- Using lift controls.
- Private-room entry and exit.

Only animate activities supported by actual simulation events.

## Performance

Reuse sprite sheets and animation components.

Avoid creating entirely separate animation engines for relationships, corridors, and lifts.

Maintain responsive performance on Windows and remote Android devices.

---

# 16. PERSISTENCE AND SAVE MIGRATION

Preserve existing Phase 4.2A saves.

New persistent fields may include:

- Personality traits.
- Habits.
- Social needs.
- Memories.
- Relationship states.
- Romantic interest.
- Consent records.
- Current private events.
- Crew route progress.
- Lift occupancy.
- Camera-follow selection, where appropriate.
- Simulation speed.

Use schema migrations where necessary.

Do not silently erase existing relationships or crew histories.

Test older saves and new saves.

Interrupted private events must not restart incorrectly or duplicate consequences after reload.

---

# 17. IMPLEMENTATION ORDER

Implement in manageable passes.

## PASS 1 — Movement, Doors, Lifts and 20×

Prioritize:

1. Diagnose corridor movement speed.
2. Fix camera projection or walking synchronization.
3. Generate all topology-accurate corridor doors.
4. Add room labels and icons.
5. Implement correct doorway transitions.
6. Improve lift boarding and travel visuals.
7. Add lift interior cameras.
8. Add 20× simulation speed.
9. Verify timing, navigation, and persistence.

**Checkpoint:** A crew member can travel visibly between decks through correct doors and lifts while the simulation remains stable at accelerated speed.

## PASS 2 — Follow Crew

1. Implement camera coverage mapping.
2. Add Follow Crew selection.
3. Add automatic corridor/lift/room handoffs.
4. Preserve preview rotation.
5. Enforce privacy boundaries.
6. Test remote viewing.

**Checkpoint:** Select one crew member and follow a complete journey across multiple decks without manual camera switching.

## PASS 3 — Living Personalities

1. Expand personality attributes.
2. Add meaningful habits.
3. Improve autonomous decision-making.
4. Add persistent memories.
5. Expand friendships and disagreements.
6. Improve social animation synchronization.
7. Test different personalities and routines.

**Checkpoint:** Crew members develop visibly different daily patterns without scripted player intervention.

## PASS 4 — Relationships and Private Lives

1. Extend the existing attraction and consent system.
2. Implement autonomous romance progression.
3. Add affectionate animations.
4. Add optional mature presentation settings.
5. Add private encounter simulation.
6. Add sock-on-the-door indicators.
7. Add relationship consequences.
8. Verify privacy and save persistence.

**Checkpoint:** Two adult characters can independently develop a relationship and choose private time without Creator Mode intervention.

## PASS 5 — Classified SOL Operations

1. Inspect and restore the existing terminal concept where practical.
2. Implement separate classified access.
3. Add SOL-only covert quarters camera feeds.
4. Preserve normal security privacy.
5. Connect observations to SOL's knowledge system.
6. Test access restrictions and sensor limitations.

**Checkpoint:** SOL can access its authorized classified surveillance network without exposing private feeds through ordinary bridge cameras.

## PASS 6 — Integration and Stability

1. Run regression tests.
2. Test long-duration autonomous behavior.
3. Test accelerated simulation.
4. Test camera transitions.
5. Test save/load.
6. Test mobile access.
7. Resolve critical bugs.
8. Document remaining limitations.

Do not expand scope until the core checkpoints work.

---

# 18. REQUIRED ACCEPTANCE TESTS

## Test A — 20× clock

Run 20× for a measured real-time interval.

Verify:

- Correct simulation-time advancement.
- Accurate task timers.
- No duplicate events.
- No skipped critical state transitions.
- Stable return to 1×.
- Correct Pause behavior.
- Save/load consistency.

## Test B — Corridor doors

Select three crew members traveling to different rooms.

Verify:

- Correct door labels.
- Correct route.
- Correct door animation.
- Correct destination.
- Correct room occupancy.
- No wall clipping or teleportation.

## Test C — Lift journey

Follow one crew member between two decks.

Verify:

- Correct lift selection.
- Boarding.
- Interior camera visibility.
- Correct floor indicators.
- Correct arrival.
- Exit into destination corridor.
- Accurate cutaway occupancy.

## Test D — Follow Crew

Track a character through:

`ROOM → CORRIDOR → LIFT → CORRIDOR → ROOM`

Verify automatic camera handoffs.

Confirm privacy handling when entering crew quarters.

## Test E — Personality differences

Observe several crew members during routine shifts.

Verify that individual traits and memories influence choices.

Avoid identical schedules and repetitive behavior loops.

## Test F — Friendship development

Observe repeated interactions between two characters.

Verify that actual experiences influence trust and familiarity.

## Test G — Autonomous romance

Use two confirmed adult characters.

Do not force attraction or consent.

Allow the simulation to develop naturally.

Verify that romance occurs only when mutually appropriate.

If romance does not occur during the test window, use deterministic seeded simulation tests to verify the mechanics without falsely claiming an organic event happened.

## Test H — Private encounter

When an eligible encounter occurs:

- Both participants are willing.
- They travel to the correct room.
- The privacy indicator appears.
- The scene uses non-explicit presentation.
- Simulation duration is correct.
- The event concludes or is interrupted appropriately.
- Relationship state updates once.
- Save/reload does not duplicate outcomes.

## Test I — SOL covert camera

Verify:

- Ordinary security cannot view crew quarters.
- Classified SOL Operations can access its own permitted feed.
- Covert cameras reflect actual occupants.
- Unavailable cameras do not provide invented footage.
- SOL's knowledge reflects observed information.
- No classified feed leaks into standard previews.

## Test J — Extended autonomous run

Run a sustained observation test at normal speed and an accelerated test at 20×.

Observe:

- Work routines.
- Social interactions.
- Crew movement.
- Lift use.
- Door transitions.
- Camera following.
- Relationship evolution.
- Save persistence.
- SOL knowledge consistency.

Do not force incidents or relationships to make the test appear successful.

---

# 19. DELIVERABLES

Provide:

1. Working Phase 4.2B implementation.
2. Updated autonomous crew systems.
3. Updated social and relationship systems.
4. Corridor door and signage system.
5. Lift cameras and travel synchronization.
6. Follow Crew functionality.
7. 20× simulation controls.
8. Optional mature presentation settings.
9. Classified SOL Operations foundation.
10. Save migration support.
11. Automated and manual test results.
12. Performance measurements.
13. Known limitations.
14. Updated GitHub backlog.
15. Startup and testing instructions.
16. Pull request or commit reference.

Clearly distinguish implemented, tested, partially implemented, and deferred functionality.

Do not claim successful physical Android or remote testing unless it was actually performed.

---

# 20. FINAL DEVELOPMENT PRINCIPLES

**Autonomy over scripting.**  
Crew make their own decisions.

**Continuity over visual tricks.**  
Every door, lift, camera, and character represents real world state.

**Consequences over random drama.**  
Events matter because they arise naturally and affect future behavior.

**Privacy through access control.**  
Ordinary cameras remain restricted while SOL's classified network operates separately.

**Simulation correctness over speed.**  
20× must accelerate the world without corrupting it.

**Observation over intervention.**  
The player watches a believable, persistent world develop.

# FINAL OBJECTIVE

At the end of Phase 4.2B, the user should be able to select a crew member, activate Follow Crew, and watch that character finish work, walk through labeled corridors, enter a lift, travel to another deck, meet someone, develop relationships over time, and return to their own routines.

At 20× speed, the user should be able to observe longer-term developments without breaking the simulation.

The ship should feel connected, inhabited, and autonomous.

**Build a crew whose lives continue even when nobody is watching.**