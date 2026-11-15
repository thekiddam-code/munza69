# Phase 4.8A architecture and security notes

## Baseline audit

`server.py` already exposes PIN pairing, hashed persisted device tokens, same-origin JSON commands, PyAutoGUI actions, local config macros/quick chat, TV controls, and the single-authority ICARUS bridge. `web/index.html` owns the browser departments. `umbra/app.js` wraps existing navigation/connection behavior. Its Engineering view previously displayed only the legacy CPU/RAM/mining summary, and Armory rendered config macros. There was no local sound library, host mixer, microphone capture engine or supported Sonar integration to extend. The installed native Android project remains external/unrecovered; existing browser URLs/contracts are preserved.

## Added boundaries

- `windows_monitor.py`: read-only WindowsProbe; independent cached MonitorService, one background thread started lazily by the first authenticated monitoring request. Three-second samples, ten-second slow-query cache, 60 history points, at most 24 partitions/eight NVIDIA devices/20 processes. Per-call errors become unavailable fields; a failed whole sample retains explicitly stale last data.
- `windows_control.py`: 25 fixed shortcut IDs; five fixed application IDs. Local asynchronous discovery, a single concurrent scan, strict supported launch schemes/targets, pre-launch revalidation, idempotent receipts (256 entries/120 seconds) keyed by paired principal and request ID. No remote arguments/path fields. Existing server input lock serializes new and old input actions; modifier release is attempted after errors.
- `windows_icons.py`: Windows Shell icon extraction via ctypes, GDI buffers/handles cleaned up, bounded 48px PNG output. Supports installed executable/shortcut and packaged AppsFolder sources. No downloaded icons; no fabricated success when unavailable. Legacy icons without useful alpha may have imperfect masks and require real Windows visual validation.
- `umbra/windows.js` / `windows.css`: appended companion module. Engineering-only telemetry, stable scroll/history preference; category-based, accessible command buttons; installed-icon blobs fetched with bearer headers; no credentials in URLs. One click handler per action, busy controls, long hold describes without execution. Existing macros, departments, TV and simulation UI remain.

## API surface

All new routes require the existing paired bearer token. GETs are cache/no-store protected; no CORS relaxation or public performance endpoint was added.

| Route | Behavior |
| --- | --- |
| GET /api/windows/monitor | Cached measurements/history, timestamps/errors; never a synchronous full hardware scan |
| GET /api/windows/catalog | Fixed shortcuts and discovered app metadata; no executable paths/arguments |
| GET /api/windows/icon?id=chrome | In-memory installed icon for a known ID only; no arbitrary filesystem lookup |
| POST /api/windows/refresh | Asynchronous local discovery; accepts only an empty JSON object |
| POST /api/windows/command | Exact kind/id/requestId object; predefined hotkey or discovered application launch |

Same-origin POST validation, pairing/revocation and existing request size limits remain. Duplicate successful commands within the receipt window return their original result; conflicting ID reuse is rejected. Receipts are volatile across server restart and expire after 120 seconds; the UI does not automatically retry commands or queue offline actions. Launch status means OS launch requested, not process-start certification. Existing unrestricted *local* config macro editing is retained, not exposed as remote config-writing functionality.

## Potentially sensitive commands and access

- Existing PyAutoGUI sends local desktop input. New code sends only documented fixed combinations. Run dialog opens only: it does not type/execute an arbitrary command. Lock uses Windows LockWorkStation.
- Fixed PowerShell `-NoLogo -NoProfile -NonInteractive -Command` performs local Start-menu/desktop shortcut metadata discovery and Get-StartApps. It does not change execution policy, download code, modify registry or invoke app-provided scripts. Scan timeout 20 seconds; output cap 2MB. PowerShell policy restrictions surface discovery errors; they are not bypassed.
- Read-only `powercfg.exe /getactivescheme` and installed `nvidia-smi --query-gpu=... --format=csv,noheader,nounits` have two-second timeouts. No power, fan, clock or thermal changes. Vendor utility resolution uses the existing local PATH; keep that PATH trustworthy.
- Windows Shell/os.startfile launches only locally discovered, validated allowed-app shortcuts; packaged apps use explorer.exe with a validated AppsFolder ID. There is no shell=True, arbitrary remote executable path, free-form argument or remote URL download.
- Telemetry includes local interface addresses and process names/PIDs/RAM/CPU. It is paired-only, in memory, does not include process command lines, and is not published to ICARUS or a cloud service. Local user-owned Start-menu shortcuts are trusted installation configuration; a hostile local administrator is outside this remote allowlist's boundary.

No antivirus disabling, administrator elevation, system installation, Windows default audio changes, microphone recording, Sonar edits or fan/power modifications occurred. Existing local-network/Tailscale/TV network operations are retained; new monitoring/discovery use no external service. No new pip dependencies: psutil and PyAutoGUI were already runtime dependencies; ctypes/PowerShell/Shell APIs are Windows built-ins, NVIDIA utility optional.

## Save and performance boundary

No ICARUS engine, calendar, map, crew, drone, expedition, recording or persistence module changes in 4.8A. The original 4.7C save schema/namespace/locking/backup/archive paths remain. Only server imports/routes and companion HTML plus the isolated Windows modules are changed. UI history preference uses `umbra-windows-history-v1`, not simulation saves. Metrics/launch inventory/receipts are memory-only and rebuilt after restart. On the final source, tests must cover the supplied old voyage and inherited paired remote/dispatch/record/startup behavior; see validation for actual results and gaps.

## Explicitly pending

Physical Windows sensor/shortcut/icon/launcher verification; final human visual review; Samsung/native/TV/Tailscale hardware and antivirus testing. Some AMD/Intel GPU metrics and CPU temperature APIs are unsupported. Exact Windows performance-overlay mode, editable custom launch registration, cross-process confirmation that a game is ready and exhaustive process enumeration are not implemented. Current app launch follows the registered target and exposes actionable errors instead. Entire 4.8B/C audio scope remains pending, with no simulated substitute for actual microphone isolation tests.
