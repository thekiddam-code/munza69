# ICARUS v1.3 — The Living Frontier

Extract the entire project, including `web/vendor`. On Windows, install the existing dependencies with `py -m pip install -r requirements.txt`, run `Start_Remote_Deck.bat`, and open the printed ICARUS PC URL. Export a v1.2 JSON backup before upgrading. Browser saves stay tied to the same origin and port.

The PC now hydrates IndexedDB before starting the world. Compatible old saves migrate without resetting crew, science, navigation or missions. The compressed v1.2 cache remains a fallback; the live save-management panel shows the actual backend, pending commits, recovery and quota warnings. Use **Commit save** or **Export complete backup** for acknowledged persistence/off-device protection.

Open Operations for the star map and Living Frontier panels. Inspect the persistent entity registry, encounter/reputation history, staged teams, incident/rescue controls, individual memories/conditions and sourced Sunday chronicle cards. SOL handles contact, field decisions and feasible rescue autonomously. Captain intervention remains optional. The paired Remote Deck tablet exposes current contacts, memories and emergency controls without running another world.

Chronicle cards are reconstructions of actual simulation events, clearly labeled as such. They support play/pause/skip; there is no invented camera footage, forced death, mandatory encounter quota or guaranteed scientific breakthrough. Weekly presentation never resets the voyage. The explicitly confirmed New Voyage control is separate.

Read ENGINEERING_v1.3.md for architecture, migration, resource equations and test commands; VALIDATION_v1.3.md for measured results; KNOWN_LIMITATIONS_v1.3.md for smaller-model boundaries, untested platforms and next work. The packaged reports contain unit/integration/adverse results, all multi-seed milestones, persistence/provenance audits, statistics and portable year-end voyages. BUILD_MANIFEST.json identifies the source and file hashes.
