# Phase 4.2A engineering changelog

Baseline: validated Phase 4.2 `7f3fb0d`. Additive merge of main `0ce493c` preserves the backlog and separate native S24+ launcher/APKs without reverting the newer simulation.

- Added original cached Canvas pixel art for live room/crew views; fixed aspect distortion and retained explicit classic schematic/replay controls. No imported rendering engine, game assets, extra world or new runtime dependency.
- Added real conversation-seeking phases and visual intent. Iris/other seekers look, approach actual eligible local crew, wait/talk only through the original source-backed social path, or give up/interruption. Speaker/listener positions/facing and source labels are persistent; rendering never drives decisions.
- Added shared observation projection, four rotating/pinnable previews, manual promotion/held primary, lower-rate previews, visibility/reduced-motion handling and bounded walk interpolation.
- Excluded ordinary quarters, executive and hygiene cameras in source selection/capture, projection and camera rotation. Navigation scenes remain reconstructions; no invented recorded video or REC flags.
- Added instrumented ship-room schematic with focus, pan/zoom, actual atmosphere/equipment/door/hazard data and persistent effective illumination. Unsupported biological sensors/CO₂/HVAC/circuit/suppression controls remain explicitly unavailable.
- Added accessible quick actions to the surveillance roster and original Home Crew Location widget. Active menu focus is preserved across updates. Profiles contain only allowed received evidence; Creator retains private inspection.
- Replaced separate Home collapse buttons with click/keyboard headers, retained presets and per-screen layouts, compacted the obstructing status strip, restored themed scrolling and exposed normal Pause/Resume in Bridge. Speed/debug/reset remain Creator-only under the approved updated permission boundary.
- Fixed observation data entering the legacy payload and the confirmed modern late-voyage packet overflow. Legacy remains ≤14,000 serialized characters; authenticated host publication cap becomes 128 KiB; commands remain 4 KiB. Pairing, host lease, deduplication and save authority retained.
- Added source/behavior/browser/protocol/performance tests and actual normal-time observation tooling. Retained failed development diagnostics separately; corrected test-driver path/clock/fixture-compression errors without discarding product assertions.

Actual accepted evidence: 430 automated case executions, 26 emulation checks, two seven-real-day campaigns, full-history audits and a 1,800.9-second ordinary autonomous watch. A final Home roster UI-line patch was tested separately after the frozen watch; all other runtime lines/files retain the watched implementation. See PHASE42A_VALIDATION.md for measured performance and exact provenance.

Not complete: full dedicated character/creature state artwork, unique authored room maps and richer furniture/crowd movement. Physical Windows/Android/TV/Tailscale/AV and human visual/GPU validation remain unverified. The 20× issue and classified/4.2B scope remain deferred. This batch deepens watchable ship life; it does not complete final-release readiness.
