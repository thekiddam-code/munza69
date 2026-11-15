# Phase 4.7A catch-up hotfix verification

This report concerns the focused performance repair, not completion of the unfinished Phase 4.7 camp/deployment scope. The frozen 145-file runtime is `ef4f12d4e745aa29de96f0fd6c6b6a6d6cc3bcc8`. All delivered runtime hashes must match `reports/catchup_fix/scope.json`.

## Matched private-voyage benchmark

Both builds imported the same supplied Episode 2 backup (SHA-256 `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`) into isolated HTTP/Chromium profiles, using the same seed and 16,000-wall-second horizon. The physical processing window stopped after exactly 120 ticks. The production pump, UI, telemetry, autosaves, actual IndexedDB and writer fencing remained active. Only the wall-time horizon and stopping point were controlled by the development harness; the performance clock was real. CPU sampling adds overhead. These are individual accepted measurements, not statistical averages or a Windows hardware guarantee.

| Measurement | Original checkpoint | Fixed runtime |
| --- | ---: | ---: |
| Saved selected rate | 20× | 20× |
| Physical minutes processed | 120 | 120 |
| Processing elapsed | 28.948 s | 1.719 s |
| Simulation seconds / real second | 248.73 | 4,188.48 |
| Pending wall seconds processed / real second | 12.37 | 208.34 |
| Mean elapsed time per physical tick, including yields/save/UI | 241.23 ms | 14.33 ms |
| Remaining canonical save/history flush | 2.708 s | 0.059 s |
| Processing plus canonical durability | 31.656 s | 1.778 s |
| Throughput including canonical completion | 227.44 sim s/s | 4,049.03 sim s/s |
| Additional optional cache-mirror flush | Already synchronous | 3.137 s |
| Processing plus canonical and compatibility mirror completion | 31.656 s | 4.916 s |

Physical processing improved **16.84×** in this pair; canonical completion improved **17.80×**. Including final completion of the optional compatibility mirror, improvement was **6.44×**. The mirror's CPU work was moved off the main thread, not made free or omitted from this report.

The initial full-world hash matched exactly across builds (`c5e052af4b8d35853ef8eab40cbc1b583cc4fa87c0e61dfdf9be8463c3827b2b`), and the final full-world hash matched exactly after 120 ticks (`1ce0048b4657630e3383ef4250ed76c6297cadd30a2a2ed55efb998bd0e5e910`). No state domain differed. Both retained writer ownership with no console/page errors. Every original received recording remained byte-equivalent. The original backup file remained unchanged.

## Sustained catch-up

The final runtime additionally drained the full **16,000 wall-second backlog**: **5,333 simulation minutes** in **117.986 seconds**, plus **0.046 seconds** for outstanding canonical writes. Measured processing throughput was **2,712.01 simulation seconds per real second**, or **135.61 pending wall seconds per real second**. Remaining backlog was zero; selected rate remained 20×. The existing fractional carry was retained, not rounded away. Writer ownership remained valid; no browser console/page errors occurred. All original received recordings remained unchanged.

The complete primary/recovery compatibility mirror finished a further 5.596 seconds later. After that, both durable/cache queues were empty and decoded physical cache equaled the canonical state. The canonical snapshot queue peaked at two. History work is separately backpressured; the recorded peak of 129 history transactions includes initial archive collection/import, before catch-up stepping, and is not a claim that initialization performs no queued work.

All 45 observed telemetry publications (including setup/flush periods) returned HTTP 200. Largest body: **109,990 bytes**, below the unchanged 110,000-byte preview budget. During the drained run, tick logic averaged 1.612 ms, pathfinding 0.047 ms/call, telemetry preparation 36.42 ms/call, and save CPU 134.42 ms/call. These diagnostic averages include their recorded scope; save/UI work is separate from tick logic. JSON validation/serialization still has main-thread cost and an individual save can exceed the cooperative 24-ms pump budget. Further incremental serialization would need separate durability testing.

The complete backlog was not run against the old slow build; its matched 120-tick comparison is the before/after evidence. An exploratory preceding stable-build profile also exposed writer-heartbeat starvation under synchronous compression; that shorter run is not counted as a successful benchmark. No lease protections were relaxed to make measurements pass.

## Regression results

**551 case executions passed** against the final source/frozen runtime, with no final failures or errors. Inherited suites overlap; this is not a unique-test count.

| Suite | Passed executions |
| --- | ---: |
| Deterministic Node models | 440 |
| active_field_profile | 1 |
| boot | 8 |
| clock | 4 |
| diagnostics | 1 |
| drone | 7 |
| durable | 2 |
| early_records | 1 |
| existing_voyage | 4 |
| features | 4 |
| reliability | 6 |
| remote | 49 |
| services | 18 |
| visual | 6 |

The six new HTTP/IndexedDB/worker regressions cover delayed-mirror restart, worker failure, changed-history persistence, atomic-import cache invalidation, primary/recovery completeness and preview backoff with live authorized commands. The production-clock diagnostics test verifies the actual Settings panel and read-only behavior. The existing-voyage suite checks original crew/maps/history/recordings, exact reload, no oversized publications, receive-only remote state and lazy media reads. All 16,954 original indexed history records were verified. Early Records1–12 remain accessible.

The separate active-field profile ran actual physical preparation, connected travel, observation and return, retaining the original assertion set. Its CPU counters are in `active_field_profile.json`; it is an explicit technical fixture, not a claim about spontaneous events in the private voyage.

Earlier technical-fixture failures were corrected before these accepted runs: the new atomic-import fixture initially supplied null before its first save, and the diagnostics fixture initially read before the disclosure toggle event. The fixes add a valid initial save and wait for actual panel population. No production assertion was removed. The earlier Phase4.7 checkpoint also documented an unlocalized concurrent remoteCore comparison and a TV tap timeout; the final serial suite passes do not establish the cause of those historical load-sensitive observations.

Raw private voyage contents and raw browser profiles are excluded from reports/downloads. Aggregate performance data are in `reports/catchup_fix/performance.json`; individual selected suites and aggregate results are in the same directory. The entire historical Python test matrix was not rerun.

## Reproduce on copies

From the source checkout, install the existing test dependencies and Chromium/Playwright. Set `ICARUS_CHROMIUM` if using a system browser. Do not point the harness at the live browser database.

```text
node --test ICARUS/test_*.js
python ICARUS/test_catchup_reliability.py --runtime PATH_TO_EXTRACTED_LITE --report reliability.json
python ICARUS/test_runtime_diagnostics.py --runtime PATH_TO_EXTRACTED_LITE --report diagnostics.json
python ICARUS/profile_field_operations.py --runtime PATH_TO_EXTRACTED_LITE --report field_profile.json
python ICARUS/benchmark_catchup.py --runtime PATH_TO_RUNTIME --backup PRIVATE_BACKUP.json --ticks 120 --horizon-seconds 16000 --profile --output comparison.json
python ICARUS/benchmark_catchup.py --runtime PATH_TO_FIXED_RUNTIME --backup PRIVATE_BACKUP.json --drain --horizon-seconds 16000 --profile --output drain.json
```

Use the same input, seed, horizon and work count for both runtime trees. The benchmark imports only into isolated technical browser contexts; it does not edit the input. Reports explicitly distinguish physical throughput, pending wall throughput, canonical flush and optional mirror completion. An incomplete run is not a pass.

## Limits and remaining verification

The actual supplied November 14 Episode 2 backup was used; the user's current Windows profile/database was not available. The approximately 1× behavior reported on that hardware was not directly reproduced here. Physical Windows, Samsung phone/tablet, TV, Tailscale routing, native APK rebuilding, antivirus scans and human smoothness review could not be performed. Existing web/TV paths are tested through emulated clients/protocol stubs, not physical hardware. Native Android source recovery remains pending.

No 30/90/365-day campaign was rerun for this targeted performance patch. Canonical IndexedDB operation is required for the off-thread cache benefit; the existing local-fallback path remains synchronous and warns when durable storage is unavailable. Unfinished vehicle departure, forward camp and camp-based rotations remain unfinished; this repair does not certify the whole Phase 4.7 release. Older full remote recording transport retains its documented limits. No new footage or voyage events were fabricated.
