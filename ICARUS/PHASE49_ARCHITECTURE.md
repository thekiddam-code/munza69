# Phase 4.9 architecture and engineering changelog

## One world and one clock

`unifiedWorld.organisms` remains the organism authority. The optional `unifiedWorld.biologicalLife49` extension contains finite habitat inspections, four existing fixture registrations, bounded service requests/history and counters. Each ordinary organism links to one specimenCustody identity, an actual carrier or enclosure, and recorded origin. No second clock, remote simulation, map or biological item inventory exists.

The authoritative minute loop synchronizes carriers, metabolism, enclosure/environment state and field consequences. The existing creature controller dispatches ordinary-life behavior through species-specific rules; legacy Xenomorph logic remains unchanged. Habitat creation is deterministic from save entropy plus cell identity, independent of mission quotas. It registers hidden local world state and does not produce acquired knowledge. Actual four-minute inspections are guarded against repeated work in one minute. Empty locations are valid. Military cells21–24 are excluded from new habitats.

## Real acquisition and work

The existing ExpeditionOps field callback performs work only at a stationary physical node, with scientist presence, working lights, carrying capacity and cargo consumables. A defensive handling response can interrupt acquisition and injure the actual handler. Successful custody uses the existing acquisition/return/research intake pipeline. The old generic specimen-return shortcut is bypassed only for linked live subjects, preventing teleportation into quarantine. B03 delivery triggers legitimate science intake; viability is grounded in the actual living observation, not guessed from old organic labels.

Biological assignments extend the existing task scheduler. Care/repair/recovery kits are prepared at C04 from Economy ledger resources before physical travel and timed work. Low-gravity work uses the existing anchoring/work factor. Emergencies release reservations and record expended prepared materials. Research, teams, social routines and furniture interactions respect biological reservations. Dead carriers leave sealed containers at real recorded locations; co-located expeditions can recover them. Deceased specimens are physically taken to B10, preserving custody rather than deleting an entity to make space.

## Cause and knowledge

Local environmental exposure, finite care reserve and enclosure condition affect organisms. Generator loss does not defeat a passive latch by itself. A mobile organism can exploit an actual compromised enclosure; sessile colonies cannot. Uncontained ordinary species never enter the legacy predator controller. Defensive contact requires actual co-location and excludes crew already traversing an edge. Movement retains from/to/duration/progress and respects existing passages and barriers.

Witnesses, installed cameras and existing radio/records supply knowledge. Source-backed briefings precede distant crew work. Public projections omit hidden habitats and exact internal biological health/energy/stress. Empty-enclosure repairs refer only to the fixture, never disclose the former occupant's hidden location. Room, corridor and field camera projections remain read-only; private rooms and unavailable links remain protected. Opaque portable/archived containers do not expose their contents as visible animals.

## UI and recording interfaces

New optional `specimens` and `enclosures` view arrays extend the shared observation model. The pixel renderer draws original small organisms and transparent fixture overlays from those arrays. Ship/suit/drone views use the same renderer; hidden or disconnected feeds do not receive replacement images. Biological field work sets the real sampling action used by suit-camera poses.

The shared containment panel consumes an optional `biology` telemetry summary on desktop and UMBRA. `biology:inspect:BIO-[1-4]` is the only new remote command, using existing pairing, fixed allowlist, request deduplication, writer fencing and backup guards. It requests qualified physical work, never changes integrity, position or latch state directly. Other controls and soundboard paths are unchanged.

Existing cinematic snapshots may include observed specimen/enclosure arrays. Sunday playback can draw a static specimen reconstruction from those saved arrays, with explicit provenance. Existing event/media archives and their retention/custody remain authoritative; no fabricated video or new continuous recorder is introduced.

## Migration, boundaries and release discipline

The existing optional-domain validator checks new biological state without resetting it. Legacy saves omit the extension and migrate additively during actual restoration. The original asteroid's25 identities, crew roster/history, scientific surveys, clock, holidays and writer namespace remain. Finite habitat/organism counts,24 recent sighting signatures per organism and64 operational history entries bound new live state. Full historical source archives follow their existing policy and can still grow; reports distinguish that from new biological-state size.

Milestones: baseline1d6569b; foundation bfc93cc; causal recovery/evidence779a085; field/camera/privacy hardening08f7525; physical-presence boundary b75f724; priority-mission isolation bc0b986. The runtime is frozen at bc0b98636b0c681416ca349667892263110086bd while validation/documentation continue. Preliminary campaign prefixes were stopped for the final field-animation fix and are not final long-duration acceptance. Final validation identifies exact runtime hashes. Tests use isolated worlds; fault injection is always labeled. Older runtimes cannot safely advance new organisms, so rollback requires the pre-upgrade backup in a separate profile. No lossy converter is included.
