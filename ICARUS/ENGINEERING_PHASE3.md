# Phase 3 engineering changelog

Baseline: verified Phase 2 runtime 113e79b, approved Phase 3 plan 35cc4a1. Existing oversized HTML still hosts orchestration; new behavior lives in six small modules rather than a second competing world state.

| Milestone | Commit | Implemented result |
| --- | --- | --- |
| 3A | 23826f1 | Seeded persistent individual routine choice, reachable activities, causal co-located communication, bounded actual memories, visible conversation pose, additive migration and regression coverage. |
| 3B | a3f5985 | Optional read-only bridge director; contextual poses, sparse real-state snapshot buffer, cached sprite markup, historical actor/location/condition continuity, tablet-emulated tests. |
| 3C–3D | 61f1993 | Source/confidence-backed bounded SOL notes; private supportive discussion and recursive gossip suppression; nonmodal Sunday timeline with real provenance, weekly persistent films and strict exceptional-lethal selection tests. |
| Packaging preparation | e4a5b58 | Source-based Lite packager, manifest/checksum, installation/backup/rollback/security and limitations documents. |
| Stabilization | 65403c0 | Quiet-watch candidate search reads recent actor entries before copying, rather than cloning the full acquired knowledge view. Source eligibility, ordering and deterministic commentary behavior remain the same. |

Intermediate defects found and corrected: paused diagnostic conversation rendering did not refresh the camera; a scenery-argument refactor initially referenced an undefined parameter; social records could recursively quote conversations; quiet commentary searches copied old knowledge unnecessarily. Final results distinguish the discarded diagnostic attempts and superseded campaigns from accepted runtime tests.

No host, launcher, Python dependencies, calendar algorithm, creature ecology, resource model or core save namespace was replaced. Optional new groups are schema-validated. Old saved crew, history, research, missions and relationships are not recreated or reset. Observers cannot create recordings, steer crew or advance world time. New modules perform no network or host command I/O. Final full artifacts identify their exact source commit in BUILD_MANIFEST.json.

See PHASE3_ARCHITECTURE.md for state ownership and tradeoffs, PHASE3_VALIDATION.md for measured evidence, PHASE3_LIMITATIONS.md for explicit remaining scope. Separate rescue awards, richer exceptional-encounter classification/capture, final animation/audio and human story-quality work are not presented as complete.

The final import regression exposed by 50,170-record Phase 2 and 10,659-record Phase 1 backups was missing immediate initialization of the three optional Phase 3 groups in `restoreBackup`. The patch initializes them there, idempotently, matching bootstrap. It does not change physical simulation logic. An explicit old-backup fixture checks original crew equality, empty new records and exact first reload; large real backups are retested separately. Failed diagnostic evidence is retained and excluded from accepted passes.
