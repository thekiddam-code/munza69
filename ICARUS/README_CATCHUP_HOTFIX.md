# Phase 4.7A catch-up performance hotfix

Focused repair to the existing Phase 4.7 development checkpoint. It does not finish the remaining Forward Operations/camp implementation. Read CATCHUP_INVESTIGATION.md and CATCHUP_VALIDATION.md for measured results and limits.

## Install on Windows without replacing your voyage

1. In the current host, export a complete backup through Settings → Data. Retain the old application folder and your private configuration. Do not clear browser storage or IndexedDB.
2. Stop the old companion server and close its authoritative ICARUS tabs. Extract this ZIP into a separate permanent folder.
3. With both servers stopped, transfer only your existing private configuration/pairing files as described in README_PHASE46.md. Keep the same browser profile, hostname and port: browser saves belong to that origin. No voyage is bundled here.
4. Run `Start_Remote_Deck.bat` with your existing Python environment. Open the host URL printed by the server, refresh with Ctrl+F5 if necessary, and wait for actual readiness. The boot screen still requires **ENTER ICARUS**. A writer wait is not permission to bypass the lock.
5. Confirm your existing crew, history, recordings and selected pacing. Open **Settings → General → Catch-up performance diagnostics** during catch-up. Phone/tablet UMBRA remains a remote terminal at the same paired server.

A folder change at the same origin does not require importing or resetting the voyage. If you intentionally move origins, use the existing complete-backup import workflow. Keep the original backup untouched.

## What changed

Full IndexedDB snapshots still occur every 15 physical simulation minutes. Lossless encoding of the compatibility cache and its preceding recovery snapshot now runs in a local worker. Durable writes apply backpressure rather than accumulating unlimited snapshots. Unchanged indexed-history rows are not rewritten repeatedly. Preview generation is throttled during catch-up; oversized history previews can be omitted without deleting original history or recordings. Remote commands and writer heartbeats do not wait for a successful preview.

The configured rate, synchronized-holiday rate, physical minute steps, six-hour catch-up policy, weekly episode boundaries, world schema, writer fencing and recording retention rules are unchanged. This is not a multiplier increase.

## Read the diagnostics

- Configured rate is the saved selection; interval rate is the actual calendar rate, including holidays.
- Pending seconds are **wall time**, not simulation time. At 20×, one pending wall second represents 20 simulation seconds.
- Throughput is measured simulation seconds processed per elapsed real second, including yields between catch-up pumps. It is a measurement, not a new clock setting.
- Average tick logic excludes separately measured saving/UI work. Save CPU includes validation and serialization; IndexedDB commit time is shown separately. Telemetry time measures preview preparation. Worker time and cache warnings are available in `ICARUSRuntimeDiagnostics.snapshot()`.
- Durable queue counts complete IndexedDB snapshots. The optional compatibility-cache queue may lag while catch-up continues; complete canonical snapshots remain available. A worker failure is reported and does not erase the database.

## Rollback

Export a complete current backup first if possible, stop this server and close its host tabs. Reopen the retained previous build at the same origin/profile. Keep a **pre-hotfix backup** for rollback; the former build may again exhibit slow compression. Its unchanged schema can read the canonical database, but it does not understand an intentionally lagging compatibility mirror and may report recovery. Do not delete storage to suppress that warning. Restore a retained backup only through the normal explicit import workflow if needed.

## Device checks still needed

The supplied Episode 2 backup was tested on isolated Linux Chromium copies, not on your live Windows browser database. Native APK rebuilding, physical Samsung phone/tablet/TV operation, Tailscale routing, antivirus scanning and human responsiveness review were not performed here. Existing Android/TV interfaces were retained. No antivirus settings were changed.
