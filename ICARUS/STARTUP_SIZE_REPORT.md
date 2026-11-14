# ICARUS 4.6 — Startup request-size investigation

## Confirmed cause

Reproduced with the user's exact `ICARUS_Phase4_6_Boot_Hotfix_Lite.zip` and an isolated imported copy of their actual Episode 2 voyage backup, then reloaded from persistent IndexedDB. The original files were not modified. Tests never cleared the user's browser storage.

The failing operation is **POST `/api/icarus/host/publish`** in `web/icarus.html`'s companion synchronization loop. The Windows-compatible Python `server.py` rejects request bodies larger than **131,072 bytes**. The original outgoing packet was **132,753 bytes** in the first captured reproduction; repeated traces measured **132,755–132,757 bytes**. HTTP **413** returned `{"error":"Too large"}` and Chromium logged a failed resource request. The saved world had already restored successfully: IndexedDB ready, storage warning null, tick 46035. No uncaught JavaScript exception accompanied the size failure.

This is a companion-server request limit, not a corrupt ZIP, oversized HTML file, IndexedDB quota error, or failed save import. Large operational-history previews together with exploration and observation projections overflowed the complete envelope. Representative untrimmed components were operations 43,321 bytes, observation 32,378, exploration 14,376, expeditions 6,455; the envelope also included classified data, legacy telemetry and acknowledgements. Those are encoded component sizes, not separate failing requests.

The previous drone limiter only removed PNG images. When there were no further image previews to remove, it returned a still-oversized payload. It measured the full envelope but had no final size check or fallback for oversized non-image content. The synchronization catch then treated the server's size rejection as a host/writer failure. A separate confirmed alias defect allowed deleting a projected image to delete the same property from an archived world frame. This patch prevents further such mutation; it cannot recover pixels absent from an earlier backup.

## Implemented correction and scope

- `web/telemetry-packet.js`: pure, complete-envelope UTF-8 budgeting at **110,000 bytes**, below the unchanged server limit. Deep-copy the disposable packet; reduce optional duplicate historical previews and captured previews only as necessary; retain a recent captured image when it fits. Explicitly label a limited preview and omitted pixels. Preserve live crew identities/conditions, known sectors, commands and receipts. If irreducible data cannot fit, report a local preview error rather than transmit an oversized packet.
- `web/drone-ops.js`: detached frame previews prevent archive aliases. Metadata-only local lists defer copying frame payloads. Explicit received-record access returns an isolated copy and never reveals onboard/unreceived recordings.
- `web/drone-ui.js` and `web/icarus.html`: resolve local archived frames on actual selection/playback, while normal hidden-panel refresh uses metadata. The state archive remains fully restored for simulation consistency; this is lazy media-preview copying, not a partial world restore.
- `web/icarus.html`: classify payload validation errors separately from host lease/network failures. Authentication, generation fences, write protection and disconnect handling remain in force.
- `web/operational-ui.js`: label limited remote history. This is a bounded remote preview, not unlimited remote archive browsing.
- `server.py`: keep existing request limits, but report the affected operation, received bytes and allowed bytes on 413.

No dependencies were added. No database migration, content reset, archive pruning or writer-lock bypass is introduced. The boot-screen files, storage module, authority module and server lease implementation remain unchanged from the supplied build. There is no new external network endpoint, shell execution or system/antivirus modification.

## Existing-voyage verification

The supplied 19,257,662-byte backup contains 20 crew, Episode 2/tick 46035, 16,954 original history records, 20 known exploration sectors and 20 drone recordings with 98 recorded state frames and 74 captured PNG frames. Tests compare the complete crew, knowledge, asteroid map, drone archive and field-evidence domains against the supplied backup. Every original history row must remain unchanged; the complete retained snapshot and full retained history must also be identical before and after restart. A prior fixture's legitimate startup history entry is allowed in addition to the imported rows; no original row is replaced or dropped.

Actual browser checks cover restart from IndexedDB, explicit ENTER, selected recording playback with all original frames, no eager frame retrieval during hidden polling, a paired phone-sized receive-only terminal, controlled HTTP 413 without loss of writer authority, and subsequent successful publishing. The original private backup is not distributed or published. Missing captured pixels are never fabricated or claimed recovered.

Final exact-source and extracted-package results are recorded in the accompanying verification files. Earlier diagnostic runs are not represented as passing release verification. The suite caught an initial preview regression (all images removed despite a feasible smaller history); it was corrected with a regression test. The retry test was also synchronized with navigation: it previously evaluated an unguarded global during document reload. Runtime boot code was not changed to accommodate that test.

## Limits and manual checks

Validation runs in Linux Chromium against the real companion HTTP server and an isolated copy of the user's existing Windows-exported voyage. Physical Windows startup in the user's browser profile, installed Samsung Android APK, Tailscale network, physical Samsung TV and antivirus scans cannot be performed in this environment. TV protocol/input operations are mocked where their tests say so. These are not physical-device results. The native Android project remains pending source recovery, not permanently unsupported.

A remote preview can omit older history or captured pixels to remain bounded. Full host playback remains available for received recordings. A future irreducibly large core telemetry packet fails visibly without modifying the world; this patch does not promise unbounded live payloads. Entire world restoration remains atomic; only presentation/media-copy work is deferred. No unrelated gameplay, clock, exploration or UI redesign is included, and no long-duration campaign was required or claimed for this startup-only hotfix.

## Final executed verification

Frozen runtime `20001c00ffaf6538cf7bb3dbbcf3c1b2dad69a06`, test source `5abc0fa7a5744eaae8fa8f9684444c72e92c8087`. All runtime hashes are verified in `reports/startup_size/scope.json`.

| Suite | Passed case executions | Duration |
| --- | ---: | ---: |
| node | 413 | 19.200594262 s |
| services | 18 | 0.003 s |
| boot | 8 | 45.963 s |
| remote | 49 | 269.624 s |
| drone | 7 | 57.783 s |
| clock | 4 | 13.487 s |
| visual | 6 | 14.226 s |
| user_voyage | 4 | 170.075 s |

**509 source case executions passed; no skipped cases in these selected suites.** These are executions across overlapping suites, not 509 independent scenarios. On the final trace, restored-world POST bodies measured **109918–109920 bytes**, all HTTP 200; startup displayed ICARUS ONLINE, writer ownership true, IndexedDB ready, warning null. See `reports/startup_size/reproduction.json` for sanitized before/after console and request evidence, including any unrelated initial resource diagnostic. The supplied backup SHA-256 remained unchanged.

The extracted ZIP receives a separate existing-voyage and boot check before publication; see the download folder's verification files for those actual results. Full-source test entry points are `node --test ICARUS/test_*.js`, the service unittest modules, `verify_operations.py` for remote/drone/visual/clock suites, `test_boot_hotfix.py`, and `test_startup_size.py --backup <private-backup>`. Select the extracted runtime with `--runtime` and Chromium with `--chromium` or `ICARUS_CHROMIUM`; tests and development tools are intentionally excluded from Lite.
