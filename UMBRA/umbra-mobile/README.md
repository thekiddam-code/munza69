# UMBRA Mobile 2.1 — Phase 2.1

A native Kotlin / Jetpack Compose Android HOME launcher for Galaxy S24+, package `com.umbra.mobile`. Android 10+ (API 29); target/compile API 35. UMBRA provides an industrial terminal interface while Android and One UI retain system security, notifications, gestures, calls, biometrics, and keyguard.

## Install or update

Download the debug APK from the sibling [downloads folder](https://github.com/thekiddam-code/munza69/tree/main/UMBRA/downloads). Install it on your phone through a file manager (allow that app to install unknown apps when Android requests), or use `adb install -r app-debug.apk`. Phase 2.1 is version code 3 and migrates Phase 1/2 preferences and favorites. Do not uninstall first if you want to preserve settings. An update requires the same signing key; this build uses the existing development key. If you build on another computer, use your own consistent key or uninstall the prior debug build (clears its local settings).

Choose **Settings → Apps → Choose default apps → Home app → UMBRA**. UMBRA also opens this screen from **Config → Display** or **Config → Configuration**. To recover One UI, select **One UI Home** in that same Android screen. No root, kiosk/device-owner mode, firmware changes, accessibility service, or protected system replacement is used.

## Everyday controls

- **Home:** local clock/date, configurable real status panel, ICARUS link/check, favorite app shortcuts, device dashboard, and Android Settings.
- **Apps:** installed launchable activities, locale-aware alphabetical order, case-insensitive search, favorites filter, refresh, and bounded asynchronous icon cache. Tap icon/label to launch; long-press for favorites, Add to Home, hide, and Android app information. Visibility queries are limited to launchable activities, supported web handlers, and standard Android widget providers. Ordinary profile only; managed-profile/private-space support remains future work.
- **Deck:** bottom navigation opens the Command Center within thumb reach. Pull down on Home's command handle, or pull downward past the top of Home content. Swipe up on the Command Center header to close; upward overscroll at its bottom also closes. Body content scrolls normally. The second downward pull offers the Android notification fallback. Gestures never intercept Android's protected screen-edge navigation.
- **ICARUS:** native Engineering / Lounge / Simulator modules. Configure the URL, connect Tailscale separately, and pair using your existing server PIN. Remote Deck browser authentication is separate. No server update is required.
- **Config:** Customization Studio categories for appearance, motion, display, layout, ICARUS, configuration files, and lock-screen wallpaper.

## Phase 2.1 workspace and widgets

Home opens with the existing Main Terminal and favorites preserved, plus Information and ICARUS pages. Swipe horizontally or use the bottom dots. **Pages** adds, renames, reorders, removes, chooses the Home page, and sets each page’s columns/header. Removing a page relocates its items to the first remaining page. Android Home returns to the selected default page; returning from another UMBRA panel preserves the current page.

Long-press a Home item, then release for management or drag to rearrange it. Drop an app over another app’s center to create a folder, or over a folder’s center to add it. Drop near an item’s edge to insert before it; hold near a page edge to change pages. Accessible long-click management also offers explicit page movement. **Folder** creates a folder manually; open it and choose Manage folder to rename, select members, or reorder them. Deleting a folder never uninstalls applications. **Config → Organization** manages hidden applications and drawer order.

Ordinary shortcuts display the original application icon on a transparent surface. **Config → Appearance** controls labels and 32–72 dp icon sizing. Visual Detail **Minimal / Enhanced / Cinematic** controls cached static grids, schematic structure, gradients, and panel markings. Enhanced is default. This choice is independent of all animation settings and remains intact with master off or Minimal motion.

**Widget** adds five clock faces (Digital, Terminal, Analog, Segmented, Date and time), weather, calendar, battery/system snapshots, ICARUS instant controls, or an installed Android widget provider. Widget options resize/recolor built-in widgets and set 12/24-hour display, seconds, transparency, and style. Long-press management moves a widget between pages. Clocks tick while visible even when optional animations are disabled; they stop ticking when inactive or the screen is off.

Android widgets use `AppWidgetHost` and Android’s binding/configuration permission flow. Their actual native views handle clicks and scrolls; only the separate Widget options handle participates in UMBRA management. Provider resize flags/minimum dimensions constrain the editor, within UMBRA’s 1–5 column / 1–6 row grid. Providers requiring larger layouts, managed profiles, or proprietary One UI hosting capabilities may not fit or be available. Portable configuration files retain provider/placement but intentionally require rebinding; local restarts retain assigned widget IDs. Canceling binding/configuration releases the new ID. Never assume a provider works until checked on the phone.

## Unified transitions

**Config → Appearance → Transitions** provides **Samsung-inspired** (default), **UMBRA Cinematic**, **Minimal**, and **Native Android**. Separate switches control app launches, folders, widget expansion, Command Center, and terminal panels. Command Center and terminal switches share the corresponding existing Animation controls. Intensity and all profile, master, Android reduced-motion, battery, thermal, and screen-power gates apply. Master off preserves individual selections and does not block navigation or change Visual Detail.

Apps launch immediately using supported `ActivityOptions` from the measured icon bounds: scale-up by default, clip reveal for UMBRA Cinematic, short fade if bounds/options are unavailable, or system defaults when Native Android is selected. No intermediary Activity or launch delay is added. Motion off requests zero custom transition resources. Samsung controls the ultimate cross-application animation and gesture return; exact One UI parity is **not verified** and requires privileged integration unavailable to ordinary launchers.

Folders and expandable UMBRA widgets share interruptible origin expansion/collapse, slight dimming, and fading contents. Closing or Android Back reverses toward the recorded icon/widget bounds. Native Android style uses a restrained fade for launcher-owned content. Third-party widgets never receive forced UMBRA expansion. Command Center reveals downward and closes upward; settings/panels use a short fade with minimal vertical movement. Home uses Compose’s gesture-driven horizontal pager with native edge navigation left to Android.

## Weather

Choose **Config → Weather**, search a city, select a result, and choose Celsius/Fahrenheit. Optional approximate Android location is a one-shot foreground request with a 12-second timeout and rounded coordinates. No location is selected by default and no forecast request is made until a configured weather view becomes visible.

The provider is [Open-Meteo](https://open-meteo.com/): [Forecast API](https://open-meteo.com/en/docs) and [Geocoding API](https://open-meteo.com/en/docs/geocoding-api), data attribution [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). City queries and chosen coordinates go directly to this provider; no ICARUS credentials or device telemetry are sent. Observe its current usage terms before commercial distribution. Compact views show actual current conditions and fetch time; details add high/low, 24 hourly entries, and five daily forecasts. Missing values are marked unavailable. Cache lifetime is 30 minutes; dated offline data is retained up to seven days in app-private cache. Updates occur on visible entry/resume or Refresh weather, with no periodic background polling. Weather configuration exports include the chosen location; share those files deliberately.

## Fullscreen and recovery

Immersive fullscreen, top-bar hiding, bottom-bar hiding, Adaptive mode, and the UMBRA status panel default ON. Native `WindowInsetsControllerCompat` requests supported hiding and transient reveal by swipe. Content respects camera cutouts, visible bars, keyboard, and safe insets. Android may retain bars for HOME, accessibility, security, keyboard, calls, or vendor policy; visible-bar feedback is displayed rather than repeatedly forcing the request. The OS manages transient bar auto-hide; requests are reapplied on relevant setting changes, resume, and window focus, not on a force-hide timer.

**Show bars / Hide bars** is always available in the header. It uses actual reported bar visibility, immediately requests the opposite state, and saves immersive/top/bottom preferences together. Transient system bars count as visible. The same action is in **Config → Display → Restore Standard Android Bars** and the native-notification fallback. Android edge gestures remain available. The app never attempts to replace the notification shade.

## Command Center and device readings

Modules can be reordered/hidden in Studio. Tile sizes, labels, and quick-app order are configurable and resettable. Device status uses `BatteryManager`, `ConnectivityManager`, `PowerManager`, `StatFs`, `ActivityManager.MemoryInfo`, and `SystemClock`; unavailable values are labeled unavailable. There are no fabricated CPU temperatures or device utilization figures. Storage/memory/uptime are snapshots refreshed on visibility entry or explicit Refresh; battery/network/power/thermal changes use callbacks and broadcasts.

System controls open Android's sound, Wi-Fi, Bluetooth, display, and battery interfaces. The brightness slider changes **UMBRA's window only**; it never writes global Android brightness or requires WRITE_SETTINGS. Choose Use system brightness to restore normal window behavior.

Notification summary is optional and OFF by default. Android notification-listener access must be explicitly authorized in system settings. UMBRA counts active notifications excluding group summaries; it does not inspect titles/text/extras, store notification content, transmit counts, or simulate zero when unavailable. Turning the local count off stops counting; revoke the OS grant separately if desired. The listener is OS-bound only after authorization, not a decorative/background polling service.

## ICARUS setup and supported actions

1. Keep Tailscale connected on the phone/PC as you already do.
2. In **Config → ICARUS**, enter the Remote Deck URL and optionally a server base URL. Empty server base uses the Remote Deck origin. An explicit base supports a reverse-proxy path prefix. Save the connection and select a 1–30 second request timeout.
3. Open the native ICARUS screen and enter the existing server's PIN. It calls `POST /api/pair`. One native pairing is stored encrypted with an Android Keystore AES/GCM key in private no-backup storage. It is bound to the exact normalized server base and is not exported. Switching servers never sends an old token to the new server. Forget native pairing attempts server revocation and always removes the local pairing.
4. Refresh status. Engineering shows actual `/api/status` CPU/RAM readings and `/api/icarus/telemetry` snapshots. Simulation buttons queue supported pause/resume/speed/save commands; queue acknowledgement is not proof of PC execution.
5. Lounge exposes existing `/api/tv/key` actions only after a server snapshot reports a configured TV. Configure/pair the TV in the existing Remote Deck. No unverified direct TV app-launch buttons are shown.
6. Simulator discovers the server's configured macros, Rocket League quick chat, and Fortnite emotes, then uses `/api/action`. The intended PC game/application must be focused. Stop held inputs uses the server's existing stop action. Arbitrary shell commands and host-key endpoints are not exposed.

HEAD checks on the home tile establish reachability only. Native authenticated snapshots distinguish unavailable/unauthorized/offline results. Requests are bounded, cancellable, and do not follow redirects (including redirects carrying authorization). Missing endpoints are reported. Optional module browser URLs fall back to Remote Deck; the inspected web app does not expose a supported URL contract for selecting its sections, so no section deep links are fabricated.

Refresh on resume/network can be switched off independently; manual Check does not permanently enable future checks. Optional native ICARUS refresh is 30–300 seconds **only while that screen is visible**, and suspends under power saving, low battery, moderate thermal pressure, or screen-off. With resume/network checks off, periodic refresh begins after one interval. No continuous inactive polling, analytics, device-information uploads, wake locks, or foreground services.

## ICARUS instant controls and Rocket League

The ICARUS Home page and native Simulator module show one-tap controls from the authenticated server’s current `/api/status` snapshot. **Sync controls** refreshes names and saved messages and displays the synchronization time. **Arrange** selects favorites, reorders, and changes local labels. Quick chat sends its server-defined name; the server resolves the current key sequence at execution. UMBRA does not copy old Rocket League key arrays or overwrite server mappings. Saved messages preserve server text/channel and use the existing balanced text-chat timing. Macros and configured Fortnite slots also use supported existing actions.

Commands show actual server feedback and allow only one request at a time; repeated in-flight taps are dropped, never queued/retried automatically. Acknowledgment is not game verification. Cancellation cannot undo a command already received by the PC. Missing/offline/authentication results stay explicit. See [ICARUS_INTEGRATION.md](ICARUS_INTEGRATION.md) for inspected source and limitations.

## Motion and customization

Adaptive is restrained and reduces motion during interaction. Cinematic uses longer transitions and richer/faster optional effects. Minimal is instant/static. Nine effect switches, master override, and intensity 0–100% persist independently. Master off, intensity zero, Minimal, battery saver, battery ≤20%, disabled system motion, severe Android thermal status, or screen-off disable optional motion. Continuous effects also pause during interaction, outside Home, and at moderate thermal pressure. Decorative updates are scheduled at 8 Hz Adaptive / 12 Hz Cinematic; these are scheduling limits, not measured frame rates or battery savings. Alert text stays readable when its optional underline effect is disabled.

Appearance includes bright custom accent colors with contrast validation, amber/green presets, three dark backgrounds, typography choices, panel density, and app columns. Quick tile labels/order seed the migrated Home and still apply to Command Center. An explicitly organized desktop retains its own item ordering. See [CONFIGURATION.md](CONFIGURATION.md) for schema, validation, migration, and reset behavior.

## Lock screen

**Config → Lock screen** exports a 1440×3120 coordinated PNG through Android's file picker or applies it to `WallpaperManager.FLAG_LOCK` where allowed. This is a static image, not a lock-screen replacement or live ambient service. Samsung may require manual application.

In **Samsung Settings → Wallpaper and style → Lock screen**, choose the exported image, then edit the native clock and select amber/muted green. Optional Good Lock **LockStar / ClockFace** can coordinate layout and clock style where available. Those modules are not bundled or controlled by UMBRA. Fingerprint and secure keyguard remain Android-managed.

## Build on Windows

Install Android Studio, Android SDK Platform 35 / Build Tools 35.0.0, and JDK 17 or 21. Open `umbra-mobile/`, let Studio sync and create `local.properties`, or set `ANDROID_HOME`. Accept SDK licenses. Set `JAVA_HOME` or add Java to PATH. Run **build_umbra.bat**. It runs host tests, lint, and the debug build with the checksum-pinned Gradle wrapper. First build needs Internet for Google Maven, Maven Central, Gradle, and Robolectric's Android runtime artifacts. Host graphics tests support x64 Windows, Linux, and macOS through Robolectric's native runtime. This Linux session does not validate Windows batch execution.

Linux/macOS equivalent:

```sh
./gradlew --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
```

Verified Phase 2.1 build: 48 tests passed, lint zero errors (13 warnings), debug app and device-test APKs assembled. App APK: `app/build/outputs/apk/debug/app-debug.apk`. Device tests require a working emulator or dedicated device: `./gradlew :app:connectedDebugAndroidTest`. See [TESTING.md](TESTING.md). Debug signing is for development, not store distribution. Never commit your signing keys or credentials.

## Permissions and validation limits

Normal permissions: INTERNET, ACCESS_NETWORK_STATE, SET_WALLPAPER. Notification access is an optional explicit Android special-access grant; its service is protected by BIND_NOTIFICATION_LISTENER_SERVICE. AndroidX adds an app-owned signature permission for internal broadcasts. ACCESS_COARSE_LOCATION is optional and requested only by Weather’s Use approximate Android location button. Manual city search needs no location permission. No QUERY_ALL_PACKAGES, precise/background location, notification posting, storage, accessibility, device-owner, privileged status-bar, or system-brightness permission is requested. Backup/device-transfer exclusions remain enabled.

See [PHASE21_REPORT.md](PHASE21_REPORT.md) for current results and limitations; [PHASE2_REPORT.md](PHASE2_REPORT.md) is historical. Host Android UI regression is distinct from emulator/device acceptance. Physical S24+/One UI immersive behavior, protected gestures, notification grant, Keystore, wallpaper, calls/biometrics, live Tailscale/ICARUS, and performance measurements remain hardware checks. Phase 1's historical report/evidence is retained separately.
