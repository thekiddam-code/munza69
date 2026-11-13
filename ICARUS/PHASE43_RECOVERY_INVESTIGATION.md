# Development campaign recovery investigation

This records a real defect found during Phase 4.3 validation, not a fabricated incident or a pre-existing user-voyage failure. All affected worlds are isolated seeded test contexts.

The first candidate was frozen at 127bda0. Seed1001 at selected20× began at 2026-10-28T00:00Z, America/Chicago, with production hourly wall intervals. At day20 all20 crew were alive; existing C07/C09 condition was67.4/75.95 and the new generator73.216. Resource/audit checks were clean. By day40 all20 crew had died and life-support equipment/resources had collapsed. A passing invariant audit therefore did not establish healthy autonomous operation.

Confirmed software defects:

1. Gravity work factor required anchoring for every ordinary task, including Resting. When actual gravity fell below0.7g and a resting character was not anchored, progress became zero. Recovery could restore energy while the rest-duration timer never finished. A worker relieved during service-isolated generator maintenance could therefore never return to work. This was introduced by Phase4.3 and is not intended danger.
2. `RepairPolicy.ready` excluded component-assigned engineers before emergency dispatch, making the new explicit preemption/release handler unreachable for them. Emergency dispatch must be able to preempt lower-priority component maintenance, retaining already paid parts and partial condition.

At tick32259 (~day22.4), the generator order opened from measured wear. By the day40 sample it had progressed14.3368 condition points to84.3062, was still service-isolated, and had been released for higher duty/welfare after its last attempt at32463. The remaining ship could not recover through permanently stalled routine timers. The first candidate is rejected for release regardless of its clean resource/state invariants.

Correction: only actual tasks needing stable support (repair/diagnosis/research/treatment/console/inspection/maintenance) use the anchoring work factor. Ordinary rest/meal/recovery duration progresses normally in low gravity. Physical zero-g movement and anchored engineering penalties remain. Emergency readiness permits genuine preemption while the ordinary-maintenance picker still prevents duplicate assignments. No resources, health, crew identities, clock rates or successful outcomes are reset to achieve recovery.

Regression protection: pure model tests distinguish zero-g rest/meal progression from unsupported repair; an actual browser test checks rest timer3→2→1→0 followed by a new autonomous choice; an emergency-preemption test requires reservation release with paid parts and exact partial progress preserved. The corrected runtime and subsequent campaign results are identified in PHASE43_VALIDATION.md. Full failure source history and comparative campaign outcomes, when available, belong to the evidence bundle; do not treat the two daily samples alone as an exact minute-by-minute death chronology.
