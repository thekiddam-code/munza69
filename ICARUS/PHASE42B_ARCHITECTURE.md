# Living Personalities architecture

## Authority and compatibility

Baseline is verified Phase 4.2A 6332248, with main e0065eb backlog updates merged additively. The Windows browser remains the single fenced world writer. UMBRA only consumes received projections/dispatches existing authorized commands. No save key, namespace, roster, prior relationships, sources, research, missions, environment or episode is reset. New fields are additive and serializable. The six new runtime modules bring the runtime to 118 files; no third-party rendering dependency or artwork was added.

## Physical continuity

Existing deckArchitecture and navNeighbors remain the topology authority: 30 rooms, five corridor stations per A/B deck, six on C (the end room is C10), ladders at stations 1 and 3, one personnel lift shaft at station 2. `transit.js` receives this actual layout, never independently generates rooms/doors.

A saved `transit.lift` owns the single cabin, capacity-four passenger list, FIFO call queue, current/from/to decks, positioning/boarding/travel/arrival/unloading and remaining simulation minutes. Passengers cannot each have an independent elevator. Calls are discarded when their authoritative route changes. Power/service loss stalls rather than teleports; existing ladders remain alternative routes for eligible non-passengers. Arrival precedes exit. `liftRide` identifies actual cabin occupancy; other room identifiers retain their legacy last-room meaning while `Spatial.position` is authoritative for current occupancy. Camera, schematic and follow use that distinction.

Physical hatch state remains physicalWorld.rooms[id].door. Transit tracks opening/closing and occupancy windows, waits for closed hatches to open, and blocks sealed/jammed/locked/blocked/unpowered access. Power loss cannot finish an opening. External privacy markers block ordinary entrants while actual safety/access obligations can interrupt. No renderer bypasses the graph. Existing bulkhead/repair/atmosphere controls remain upstream.

The old navigator measures edges in abstract simulation minutes, not metres: ordinary corridor edges take three baseline minutes, entering a room two and ladder transitions five before individual mobility factors. There is no defensible metre/second number in the source. The old deck-wide 384-pixel projection compressed these distances into about 65 pixels per station. New cameras frame one station and its real connected doors. Labels/side/door identities come from actual topology. Walking cadence now follows presented displacement and facing follows the actual edge/threshold. No physical travel duration was shortened. Sub-room/furniture routing remains the previous compatible visual layer, not a newly completed furniture solver.

## Camera follow and observation

`observation-model.js` adds ordinary per-station corridor feeds and LIFT-01 to the same projection as rooms. One actor belongs to one ordinary camera; cabin passengers are not also corridor or room occupants. Ladder imagery remains an explicitly labeled telemetry reconstruction, not a newly invented installed camera. Four preview banks/pins/manual promotion remain independent of Follow Crew.

Follow resolves from received camera IDs/availability, never names alone. Manual selection exits follow; unavailable/private coverage clears the subject image and preserves the follow selection for a later permitted return. Resolution happens even while the panel is offscreen. UI follow/bank/content settings are separate local preferences; world navigation and speed are saved with the world. Stale remote views never create a world. The new schematic exposes actual cabin phase/occupancy; the old hologram uses saved shared-cabin progress for passenger projection.

## Personal choices and relationships

Existing CrewLife shift/needs/task selection and CrewSocial numeric bonds remain the authorities. `personalities.js` supplies persistent stable tendencies reusing existing sociability/curiosity. Discipline/privacy/empathy/patience/humor/boundaries affect actual ordinary choice weights or interaction responses. Habits are learned only from completed activity IDs, bounded to 32 types. Relationship-influenced visits use remembered locations, not omniscient friend tracking. Survival, operational assignments and existing task commitments retain precedence.

Real co-located conversations can yield support, jokes, disagreement or reconciliation according to recorded fatigue/stress, prior resentment and individual tendencies. No dialogue is fabricated as a quote. Social memories retain source, participants, location, confidence, significance and actual relationship effects. Per-person memories remain bounded; source history is retained by the existing durable archive.

`relationships.js` extends crewSocial rather than introducing a competing relationship store. Confirmed adult status is required; unknown age is never inferred from profession. Existing named preferences are retained as restrictions. Missing restrictions do not grant consent. Repeated acquired interactions, trust and gradual attraction allow independently seeded decisions, with health/fatigue/stress/obligations/impaired-judgment/boundary checks for each actor. An invitation can fail. Creator has no normal partner/attraction/consent controls; adult metadata confirmation remains clearly authored configuration.

Consent records include scope/source/time. Legacy relationship consent is preserved but cannot authorize private time. A new private-time event needs two current acceptances from that actual invitation. The two actors use existing physical routes; an empty safe private room must be available. A saved event progresses through travel/wait/private/completed or interrupted, with 8–20 simulation minutes of private duration. Doors/markers are actual state. Welfare, reassignment, departure, emergency, necessary access or withdrawal interrupt; completed effects apply once. Prior consent never permanently grants willingness. Dating can change/separate following actual unresolved interaction history.

Off/Romance/Mature-Implied are presentation preferences only, not history editors. Shared affectionate cues are non-explicit. Private activity is off ordinary cameras and fades to black in the restricted console. No explicit sexual acts, sexual-motion animations or nudity assets were created. Detailed kissing/handholding/shared-bed art remains refinement work.

## Classified SOL foundation

`classified-ops.js` is an explicit saved fictional hardware registry for two approved concealed quarter sensors, COV-A05/A06, each with enabled/condition/FOV. Power, receiver hardware and room visibility gate availability. Only actual visible crew postures/identities are projected. No intentions, unseen organisms or private thought scores are read. Changed observations create source records with privateKnowledge and SOL-CLASSIFIED classification and acquired SOL facts with disclosure `classified`. Ordinary queues, record reads, public views and SOL commentary exclude these facts. This is separate from private participant knowledge; SOL does not automatically acquire conversations or consent records.

The fenced host publishes restricted sensor data beside (never inside) normal telemetry. BridgeService stores it in a separate bounded 24 KiB volatile slot, clears it on host replacement and marks stale data. Ordinary SSE/legacy/paired endpoints contain no classified payload. `/api/icarus/classified` requires both loopback host origin and host capability; a normal paired token is insufficient. The local terminal explicitly authorizes in-memory capability, locks/clears feed state, rejects late responses after locking, and supports only fixed UI commands help/status/cameras/view/lock. No terminal input is evaluated as JavaScript or passed to an OS shell. This first foundation does not grant remote classified roles or secret missions.

## Clock

Production `calendar.selectedRate` supports Auto/1/4/10/20 and is saved. Synchronized holidays remain 1× and episodes remain real local Monday–Sunday. Existing Creator-only development rates remain a separate unsaved diagnostic interface, not relationship controls. Production pacing drains the old interval before switching, preserves fractional carry, and steps every simulation minute through all controllers. The ordinary 120-minute pump work budget keeps rendering independent. A backlog warning reports inability to keep up; the inherited six-real-hour suspension recovery policy remains explicit and logged. This is not an unlimited offline catch-up engine.

## Test provenance

See PHASE42B_VALIDATION.md and machine-readable delivery reports. Never turn a mechanics fixture into an organic romance claim, emulation into physical-device testing, or a source-based procedural view into recorded video. The final schematic/hologram UI patch is separately identified from the timed-watch runtime. Native UMBRA S24+ source/APKs and the older installed app boundary remain unchanged.
