# Phase 4.7 checkpoint verification

**Phase4.7 is incomplete and is not ready for a final release.** Truck deployment, a persistent field camp and camp-based rotations have not been implemented or verified. The supplied acceptance guard is retained.

Frozen runtime `58232819cd68a2748d43576a7984e35395f23f39` contains141 files; all hashes match the source and are recorded in reports/phase47/scope.json. Boot/store/authority/lease files remain byte-identical to the preceding stable hotfix. No runtime change followed the accepted runs.

## Final executed suites

| Suite | Passed case executions | Duration |
| --- | ---: | ---: |
| node | 428 | 24.064045585 s |
| services | 18 | 0.003 s |
| features | 3 | 38.628 s |
| industrial | 1 | 8.902 s |
| drone | 7 | 83.718 s |
| clock | 4 | 22.521 s |
| visual | 6 | 19.757 s |
| boot | 8 | 56.52 s |
| existing_voyage | 4 | 139.137 s |
| early_records | 1 | 19.62 s |
| remote | 49 | 240.333 s |

**529 case executions passed in the final selected runs.** Suites have inherited overlap. The actual private Episode2 backup passed all four original startup/continuity checks and an additional archive-access check: every retained ID listed, Records1–12 selectable, playback does not mutate the archive. Crew, knowledge, maps, field/drone recordings, all original16954 history rows and full before/after restart snapshots were checked. The original input SHA-256 stayed unchanged. The private backup is not published.

## Earlier failures and remaining diagnostic concerns

One concurrent full-snapshot comparison reported a remoteCore difference. Two isolated reruns and the final serial four-case suite passed unchanged. Exact field/root cause was not reproduced; path-only diagnostics were added. This remains an investigation item under load.

One concurrent remote-suite TV tap timed out. Its isolated retry and final serial 49-case suite passed; TV implementation was unchanged. No physical-TV result is implied.

The earlier oversized archive preview was corrected by compacting historical metadata and exterior-only camera DTOs. A captured-PNG regression was corrected by reducing redundant state frames before removing the last feasible captured image.

A 19MB import exceeded the old 30-second harness deadline during concurrent suites. The private import fixture now allows120 seconds; all original preservation assertions remain.

These earlier diagnostics are not counted as final passes or asserted resolved without evidence. The intermittent load-sensitive remoteCore comparison should be localized before recommending this checkpoint as a production release. TV emulation remains separate from physical validation.

## Acceptance status

| Requested acceptance | Actual status |
| --- | --- |
|1 FOC begins aboard C03 | Verified optional migration/initial state, parked and restrained |
|2 Scaled cargo camera | Actual renderer screenshot; declared visual scale, not full metric clearance physics |
|3 Crew preparation and vehicle deployment | Physical inspection/travel verified; vehicle deployment not implemented |
|4 Reachable persistent camp | Not implemented |
|5 Exterior camp occupancy | Not implemented |
|6 Camp launch/charge/maintenance | Not implemented; existing ship-dock operations pass regressions |
|7 Escort relief | Six deterministic controller tests cover ship-dock launch/rendezvous/overlap/gaps/reload; camp/integrated browser handoff not verified |
|8 Live moving drone view | Running engine reaches connected segments; current view changes with actual movement; rendering cannot advance the world |
|9 Different environments | Actual surface/passage and industrial camera captures; complete military/corporate art review pending |
|10 Playable event clips | Genuine retained low-cadence captured-state/PNG sequences with play/pause/replay; high-rate encoded video/audio not implemented |
|11 Missing Records1–12 | Confirmed retained in supplied archive, hidden by old last-eight list, now accessible under original IDs |
|12 Crew expedition progression | Existing preparation/pressure-cycle/physical travel/field/return and remote regressions preserved; FOC integration not implemented |
|13 Save/reload | Implemented domains verified, including supplied voyage; no camp state exists to verify |
|14 Existing systems | Selected Node/service/clock/visual/boot/drone/remote suites pass; physical devices untested |
|15 Catch-up usability | Cooperative yielding implemented and deterministic equivalence tested; full16000-real-second production benchmark not run |

## Actual screenshots and unavailable checks

reports/phase47/screenshots contains cargo_foc01.png, live_drone_connected_passage.png, industrial_drone_camera.png and captured_event_playback.png. These are actual running canvas captures over explicit technical worlds, not conceptual mockups, not physical footage and not events asserted to have occurred in the user's voyage. Provenance/hashes accompany them.

Physical Windows, installed Samsung APK, tablet/TV hardware, LAN/Tailscale, GPU/touch accessibility and antivirus testing were unavailable. Native APK rebuilding remains pending original source recovery. No new long-duration campaign or full16000-second backlog benchmark is claimed. Existing real-week, holiday1×, ordinary4× and selected20× behavior remains covered by clock regressions. The inherited six-real-hour catch-up cap remains.

## Next implementation milestone

Implement a real cargo-rated C03→C01 freight path and vehicle transport/loading controller with clearance, safety and actual performed crew work; then a reachable persistent camp with finite transfers, deployed equipment/occupancy, environmental supplies and pack/recovery. Generalize drone home/return reserves to real camp docks and power, then test camp-based handoffs, maintenance, patrols, medical/ATV support and resupply. Add on-demand authenticated full historical-media transfer and higher-cadence event capture. Localize the load-sensitive snapshot finding, measure the requested production backlog, then rerun full acceptance and hardware checks. This is remaining implementation, not a request for new scope approval.
