# Phase 4.3 verification and acceptance record

The baseline was inspected and tested before implementation:332 Node cases passed on verified Phase4.2B d5add5b. Main f5d63a4 contributed approved backlog scope without replacing that engine. Integration/reliability commits are f203314 and127bda0; the latter was rejected after an actual campaign exposed a recovery deadlock.

The corrected runtime is **13ab44756314a1e99587c3070914cefbfbe26fe0**, exported with122 exact runtime files. Final tests/campaigns use that immutable export. Later documentation, evidence and packaging commits must retain those122 hashes. The package BUILD_MANIFEST identifies its exact committed source; package verification compares all runtime hashes to the corrected export. No final runtime patch is silently substituted after testing.

## Executed mechanics and compatibility coverage

- The complete Node suite executed346 cases with zero failures. Fourteen new systems tests cover additive migration/30-room mapping/normal1g, independent controls/circuits, rejected authorization/ranges, real zero-g mobility/anchoring, discovered loose objects and deterministic restoration/reload, finite energy without SOL, conditional fall harm, once-per-tick wear/energy, stale instrumentation, bounded severe diagnostics, unqualified/uninformed/unresourced repair rejection, empty-energy cold start, real drive/bridge power gating, non-work recovery timers and preserved emergency preemption.
- Six focused physical-browser cases pass: actual zone controls and exact reload, actual floating crew/discovered objects, real informed engineer tools/parts/travel/diagnosis/repair/test with camera pose and source, local outage/recovery, mid-repair exact reload/continuation, and zero-g rest3→2→1→0 followed by a new autonomous choice.
- Final remote-browser suite36/36 passes. Its two new cases use actual HTTP pairing, validation, request deduplication and an emulated phone reading the same host gravity. The remote has neither `__icarusSoak` nor the ship simulation module. Existing single-host, stale/reconnect, live-source privacy, responsive UMBRA, TV protocol, layout and late-voyage telemetry budget tests remain.
- Final production clock4/4 passes: ordinary4×, pause, selected20× switch/reload, synchronized holiday1× and unique sources. Clock/calendar source files remain unchanged.
- Bridge/TV/classified service tests18/18 pass on the unchanged service implementations; remote tests additionally exercise the modified server command whitelist.
- Python compilation passes for modified server and new test/campaign/packaging/audit tools. Node/browser execution loads all new runtime modules.

The full inherited browser suite, final elapsed watch, campaign audits and exact packaged-runtime checks are recorded in the results appended below. Do not substitute the earlier development run for those final results.

## Failure investigation and provenance

The first127bda0 candidate seed1001 selected20× lost all20 crew by tick44160 (day30.6667). Clean invariant checks did not make it acceptable. Source records and repair state identified support-dependent work restrictions freezing ordinary rest timers; emergency readiness also prevented new component work from being preempted. Both defects were corrected with explicit tests. No world/resources/crew were reset to obtain recovery. PHASE43_RECOVERY_INVESTIGATION.md supplies source IDs and a causal timeline.

Corrected13ab447 repeated identical seed/start/timezone/selected20× for40 ship days: all20 at100 health, two actual autonomous paid generator repairs and powered tests, generator79.2092% in service, no open component order, exact checkpoint reload and empty resource/world/operational audit errors. This comparison verifies the correction for this seed, not guaranteed survival in every future voyage.

An earlier non-frozen development browser run executed77 cases and had one30-second reload-startup timeout in `test_military_archive_is_not_shared_until_report_received` while several campaigns/suites ran concurrently. Its results are retained as diagnostic evidence. The corrected immutable full run separately executes that case under the original assertion/timeout; no assertion was weakened. Other early unit-fixture adjustments are documented in progress rather than portrayed as simulation successes.

## Acceptance mapping

| Requested behavior | Executed evidence / boundary |
| --- | --- |
| Healthy1g, authorized adjustment, independent neighbor, correct power dependency (1–4) | Node normal/zone/circuit/finite-power tests, actual local and paired browser controls. |
| Zero-g movement/objects, restoration (5–6,11) | Actual float actor/loose object projection, support-dependent work/mobility, conditional impact/restoration tests and inspected technical-fixture screenshots. No full physics claim. |
| Fault knowledge, correct location, visible real repairs, actual outcome (7–10) | Physical engineer browser workflow requires diagnosis/parts/repair/testing phases and `repair` camera pose; corrected campaign source-linked paid repairs. |
| Accurate telemetry and persistence (12–13) | Paired actual HTTP matching state, stale instrument tests, exact mid-work reload and genuine older backup import coverage in full browser suite. |
| Acceleration and weekly continuity (14) | Once-per-tick controls; production4×/20×/holiday1× tests, campaign hourly real intervals and exact checkpoint reload, actual elapsed watch. |
| Desktop/Android agreement (15) | Protocol plus Chromium phone/tablet emulation verified; **physical Android/native APK agreement remains unverified**. Native sources/APKs untouched. |
| Preserve4.2B cameras/personality/transit/Follow Crew (16) | Full inherited browser/remote/Node coverage, actual source-based visual examples/watch; final art/crowd/cabin-rescue limits remain. |
| Operations without SOL (17) | New hardware controls/controller model operates with no SOL object and does not create an AI lifecycle authority. **Complete all-AI termination/takeover behavior across the legacy game is not globally certified.** |
| Extended unforced operation (18) | Corrected40-day replay plus weekly normal/adverse campaigns below. Adverse initial conditions are explicit fixtures; no forced drama or guaranteed repairs. |

This is a verified implementation increment within stated model limits. Physical-device gates and broader recovery/physics/art refinement mean the complete phase/final game is **not** declared unconditionally complete solely from automated tests.

## Unavailable/manual checks

No physical Windows laptop, Samsung phone/Tab S5e/TV, installed-native-APK rebuild, real LAN/Tailscale, human accessibility/GPU or antivirus test ran in this Linux environment. Desktop/TV I/O is stubbed in browser tests; HTTP/auth/TV protocol tests are distinct from hardware. Original installed/native Android functionality is preserved, with the earlier Tab S5e native source still pending recovery rather than unsupported. No antivirus was disabled. Use README_PHASE43.md and PHASE41_DEVICE_TESTING.md before replacing a working installation.

## Final frozen-runtime results

The immutable corrected export passed346 Node,78 full inherited core-browser,36 real-HTTP remote-browser,4 production-clock and18 service cases:482 main case executions with zero final failures/skips. The focused six-browser development rerun is additional evidence, not added again to that total. Exact test names, timings and failures are retained in machine-readable reports. Any additional legacy/package smoke executions are reported separately.

All three corrected campaigns passed the independent full-history source/privacy audit, daily conservation/world/operations checks and exact checkpoint reload. Production real-week/holiday rules remain active; seven real days here correctly equal25 ship days rather than forcing28.

| Campaign | Real days / ship days | Alive / deaths | Arrivals | Science cases | Conversations | Source records | Paid new-component repairs | Sunday films |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| adverse_4807 | 7 / 25 | 20 / 0 | 5 | 25 | 427 | 12463 | 1 | 1 |
| normal_1001 | 7 / 25 | 20 / 0 | 5 | 21 | 470 | 12647 | 1 | 1 |
| recovery_1001 | 2 / 40 | 20 / 0 | 5 | 21 | 794 | 19884 | 2 | 0 |

Science cases are investigations, not claimed confirmed breakthroughs. No lethal encounter or Legendary segment was manufactured. Normal/recovery worlds use only the fixed seed/clock; the adverse world explicitly imports B07=10%,C09=32%,C07=45% and one45-health-point injury through the backup interface. That fixture is validated before advancement and is not labeled an organic incident.

The resource ledger records actual additional gravity/environmental electrical consumption:1509.816 units normal25-day,1509.720 adverse25-day,2409.408 recovery40-day, plus finite paid repair energy/tools and physical collected replacement parts. Existing generation/conversion sources and inventory ledgers account for these quantities; all daily conservation errors are empty. The raw ledger and aggregate totals are in campaign_summary.json. New hardware summary histories remain bounded; snapshot growth still reflects genuine retained source history (about2.73→8.03MB normal25-day,6.89→10.90MB recovery20→40-day). Arbitrary-duration archive growth is not declared solved.

The actual elapsed host watch ran normal and20× phases for181.71/180.44 seconds respectively, measuring3.9624×/20.2835×. Reload resumed tick42 at tick42 with20× retained; the host reached tick73, all20 crew alive, six completed lift trips and one actual conversation. Phone disconnect/reconnect and source uniqueness checks pass. No fake clock/soak hooks or injected incidents/needs/relationships were used in this watch. The whole harness took376.56 seconds including setup/teardown.

Performance is measured Linux headless Chromium, not Windows hardware certification. The final post-reload sample counted789 main and1380 preview frames with1838.5ms accumulated drawing time (~0.85ms per counted frame); that segment's maximum was51ms, and the maximum across sampled segments was122.3ms. Brief rendering stalls remain visible rather than hidden by an FPS claim. The simulation maintained the measured pacing independently of drawing.

Technical visual fixtures were separately captured and inspected: an actual paid repair with positive progress at the C07 generator anchor, a real float actor plus one discovered loose sample container in0g, and the existing Engineering controls. Those examples are explicitly labeled fixtures, not recorded video or natural campaign events. They preserve the existing detailed pixel scenes.

## Delivery verification boundary

The Lite ZIP is built from a committed source tree with all122 runtime files and documentation, excluding tests/reports/development tools/generated secrets/test worlds. Adjacent package_verification.json records the source commit, SHA-256, ZIP CRC and manifest verification; delivery test reports record any tests executed against the extracted exact ZIP. Runtime equality against13ab447 is checked separately. The evidence ZIP contains isolated fictional test worlds and development diagnostics; **never import those as your own voyage**. Use your own exported backup.

No source/main/release reset or native APK replacement is part of this delivery. Development changes live on codex/living-ship-operations-phase4-3; installation, backup, migration and rollback instructions are README_PHASE43.md.

Additional legacy/continuity suite:19/19 passed against the same immutable corrected runtime, bringing the main plus legacy executions to501. This includes old transition/repair/research/medical/emergency, genuine harm/death/memorial, failed-team cargo and reload behavior; it does not activate the Extended Universe in core.

Reproduction fixtures: the full old-voyage import and late-telemetry cases use real archived Phase4/4.1 campaign backups; the true-v1.3 case uses the cached v1.3 source web tree from ea984a8749c907fd373492283f085d769eebbd03. These are included as clearly labeled test fixtures in the evidence bundle, with hashes. `verify_operations.py` accepts portable paths for them and for an extracted Lite runtime. They are not personal user saves and must not replace the user's voyage.
