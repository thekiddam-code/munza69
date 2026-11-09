# v1.3 limits, unverified behavior and next priorities

This release adds an integrated local living-frontier loop. It does not claim a complete autonomous civilization or unrestricted narrative intelligence. Final acceptance is governed by reports/validation_summary.json and actual activity metrics, not this feature list.

## Deliberate model boundaries

- Persistent actors are resident at their recorded destinations. Their inventories, provisions, condition, activities, history and reputation persist off-screen, but independent interstellar navigation, ship interiors and detailed NPC clinical/crew psychology are not simulated. Four organization policies are distinct heuristics, not a strategic faction economy. Actor discovery is finite/seeded and capped at 256 materialized contacts per voyage.
- Communication is local registry/protocol exchange, refusal, misunderstandings, finite barter and capability-backed cooperation. There is no unrestricted dialogue generator, price market, combat, boarding or human recruitment. Derelict histories are limited damaged procedural records; unknown causes remain unknown. Foreign research collaboration and prisoner/passenger evacuation are deferred.
- New field teams have two to four people using one primary pod. Objectives use assessment/work/securing stages and abstract local range, not new fully walkable planet maps or orbital mechanics. Old active manifests can complete without a forced conversion. Equipment types are actual metered allocations, with simplified wear and repair. If a full field team is lost away from the ship, its primary pod remains unavailable; no free replacement is created. Dedicated lost-pod retrieval/replacement is deferred.
- EVA rescue uses one responder and six shared suits, local range at most 40, functioning ship systems, actual supplies and finite attempts. It is not another interstellar shuttle. Field repair, shelter, triage, unsuccessful intervention and casualty consequences exist; full mass evacuation, towing, multi-vessel rescue and prolonged independent abandoned-colony simulation are deferred. Existing ship emergencies retain their own physical response system.
- Crew memory is event-backed numerical confidence, caution, relationships and willingness. It preserves personality rather than generating free-form psychological biographies. Bereavement retains the existing relationship-weighted grief and memorial system; not every bystander loss produces a separate new career-memory entry. Serious injury recovery uses individual seeded rates/ceilings and resource-dependent care; it is not a clinical prognosis model. No guaranteed Lazarus breakthrough or resurrection is added.
- Chronicles are sourced event cards with play/pause/skip, existing memorials and optional anthology presentation. There is no new rendered video montage or humorous-awards generator. Real camera footage is never claimed. No new combat/kill generator exists; extraordinary lethal eligibility is strict and need not occur in any campaign.
- The paired tablet presents recent telemetry and commands. Full indexed archives, backup import/export, detailed registry selection and chronicle playback are available on the main PC interface. The tablet remains a thin client and never runs a second simulation.

## Storage boundaries

IndexedDB transactions protect acknowledged snapshots and retain indexed significant history. A crash can lose unacknowledged in-memory progress; a queued cache write is not falsely labeled a durable commit. The old compressed cache remains for compatibility/fallback and can reach its smaller quota before the database. Warnings are visible; export remains the off-device protection against browser/profile/origin deletion. Export merges readable indexed records with pending history even when writes fail, reports whether the snapshot was durably committed, and labels missing source history as a partial rescue backup. It cannot recreate an unreadable/deleted archive.

Three rolling snapshots are retained alongside significant history, rather than an infinite set of full snapshots. Available v1.2 journal data migrates; history already pruned by that version cannot be recreated. Future events receive rollback-safe namespaces when older backups are restored; this is not a general branching-universe comparison UI. Compatibility with downgrading the application binary is not promised.

Snapshots, compression and large JSON imports still use browser memory. Historical growth is legitimate and measured, not bounded forever. The year-long acceptance budget is 64 MB logical snapshot / 512 MB origin IndexedDB usage; measured sizes and performance are reported. Large portable backups include the indexed history and take time to create/import. A developmental 75 MB year-end backup took about 19 seconds to import and 35 seconds to reload under concurrent validation load; final measured timings are in reports. This is not an instant-load or low-memory mobile certification. IndexedDB quota estimates vary by browser/device. Checksums detect accidental corruption, not malicious tampering. Structural checks cover the major new domains and finite inventories, with semantic consistency audited separately; arbitrary hand-edited game states are not a supported import format. Unsupported future database schemas fail visibly into compatibility fallback rather than being silently overwritten.

## Tests not run

No physical Windows keyboard/mouse, real Android tablet, Samsung TV, Safari/Firefox, real LAN-disconnection, browser-profile deletion recovery from an external service, or hostile multi-tab concurrent-writer stress certification is claimed. Linux Chromium desktop/tablet viewports, isolated real IndexedDB and a real loopback paired bridge are tested. Bridge tests stub desktop input. There is no remote cloud backup service.

Deterministic fixtures explicitly create adverse initial conditions. Forced random values in focused failed-repair tests are not natural campaign events. The reports distinguish these from uninterrupted multi-seed voyages. Passing two normal seeds does not guarantee all seeds survive or make every rare contact/rescue outcome appear.

## Recommended next batch

1. Independent NPC routing and external supply chains with bilateral conservation; faction goals/reputation beyond per-contact heuristics.
2. Multi-vessel towing/evacuation and passenger accounting, richer field maps and selectable mission plans.
3. Versioned append-only history tooling, incremental/streamed backups, explicit restore-branch browsing and multi-tab writer arbitration.
4. Deeper medical trajectories and experience models with empirical long-run balancing, preserving source provenance and established personalities.
5. Broader seeded fuzzing, compound emergency campaigns, real tablet/Windows/browser accessibility and network-interruption tests.
