# Field Deployment checkpoint verification

The whole Phase4.7 release is not complete. This milestone implements the FOC-01 freight/camp lifecycle at Landing Shelf0; camp-based services and later media work remain open. Final selected results and artifact verification below apply only to this bounded scope.

## Source and preservation

The baseline is the published catch-up hotfix `588507b19cf4078d81a43ae422059d799acdcde3`. Final frozen runtime: `13f5ed7d17182f6923e7e19f9fdbba76564dd5bc`,146 runtime files. Critical boot, writer authority, canonical/worker-backed saving, calendar multipliers and telemetry budget mechanisms are retained. The server change adds only validated freight command forms. No user database or source backup is modified by tests.

The supplied Episode2 backup is used only through isolated imported Chromium contexts. Its SHA-256 is `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`; raw contents are excluded from Git and packages. Existing original crew identities, maps, research, history and recordings must survive the original restart/remote/lazy-record tests, rather than being inferred from a fresh world.

## Functional acceptance exercised

- Physical engineer navigation, paid installation/test, freight clearances/payload, one shared transport reservation and finite crew/suit/cargo allocation.
- C04 → C03 collection/staging, eight loading minutes, pressure cycle, fifty-minute travel, eight ramp minutes and twelve camp-setup minutes.
- Persistent exterior equipment transferred once from the original vehicle kit; no phantom actors inside tents.
- Physical packing, loading, fifty-minute return, repressurization and subsequent C03 re-restraint; no instant recovery or duplicate resources.
- Recall during partial loading, cargo-power interruption, unknown field status during radio loss, legitimate returned-crew evidence, mid-load/released-camp reload, and Monday transition during active flight.
- A hidden site change remains unknown at preflight; actual approach checks divert the loaded carrier without landing or creating a camp.
- Paired HTTP deployment/hold commands, request-ID deduplication, unknown-command rejection, source-labeled unreported transit condition and receive-only mobile browser behavior.
- Existing minute/holiday/week/catch-up mechanics, crew and creature continuity, camera/replay provenance and previous archive access.

## Development findings

Strict tests caught and corrected the following before delivery:

1. Loading continued past eight minutes while ordinary staging dwell checks ran; an idempotent completed-load guard now preserves valid saves.
2. Unknown transit condition caused numeric formatting to fail on reload; unreported state is now explicitly rendered as unknown.
3. A malformed camp payload could throw inside the equipment audit instead of returning an invalid-save result; validators now reject it safely.
4. Reusing one completed sortie as autonomous justification could cause deployment/recovery loops; the consumed evidence basis persists.
5. Initial site preflight looked at actual off-site hazards; it now uses received evidence, with actual hazards evaluated on physical approach.

An earlier full run was superseded after the source-awareness refinement and is not counted as final acceptance. A frozen-runtime camera test initially compared identical frames after a fixed1.1-second wait. The test now waits for the displayed source-tick label while retaining actual pixel-change and no-world-mutation assertions. Its original diagnostic result is retained separately; accepted rerun results must be recorded rather than assuming a pass.

## Final executed results

**570 selected case executions passed against the final source/frozen runtime.** No final failures/errors remain. Counts include inherited overlap; the entire historical matrix was not rerun.

| Suite | Passing executions |
| --- | ---: |
| Node deterministic/regression models |452|
|boot|8|
|clock|4|
|deployment|7|
|diagnostics|1|
|drone|7|
|durable|2|
|early_records|1|
|existing_voyage|4|
|features|4|
|freight_remote|1|
|reliability|6|
|remote|49|
|services|18|
|visual|6|

All original 16,954 indexed history rows, all retained received recordings and first-twelve archive access passed the supplied-voyage checks. The input file SHA-256 remained unchanged. Seven deployment cases cover normal/recovery/recall/power/radio/weekly transition and changed approach conditions. The paired new freight test and 49 inherited remote cases use actual HTTP with physical controls stubbed.

The final catch-up workload drained 16,000 pending wall seconds and 5,333 physical minutes in **118.929 seconds**. Throughput: **2690.51 simulated seconds/real second**, **134.53 pending wall seconds/real second**. Configured rate remained 20×; backlog ended at zero. Remaining canonical flush: 0.008s; optional mirror completion: a further 6.833s. Writer retained; no page/console errors; decoded cache matched the canonical state after flush. All 46 observed publications returned HTTP 200, largest **109,963 bytes**, within 110,000.

Against the prior accepted hotfix's equivalent full backlog, the initial full-world hash matched; only `forwardOperations` differed in the final domain hashes. All other world domains matched exactly. All original received recordings remained byte-equivalent. These sampled Linux results do not establish physical Windows timing or statistical improvement.

The initial fixed-wait camera failure was superseded by a successful complete four-case rerun using the displayed source tick. Actual pixel-change, captured playback and no-world-mutation assertions remain. Raw PNG comparison strings were omitted from the diagnostic summary; no private voyage data are published.

Actual screenshots: `reports/phase47a/screenshots/actual_camp_body_camera.png` and `actual_empty_cargo_parking.png`, with a provenance note. These show isolated technical simulation states, not invented historical footage or the private voyage.

Machine-readable scope, cases, timings and hashes are in `reports/phase47a`. Extracted-package checks and SHA-256 verification are reported in the download directory after packaging.

## Hardware and remaining work

Tests use Linux Chromium and actual HTTP/IndexedDB/worker code with isolated technical worlds. Existing remote/TV protocol tests stub physical controls. Physical Windows responsiveness, Samsung phone/tablet/TV, Tailscale routing, antivirus scanning and native APK rebuilding could not be performed. Native Android source recovery remains pending; existing Android functionality was retained. No physical-device success is claimed.

No new thirty-/ninety-/year-long campaign is claimed for this focused milestone. The exact long-duration catch-up workload is reported separately. Art remains a simplified exterior pixel presentation with the existing camera abstraction, not a CAD/rigid-body/FOV clearance solver. The declared freight geometry is a new explicit engineering model for previously abstract spaces, not a recovered historical measurement.

Camp-based drone power/repair/rotations, ATV driving, clinical treatment, sleeping occupants, security patrols, resupply, off-shelf relocation, independent heavy rescue and freight-interface repair remain Phase4.7B. No fake working controls are supplied for them. Encoded high-rate event media/full remote archive transport remain Phase4.7C. The older checkpoint's previously reported unlocalized concurrent snapshot/TV timing observations are not claimed resolved solely by passing serial tests.

## Run the focused tests from source

```text
node --test ICARUS/test_*.js
python ICARUS/test_phase47a_deployment.py --runtime EXTRACTED_LITE_ROOT --report deployment.json
python ICARUS/test_phase47a_remote.py --runtime EXTRACTED_LITE_ROOT --report freight_remote.json
python ICARUS/test_boot_hotfix.py --runtime EXTRACTED_LITE_ROOT --report boot.json
python ICARUS/test_catchup_reliability.py --runtime EXTRACTED_LITE_ROOT --report durability.json
python ICARUS/benchmark_catchup.py --runtime EXTRACTED_LITE_ROOT --backup PRIVATE_BACKUP.json --drain --horizon-seconds 16000 --profile --output catchup.json
```

Use the existing source test dependencies/Playwright browser installation; optionally set `ICARUS_CHROMIUM`. Tests are excluded from Lite, but remain in the source branch. Do not point tests at the live browser database.
