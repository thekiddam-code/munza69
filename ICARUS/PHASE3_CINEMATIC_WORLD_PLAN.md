# ICARUS Phase 3 — Cinematic Living World

**Status:** development authorized; not implemented by this document. **Branch:** `codex/cinematic-living-world-phase3` from verified Phase 2 branch `codex/living-world-phase2`.

## Objective
Make the existing autonomous world readable, distinct, emotionally coherent and worth observing, **without manufacturing incidents**. Prioritize the bridge-only spectator experience and optional management interventions. Preserve UMBRA Remote Deck functionality.

## Required context
Read `AGENTS.md`, `FINAL_DESIGN.md`, `FINAL_RELEASE_ROADMAP.md`, `PHASE2_VALIDATION.md`, `PHASE2_LIMITATIONS.md`, `ENGINEERING_PHASE2.md`, `UNIFIED_ARCHITECTURE.md`, `UNIFIED_LIMITATIONS.md`, and actual UI/simulation modules. Identify current behavior before writing replacements.

## Non-negotiable constraints
- Existing Phase 2 source-backed knowledge, delivery and secrecy, physical route and mobility, creature ecology, real resources, finite paid repair, research provenance, injuries/deaths, source history and saves are authoritative. No render function may mutate simulation state.
- Production 4× physical pacing; nine synchronized 1× holidays; real Monday–Sunday anthology; six-real-hour bounded offline catch-up; no rewinds, forced incidents, mandatory deaths, forced missions, guaranteed discoveries, fabricated recordings, or quota-based drama.
- Existing military asteroid rooms 21–24 and initial organism registry are unchanged; no galaxy/faction/economic expansion. Do not imply every character has been given full AI reasoning when not implemented.
- Preserve old voyage imports and stable local server origin/port, Android pairing and remote deck. Do not trigger real host commands or network actions from simulated agents.
- Any recorded clip must be actual saved frame/state data. If reconstructing from event records, clearly label it **RECONSTRUCTION** and retain provenance. Never silently invent a visual or death scene.

## Implementation batches

### 3A — Readable character autonomy and social causality
1. Audit existing `living.js`, `experiences.js`, `teams.js`, `story.js`, `anthology.js`, `chronicles.js`, `embodiment.js`, knowledge/crew state and UI.
2. Improve distinct crew choices through existing personality, job, energy, fatigue, physical location, mobility, knowledge and relationships. Add *bounded*, causal preferences/routines and interaction memories. Preserve human agency and captain overrides; avoid repetitive relationship/liaison loops.
3. Conversations and gossip require co-location or legitimate delivered communication. Rumors have source/confidence, and cannot reveal private creator canon or inaccessible field observations. No spontaneous universal awareness.
4. Add source-backed visible activities: actual repair, experiment, treatment, tool use, conversation, rest, carrying, observation, and physical response to alarms. Activity and pose must reflect the true actor and location, not random cosmetic simulation events.
5. Tests for different personalities, fatigue/assignment constraints, no remote gossip, no dead actor activity, no forced romance/conflict, save/reload determinism, and quiet-week plausibility.

### 3B — Visual camera and environmental presentation
1. Improve existing procedural 2D character silhouettes/poses and prop interaction cues incrementally. Support reduced-motion and legibility on Samsung Galaxy Tab S5e landscape and Windows desktop. Do not advertise final art until delivered.
2. Add optional bridge spectator camera selection and context-driven shots based on *actual* activity, with explicit live/reconstruction/telemetry status. No camera can see unobserved or unrecorded field action as live footage.
3. Make scene continuity reflect nav edges, lifts, wheelchair/prosthetic constraints, damage, repairs and room occupancy. Avoid expensive full DOM redraws.
4. Tests: actual location and motion, pause, reduced motion, live-versus-reconstruction provenance, no render-side effects, tablet layout.

### 3C — SOL grounded commentary and character memory
1. SOL speaks from legitimately delivered ship knowledge, recorded source events, and established uncertainty. Explain operational decisions and refusals concisely; allow quiet periods.
2. Add varied commentary templates and persistent references to real character-specific experiences, without claiming unsourced personal beliefs, hallucinated scenes or omniscience.
3. Preserve rare dry corporate humor without overwhelming urgent situations. Test privacy, tone, repeat suppression, and persistence.

### 3D — Sunday cinematic chronicles
1. Preserve Monday–Sunday archival boundaries and source-backed selection. Build a skippable, pauseable, 3–5-minute *target* presentation, with graceful shorter runtime for quiet weeks and no fabricated content.
2. Structure: opening, real highlights, crew developments and fates, unresolved threads, rare grounded awards, SOL assessment, closing credits/archive. Optional styles for future anthology variants should not override provenance.
3. Genuine recorded visual snapshots/clips only if captured and retained; otherwise label reenactments **RECONSTRUCTION**. Avoid creating an expensive video-encoding dependency without a validated design; a timeline of actual/reconstructed in-app shots is acceptable if clearly named.
4. Optional **Legendary Kill Cam** only for an actually extraordinary lethal encounter supported by source history; use explicit selection criteria (danger, disadvantage, ingenuity, consequence, rarity, evidence). Never manufacture kills to fill the segment. No segment if nothing qualifies.
5. Tests: empty/quiet week, source-labeled clip, missing recording, exceptional kill, ordinary death excluded, save/archive/replay, Monday transition, no source leakage.

### 3E — Stabilization and distribution
1. Validate Node tests, browser/Chromium tests, regression suites, normal 4×/holiday 1× timer, Remote Deck bridge, import/export, real-week archive, 30-real-day seeded campaigns and adverse fixtures. Record actual counts and environments, no fabricated passes.
2. Track save size, memory, render performance, deterministic replay, camera provenance, and long-term story repetition. Avoid claims of final audiovisual polish or human approval without tests.
3. Write `PHASE3_PROGRESS.md`, `PHASE3_VALIDATION.md`, `PHASE3_LIMITATIONS.md`, update `FINAL_RELEASE_ROADMAP.md`.
4. Build a source-based **Phase 3 Lite** ZIP plus manifest/hash and optional full source/testing package. Do not bundle opaque executables, disable antivirus, change browser origin, or overwrite the user's voyage. Provide migration and rollback steps.
5. Physical Windows/Android/Samsung TV and human long-form playtests are release gates, not inferred from Linux/browser emulation.

## Execution instructions
**Start with 3A**. Implement source code and focused tests, commit a verified batch, report exactly what is working and incomplete. Continue 3B–3E in substantial but independently testable batches. No documentation-only completion, no silent scope expansion, no declaring all of Phase 3 done before evidence.
