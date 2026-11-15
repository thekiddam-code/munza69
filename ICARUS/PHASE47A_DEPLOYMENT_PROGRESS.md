# Phase 4.7A continuation: freight and camp deployment

Baseline: verified catch-up hotfix `588507b19cf4078d81a43ae422059d799acdcde3`. The full Phase 4.7 brief remains authoritative; this is the next bounded implementation milestone, not the finished whole phase.

1. Audit existing C03, ExpeditionWorld/ExpeditionOps, team/suit/cargo accounting, paired commands, camera provenance and asynchronous durable saves. Preserve the selected clock, catch-up worker and writer fences.
2. Introduce explicit C03 cargo-lock/shared-lander freight ratings and paid physical engineer installation/testing. No second spacecraft or personnel-hatch truck route.
3. Extend the existing expedition lifecycle with freight manifests, loading, pressure cycling, fifty-minute travel, ramp work, camp setup, packing, recovery and later C03 re-restraint.
4. Account for every original camp equipment item, finite vehicle-bank power, interrupted work and last physical locations. Publish field intelligence only through actual knowledge acquisition; render exterior equipment through existing local suit/drone cameras.
5. Validate normal/adverse lifecycle, active-mission reload/week boundaries, existing private voyage, remote controls and catch-up compatibility. Freeze, regression-test and package exact source before publishing.

## Verified implementation milestones so far

450 deterministic model cases and six new physical browser lifecycle cases passed. New tests exercise loading/setup/recovery, precise reload, recall, C03 power interruption, Monday transition in transit, and delayed field intelligence. Two defects found by the tests were fixed: completed loading advanced beyond its eight-minute limit during staging checks; an unreported transit condition was formatted as a number during reload. Strict validators and original state assertions remain.

The next validation pass checks the paired HTTP client, previous voyage, inherited camera/remote/boot suites and sustained catch-up on the frozen runtime. Final delivery evidence supersedes these intermediate counts.

## Intentional boundary

Only the existing Landing Shelf (node0) is freight-rated. Crew still use the existing graph elsewhere; no truck is inserted into tunnels without surveyed clearance. Camp equipment is physically erected and recoverable, with finite relay/floodlight draw, but camp-based drone docks/rotations, medical treatment, overnight occupants, ATV driving/patrols, resupply and relocation remain Phase4.7B. High-rate encoded media remains Phase4.7C. No interiors, phantom occupants, free supplies or guaranteed encounters.
