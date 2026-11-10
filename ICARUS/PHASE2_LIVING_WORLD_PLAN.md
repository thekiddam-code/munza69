# ICARUS — Phase 2: Living World (Codex implementation handoff)

**Status:** approved for development; **not implemented or validated** by creation of this document.
**Starting branch:** `codex/living-world-phase2`, created from `codex/unified-world-phase1`.
**Product:** autonomous, persistent local spaceship anthology simulation; retain UMBRA Remote Deck integration.

## Read before editing
- `AGENTS.md`, `FINAL_DESIGN.md`, `FINAL_RELEASE_ROADMAP.md`
- `UNIFIED_WORLD_SPEC.md`, `UNIFIED_ARCHITECTURE.md`, `UNIFIED_LIMITATIONS.md`, `UNIFIED_VALIDATION.md`
- `web/icarus.html`, `web/unified-world.js`, `web/spatial.js`, `web/navigation.js`, `web/living.js`, `web/experiences.js`, `web/calendar.js`, `web/voyage.js`, `web/unified-ui.js`, `web/durable-store.js`
- Current tests: `test_unified_world.js`, `test_unified_integration.py`, `test_stability_integration.py`, `test_living_frontier_integration.py`, `test_calendar.js`.

## Non-negotiable invariants
1. Preserve all existing saves, crew, injuries, deaths, discoveries, missions, personal objects, research, calendar, and archived episodes. New schema fields must migrate older saves safely; full export/import round-trip must work.
2. The actual production clock stays 4× elapsed wall time except the nine approved synchronized local holidays at 1×. Recognized and personal observances do not change speed. Real Monday–Sunday episodes remain source-backed. No physical time rewind, fabricated catch-up, or duplicate calendar markers.
3. Physical navigation, access control, wheelchair constraints, lift failures, finite resources, paid repair, local radio relay and existing research custody are authoritative. Do not teleport crew/creatures, invent battery charge or ignore sealed compartments.
4. No scripted mandatory incidents, forced creature attack, arbitrary deaths, fixed mission quotas, automatic Lazarus breakthrough, or made-up camera evidence. Quiet weeks are valid. No galaxy/procedural planet/faction economy expansion.
5. Preserve the existing military region in asteroid rooms 21–24 and the initial dormant adult and eggs; no duplicate warship or duplicate initial queen/creature population.
6. Simulation agents never issue real PC commands or network calls. UMBRA bridge, PC controls, and Android/Windows compatibility must not regress.

## Delivery sequence (small independently testable batches)

### 2A — Knowledge and communications
- Audit existing acquired-record, field-relay, radio, archive, research, and crew-state models; identify a single authority for each.
- Add **per-actor knowledge** with evidence/source ID, acquired-at physical tick, location/method, confidence, disclosure state, and optional transmission/delivery timestamps. Distinguish direct observation, overheard report, recorded evidence, captain-authored canon, and inference.
- Only deliver information when communication is physically and operationally possible (same room, actual conversation, working radio relay, retrieved records, or other already-established paths). Delayed/disrupted radio stays pending, not magically delivered.
- Gate SOL commentary, mission decisions and ordinary crew-facing UI on delivered/observed knowledge. Creator lore remains private and never becomes crew knowledge without a causal discovery.
- Tests: isolated discoverer; interrupted radio; later delivery; death before transmission; offline/reload; backup restore; secret creator note; no leaked military discoveries.

### 2B — Autonomous creature behavior and ecology
- Reuse `unified-world.js` initial adult/egg/host lifecycle and the real navigation graph. Do not spawn extra initial adults or delete legacy organisms.
- Implement deterministic seeded decision cycles for **dormancy, sensing, hiding, movement, pursuit, attack, retreat/rest, and containment response**, each constrained by actual location, physical routes, barriers, energy/condition and observable stimuli. Add no arbitrary teleportation or guaranteed encounters.
- Integrate biological host eligibility, 240-minute juvenile development and 180-minute maturation without breaking the existing lifecycle, injuries, deaths, or memorials.
- Creature detection must be local and source-grounded; SOL/crew cannot know an unseen creature's exact location. Consider environmental constraints (vacuum/pressurization) and preserve any established species-specific rules.
- Tests: sealed-room containment; inaccessible route; no-signal quiet run; local pursuit; attack provenance; save/reload determinism; crew injury/death causality; android ineligible host; multi-seed adverse campaigns.

### 2C — Crew movement, activities, and visible embodiment
- Keep existing physical path and mobility modifiers as authority. Support actual corridor/lift transitions, work gestures, equipment use, rest, treatment, conversation, carrying/placing items, and responses to alarms.
- Begin with coherent, readable 2D procedural silhouettes/poses and item cues; do not claim final character art, detailed anatomical prosthetics, or full animation until actually delivered. Add a reduced-motion mode.
- Crew autonomy must respect jobs, access, fatigue, injuries, relationships, ongoing assignments, and the captain's intervention. Distinct characters may act differently, but no artificial drama schedule.
- UI camera/cutaway positions must reflect actual physical nodes and transit; reconstructions clearly labeled. Avoid changing state through render loops.
- Tests: corridor/lift/wheelchair, stationary crew, item handoff only when co-located, pause/resume, reduced-motion, and actual browser visual checks.

### 2D — Individual observances and lunar accuracy
- Replace approximate full-moon markers with a documented reproducible offline ephemeris or well-tested astronomy calculation with declared supported date range; verify known dates and timezones. Atmospheric effects remain presentation-only, never incident triggers.
- Support opt-in individual observances with explicit personal configuration and voluntary acknowledgments using actual available crew and funded resources. No inference of religion, ethnicity or birthdays.
- Keep nine synchronized global holidays and eight recognized observances unchanged; no holiday or timezone operation rewinds physical history.

### 2E — Integration and release
- Add `PHASE2_PROGRESS.md`, `PHASE2_LIMITATIONS.md`, `PHASE2_VALIDATION.md`, update the final roadmap accurately.
- Run JS unit tests, Python/browser integration tests, deterministic campaigns with multiple seeds, adverse scenarios, full save/export/import/reload, and UMBRA bridge checks. Record **actual** counts, source commit, test environment, and failures. Do not claim unrun tests.
- Keep build/package verification with per-file hashes and checksum; generate a **Lite source-based ZIP** (no executable bundler or obfuscation) alongside optional full developer archive. Security-scan if available; never recommend bypassing Chrome Safe Browsing.
- Maintain the existing host launcher and browser origin/port to preserve voyage data. Clearly mark incomplete features.

## Execution instructions for Codex
1. Start with **2A only**. Audit actual source, state the specific schema/API changes, implement in small commits, add tests, and validate. Do not attempt to complete all of Phase 2 in a single speculative patch.
2. After 2A, report exact changed files, tests/results, remaining risks, migration behavior, and the next smallest batch. Continue 2B–2E only with the same evidence discipline.
3. The user's preference is a living autonomous world with rare emergent extraordinary events, not a scripted horror attraction. Preserve the Sunday genuine-footage/clearly-labeled-reconstruction rule and optional Legendary Kill Cam.
