# Phase 4A engineering changelog

Scope: refine the existing UMBRA browser Remote Deck and Windows Python host without replacing the installed Android application or changing ICARUS world authority. See PHASE4A_VALIDATION.md for measured results and PHASE4A_LIMITATIONS.md for open gates.

## Milestones

- `91c249a`: bounded source-backed SOL companion projection; reusable existing TV transport; authenticated, monotonic, server-managed sleep timer. Timer replacement, cancellation, target/owner changes, restart and late wake invalidate pending power-off operations. No automatic repair, simulation event generation or host shutdown added.
- `65e68f1`: cool corporate UMBRA shell, tablet right-side remote and separate phone layout, validated local profiles with reversible editing, original renderer reuse, truthful camera/follow labels, local SVG icons, default-off fictional arcade gallery and guarded idle decoration. Existing Engineering/Lounge/Simulator/Armory functionality retained.
- `3b6d986`: preserve exact legacy TV response and Android telemetry contract; companion metadata requires browser opt-in. Harden offline interactions, touch edits, connection recovery, timer late wake and source freshness. Added source-based installation/recovery/capability documentation and browser/service regressions. This is the frozen runtime tested by the final evidence.
- Final evidence milestone: independent ZIP extraction, full regression suites, phone/tablet touch checks, five historical full-history migrations, representative campaigns and byte/hash/security checks; no runtime changes after freezing. The package's BUILD_MANIFEST.json identifies its final source commit and every retained file.

## Architecture and tradeoffs

`tv_service.py` is a required standard-library runtime module; `server.py` retains the old port, pairing files, token hashes, host authority and key allowlist. A dedicated TV lock avoids blocking the simulation's bridge lock during TV I/O. A successful send is not a physical-device acknowledgement. The timer is intentionally volatile and skips callbacks more than 60 seconds late.

`web/companion-view.js` projects existing knowledge, hardware coverage, physical locations and sourced activity without mutating simulation state. `web/camera-sprites.js` reuses original standard/Canadian schematic renderers. `web/umbra/` separates bounded layouts, icons, companion rendering, TV interactions and optional fictional presentation from the old host shell. Client preferences are distinct from world saves; no second simulation or namespace is introduced.

The browser uses the existing telemetry poll and opts into bounded companion metadata; native clients keep their original response. New local assets and profile editing work after disconnection in an already loaded browser. Fresh reload still needs the server; a service worker/native packaging change is deliberately absent. Browser defaults leave corporate anomalies and Arcade Kill Cam off. The six supplied GIFs are fictional, 12 frames at 240 ms each, never recorded simulation events.

## Compatibility and open work

Retain local config.json, paired_devices.json and samsung_tv.json during an upgrade. Back up the actual browser voyage before changing files; preserve origin and profile. See README_PHASE4A.md for installation and rollback. The original APK remains installed and is not rebuilt, removed or replaced. Recover its original Android Studio project before preparing a native update; preserve its application ID and signing continuity. Native APK build remains pending source recovery.

No new public networking, native TV app identifiers, streaming, push, voice, arbitrary command editor or universe expansion. Physical Windows, Android/Tab S5e, Samsung TV, antivirus and human usability validation remain unexecuted. Core simulation behavior and calendar rules are retained rather than tuned to make campaign results look better.
