# UMBRA 3.0 — Engineering, navigation and shared PC connection

These two Phase 3 addenda are applied incrementally to the existing native 2.3.1 launcher. Kotlin/Compose launcher, Android widgets, app launching, animation policy, soundboard engine and Windows/ICARUS server are preserved. This is not a rebuilt launcher or an assertion that unspecified earlier Phase 3 work has been implemented.

## Navigation and TV removal

The primary navigation is **HOME | APPS | DECK | SIMULATOR | ICARUS | CONFIG**. The internal `COMMAND` route ID stays for migration; its visible label is DECK.

- HOME retains existing pages and adds named independent dashboard presets.
- DECK contains Command library, Engineering, Soundboard, Instant Buttons and preserved Android Device controls. The existing Home pull-down still opens those Device controls and preserves the second-swipe notification guidance.
- SIMULATOR separates Rocket League quick chat, Fortnite emotes, Minecraft configured mining controls, and existing ship simulation controls. Missing mappings remain unavailable; actual simulation telemetry gates the built-in ship controls.
- ICARUS contains native PC connection status/pairing and the existing PC Remote Deck shortcut. The companion has no native desktop video/input stream API: remote access opens the configured existing interface in the browser. No simulated desktop or unsupported RDP implementation is claimed.
- CONFIG retains system/app settings and the server-owned soundboard Audio Output page.

No Lounge / Samsung TV page, TV key editor, TV pairing UI, Lounge URL setting or Lounge status toggle is exposed. Native HTTP dispatch no longer allows the TV endpoint. Legacy `TvKey` mappings, URL and grid positions remain inert in stored/imported configuration to avoid corrupting unrelated layouts and exports. They are omitted from all native action catalogs and cannot execute. Shared ICARUS TV backend and the TV itself are unchanged; Samsung's official/native remote remains independent.

## Engineering and HOME presets

DECK → Engineering has dedicated CPU, GPU, RAM, power/battery, network and supported PC action modules. HOME → long-press page heading → Add widget exposes the same six modules. Each instance has its own stable ID, existing snap-grid placement, size, collapsed state, detail preference, transparency and accent. Long-press/drag uses the existing contextual editor; Configure adjusts display preferences, Resize adjusts grid size, Collapse/Expand retains the instance. Active visible instances share telemetry; offscreen pages, clipped widgets, collapsed widgets and inactive presets do not request fast sensor updates. Expanded details use the existing transition engine, including master-off behavior.

The HOME Presets bar switches named dashboards. Create a blank preset through Presets (up to eight); each retains its own existing pages, widgets and HOME grid arrangements. The existing desktop becomes Default without a reset. Switching snapshots the current HOME layout, loads the selected one and leaves DECK/soundboard grids and all command mappings alone. Original layouts remain authoritative in the existing active `desktop` field; inactive snapshots use `homePresets`. Third-party Android widget bindings are retained across inactive presets and are stripped from portable exports across **all** presets. Preset switches cancel only a pending widget binding and clear cross-preset layout Undo; they do not delete saved Android bindings.

Schema 5 imports versions 2/3/4/5. Local DataStore name and `config_v2` key are unchanged. New defaults enable the compact PC indicator; old per-app/panel settings persist. Output devices, favorites and normalization remain authoritative on the ICARUS sound server: no preset switch, migration or TV removal sends an audio-output reset.

## Shared telemetry and connection state

The existing `InstantController` is extended; the same native HTTP client, encrypted server-bound credentials, status snapshot, action gate and token provider remain. One lifecycle-bound root loop handles all header and Engineering demand. Multiple widgets register consumer IDs; they do not start collectors or individual network loops.

- Header/PC remote status checks: at most every 30 seconds while visible.
- Visible Engineering demand: one shared monitor request every 3 seconds; normal command/status mappings and Windows action catalog reuse their cached snapshots (30/60 seconds).
- Older companion without the monitor endpoint: actual `/api/status` CPU/RAM every 10 seconds while Engineering is visible; advanced sensors explicitly unavailable, missing endpoint retried at most once a minute.
- Low battery or Android power saver: shared checks reduce to once a minute.
- Hidden/stopped launcher: root requests cancel, no polling, service or wake lock. Re-entry requests fresh authenticated status. Inactive readings never establish a green connection.
- Manual Reconnect cancels the prior polling iteration and checks the configured server immediately. Network changes also trigger a fresh check. Concurrent control actions share the existing gate and cannot enqueue repeated taps.

Connected (green) requires a successful authenticated response from the configured companion. Connecting/reconnecting is amber; no pairing, network errors, malformed responses or inactive status are offline/red. A colored **● PC** button is in the existing header on all six tabs. Its 48 dp touch target opens a compact panel with PC name, status, detected address class, measured HTTP round-trip latency, last response and Reconnect. CONFIG → ICARUS → Show PC connection indicator hides it persistently without modifying HOME layouts or Android fullscreen flags. Status uses text/accessibility descriptions as well as color.

PC names are displayed only when the companion actually reports `hostname`/`computer_name`; inspected older versions do not report these and show **Not reported by companion**. Tailscale DNS/address ranges and local private addresses are classified conservatively; the actual transport route is explicitly unverified. Custom public DNS aliases remain Unknown. No DNS/Internet probing, invented host name or asserted Tailscale session is used. Latency is HTTP round-trip time, not ICMP ping or internet latency.

## Existing companion contracts

The Windows APIs are already present on `codex/umbra-windows-command-phase4-8` and the soundboard/Sonar branches (soundboard reference `958f3efdb72e2998a1b741e7670703c69ada1569`). No ICARUS server file, collector or web asset is changed.

| Endpoint | Use |
| --- | --- |
| `GET /api/status` | Existing authenticated PC command mappings and basic CPU/RAM fallback |
| `GET /api/windows/monitor` | Existing shared `MonitorService` sample, age and sensor metadata |
| `GET /api/windows/catalog` | Supported fixed Windows hotkeys; no arbitrary executable/path controls |
| `POST /api/windows/command` | Exact `{kind:"hotkey",id,requestId}`; server validates discovered predefined ID |
| Existing `/api/sounds/*` | Unchanged native soundboard catalog, playback, favorites and saved output |
| Existing `/api/icarus/telemetry` and `/api/icarus/command` | Ship controls in SIMULATOR, separate from PC Engineering |

Use the existing working Windows/soundboard-capable companion and Tailscale setup. The older ICARUS server on main lacks the extended Windows monitor and soundboard APIs; pointing UMBRA at it provides only the status fields it supports. Do not overwrite a working companion/private library with that older server.

GPU utilization/VRAM/temperature, CPU temperature, battery, power scheme and network rates use their actual optional sample fields. Missing, stale (>20 seconds including reported sample age), unsupported, invalid or offline sensors show Unavailable. CPU/RAM basic fallback is labeled. Network link-up is not described as proven internet connectivity. Power actions appear only when the server advertises support; Lock PC requires explicit UI confirmation and uses the existing backend action. No unsupported shutdown/power-mode changes are invented.

## Verification, installation and limits

See [executed results](verification/phase3/RESULTS.txt), JUnit XML, lint, build log and native host renders. Tests cover older-schema migration, retained-but-inert TV mappings, exact authenticated telemetry/action payloads, cached/shared polling and cancellation, unavailable sensors, per-preset widget bindings and layouts, all six native destinations, indicator preference persistence, independent Engineering resizing/collapse, soundboard and gaming regressions. Renders use generated/explicit backend fixtures and are not physical-device captures.

Install the signed debug APK over 2.3.1 to keep local settings; the supplied artifact retains its signing certificate. If selecting a launcher is necessary: Samsung Settings → Apps → Choose default apps → Home app → UMBRA. Choose One UI Home there to restore Samsung. The source ZIP includes the Android Studio project and `build_umbra.bat` (SDK 35, Build Tools 35.0.0, JDK 17/21).

Physical S24+/Windows/Tailscale sensor availability, real sound routing, native Android HOME selection/gesture behavior, actual Windows hotkey effects and performance/battery measurements remain device checks. No exact One UI animation parity, native desktop stream, measured PC name absent from the server, or verified Tailscale route is claimed. Windows batch execution is not tested on this Linux host. Recommended follow-up: physical acceptance on the user's PC/phone, add a server-reported machine name if needed, and integrate a real remote-desktop stream only when the companion exposes one.
