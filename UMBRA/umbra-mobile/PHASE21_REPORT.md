# UMBRA Mobile 2.1 implementation report

Phase 2.1 and the Unified Transition Engine extend the existing Phase 2 Android Studio project in `UMBRA/umbra-mobile/`. Package `com.umbra.mobile`, version name **2.1**, version code **3**, min API 29, compile/target API 35. Existing Gradle wrapper, launcher Activity, DataStore migration, app discovery/cache, native ICARUS modules, Android system shortcuts, display controls, and security boundaries are retained.

## Delivered behavior

| Area | Implementation |
| --- | --- |
| Visual Detail | Minimal / Enhanced default / Cinematic, native cached static grid/hull/schematic/gradient layers and fine panel highlights; independent from all motion |
| App shortcuts | Original icon, transparent surroundings, optional labels, adjustable size, long-press actions, favorites, hidden apps and drawer order |
| Home organization | Stable persistent page/item/folder IDs; gesture pager; manual and drag grouping; membership/order/rename/delete; grid/page add/remove/reorder/default; explicit and drag page movement |
| Migration | Existing terminal and favorite/quick-order data preserved; adds editable Information and ICARUS pages; schema 2 accepted without resetting prior selections |
| Built-in widgets | Five clock styles with format/seconds/accent/transparency/size; weather, calendar, battery/system, ICARUS controls; contextual details from measured widget bounds |
| Weather | Actual Open-Meteo forecast/geocoding, manual city and optional foreground approximate location, units, current/hourly/five-day/high-low, dated private cache and offline errors; no demo values or inactive polling |
| Android widgets | Public AppWidgetHost picker/bind/provider-configuration flows, native view/PendingIntent clicks, provider resize constraints, persistent local host IDs, cancellation/removal cleanup, imported-widget rebinding |
| Bars | Immediate two-way header request using actual inset visibility; persisted immersive/top/bottom preferences; OS transient/protected UI respected |
| ICARUS | Shared one-tap current-server catalog, sync time/manual refresh, favorites/order/local labels, real feedback, duplicate in-flight suppression; authenticated existing mechanisms |
| External launch transition | Immediate native main intent; measured-icon scale-up by default, clip reveal Cinematic, short fade fallback; no sideways custom slide or intermediary screen |
| Folder/widget transitions | Interruptible Compose expansion/collapse from actual captured bounds; dim/fade; Back reverses; never forced on native third-party widget content |
| Command/panels/pages | Short downward Command Center reveal/reverse, restrained panel fades/vertical offset, horizontal touch-tracking pager |
| Transition controls | Appearance → Transitions: Samsung-inspired / UMBRA Cinematic / Minimal / Native Android; five category switches, persistent and gated by existing master/profile/intensity/power/accessibility rules |

The master override leaves saved individual selections and Visual Detail intact. Clock ticks and functional alerts remain available with optional motion disabled. Static detail has no timer or animation state. Clocks, host listeners, network requests, and optional effects are scoped to visibility/lifecycle; no new persistent service or wake lock is introduced.

## Build and evidence

The Phase 2 baseline passed before edits (`stage-a-baseline.log`). Foundation and integrated source compiled incrementally (`stage-b-foundation.log`, `stage-c-d-integration.log`); the initial complete integration build also passed tests, lint, app APK, and test APK (`integration-checks.log`). Focused new regressions exposed intrinsic-sizing loops in scrollable editor dialogs, stale drag hit targets and a callback retaining a prior layout, and paused-host-looper/fake-clock test timing. The final implementation uses bounded editors and current-layout callbacks; host tests explicitly process Android’s paused event queue. Intermediate failed/interrupted diagnostics are retained separately from the successful final run.

Final command:

```sh
./gradlew --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
```

**Final result: BUILD SUCCESSFUL in 2m 22s. All 48 tests passed, with zero failures, errors, or skips. Android lint reported zero errors and 13 warnings: 11 dependency-update notices and two notices about synchronous SharedPreferences commits used to persist pending widget binding before external provider Activities. Both app and device-test APKs assembled. The debug signing certificate matches the previously published Phase 2 APK.**

The final command log (`final-checks.log`), JUnit XML, lint XML, suite summary (`RESULTS.txt`), APK metadata/signature inspection, and fresh host UI renders are stored under `verification/phase21/`. Debug APK: `app/build/outputs/apk/debug/app-debug.apk`; distributable: `UMBRA/downloads/umbra-mobile-debug.apk`. The APK ZIP contains the same installable APK. Source ZIP includes the complete Gradle/Studio project, wrapper JAR, Windows batch script, documentation, and verification evidence, excluding build caches, SDK, local paths, credentials, and signing keys.

Host Android tests run actual Activity/Compose/native graphics on SDK 30 and 34. Local MockWebServer tests use real sockets and documented HTTP formats. The device-test APK is compiled; device instrumentation is **not executed** here. No KVM is available and emulator data-partition allocation exceeds the environment’s available disk. Windows batch execution, physical Galaxy S24+, live private ICARUS/Tailscale, and measured frame/battery performance are not claimed.

## Known limits and remaining acceptance

- Samsung owns cross-application launch/return animation and protected gestures. Public ActivityOptions supply the icon origin but cannot guarantee One UI’s privileged Quickstep choreography. Exact Samsung parity is unverified. Native Android preference deliberately delegates launch animation to the OS. A vendor may override even a zero-resource request.
- Third-party widget binding/configuration, RemoteViews interactions, resize dimensions, provider uninstall/recovery, reboot, and proprietary Samsung providers require real-device testing. Hosting is limited to ordinary-profile compatible providers and the documented grid; no managed-profile/private-space or OEM privileged hosting support is claimed. Exported providers must be rebound by Android.
- Home uses an ordered responsive grid, not a pixel-positioned desktop. Movement across pages and folder management are available through explicit menus in addition to drag. Limits are 12 pages, 96 items/page, 256 total, 64 members/folder. Unsupported capacity changes fail validation and retain the prior layout.
- Cinematic detail is efficient native vector/gradient industrial structure, not photorealistic environmental artwork or heavy blur. No frame-rate/battery saving figures are asserted. Large fonts, very narrow widths, rotation, and complex provider widgets need hardware acceptance.
- Weather service availability, usage terms, location permission/provider availability, and current forecast values depend on the real provider/device. No location is selected initially. A canceled lookup or offline request never fabricates data. No timed inactive refresh occurs.
- Rocket League key arrays are not exposed by `/api/status`; UMBRA synchronizes current names and lets the PC resolve keys at execution. Saved messages are a dated snapshot refreshed manually/on visible resume. Actual game focus/input delivery cannot be verified from HTTP acknowledgments. See [ICARUS_INTEGRATION.md](ICARUS_INTEGRATION.md).
- Android bar visibility, HOME selection, native notifications, calls, biometric keyguard, edge/Recents gestures, optional grants, real Keystore encryption, and wallpaper application remain physical acceptance checks. One UI Home recovery remains Android Settings → Apps → Choose default apps → Home app.

Use [TESTING.md](TESTING.md) to record physical acceptance separately. This development-signed build is not a store release.

## Next phase recommendations

Prioritize the S24+ acceptance checklist and provider compatibility fixes, then measure frame timing/battery use with Android Studio/Perfetto. Follow with larger-layout/landscape refinement, widget resize previews and provider padding, optional managed-profile support through supported Android APIs, richer accessibility drag alternatives, and a versioned read-only ICARUS capability contract if server changes are explicitly authorized later. Privileged OEM launcher choreography is outside an ordinary app’s guarantees.
