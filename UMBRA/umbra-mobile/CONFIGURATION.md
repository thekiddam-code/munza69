# UMBRA configuration schema 7

Preferences are private Jetpack Preferences DataStore (`datastore/umbra_settings.preferences_pb`), with a validated JSON envelope in `config_v2`. Existing Phase 1 scalar keys are read as a migration source until the first current write. Favorites, URL, timeout, profile, master, effects, panel, and accent choice are preserved; the old transitions selection also initializes the now-independent startup selection. Corrupt Preferences recover to defaults; invalid stored JSON also recovers to safe defaults. Disk-write errors remain visible in the launcher.

## Import/export

Export and import use Android's Storage Access Framework, without broad storage permissions. Export is a schema 7 snapshot with portable Android-widget placeholders. Schemas 2–7 are accepted with the corresponding migration defaults; exports use schema 7. Import reads at most 1 MiB, requires valid UTF-8/JSON and exact types, rejects unknown fields/versions, validates everything before showing an Apply preview, then replaces preferences atomically. An import is **replacement, not merge**: omitted settings take schema defaults. No partial import is applied on failure. Exported URLs may be private/user-specific; choose your export destination accordingly. Credentials, PINs, device readings, notification contents/counts, and encryption keys are never serialized.

Envelope:

```json
{
  "schemaVersion": 7,
  "settings": {
    "profile": "Adaptive",
    "master": true,
    "intensity": 65,
    "immersive": true,
    "hideTopBar": true,
    "hideBottomBar": true,
    "statusPanel": true,
    "url": "",
    "serverUrl": "",
    "timeout": 5
  }
}
```

Only the envelope keys `schemaVersion` and `settings` are accepted. Configuration booleans must be actual booleans, numbers actual numbers, collections the expected arrays/maps. Quoted booleans and numeric strings are rejected. Current defaults and validators are in `Configuration.kt`.

## Settings

| Field | Default / allowed values |
| --- | --- |
| `profile` | `Adaptive`; also `Cinematic`, `Minimal` |
| `master` | true; gates optional motion without changing individual selections |
| `intensity` | 65; integer 0–100; zero disables optional motion |
| `ambient`, `transitions`, `startup`, `parallax`, `statusEffects`, `alerts`, `commandAnimations` | true; independent optional effects |
| `wallpaper`, `environment` | false; animated in-app background / atmosphere |
| `immersive`, `hideTopBar`, `hideBottomBar`, `statusPanel` | true |
| `indicators` | Time, Date, Battery, Network, ICARUS; optional Notifications; only known names allowed |
| `accent` | empty uses preset; otherwise bright `#RRGGBB` with relative luminance ≥0.25 |
| `greenAccent` | false; chooses muted green instead of amber when custom accent is empty |
| `background` | `Void`; also `Graphite`, `Blueprint` |
| `typography` | `Technical`; also `Mono`, `System` |
| `density` | 2; integer 1–3 (Compact, Balanced, Spacious) |
| `gridColumns` | 3; integer 3–8 |
| `tileSize` | 2; integer 1–3 (Small, Standard, Large) |
| `moduleOrder` | Device, System, ICARUS, Notifications, Applications; every module exactly once |
| `hiddenModules` | empty; subset of known modules |
| `favorites` | empty set of Android component IDs; max 256 |
| `quickOrder` | empty; distinct component IDs, max 256; remaining favorites append alphabetically |
| `quickLabels` | component-ID→label map; max 256, 1–48 characters, no control characters |
| `swipeDown`, `secondSwipe` | true; launcher gestures only, never protected screen-edge gestures |
| `windowBrightness` | -1 (system); otherwise finite 0.1–1.0, UMBRA window only |
| `url` | empty; external Remote Deck destination |
| `serverUrl` | empty derives Remote Deck origin; explicit base supports a path prefix |
| `engineeringUrl`, `loungeUrl`, `simulatorUrl` | empty falls back to Remote Deck; browser shortcuts only |
| `timeout` | 5; integer 1–30 seconds per HTTP request |
| `refreshOnResume`, `refreshOnNetwork` | true; manual checks remain available |
| `foregroundRefreshSeconds` | 0 (manual interval); otherwise integer 30–300, visible native ICARUS screen only |
| `notificationsEnabled` | false; true still requires an explicit Android notification-listener grant |

All URLs must be empty or a valid HTTP(S) URL ≤2048 characters with a host and valid port. Credentials, query, fragment, whitespace, and control characters are rejected. No certificate checks are bypassed. Component IDs must be conventional Android `package/class` strings ≤512 characters; imported components do not cause arbitrary activity execution—only discovered launchable apps are rendered/launchable in the drawer and quick tiles.

## Reset behavior

Appearance, Animation, Display, Command Center, and ICARUS categories can be reset independently. Command Center reset restores module order/visibility, tile size/order/labels, and gesture defaults; it preserves favorite membership. Appearance reset does not modify animation choices. ICARUS category reset clears URLs and connection preferences; native pairing is a separate explicit clear/forget action. Full restore clears favorites and local native pairing, then restores defaults. Android's special-access grants remain under system control; revoke notification access through its Android settings screen.

A native token lives in `noBackupFilesDir/icarus_pairing.enc`, AES/GCM encrypted using Android Keystore alias `umbra_icarus_pairing_v1`. The exact canonical server base is authenticated as part of encrypted data. No token crosses to another scheme/host/port/base path, follows a redirect, enters DataStore, appears in export, or is logged. Clearing a local token while offline cannot revoke an existing server-side grant; use the existing server's pairing/device controls if server revocation is required.

## Phase 2.1 preferences

| Field | Default / values |
| --- | --- |
| `visualDetail` | `Enhanced`; `Minimal`, `Cinematic`; static appearance independent of motion |
| `transitionStyle` | `SamsungInspired`; `UmbraCinematic`, `Minimal`, `NativeAndroid` |
| `appLaunchTransitions`, `folderTransitions`, `widgetTransitions` | true; independent category switches |
| `commandAnimations`, `transitions` | existing shared Command Center / terminal-panel switches, true |
| `showAppLabels`, `iconSize` | true; 48 dp, valid 32–72 |
| `hiddenApps` | empty component set, max 256; hiding never uninstalls |
| `drawerOrder` | empty distinct component list, max 512; remaining apps retain alphabetical order |
| `desktop` | null derives migrated three-page workspace; explicit validated nested layout after editing |
| `weatherPlace`, `weatherLatitude`, `weatherLongitude` | empty / null pair; named manual location or rounded approximate foreground location |
| `weatherFahrenheit` | false (Celsius) |
| `instantOrder`, `instantFavorites`, `instantLabels` | empty; local action ID order, favorite set, label map; each max 256 |

Nested desktop schema version 1 stores `homePageId` and 1–12 ordered pages. Each page has a stable ID, name, header kind (`terminal`, `information`, `icarus`, `blank`), 2–8 columns, and ordered items. Limits: 256 items/page, 256 total, globally unique item IDs; folders up to 64 distinct launchable component references; no nested folders. Widget specifications store kind, one of five clock styles, 1–8 column span, 1–12 row height (64 dp/row), 12/24-hour/seconds, transparency/accent, Android provider and locally assigned host ID. Native hosting may increase the view height to its provider minimum. Actual provider support needs physical validation.

Local DataStore serialization preserves Android widget IDs. Export **zeros those IDs**, and import strips IDs even from a hand-edited file, preventing reuse of another installation’s binding. Rebind imported providers through Android. Reset/import removes unused local host IDs after preferences commit. Pending provider allocation is private local state and is not exported. Layout names, IDs, collection sizes, numeric ranges, nested primitive types, and references are validated before application. Removing pages relocates contents; operations beyond limits fail without replacing the current layout and show a save error.

Null desktop preserves legacy favorite and quick-order migration until the first organization edit. Once explicit, desktop ordering is independent from Command Center quick order. Favoriting a new app places a shortcut on the default Home page; removing a favorite removes its standalone shortcuts but does not erase folder membership. Hiding filters all launcher-owned app lists, including folders. Hidden choices remain recoverable in Organization.

Master override, profile, effect selections, and transition categories are independently stored; toggling master never rewrites selections or `visualDetail`. Appearance reset restores Enhanced and app styling, preserving transition choices. Reset transitions restores category/style defaults without changing master/profile/detail. Animation reset restores existing motion settings without changing detail. Full defaults clears the workspace, weather choice, instant preferences, favorites, and native pairing. OS grants remain Android-managed.

Weather cache is a separate bounded private file (`cache/umbra-weather-v1.json`), not part of exports, with location/unit binding and timestamps. Removing the weather location immediately prevents future weather-view fetches; the app’s cache can be cleared through Android App info. Forecasts and instant server snapshots are not configuration data and are not substituted with sample values.

## Phase 2.3 shared layouts and controls

The authoritative new storage guide is [LAYOUT_MIGRATION.md](LAYOUT_MIGRATION.md). Schema 4 adds `gridLayouts`, `deckColumns` (2–4 reference density, responsive up to 8), `editHaptics` (false), `commandExpanded` (true on migration), `statusTabs` (per-context booleans), `customButtons`, nullable `instantSelection`, and `widgetButtonSelections`. Existing fields and local native widget bindings are preserved. No movement or visibility setting depends on optional motion.

Expanded module sizes remain stored while collapsed rendering uses a single compact header row. Placement is normalized without overlap after density/orientation changes. Changes use atomic DataStore writes; invalid imports or capacity violations preserve the prior stored layout and show an error. Button-only files are separately versioned and strictly typed; output payloads are specified in [ICARUS_OUTPUTS.md](ICARUS_OUTPUTS.md). Full exports include the shared grid, button definitions, selection, and per-tab status settings, while excluding credentials and portable widget bindings.

## Soundboard 2.3.1

`gridLayouts["soundboard"]` stores only local native button placement, size and visibility. The schema remains 4 and existing layouts are preserved. Sound definitions, favorites, output selection and optional normalization are loaded from and saved to ICARUS, never copied into local settings exports. See [SOUNDBOARD_INTEGRATION.md](SOUNDBOARD_INTEGRATION.md).

## Phase 3 / schema 5

Schema 5 reads 2/3/4/5 without resetting the existing desktop, grid arrangements, command mappings or server configuration. `pcIndicator` defaults true. `activeHomePreset` defaults `default`; `homePresets` holds named inactive/saved desktop and HOME-grid snapshots. The existing `desktop` and HOME grid entries remain the active preset's authoritative working layout. Preset switching snapshots before loading and preserves non-HOME grids. Per-widget `collapsed` and `showDetails`, plus existing `accent`/`transparent`/`span`/`rows`, persist independently. All inactive Android widget IDs remain owned locally; portable exports remove bindings in every preset. TV mappings/legacy Lounge settings are retained for round trips but hidden and blocked from execution. No audio-output preference is introduced or reset. See [Phase 3 details](PHASE3_REPORT.md).

## 3.1 / schema 6: widget scope and Recents

The DataStore key remains `config_v2`. Existing schemas 2–5 migrate without resetting layouts. `recentsShortcut` defaults true and only controls visibility of the footer icon; Android owns the actual Accessibility grant and it is not exported or enabled by that preference. Hiding the icon does not revoke the OS grant. Revoke optional access in Android Accessibility settings.

Each `DesktopWidget` adds `title` (empty/default), `buttonSet` (`all`, `pc`, `rocket`, `fortnite`, `minecraft`, `simulation`, `favorites`), `buttonColumns` (1–6, default 2), `buttonHeight` (56–96, default 64), and `buttonOverrides` (source-ID → validated CustomButton, maximum 512). The picker offers favorites-only for sound widgets. `widgetButtonSelections` stores independent selected IDs; sound IDs are namespaced `sound:<server-id>`. No global selection rewrite occurs when editing one widget. Owned custom definitions use widget-prefixed IDs. Existing global definitions/labels remain available for migration; legacy global shared selections initialize only older button instances without an explicit selection. Inactive presets are migrated too.

Page/widget size limits are documented in WIDGETS31_REPORT.md. Button widgets enforce at least 3 editing rows. Instance sound layouts use `sound-widget:<widget-id>`; the standalone SIMULATOR soundboard layout remains separate. Shared ICARUS favorite/output/profile data are not duplicated in DataStore. PIN is transient, masked, cleared, never exported; only the existing encrypted server-bound token is retained. The PC patch retains its authoritative schema-1 sound library and adds no launcher-side audio-output copy.

## 3.2 / schema 7: HOME chrome and mixed controls

`homeHeaderCollapsed` and `homeFooterCollapsed` default false and persist global HOME chrome choices. Neither changes Android immersive/inset preferences or other screens. Appearance reset restores both false. Header collapse hides HOME status rendering without rewriting status settings. The single 48 dp recovery strip remains outside widget content, carrying the existing PC indicator and optional Recents when needed.

`DesktopWidget.fillPage` defaults false and is allowed only for built-in Button/Soundboard widgets. It adapts rendered width/height to the viewport without writing grid positions merely on screen-size changes. `buttonColumns` now accepts 1–12. Inner grid storage supports up to 12 columns with a 12-column collision stride; outer HOME pages still use 2–8 logical columns. Narrow views adapt rendered button columns without changing the preference. `buttonSet` additionally accepts `mixed`; its selection combines stable command IDs and `sound:<original-id>` under the existing widget selection map. Sound references are presentation data only, never a second sound library or audio settings store. All fields use exact JSON types. [Current guide](HOME32_REPORT.md).

## 3.3 host actions and windowed chrome

Schema remains 7 and no preset is reset. `immersive=false` now selects the simplified one-Fullscreen-button launcher chrome. Existing HOME collapse flags are independent and restored on re-entry; transient OS bar visibility does not rewrite them. Stable optional IDs `host:arctis` and `host:save-clip` use existing per-widget selections and grids, including inactive presets. Neither is included in implicit defaults. Vectors are static code assets, not emoji or serialized user settings.

Arctis target identity and Moments observation folder live in the PC's private `umbra_host_actions.json`. The keyboard binding stays solely in the existing host `config.json.macros["Save Clip"]`, read on each request; there is no Android Alt+S copy. Pending request results are transient and do not automatically replay after restart. Credentials remain in the original server-bound encrypted vault, excluded from exports. [Current contracts and limits](HOST33_REPORT.md).
