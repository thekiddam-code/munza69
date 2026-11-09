# v1.4 engineering changelog and architecture

## Audit and preservation

Baseline: ea984a8749c907fd373492283f085d769eebbd03, verified v1.3 Living Frontier. Read AGENTS.md, CODEX_START_HERE.md, prior architecture/limits and source for initialization, physical crew life, research/custody, economy, expeditions/rescue, navigation, chronicles, bridge and persistence. All 91 baseline unit cases passed before modification.

The audit found useful module boundaries, but the default progression continuously accumulated procedural sectors and planets and most new opportunities required traveling to another destination. This diverged from the new core identity. Full v1.3 source/tests/docs are preserved before edits as archive/extended-universe-v1.3 and an independent complete ZIP; recovery instructions are in MIGRATION_v1.4.md.

## Core boundary and storage

`web/edition.js` installs core storage aliases before the lossless codec and durable bootstrap. Logical compatibility API keys stay readable to the engine, but writes go to an independent physical namespace; IndexedDB is independently named. Existing v1.3 data is never silently replaced or auto-imported. An explicit JSON import initializes missing narrative state and appends a bounded local context without deleting existing galaxies or interrupting physical transit/mission state. New v1.4 imports require the narrative history structure; partial histories are not regenerated as empty stories.

`web/core-context.js` adapts the existing universe/navigation interfaces. New core worlds contain HOME plus five finite local observational/supply/salvage venues in two context records. These are not new planetary systems. Scans never add sectors or planets. Migrated old systems stay frozen and auditable; new routes are restricted to local venues and HOME. Existing in-flight legs can complete. Automatic travel occurs for unsurveyed local contacts or actual reserve needs, then can stop. Recycled healthy reserves do not trigger a forced mining mission.

Existing economy, logistics, custody, research, equipment, crews, field teams and rescue retain their conservation/safety rules. Local deposits have explicit initial inventories, remaining amounts and extracted balances. Actors' inventories are likewise finite; communications do not create ship cargo. Resource acquisition under shortage is tested separately from normal campaigns rather than manufacturing a deficit to satisfy an old galaxy-expansion acceptance rule.

The original galaxy module implementations remain accessible to legacy references and a soak-only compatibility fixture. Core has no player toggle to enable galaxy progression. The independent archive is the supported Extended Universe edition.

## Causal anthology engine

`web/anthology.js` holds versioned config, stable arc IDs, observed/seen keys, source lists, stages/history, affected crew/actors, elapsed work, pauses, links, conclusions and optional traditions. The journal hook processes actual relationship, research, medical and encounter records. Pair/category cooldowns prevent every social tick becoming a new story. Source records are still preserved when no arc is opened.

External observations use stateless seeded hourly probability, receiver/power conditions, finite concurrent attention and configurable emotional weights. Frequency is 0–3; weights are 0–5. No weekly category or dramatic quota exists. Profiles cover courteous/visitor contact, an odd acknowledgment carrier, a peaceful pass, measured spectral uncertainty, a philosophical question, sign-off, unidentified signal and an engineering warning. These are a deliberately small interaction vocabulary, not an unrestricted plot/dialogue generator. Contact actors can recur; earlier registry/history references link later threads without inventing encounters.

Work advances only with actual available onboard crew and paid communications energy; local liaison duty occupies existing task time and cannot replace expedition, research, clinical or emergency reservations. Unavailable staff/reserves pause work; an exchange can be declined. Research threads wait for subsequent recorded case results or retain uncertainty after four weeks. Medical threads follow actual patient health, ceilings and loss. No story result changes a scientific conclusion or guarantees Lazarus advancement.

Positive shared exchanges update actual social/stress/morale state, source-backed memories and relationships. A seeded subset can form a remembered tradition; later observance needs available original participants and paid food. Scientific follow-ups may close after failed/inconclusive results without calling those results a breakthrough. Outcomes need not injure anyone. Occasional dry SOL commentary follows a recorded positive result; it never adds an unobserved incident.

## UI and weekly presentation

`web/anthology-ui.js` replaces the large star-map dashboard with a combined ship/story Operations overview, optional local travel/context, current/resolved threads, source IDs and encounter preferences. Existing visual typography/colors/controls and specialist crew/science panels remain. Details retain their open state on refresh. Thin tablet telemetry offers bounded local contacts; captain local-course commands use the existing authenticated restricted grammar. No new simulation runs on the tablet.

Chronicles retain recorded anthology/observation cards, conclusion-derived tones, direct injury/death tones and references to open stories at weekly closure. Cards are explicitly reconstructions. Story state never resets or ends merely because of Sunday. Existing rare lethal eligibility/causal recording checks and anthology options remain; this batch adds no combat or invented footage.

## Verification and provenance

`test_anthology.js` covers bounded/frozen contexts, imported travel, unavailable crew, positive metered work/memory, multiweek research without invented results, repeatable frequencies, atomic preference validation and sourced quiet/positive chronicles. `test_anthology_integration.py` exercises **default core mode**, original physical/autonomy adverse regressions, actual v1.3 import on the same origin, namespace isolation, real downloadable backup roundtrip, rollback, tablet layout, preference controls and real local extraction under an explicitly injected fuel deficit.

The 44-case inherited frontier suite remains an explicit Extended Universe compatibility lane, preserving old assertions rather than weakening them to describe a different game. Core tests/campaigns separately verify the new default. Bridge tests authorize LOCAL routes, retain old save-route grammar validation and reject unrecognized input.

`anthology_soak.py` advances real Chromium continuously, checks physical/source/conservation audits daily, validates crew census, fixed context count and monotonic clock, and performs exact full-world save/reload comparisons at milestones. It retains raw story histories, science state, inventories, crew outcomes, histories and timings. A previous copied galaxy runner rule demanded extraction even with healthy stocks; that stopped diagnostic runs at day 90 and is explicitly retained as an obsolete-criterion failure. The original v1.3 runner remains unchanged. Final core validation does not impose mining/travel quotas after local objectives are exhausted.

See VALIDATION_v1.4.md and packaged reports for actual final tests, diversity/overlap/durations, conservation, science/Lazarus, source hashes, failed attempts and incomplete coverage. FINAL_DESIGN.md governs scope; FINAL_RELEASE_ROADMAP.md distinguishes verified mechanisms from unfinished polish and content quality.

## Long-run medical regression repaired

A pre-release seed-1001 run reached day 346, then crashed on an actual unreachable medical route: navPath legitimately returned null for sealed access and medicalRecoveryTick dereferenced .length. Availability now treats null as unreachable; sorting likewise tolerates a missing path. No casualty is teleported or labeled treated. A sealed-hatch incapacitated-patient browser regression verifies physical waiting without a crash. The failed campaign and interrupted peer remain diagnostics; acceptance uses fresh post-fix worlds.
