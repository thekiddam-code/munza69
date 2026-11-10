# ICARUS Unified World Phase 1 Lite — verification report

Source: `c73c7da49e19fe82b2fb8028cbd6fc30915d2864` in `thekiddam-code/munza69`. Target branch: `downloads/unified-phase1-lite`. Runtime packaging verification: **passed**. Existing Phase 1 incomplete design scope is unchanged.

## Package identity

ZIP: `ICARUS_Unified_World_Phase1_Lite.zip` · 249162 bytes (about 249 KB). Original full ZIP: 8283798 bytes. Reduction: 96.99%.

SHA-256: `2be4872de017331b5615449e004b5bf8fb1e26c9f8f16b41794a9097b0940165`.

There are 43 source-identical runtime files and three distribution metadata/documentation files, 46 archive entries total. All runtime hashes match the exact pinned Git source. All manifest hashes and ZIP CRCs verify. Standalone tests, test reports, developer utilities, packaging scripts, caches, private device tokens and saved user worlds are absent. All loaded local web references resolve and the LZ-String library/license remain present.

Python package declarations are unchanged. This is not a standalone EXE or an offline Python/wheel bundle; users install CPython and requirements.txt packages for their platform. The guarded embedded browser diagnostic mode and loaded diagnostic JS helpers remain unchanged dependencies; standalone developer programs are excluded.

## Tests run against the Lite distribution

| Check | Actual result |
| --- | --- |
| Node unit suite | 158/158 passed; zero failures/skips |
| unified browser/bridge suite | 27 passed |
| stability browser/bridge suite | 30 passed |
| compatibility browser/bridge suite | 44 passed |
| production browser/bridge suite | 2 passed |
| bridge browser/bridge suite | 3 passed |
| Android-style mobile/touch functional checks | 15 passed |
| Syntax | 1 Python AST, 35 JS files and 4 inline script blocks passed |
| Runtime dependency/reference closure | No missing local loaded assets |
| Frozen source/package identity | All 43 runtime hashes match |
| Seven-real-day calendar replay | 25 simulated days, real-week/holiday transition, exact checkpoint reload; no audits failed |
| Complete save file import/reload/resumption | Passed |

Pinned suites and runners remained external to the distribution. Their runtime roots were redirected to an independent extraction of the candidate Lite ZIP; runtime source was not patched. The final ZIP was extracted independently and compared again, then ordinary-page production and Android-style touch checks were repeated against that final extraction. Overlapping inherited browser suites are not claimed as distinct new regressions.

Mobile checks exercise actual Lite HTTP pairing, incorrect-PIN/unauthenticated refusal, host-side token hashing, reconnect, course/hold on the authoritative PC simulation, thin-client behavior, viewport fit, foreign-Origin refusal, predefined keyboard action/stop contracts, private-TV address checks, TV key serialization and unpair/revocation. Desktop input and TV sockets are explicitly stubbed; no commands were sent to real applications or devices.

The new Lite calendar replay uses seed 1001 and explicit hourly real-clock inputs. At seven elapsed real days it reaches tick 36000 (25 simulated days), episode 2, 20 living founders, 0 deaths, 94 recorded stories and 5 ship arrivals. Halloween is observed once. Daily resource/navigation/crew/source checks report no errors. This is an accelerated replay, not a claim the test machine ran unattended for seven actual days.

Its complete backup imports 10659 history records, matches all checked domains (including calendar/unified state), reloads exactly and resumes tick 36000 → 36120. Import: 0.83s; reload: 1.81s.

## Static security findings

The source intentionally supports paired LAN keyboard/mouse control, clipboard/game shortcuts, an all-interface plain HTTP listener on port 8765 and optional private-IP Samsung WSS on port 8002. The inherited TV path uses CERT_NONE (certificate verification disabled). Host configuration, token-hash and TV-token files and browser-origin saves are written as documented. These can draw security-software attention and have real trust/transport risks. SECURITY_REVIEW.md inventories exact commands, network access and system effects.

No reviewed runtime command disables antivirus, adds an antivirus exception, edits firewall/registry policy, installs startup persistence or invokes a shell/process launcher. No protection was disabled or circumvented. This is not an antivirus certification, third-party dependency audit or Internet-hardened security claim.

## Tests that could not run / were not rerun

- **Windows BAT launcher and native desktop/game input**: Linux execution environment; PyAutoGUI is not installed and no physical Windows/game desktop is available. Desktop I/O explicitly stubbed.
- **Physical Android Chrome and actual Wi-Fi/firewall/hotspot path**: No physical Android hardware or target LAN. Pixel 5 Android-style touch/viewport emulation with real HTTP pairing and host bridge was run.
- **Real Samsung TV WSS connection/control**: No paired physical TV; websocket-client is not installed in this environment. Private-IP validation, configured route and allowlisted key serialization tested with a socket stub.
- **Antivirus engine scan / Windows Defender verdict**: No antivirus engine available here. Static source review only. No antivirus settings, exclusions or protections changed.
- **Fresh Windows dependency installation / fully offline Python bootstrap**: No Windows runtime. Unchanged requirements and vendor library/license are retained; Python and its platform packages are separately installed.
- **Firefox, Safari, hostile concurrent tabs, Internet penetration/DoS, dependency vulnerability database audit**: Outside the available Chromium/loopback packaging verification; not represented as passed.
- **Historical one-off v0.94–v1.3 soak/upgrade runners and new 30/90/365-day Lite campaigns**: Not rerun for a byte-identical packaging change. Current regression suites include migration/continuity cases; the new Lite soak covers seven real-time days / 25 simulation days.

## Publication protection

Only a new downloads/unified-phase1-lite branch is written. Source and existing release branches are retained. The JSON report records the main, existing downloads/unified-phase1 and source branch refs before publication; the post-publication check is added after the first new-branch push. The ZIP itself remains unchanged when publication evidence is updated.

Runtime capabilities and unfinished Phase 1 features are those of the pinned source. Lite reduces distribution contents; it does not resolve the source’s incomplete creature, art, lunar-ephemeris, knowledge-delivery or spatial-consolidation work.
