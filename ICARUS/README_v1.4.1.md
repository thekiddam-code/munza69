# ICARUS v1.4.1 — Stability & Survival

Continue the core autonomous science-fiction anthology. This update repairs the verified inaccessible-galley/engineering-reservation cascade from v1.4, adds finite physical repair/recovery checks and validates legitimate unrecoverable failures. It does not expand the universe or add a new gameplay system.

Extract the complete folder. On Windows, install the existing requirements (`py -m pip install -r requirements.txt`) and launch `Start_Remote_Deck.bat`; open the printed ICARUS PC URL. Keep the same origin/port to continue the existing core save. Export a complete backup before updating. V1.4 saves initialize policy diagnostics and paid-progress fields without resetting the world; core/Extended Universe namespaces remain separate.

Recorded deaths remain permanent when upgrading. Recovery demonstrations start from the captured pre-collapse world; the update preserves the current voyage and its existing consequences.

SOL continues preventive work, safe response and recovery autonomously. Captain intervention remains optional. A sealed hatch is respected; a damaged jam requires a fit worker physically at its accessible side plus actual parts and work time. Insufficient supplies or unsafe access can still cause injuries, loss or death. Sunday cards remain sourced reconstructions.

Read ROOT_CAUSE_v1.4.1.md for the exact reproduction/timeline, ENGINEERING_v1.4.1.md for changes/costs, VALIDATION_v1.4.1.md and reports for actual outcomes, KNOWN_LIMITATIONS_v1.4.1.md for boundaries, and FINAL_RELEASE_ROADMAP.md for remaining work. Automated survival is not itself proof of good decisions or final-release quality.

Validation commands:

```
node --test test_*.js
python test_stability_integration.py --report stability_integration.json
python stability_adverse.py --report adverse.json
python test_living_frontier_integration.py --report compatibility.json
python test_frontier_bridge.py --output bridge.json
python stability_soak.py --seed 1001 --days 365 --milestones 30,90,180,365 --output reports
```

Browser checks require Playwright and Chromium; set ICARUS_CHROMIUM if using an existing binary. Migration tests require archived v1.3 web files at ICARUS_V13_WEB. To reproduce v1.4, obtain source 602b4a2 (preserved codex/v1.4-anthology branch/download), then run `investigate_stability.py --web-root /path/to/v1.4/web --output original_profile --seed 1001 --days 365 --original-checkpoints`. The replay handler adds only passive diagnostic response code and leaves baseline files unchanged. Packaged captured-state/history artifacts support shorter old/repaired counterfactual replay through recover_cascade.py.
