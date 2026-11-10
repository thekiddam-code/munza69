# Unified World Phase 1 — engineering notes

Baseline: v1.4.1 a363799. This build is identified as 1.5.0-phase1; it is an implementation increment, not a claim that the entire uploaded design is finished. UNIFIED_WORLD_SPEC.md preserves the user specification. Existing repair/resource/source rules and core/Extended Universe separation remain in place.

## Audit and reuse

The baseline passes 117 Node tests. The existing simulation advances in minute steps and already has a continuous tick counter, thirty ship rooms, corridor/hatch/ladder/lift graph, connected asteroid and derelict grids, finite missions, medical consequences, individual relationships, IndexedDB snapshots and sourced chronicles. Inspection found the military wreck already occupies asteroid rooms 21–24. These rooms are reused; there is no second military vessel or procedural system expansion.

The old normal timer executed one minute per second (60×), and 5/20 buttons multiplied that. Episodes followed 10,080 accelerated minutes. Cameras inferred movement from the last room and coarse destination tokens. Derelict tooltip titles and asteroid zone headings could expose undiscovered information. The update corrects these paths.

## Clock and calendar boundaries

`calendar.js` owns wall-time pacing and adjustable displayed calendar mapping. It never writes crew, resources, missions, injuries or simulation ticks. Existing `voyage.js` alone increments physical minutes; `step()` and `fieldTick()` retain all operational behavior.

Production pumps real milliseconds, accumulating 60,000 simulated milliseconds per minute. Normal rate is four simulated milliseconds per real millisecond; each official synchronized holiday uses one. The engine segments by actual local midnights in an IANA timezone, including 23/25-hour DST days. The nine approved dates and eight recognized observances are computed independently. Recognized and personal observances cannot enable global slowdown. Gregorian Easter uses a deterministic computus.

The displayed calendar starts at the real instant of world initialization. It does not invent prior crew history or require beginning on the first day of a month. Holiday synchronization adjusts only this presentation mapping; it does not call physical rewind, restore inventory or repeat a mission. Ship elapsed time and existing minute-of-day behavior remain independent of display corrections. The UI shows ship time separately from the mapped calendar.

Each real date/holiday pair is recorded once, independent of timezone, with a persistent occurrence marker. Personal observations add crew identity to their occurrence key. Individual observances currently use explicit MM-DD configuration; automatic Hebrew/lunisolar calendar conversion is not implemented.

## Real-week episodes and recovery

Monday–Sunday keys are computed in the configured timezone, separately from ship time. The transition to Monday closes the previous source-backed week, archives its actual recap, and increments the presentation episode without resetting the world. Event records carry wall time and real-week metadata. The first episode may be a partial week, with no fictional earlier events.

Timezone changes do not recreate already visited episode keys. Existing event assignments are never moved to manufacture a recap. During a timezone change across a week boundary, the active archive episode remains monotonic until the next unseen real week; the UI reports the actual configured local week. This policy prioritizes no duplicate archives and no rewritten history.

Recovery is deterministic from saved cursor, target wall time and timezone. At most six real hours are caught up after suspension; older elapsed intervals are omitted with an explicit journal notice. A production pump applies at most 120 physical minutes, draining retained backlog over later pumps. Time rollback freezes advancement until wall time catches up; it cannot produce duplicate history. Pausing drops wall time from physical progression. Extremely long offline periods do not simulate an unbounded backlog or fabricate missing-week events.

The deterministic soak endpoint requires `?icarus_soak=1`, disables the automatic timer and explicitly advances either legacy fixed steps or the real-calendar driver. Calendar test pumping suppresses per-step autosave and performs explicit checkpoints; it uses the same physical simulation controllers. Old fixed-step tests deliberately retain the legacy episode mode on fresh test worlds without a calendar; they supplement, not substitute for, real-calendar campaigns.

## Authoritative spatial presentation

`spatial.js` reads `p.nav.at`, current edge and edge fraction. Camera follow now presents the actual corridor or lift/ladder transition; a traversing character is not shown successively occupying adjacent compartments. Room cameras and cutaway occupancy use the same projection. Legacy horizontal cutaway marker and some hologram coordinates remain schematic; their full coordinate consolidation is still incomplete. Field actors do not receive invented authenticated camera footage. Bridge telemetry identifies physical corridor nodes.

Wheelchair routing excludes ladder edges, respects lift outages and can legitimately fail to find a route. Mobility profiles affect traversal rate. Build/locomotion profiles are persistent and configurable for stationary crew. This provides data and navigation support; it is not a completed anatomy, natural-animation or wheelchair/prosthetic art pipeline. Historic reconstruction frames without navigation data retain their old limited room information and their reconstruction label.

## Connected-world, lore and biology scope

`unified-world.js` stores the authoritative references to existing environments, creator canon, acquired records, personal objects, observance preferences and initial biological state. Military exploration is triggered by actual visits to existing asteroid rooms 21–24. Local power restoration consumes five of the wreck's twenty initial battery units and is recorded once. Its compartment interlock can fail under the seeded simulation, without guaranteed release. No seasonal flag creates enemies or casualties.

Exactly one initial registry adult exists: dormant, isolated in a concealed chamber associated with asteroid room 23. Other initial registry organisms are dormant eggs. Actual military cargo exploration may produce exposure. An eligible biological host then requires 240 physical minutes to produce a juvenile, with a fatal recorded emergence, and another 180 minutes to reach adult stage. Android hosts are ineligible; biological build/species influence generated attributes and prostheses are not inherited as organic anatomy. Death passes through the existing injury/death/memorial system. Initial stage, exposure, maturation and one co-located released-adult encounter are implemented. Autonomous creature hunting, a full lifecycle/ecology, parasite diagnosis/treatment, elaborate mutations and final creature artwork remain incomplete.

Creator canon editing never promotes notes into crew knowledge or retroactively changes physical events. The ordinary archive accepts recorded acquired evidence with source IDs. Existing research/custody/Lazarus stores remain authoritative for scientific conclusions. Unified field records are an observer archive of events acquired by actual expedition crew; their radio-delivery gating is not yet consolidated with the existing relay/report queue. SOL's existing mission safety and radio systems are preserved, but no claim of a fully unified individual-knowledge model is made.

Personal keepsakes are registered initial inventory (or explicitly labeled legacy inventory registration), not fabricated memories. Carried objects follow their owner; placement, co-located gifts and memorial inheritance require physical access and source-backed transfers. There is no new consumable resource economy. Detailed prop physics, corridor recovery and a rendered decoration library are not complete. Holiday acknowledgments use an already funded meal and an available volunteer; they do not override emergency/research/field assignments.

## UI and persistence

Calendar, creator lore and individual preferences live in existing Settings; acquired records and optional object transfers live alongside the existing Operations/chronicle views. Amber/cyan instrumentation, captain intervention, bridge authentication, PC/TV/gaming routes and optional observation are retained. Home widgets gain vertical resizing, but saved widget dimensions and a full interface polish/accessibility pass remain future work.

Optional `calendar` and `unifiedWorld` save groups migrate without changing existing crew, work, resources or deaths. Structural validation rejects malformed groups; new backup envelopes require unified state. Complete backups include both groups and source history. Upgrade is supported; downgrading new-world saves into older runtimes is not a supported workflow.

## Verification and honest boundaries

UNIFIED_VALIDATION.md and reports record the actual checks and outcomes. No single survival count certifies this design. A complete final game still needs the art, character-specific cultural content, connected prop/knowledge delivery, creature behavior and platform/human review listed in UNIFIED_LIMITATIONS.md and FINAL_RELEASE_ROADMAP.md.
