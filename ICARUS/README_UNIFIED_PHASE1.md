# ICARUS — Unified World, Phase 1 implementation

Extract the complete project and launch the existing Start_Remote_Deck.bat on the host PC. Runtime installation and pairing remain unchanged; see the existing server instructions. Keep the same browser origin/port to preserve the voyage and export a full backup before upgrading.

Normal production pacing is now **4× actual elapsed time**, not the old minute-per-second fast demo. The nine approved local holidays automatically run at **1×**. Settings → Time & Calendar selects an IANA timezone, for example America/Chicago. Pause/resume remains available. Old speed commands do not override the synchronized production clock; fixed-step acceleration remains a diagnostic tool.

Episodes follow real local Monday–Sunday weeks. Physical simulation time, the displayed calendar and real time are distinct. Old crew, deaths, research, resources, missions and history persist. At most six offline real hours are caught up, with older gaps explicitly logged; a clock rollback never repeats physical history. New saves include optional calendar and unified-world state and remain in the existing core namespace. Do not downgrade new saves into an older runtime.

Camera follow reads actual corridor/lift edges. The military wreck uses the existing asteroid region. Settings contains a clearly labeled private Creator Lore Editor and individual observance/body preferences. Operations contains the acquired archive and physically constrained personal-object transfers. Existing Research remains authoritative for scientific and Lazarus findings. There is no automatic breakthrough or scheduled catastrophe.

This is a **partial implementation of the complete uploaded design**, not a finished overhaul. Read UNIFIED_ARCHITECTURE.md, UNIFIED_LIMITATIONS.md and UNIFIED_VALIDATION.md. Full creature behavior, natural character/prop art and animation, precise astronomical dates, richer individual observances and complete knowledge/geometry integration remain open work. The original specification is preserved in UNIFIED_WORLD_SPEC.md. The roadmap distinguishes tested functionality from incomplete scope.

Developer checks:

```
node --test test_*.js
python test_unified_integration.py --report unified_browser.json
python test_stability_integration.py --report stability_browser.json
python test_living_frontier_integration.py --report compatibility.json
python test_frontier_bridge.py --output bridge.json
python stability_adverse.py --report adverse.json
python unified_soak.py --seed 1001 --days 30 --output reports/campaigns
```

Browser tests require Playwright and Chromium; set ICARUS_CHROMIUM to an installed binary. The archived v1.3 source is needed for the existing explicit migration case (ICARUS_V13_WEB). Real-calendar campaign seeds, target wall instants and timezone are part of the reproducibility profile. Automatic test-mode pumping is disabled so deterministic replay never advances from the machine's current clock.
