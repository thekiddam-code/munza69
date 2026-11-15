# Phase 4.8A validation — software checkpoint

Final runtime `73f5504f618e570169c94ebfcd91a9416491e59b` extends confirmed Phase4.7C baseline `20a0a25`. All **154 runtime hashes** are recorded in reports/phase48a/scope.json. The supplied Field Deployment ZIP was confirmed by the user as the older baseline already included by C; no extra unpublished B merge is required. Previously documented unfinished camp services remain unfinished.

**566 selected case executions passed**, with inherited overlap (not that many unique tests). Final evidence:

| Suite | Passing executions |
| --- | ---: |
| JavaScript simulation/regressions |456|
|archive_http|1|
|boot|8|
|phase47c|3|
|remote|49|
|services|40|
|voyage|4|
|windows_browser|5|

The services run includes 19 new Windows fixture cases and 21 inherited bridge/TV/media cases. Five new real-HTTP/Chromium tests verify authenticated new endpoints, no arbitrary paths/arguments, idempotence, icon-only blob-backed tiles, hold descriptions, keyboard access, old macro dispatch, live/stale/unsupported states, history preference persistence, process scroll continuity and 393px/851px/1280px layouts. Input and Windows readings are explicitly stubbed; this is not a claim of real Windows execution. A deliberately slow probe does not block 100 cached reads; history/receipt limits are asserted. Optional failures and unsupported sensors are exercised.

The initial UI test checked an empty chart before its asynchronous response and attempted to click a game subtab without opening its Simulator menu. The final test waits for the rendered chart and operates the existing parent menu. No runtime behavior was bypassed. A code review also corrected unknown uptime being displayed as zero rather than Unavailable before the final freeze.

The original 19,257,662-byte supplied Episode2 backup was imported into isolated browser storage. Four actual original-voyage checks passed: full crew/map/knowledge/record/history restoration, restart continuity and explicit ENTER, paired receive-only terminal, source-preserving lazy original recordings and unchanged telemetry limits/error attribution. Original input SHA-256 remains `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`. Private data are not bundled. The regression driver's first invocation omitted the private backup parameter and skipped those four cases; those skips are excluded and replaced by the explicit --backup run reported here.

Inherited 4.7C physical expedition departure, rover render purity, actual captured event clips and real-HTTP original-record playback/pause/scrub passed. Eight writer/boot protections and 49 inherited remote/TV/compatibility cases passed. No ICARUS engine/calendar/save modules changed. Long-duration soaks and the complete historical Python matrix were not rerun for this companion-only stage. No result certifies final-game quality.

## Physical Windows acceptance — PENDING

No Windows session, Alienware hardware, SteelSeries Sonar, physical Samsung tablet/phone/TV, native Android source or antivirus engine was available. All physical sensor accuracy, Shell/GDI icon extraction, Start menu/Store discovery, actual app activation, shortcuts, native APK rebuild and Tailscale hardware checks remain pending. Windows-specific ctypes/PowerShell/native branches were reviewed and fixture-tested where feasible; their actual operating-system execution is not certified. Source does not alter antivirus or require administrator rights.

Perform these checks on the PC after backing up and following README_PHASE48A.md:

1. Record `powercfg /getactivescheme` before and after. Start UMBRA normally; pair/reconnect the tablet over the existing LAN/Tailscale URL. Confirm no default audio, power or Sonar settings changed.
2. Open Engineering. Compare CPU/RAM/processes/battery/uptime/drives against Task Manager/Windows, network rate changes against a known transfer and available NVIDIA sensors against the installed utility. Wait at least two samples; unavailable sensors must say Unavailable. Confirm unsupported GPU vendors do not invent values. Link state is not an internet probe. Windows overlay power mode is not reported as the active scheme.
3. Toggle short-term history, restart browser and confirm preference retention. Leave Engineering; confirm no Windows monitoring overlay appears on SOL, Lounge or Simulator. Keep multiple devices connected; observe gaming performance and stale/reconnection states when the server is stopped.
4. Open Armory / Hotkeys and Refresh installed applications. Verify the five actual installed apps and recognizable transparent Shell icons. Missing/moved apps must give actionable errors; missing icons must explicitly use text fallback. Launch each installed app, including an already-running app; Windows owns activation/new-window behavior. Do not mistake 'requested' for verified game readiness.
5. Test Start, Settings, Explorer, Task Manager, Desktop; Task View/Alt+Tab/Snap/Maximize/Restore-Minimize; previous/next virtual desktop with two desktops; Snipping Tool, Clipboard History when enabled, Emoji, Search and Run. Run opens only the dialog. Test media keys with a supported player. Test Lock last and unlock locally. Foreground applications/policy may intercept keys; report mismatches.
6. Test existing config macros, chat/emotes, TV controls and unchanged remote ICARUS. Confirm tablet/phone portrait/landscape usability, tooltips/long-hold descriptions, keyboard activation and no public executable-path entry.
7. Revoke a paired device; all new telemetry, icon and command endpoints must reject it. Stop/restart the server during a command: no offline command should be queued or automatically replayed. Receipts expire after 120 seconds/restart, so retry only deliberately.

Physical microphone-before/during/after/shutdown/forced-kill tests are **not run** and cannot be replaced by mocks. No microphone/audio routing code has been added in A. Stages B/C require separate implementation and independent private/public path validation, not silent device-default changes.

## Known limits / remaining work

- Phase 4.8 as a whole is **not complete**. 4.8A is a tested software foundation pending real Windows/human acceptance.
- CPU temperature, non-NVIDIA GPU performance and Windows performance-overlay mode may be unavailable. Inventory is the top 20 measured processes and active IPv4 interfaces, not an exhaustive process/network analyzer.
- Discovery supports five named apps through compatible local shortcuts/registered packaged apps. A missing normal shortcut must be repaired locally; no remote arbitrary launcher is provided. Shell owns startup/existing-instance behavior, so launch success means request submission. Legacy/monochrome icon transparency requires Windows visual review.
- No new pip dependencies; Windows PowerShell/Shell/ctypes built in; existing psutil/PyAutoGUI retained, nvidia-smi optional. No policy/power/driver/fan/default-device/antivirus changes.
- 4.8B local sound import/library/tap/hold playback and 4.8C microphone calibration/normalization/limiting/Sonar injection/emergency reset remain **not started**. Their hardware acceptance tests remain pending; no decorative controls pretend otherwise.

See PHASE48A_ARCHITECTURE.md for files/endpoints/security details, README_PHASE48A.md for installation/backup/rollback, and downloads/phase48a for final extracted-ZIP verification and checksum.
