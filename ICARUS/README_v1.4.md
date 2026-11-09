# ICARUS — v1.4 Anthology Recalibration

**Autonomous Science-Fiction Anthology Simulation.** One ship, persistent crew, SOL and an optional captain. Stories can be ordinary, joyful, humorous, uncertain or dangerous. Neither a disaster nor a scientific breakthrough is required every week.

**Unresolved viability issue:** seed 1001 suffers total crew loss late in a normal year-long run; seed 2026 retains all twenty. Mechanical/persistence audits pass, but overall acceptance and final-release readiness are not verified. See VALIDATION_v1.4.md.

Extract the entire project. On Windows, install the existing dependencies (`py -m pip install -r requirements.txt`) and run `Start_Remote_Deck.bat`; open the printed ICARUS PC URL. Use a stable browser origin/port. The paired Remote Deck tablet observes and commands the authoritative PC.

v1.4 starts a **separate core save**. To continue v1.3, first export its complete JSON backup, then explicitly import it in core save management. Read MIGRATION_v1.4.md before replacing anything. The preserved v1.3 Extended Universe archive is independently runnable; old galaxies are retained as frozen history when imported into core.

Open **Operations** for developing stories, local travel, optional captain controls and encounter preferences. Set frequency/weights if desired, then commit a save. SOL continues research, maintenance, crew life and feasible operations without mandatory choices. Existing crew/medical/science views remain. Sunday cards reconstruct recorded events and retain unresolved threads; they are not authentic camera footage.

Read FINAL_DESIGN.md for the intended finished game, FINAL_RELEASE_ROADMAP.md for verified/unfinished milestones, ENGINEERING_v1.4.md for implementation, VALIDATION_v1.4.md for measured results and KNOWN_LIMITATIONS_v1.4.md for scope/coverage. Tests passing does not mean ICARUS is ready for a commercial final release.

For automated browser checks install Playwright and Chromium separately from runtime requirements. `node --test test_*.js`, `python test_anthology_integration.py --report core_integration.json`, `python test_frontier_bridge.py --output bridge_results.json` and `python anthology_soak.py --seed 1001 --days 365 --milestones 30,90,365 --output reports` reproduce the principal checks. Migration testing needs extracted original v1.3 web files; set ICARUS_V13_WEB to that directory. Set ICARUS_CHROMIUM to an installed browser binary if needed.
