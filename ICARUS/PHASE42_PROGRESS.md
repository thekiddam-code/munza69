# Phase 4.2 Living Ship — development checkpoint

**Status: first implementation milestone; Phase 4.2 is not complete.** Baseline 0854442 / Phase 4.1. Branch: codex/living-ship-phase4-2. The supplied specification contains sections 1–4 and stops at section 5, “Conversations and Gossip — Implement”. The remaining instructions and acceptance criteria have been requested; do not invent them or publish a complete Phase 4.2 release from this checkpoint.

## Architecture audit and completed code

Reuse crew-life.js, the original taskFor/assign/physical controllers, finite workstations/supply collection, knowledge channels, experiences.js and existing embodiment/animation. No parallel crew controller, duplicate relationship score or replacement simulation was created.

- Persistent private activity identities, goal/destination, remaining existing budget, travel/wait/active-minute accounting, bounded 16-entry activity history, actual completion versus interruption, supply-fetch continuity and terminal recorded-death state. Migration adopts ongoing work without resetting its task, route, crew identity or social history. Repeated rendering or same-tick observation cannot progress activities. A forced budget drop cannot manufacture observed completion.
- Stable per-role staggered eight-hour shifts, rotating after seven physical voyage days. They use monotonic elapsed time, never episode presentation resets. Ordinary choices incorporate duty, actual hunger/fatigue, stress, social needs, existing preferences, recent choices and reachable locations. Emergency/maintenance/medical/research controllers retain priority. Existing task durations, routing, finite supply costs and completion remain authoritative.
- Fixed the confirmed relationship-range defect: ordinary conversations previously clamped established scores such as 75 down to 20. They now keep the existing -100…100 domain and apply the existing gradual +0.5 increment. No new friendship, romance or dispute is forced.
- Incapacitation/death outrank stale conversation, route and carried-tool pose cues. Custody itself remains intact; a disabled person does not animate fabricated tool use.

Activity records are internal mechanical bookkeeping, not fabricated story records, camera footage or automatically shared personal knowledge. Existing chronicles/cameras/SOL projections retain their source and visibility rules. No existing voyage is regenerated. Save namespaces, original crew/relationships/memories and the Phase 4.1 server/UMBRA/layout code remain.

## Timing boundary

The known 20× acceleration issue is explicitly deferred to Phase 4.1.1. calendar.js, command-ui.js, host-authority.js, remote-sync.js, server.py and the original main clock/pause/test-rate handlers are unchanged from Phase 4.1. Shifts change crew decisions in physical ship minutes; they do not change clock speed, holidays or real Monday–Sunday episodes.

## Remaining work / exact scope limits

This milestone is not the complete activity/social overhaul. Typed friendships/respect/rivalry/distrust/mentorship/loyalty, explicit consensual-romance behavior, richer social consequences/reconciliation, detailed engineering/clinical/scientific gestures and section 5 gossip/conversation requirements still need implementation/integration. Existing numeric relationships and source-backed conversations continue working; do not describe them as all the requested new relationship types. No cleaning/ecology/resource mechanic or dialogue quotation has been invented to fill the missing specification.

No Phase 4.2 Lite/release ZIP or full-phase acceptance is issued at this checkpoint. Long-duration Phase 4.2 campaigns, full extracted-package regression, broad historical-save matrix and physical Windows/Android/TV/AV tests remain pending. Native APK rebuild remains pending recovery of original Android Studio sources; existing installed functionality is not removed.

## Verification record

Baseline Node suite: 279 passed. Added lifecycle/shift/preservation tests cover migration, bounded history, actual work versus waiting/travel, interruption, death, deterministic continuation, resource-fetch continuity and relationship-range preservation. Current measured results are in reports/phase42/milestone1; only completed executions may be claimed. A development run of the existing cinematic module executed 101 inherited browser cases successfully; it was a development regression run, not a full Phase 4.2 release gate.

The first custom browser harness accidentally used the old Extended-edition base and then an incorrect base-class name. Those test-driver failures were corrected by using the existing core LivingWorldIntegration helper; no product assertion was removed. Final targeted browser cases exercise actual activity progression, exact reload, a real Monday transition, view purity and full genuine Phase 4.1 backup import with retained crew/routines/resources/navigation. Continue from this checkpoint once the remaining specification is available.
