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
