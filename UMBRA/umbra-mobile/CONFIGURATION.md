# UMBRA configuration schema 2

Preferences are private Jetpack Preferences DataStore (`datastore/umbra_settings.preferences_pb`), with a validated JSON envelope in `config_v2`. Existing Phase 1 scalar keys are read as a migration source until the first Phase 2 write. Favorites, URL, timeout, profile, master, effects, panel, and accent choice are preserved; the old transitions selection also initializes the now-independent startup selection. Corrupt Preferences recover to defaults; invalid stored JSON also recovers to safe defaults. Disk-write errors remain visible in the launcher.

## Import/export

Export and import use Android's Storage Access Framework, without broad storage permissions. Export is a complete schema 2 snapshot. Import reads at most 64 KiB, requires valid UTF-8/JSON and exact types, rejects unknown fields/versions, validates everything before showing an Apply preview, then replaces preferences atomically. An import is **replacement, not merge**: omitted settings take schema defaults. No partial import is applied on failure. Exported URLs may be private/user-specific; choose your export destination accordingly. Credentials, PINs, device readings, notification contents/counts, and encryption keys are never serialized.

Envelope:

```json
{
  "schemaVersion": 2,
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
| `gridColumns` | 3; integer 3–5 |
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
