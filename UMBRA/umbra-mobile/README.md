# UMBRA Mobile 1.0 — Phase 1

Native Kotlin / Jetpack Compose Android home launcher, package `com.umbra.mobile`. Designed for Galaxy S24+ and Android 10–15+ (minimum API 29, target API 35). No root, firmware changes, WebView, service, wake lock, analytics, or runtime permissions.

## Build on Windows

1. Install current Android Studio, its Android SDK Platform 35 and Build Tools 35.0.0, and JDK 17 or 21 (Android Studio's bundled JDK 21 works). Accept the Android SDK licenses in SDK Manager.
2. Open this `umbra-mobile` folder in Android Studio and allow Gradle sync. Studio writes your local SDK path to `local.properties`. Alternatively set `ANDROID_HOME` to your SDK directory. Do not copy the Linux `local.properties` onto Windows.
3. Run `build_umbra.bat`. It runs JVM tests, Android lint, and the debug build using the included Gradle wrapper. First build requires Internet access to Google Maven, Maven Central, and the Gradle distribution host.
4. Output: `app\build\outputs\apk\debug\app-debug.apk`.

Linux/macOS: `./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug` with SDK configured. Gradle 8.9, AGP 8.7.3, Kotlin 2.0.21; UI dependencies are pinned in `app/build.gradle.kts`.

## Install and select Home

1. Copy the debug APK to the phone and open it. Allow installation from that file manager when Android asks. Alternatively enable Developer options / USB debugging, connect USB, and run `adb install -r app-debug.apk` from Android SDK platform-tools.
2. Open UMBRA from the app list. Tap **Config → Choose default Home application → UMBRA**. Samsung also exposes this at **Settings → Apps → Choose default apps → Home app**.
3. Press Home to return to UMBRA. Bottom navigation provides Home, Apps, and Config. Back from Apps or Config returns Home. Pressing Home while a panel is open resets it to the terminal.
4. **To restore Samsung**, use that same Home app settings screen and select **One UI Home**. You can then uninstall UMBRA normally. Samsung's notification shade, lock screen, biometrics, phone apps, edge panels, and system navigation stay under Android/One UI control. Third-party launchers cannot provide Samsung's proprietary Recents transitions.

Debug signing is for development. A new machine may generate a different debug key; if Android rejects an update with a signature mismatch, uninstall the previous debug build (clears local UMBRA configuration) before installing, or reuse your own debug keystore securely. No signing keys belong in source control.

## Daily use

- **Apps:** alphabetically sorted launchable activities, case-insensitive search, favorites filter, and Refresh. Tap an app icon/label to launch. Tap its star to pin or unpin it on Home. Multiple launchable activities from one package are kept as separate shortcuts. Removed apps disappear; stale favorite IDs are harmless and can reappear if the app is reinstalled.
- **Home:** minute-aligned local clock/date, actual battery/charging state, current network transport, ICARUS tile, favorites, optional device status, and Android Settings shortcut. Scroll vertically on small screens or at large font sizes. Bottom navigation remains within easy thumb reach.
- **ICARUS:** enter your own Remote Deck HTTP(S) URL and timeout (1–30 seconds) in Config, then Save connection. Connect Tailscale separately. Open deck uses your existing browser and its authentication. No server changes required.
- **Check:** makes one bounded HTTP HEAD request on resume, URL/timeout change, network change, or manual Check. There is no periodic polling. The tile reports HTTP status, auth-required, redirect, or offline/unreachable; a HEAD response does not verify server identity, application readiness, or Tailscale itself. Some servers return 405 to HEAD; this is reported as a response rather than a false offline result. Redirects are not followed by the checker. Browser navigation can follow them normally. Offline never prevents trying Open deck.

## Configuration

Jetpack Preferences DataStore stores settings in the app's private internal storage (`datastore/umbra_settings.preferences_pb`). Android backup is disabled. No settings export or cloud sync. Corrupt preferences recover to defaults; disk read failures use defaults, and write failures show an error. Uninstall clears settings. URLs must have an HTTP(S) host, valid port, and no embedded credentials, query, fragment, whitespace, or controls. Keep authentication tokens out of URLs; authenticate in the browser instead. HTTPS certificate checks are never disabled. HTTP is supported for existing private Tailscale deployments; only the configured destination receives the health request. No sensitive connection logging is implemented.

| Setting | Default | Behavior |
| --- | --- | --- |
| Profile | Adaptive | Adaptive: restrained transitions and slow idle effects; Cinematic: longer transitions and faster ambient drift; Minimal: no optional motion |
| Master animations | On | Gates effects without modifying individual selections |
| Ambient lighting | On | Very low contrast slow lighting drift on Home |
| Terminal startup and transitions | On | Screen fade/slide transitions |
| Environmental effects | Off | Sparse subtle moving terminal particles |
| ICARUS alert animations | On | Single subtle status emphasis; text alerts always remain |
| Animated terminal background | Off | Slowly drifting geometric line; in-app background, not an Android live wallpaper |
| Muted green accent | Off | Switches amber accent to muted green |
| Device status panel | On | Battery/network/profile readout |
| Remote Deck URL | Empty | No request until configured |
| Connection timeout | 5 seconds | Overall call timeout, 1–30 seconds |
| Favorites | Empty | Component IDs, shown alphabetically on Home |

All optional animation stops under Android power saving, battery ≤20%, system animator/window/transition scale zero, Minimal profile, or master off. Continuous effects also stop on interaction and outside Home. Resuming master restores the saved individual switches. Continuous effects and observers exist only while the activity is visible; clock and network checks use lifecycle cancellation. Alerts remain readable and announce status politely to accessibility services. Icon bitmaps use a bounded 128-entry cache; app queries and icon decoding run off the UI thread. Only launchable apps are visible through the manifest's scoped MAIN/LAUNCHER query; `QUERY_ALL_PACKAGES` is not requested.

## Verification and remaining work

For device checks, see [TESTING.md](TESTING.md). See [PHASE1_REPORT.md](PHASE1_REPORT.md) for actual build results, test evidence, limitations, device acceptance checklist, and recommended Phase 2 work. Successful compilation alone does not establish Samsung device acceptance.
