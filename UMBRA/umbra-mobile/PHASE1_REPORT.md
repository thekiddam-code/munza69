# UMBRA Mobile — Phase 1 delivery report

Date: 2026-11-11. Standalone project created in `umbra-mobile/` after workspace inspection found no existing source repository. No ICARUS/Windows server, Remote Deck, TV integration, or simulation was modified.

## Delivered implementation

- Native Kotlin/Compose home launcher with exported MAIN/HOME/DEFAULT filter, separate app-list entry, single-task Home intent handling, Back navigation, and edge-to-edge safe insets.
- Industrial near-black/charcoal terminal, chamfered panels, amber or muted green accent, restrained red offline alerts, technical sans and monospace readouts, large responsive clock/date, battery/charging, network transport, optional device panel, Android Settings and Home-selector shortcuts, bottom navigation.
- Scoped installed-launchable-activity discovery, locale-aware alphabetical order, search, favorites filter, persistent favorite component IDs, functional home shortcuts, lazy drawer grid, background icon loading and bounded cache. Updates on visible package changes and activity resume.
- Adaptive/Cinematic/Minimal profiles; master gate preserves all five individual selections. Independent ambient, startup/transitions, environment, alert emphasis, and in-app animated-background effects. Visible Home effects run at 8/12 Hz, pause during interaction, and stop outside Home. Power saving, ≤20% battery, disabled system motion, master off, and Minimal override optional effects. Functional alerts and accessibility announcements remain.
- Local Jetpack Preferences DataStore, corruption recovery, URL/timeout validation, write-error UI, backup and device-transfer exclusions. No analytics, credentials, intrusive permissions, services, wake locks, or protected-system modifications.
- Configurable ICARUS external-browser shortcut and actual cancellable, timeout-bounded HEAD reachability check. Checks on visible lifecycle entry, network/configuration changes, or manual action. No redirects followed by the checker, continuous polling, background monitoring, server changes, embedded authentication, or private endpoints in production source.
- Complete Gradle Kotlin DSL project and checksum-pinned Gradle wrapper, Windows `build_umbra.bat`, README, JVM tests, device UI tests, and [device acceptance checklist](TESTING.md).

## Build and host verification

The debug APK was successfully produced by Gradle, not inferred from source. Final validation used:

```text
./gradlew --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
BUILD SUCCESSFUL
```

Build host: OpenJDK 21, Gradle 8.9, Android Gradle Plugin 8.7.3, Kotlin 2.0.21, Android SDK 35 / Build Tools 35.0.0. The initially missing SDK was installed locally for verification. A host-only proxy configuration was necessary for Gradle dependencies; it is not included in the source delivery.

- 8 JVM tests passed, zero failures/errors/skips: five policy/URL tests, one on-disk persistence test, and two local HTTP integration tests. Tests verify real HEAD requests, status classification, redirect behavior, overall timeout, cancellation, invalid URLs, power/accessibility overrides, master restoration, and preferences/favorites surviving DataStore recreation.
- Android lint passed with zero errors; remaining warnings are dependency-update advisories for pinned versions.
- APK signature verified with Android `apksigner` (v2 signature).
- APK metadata verified with `aapt`: `com.umbra.mobile`, version 1.0, min SDK 29, target SDK 35. Manifest contains HOME integration, scoped app/browser queries, and no QUERY_ALL_PACKAGES or dangerous runtime permissions. AndroidX adds a signature-only internal broadcast permission.
- Device UI test APK compiled successfully. Native runtime tests did not execute; see the blocker below.
- Windows batch execution is not tested on this Linux host; the included wrapper performed the equivalent Gradle tasks here.

Generated app: `app/build/outputs/apk/debug/app-debug.apk`. Debug signing is suitable for development installation, not store distribution. The delivery includes a source ZIP without build caches, local SDK configuration, SDK files, credentials, or signing keys.

## Installation

Install the provided APK by opening it on the phone or with `adb install -r app-debug.apk`. Set **Settings → Apps → Choose default apps → Home app → UMBRA** (also reachable from UMBRA Config). To restore Samsung, select **One UI Home** in the same screen. Keep Tailscale enabled separately, enter your own ICARUS URL in Config, and save. See [README](README.md) for Windows build/setup and full configuration documentation.

## Known limitations and acceptance status

Physical Galaxy S24+/One UI testing remains required. Do not treat host compilation or an AOSP test result as Samsung acceptance. The checklist in TESTING.md covers default Home selection/restoration, installed-app launching and favorites, power saving and reduced motion, Tailscale/browser behavior, accessibility, configuration changes, native phone controls, and battery/frame profiling.

Reachability establishes an HTTP response, not authenticated ICARUS health or Tailscale tunnel status. A 405 or server error is reported honestly as a response. Certificate/DNS/transport errors become offline/unreachable without logging connection details. HTTP is intentionally supported for existing private tailnet deployments; prefer HTTPS. Query-string/fragment authentication is not supported; use browser authentication.

Phase 1 customization covers favorite shortcuts, accent choice, effects/profiles, and optional telemetry. Arbitrary palette/font editing, user wallpaper import, panel rearrangement, drag-and-drop, folders, Android widgets, icon packs, and multiple home pages remain work. The animated background is internal to UMBRA, not an Android live-wallpaper service. Work-profile/private-space app support and Samsung proprietary Recents integration are not implemented. No bundled ICARUS server, synthetic telemetry, notification listener, or lock-screen replacement is included.

## Recommended Phase 2

1. Complete S24+ acceptance and measured frame/battery profiling; test current One UI updates, TalkBack, and large fonts.
2. Expand appearance controls, wallpaper import, icon packs, configurable home order/layout, folders, and widgets.
3. Add LauncherApps-based managed-profile/private-space support and richer app details/shortcut actions.
4. Add an optional authenticated ICARUS health API integration only after its server contract and secure credential storage are agreed; retain foreground-only checks.
5. Set up CI Android builds/device tests, dependency maintenance, release signing, and distribution packaging.

## Native runtime test result

`connectedDebugAndroidTest` was attempted, but no application tests ran (device report: tests=0). This host has no `/dev/kvm`; the software emulator initially failed disk-capacity checks. Android 15 and Android 10 images could not run within available storage. A compact Android 11 AOSP ATD image was then tried with sparse storage. It exposed ADB but failed to initialize Android services. The final Gradle device-test task stopped during APK installation with:

```text
cmd: Can't find service: package
```

This is a test-environment failure before application installation, not a passing application test. Default-Home selection, native app launching, UI interactions, actual lifecycle/power behavior, screenshots, and Samsung compatibility remain unverified at runtime. The two device UI tests are provided and compile; run them on a working emulator/phone. Physical-device acceptance and the live ICARUS/Tailscale connection are still required before declaring Phase 1 acceptance complete. No measured battery or frame-rate claims are made.

Build/test evidence is included in `verification/`: successful Gradle log, unit-test XML results, lint summary, packaged manifest, APK signature output, and the failed native test task log.

APK SHA-256: `e6de8c5a6df04a5d6c0fe8a9f6d6a966bb56c6aee69bde2776ccfcabc4500c9b`
