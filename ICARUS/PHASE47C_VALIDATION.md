# Phase 4.7C verification and limits

Baseline is repository Phase4.7A (`1785987`). No separate B implementation exists on the available remote branches; unpublished B compatibility remains an explicit unresolved source dependency. This is a tested C checkpoint, not a claim that the whole Phase4.7 release or an unseen B merge is complete.

## Verified changes

Dispatch selection survives refresh/reload, the chosen scientist no longer occupies two role slots, blockers are explicit, and actual dispatched crew collect equipment, pass C02 and physically reach the asteroid. Read-only dispatch remains fenced. FOC-01's shared rover asset preserves dimensions, inventory, transport and persistent state. Its actual-renderer screenshot is in `reports/phase47c/screenshots`.

The live camera uses current authorized observations. Natural/mining/military/corporate architecture is source-based; categories never invent installed feeds. An actual displayed event produced an optional bounded captured live clip that survived save/reload. Previously captured media are never overwritten. Oversized sample tests prove the 96KiB budget without deleting original event frames. Capture is best effort only while visible/running/connected; old minute sequences remain the fallback. This is not encoded audio/video or continuous offline high-rate footage. Nominal motion playback is a simple125ms image sequence, not an AV synchronization engine.

A real paired terminal retrieved an older complete original record through the chunk service and stayed receive-only. Service tests cover ordered/repeated chunks, generation invalidation, token/ID spoof rejection, limits and queue expiry. Received IDs come from advertised archives; host reads never expose onboard/private clips. Oversized/missing transfer errors preserve the host original and explain availability.

Records 1–12 in the supplied November14 Episode2 file were retained but hidden by an eight-record UI slice, not recovered from nonexistent footage. All 20 retained records keep their IDs; the original 98 state frames and 74 PNGs are preserved. Frames without PNGs remain reconstructions. Existing retention caps/known eviction metadata remain.

## Final selected runs

**580 selected case executions passed**, with inherited overlap. Node 456 and record-service 3 cases passed.

| Suite | Passing executions |
| --- | ---: |
|boot|8|
|clock|4|
|deployment|8|
|drone|7|
|durable|2|
|early_records|1|
|features|4|
|features_c|3|
|media_remote|1|
|reliability|6|
|remote|49|
|services|18|
|visual|6|
|voyage|4|

Broad suites ran against `5038e48323d89a1844e8cdad2c4732735aba42f2`. The final bounded-media/offline-poll changes produce runtime `c3670d0fdb623415202b7888b0cd2dcbce6ac9a8`; Node 456, C feature 3 and archive HTTP 1 checks then passed again. The six catch-up reliability checks also reran on the final runtime. Their first run hit a Playwright cleanup expression that returned a function and accidentally invoked the restored telemetry preparer with null; an explicit no-return callback fixed the test harness without changing the runtime. All 149 delivered runtime hashes match the final scope. A prototype recorder test initially failed because the controlled soak page was paused; explicitly resuming via the real pause control verified the recording path. An adverse PNG test exposed a prebuffer trim defect, corrected with strict byte validation retained. No assertion was removed or source voyage reset.

The original supplied voyage passed restart/remote/lazy-record/early-archive checks, including all 16,954 indexed history rows. The input SHA-256 remains `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`. Raw private data are excluded.

The 16,000-wall-second backlog processed 5,333 physical minutes in **127.327s**, **2513.06 simulated seconds per real second**, unchanged 20× selection. Backlog ended at 0ms. Remaining canonical flush 0.069s; optional mirror 4.515s. Writer retained, no page errors, original recordings unchanged, cache equals canonical after flush. All 47 publications returned 200, maximum **109961 bytes** under 110,000. The earlier A benchmark was 118.929s for the equivalent workload; this run was 127.327s (about 7.1% slower), rather than a claimed speed improvement. These are single Linux Chromium measurements, not Windows hardware certification.

## Unavailable and incomplete verification

Physical Windows/Android/Samsung TV, Tailscale hardware, antivirus and native APK rebuilding were not tested. Existing native/web/TV paths remain; APK source recovery is pending. The complete historical Python matrix and long-duration 30/90/365-day campaigns were not repeated. Unknown additional B code/save fields cannot be certified without that source. Never replace such an installation with this checkpoint before merging/testing its source.

Existing camp-based drone/clinical/ATV services were already unfinished in the available A source; this C task does not claim to finish B. Full encoded audiovisual recording, precise camera FOV/rigid-body clearance and human final-art acceptance remain outside this bounded implementation. Chunk transfers cap originals at 512KiB; larger records remain usable on the host. High-rate event clips are opportunistic foreground captures, not a guarantee for every event. Saved simulation-minute PNG/state records retain their existing behavior.

See README_PHASE47C.md for install/backup/rollback and PHASE47C_ARCHITECTURE.md for resource/security/provenance bounds. The download directory records exact ZIP/checksum/extracted-package checks.
