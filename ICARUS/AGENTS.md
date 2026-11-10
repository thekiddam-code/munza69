# Current handoff: Unified World Phase 1

Read UNIFIED_WORLD_SPEC.md, UNIFIED_ARCHITECTURE.md, UNIFIED_LIMITATIONS.md, UNIFIED_VALIDATION.md and the final-design documents. Baseline is v1.4.1 a363799. Real production pacing is 4×, official holiday pacing 1×, episodes real local Monday–Sunday; do not restore legacy minute-per-second production or accelerated weekly resets. Preserve physical route authority, paid repair, actual sources and captain controls. Military wreck state references existing asteroid rooms 21–24. Full uploaded scope is not complete: finish the documented art, creature, knowledge and calendar limits before expanding elsewhere.

# Current maintenance handoff: ICARUS v1.4.1

This focused Stability & Survival update continues v1.4 602b4a2. Read ROOT_CAUSE_v1.4.1.md, ENGINEERING_v1.4.1.md, VALIDATION_v1.4.1.md, KNOWN_LIMITATIONS_v1.4.1.md and the final-design documents. Retain paid physical repair, safe near-side hatch access, bounded reservations, real station/supply checks and exhausted-objective navigation limits. Replay seed plus external checkpoint profile; preserve deaths and captain seals. Packaged reports distinguish final evidence from superseded diagnostic attempts. Historical directions below remain context, not a request to expand scope.

# Current direction: ICARUS v1.4 core anthology

Official title: ICARUS. Genre: Autonomous Science-Fiction Anthology Simulation. Read FINAL_DESIGN.md and FINAL_RELEASE_ROADMAP.md before adding scope. Preserve v1.3 independently as the Extended Universe edition; core must not activate procedural planetary/galaxy expansion or territorial/economic management. Respect separate save namespaces and explicit migration. Depth, cohesion and completion take priority. Current baseline is v1.3 ea984a8; historical setup and milestone notes below do not override the current user assignment or final design.

# ICARUS engineering instructions for Codex

## Product
ICARUS Remote Deck is an autonomous, mission-based spaceship simulation. The human user may intervene, but SOL and the captain have authority to authorize missions without human approval. Preserve existing crew, psychology, relationships, ship systems, derelict/asteroid exploration, science, and weekly episode behavior. Never fabricate discoveries solely to create missions. The simulation should produce emergent stories based on real state changes.

## Source of truth
The baseline is v0.94.8 Shipboard Science. Main simulation UI and JS: `web/icarus.html`; local Python server: `server.py`; browser soak test: `soak_test.py`. Read these files and existing README files before changing behavior. Preserve existing save compatibility and mission logs.

## Development discipline
1. Inspect and explain existing architecture before significant refactoring.
2. Make small, reviewable changes. Do not remove features or weaken test assertions to obtain a pass.
3. Add focused automated tests for every new subsystem and regression tests for missions, crew, persistence, weekly rollover, and timing.
4. Test with actual browser execution where available, and state clearly when browser binaries or dependencies prevent a test.
5. Keep all science hypotheses traceable to actual recorded evidence. Distinguish verified observations, tentative hypotheses, and unknowns. No automatic breakthroughs.
6. Maintain full autonomous mission authorization with user intervention (explain, recall, abort, command, release). No mandatory daily mission quotas.
7. Keep diagnostics in `soak_report.json` and preserve existing report fields; add new fields rather than silently changing semantics.
8. Do not add network calls or execute arbitrary commands on behalf of in-game agents. This is a local simulation.

## Current milestone: v0.94.9 Scientific Reasoning
- Model hypotheses tied to existing science cases, with evidence for/against, confidence and explicit uncertainty.
- Group related cases into persistent research programs; Lazarus is possible only when evidence supports it.
- Implement autonomous, resource-aware experiment selection and outcomes, including safety gates and meaningful failure/no-result states.
- Preserve chain of custody, containment and scientist availability.
- Add report diagnostics and focused tests for persistence and evidence provenance.
- Do not silently promote preliminary classification to confirmed scientific fact.

## Suggested validation
From the project root: `python -m pip install playwright` and `python -m playwright install chromium` (where supported), then `python soak_test.py --days 7`. Existing `requirements.txt` lists runtime/bridge packages, not Playwright. Check Python and JS syntax as well.
