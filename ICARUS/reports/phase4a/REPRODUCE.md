# Phase 4A evidence reproduction

Runtime frozen at 3b6d986f5e26c3fa33c42c61abc3f0e830b286c6; no runtime edits during verification. Final documentation-only source commit and ZIP identity are in BUILD_MANIFEST.json and package_verification.json. Compare all 90 runtime hashes to runtime_identity.json.

Development dependencies: Python 3.12, Node 24, Playwright 1.62, Chromium /usr/bin/chromium, Pillow, original runtime requirements. TV/desktop I/O is deliberately stubbed. No physical Windows, Android or TV test is implied.

1. Extract Lite into tested/ICARUS_SOL_Command_Interface_Phase4_Lite. Source checkout is separate; adjust SOURCE, paths and ICARUS_CHROMIUM in the external harnesses for your environment.
2. `python run_suite.py NAME` with NAME cinematic/stability/compatibility/interface/production/bridge/umbra/tv_service. The wrapper imports pinned source tests and points runtime roots/imports to Lite. The compatibility suite also needs the authentic v1.3 web fixture (ICARUS_V13_WEB); missing it is a failed/unavailable test, not permission to skip assertions.
3. Copy source test_*.js to an external node folder, symlink web to Lite/web, and run `ICARUS_REPO_ROOT=/path/to/repository node --test test_*.js`. The repository is required only for byte-exact historical sprite comparison.
4. Run mobile_functional.py with PYTHONPATH pointing to Lite; run tablet_touch.py. These use real local HTTP/Chromium touch emulation, with host/TV I/O stubbed.
5. `python migrate.py backup.json --report result.json`, ICARUS_BACKUP_TIMEOUT=600000. Historical fixtures are genuine Phase 1/2/3/3.5 full exports; one Phase 3 fixture has 19 living plus Nadia's memorial. Full donors are not published in Lite; their names, digests and measured migration domains are documented in results.
6. From committed project source run unified_soak.py --seed 1001 --days 30 --scenario normal --output PATH, then seed 4807 --days 7 --scenario compound. These advance hourly real-calendar intervals through production simulation controllers, disabling per-step autosave only in the driver; checkpoint reloads and full history exports are real. Fixed start 2026-10-28 UTC, America/Chicago; a synchronized holiday changes effective simulation duration. Compound explicitly starts three damaged pieces of equipment and one injured crew member; it does not fabricate resulting events. Use summarize_refinement_campaigns.py only after both campaigns finish.
7. Run verify_phase4a_package.py ROOT --report static.json against independent extraction. It checks source hashes/syntax, unchanged native protocol primitives/key allowlist, original assets and exclusion of private credentials/tests/APK.

The source/runtime changes are committed. Reports preserve actual runs; test count includes inherited regression cases. Retry a failing driver only with a documented cause; do not suppress assertions or relabel native emulation as device testing.
