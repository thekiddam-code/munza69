# UMBRA Mobile 3.3

A native Kotlin / Jetpack Compose Android HOME launcher for Samsung Galaxy S24+, package `com.umbra.mobile`. Android 10+ (API 29), target/compile API 35. This increment preserves the existing industrial terminal interface and native Android functions while moving arrangement controls out of normal use.

## Current increment: fullscreen recovery and silver host actions

Outside Android fullscreen, UMBRA shows one **⛶ Fullscreen** recovery button instead of the launcher header/tab names. It restores the retained page/preset/tab/navigation. Existing HOME focus/collapse settings remain independent. Category footers now use custom vector line icons with the existing colors and accessibility names.

In a mixed widget's existing picker, optionally select the silver **Switch to Arctis** and **Save Clip** Host actions. A separate [Phase 4.9 PC API installer/setup](../pc-update/phase49-host-actions/README.md) is required. Arctis switches only four playback routes and reads them back. Save Clip uses the saved host binding with scan-code input and bounded new-file observation; a hotkey acknowledgment is not clip confirmation, and actual GG acceptance must be tested on the PC.

[Current setup, contracts, verification and limits](HOST33_REPORT.md) · [3.2 full-page/12-column setup](HOME32_REPORT.md). Existing presets, 12-column tablet widgets, bindings and soundboard preferences are retained. The private Windows PC was not deployed remotely.

## Install / update / recover

Download `umbra-mobile-debug.apk` from the sibling [GitHub downloads folder](https://github.com/thekiddam-code/munza69/tree/main/UMBRA/downloads), or extract the APK ZIP first. Open the APK on the phone and grant the opening file manager/browser installation permission when Android requests it. ADB alternative: `adb install -r umbra-mobile-debug.apk`.

Version **3.3 (code 9)** updates the previous signed build without requiring an uninstall. Keep the same signing key when building future updates; a build signed on another computer may need your consistent key or an uninstall, which clears local data. The distributed debug build is for development, not store distribution.

Select **Samsung Settings → Apps → Choose default apps → Home app → UMBRA**. Select **One UI Home** in that same screen to restore Samsung. UMBRA can open Android's Home settings from its Settings categories. No root, kiosk/device-owner mode, protected notification shade, secure lock-screen replacement, or firmware changes are used.

## Everyday interaction

- **Tap** performs the normal action. Tap a deck module header to expand/collapse it.
- **Long-press** an app, folder, widget, control, or module header to edit. Hold and drag to reposition; release snaps and saves. Collapsed headers move without expanding. Contextual options provide configure, resize, remove/hide, duplicate where supported, and page movement.
- Only editing shows the Arrange toolbar (Options, Undo, Done). Back or tapping blank space exits. Amber available-cell guides appear during drag/resize and clear afterward, including with animations off. There are no permanent Widget Options rows.
- Long-press the **Home page title** to add folders/widgets/pages or restore hidden items. Swipe horizontally or use dots to change pages. An Android Home intent returns to the configured default page. Folder membership and widget IDs follow their stable item IDs when moved.
- **Apps** discovers launchable activities, sorts alphabetically unless customized, searches, filters favorites, and opens native app information. Long-press to favorite, pin, or hide. Original icons remain borderless, with adjustable size/labels. Hidden apps can be restored in Settings → Organization.
- **Deck** opens the Command Center; Home's handle/downward overscroll also opens it. Swipe up on the Command Center header to close. The second downward pull offers the native notification-shade fallback. Protected Android edge navigation remains available.
- **Show bars / Hide bars** is an immediate persistent two-way header control based on reported WindowInsets visibility. Android may retain or transiently reveal protected bars for HOME, keyboard, calls, accessibility, or vendor policy; UMBRA does not force them on a timer.

## Modular decks and Command Center

Command Center remembers **Compact / Expanded** independently from each module's expansion choice. Modules can expand simultaneously. Collapsed sections show an icon, title, relevant status where available, and affordance, without large empty panels. Long-press the header to move it while still collapsed. Contextual Configure exposes density, visibility, and restoration; Settings → Command Center can restore all hidden controls.

Home, module headers, button widgets, system controls, Engineering, Simulator/Rocket League controls, ICARUS shortcuts, and Device Status use the same collision-aware grid. Reference density adapts to available width/orientation; mixed spans cannot paint across neighboring controls. Expanded sizes, positions, hidden flags, and collapsed flags persist. TalkBack exposes long-click and accessible reordering alternatives without permanent arrangement buttons.

Wi-Fi, Bluetooth, sound, display, battery, media, and device controls open their supported Android interfaces. Brightness applies to **UMBRA's window only**, with Use system brightness recovery. No restricted system setting is reported changed merely because a shortcut was tapped. Android notifications remain native; optional notification counts require explicit OS listener authorization and exclude notification content.

## ICARUS soundboard hotfix

Open **SIMULATOR → Soundboard** for the existing server sound library. Output selection is now under **CONFIG → ICARUS → Soundboard → Audio Output**, saved on ICARUS and shared with Remote Deck. Keep using the working soundboard-capable Phase 4.9 server; main’s older server has no soundboard API. See [integration, storage, exact APIs and verification](SOUNDBOARD_INTEGRATION.md).

## Button widgets / ICARUS

Keep Tailscale connected separately. Save the Remote Deck/server address in CONFIG → ICARUS, then enter its current server PIN and pair. Browser authentication is separate. One server-bound token is AES/GCM encrypted with Android Keystore in private no-backup storage, excluded from exports. Changing servers never forwards the prior token to the new base.

Long-press a HOME page title → Add widget → Button widget or Soundboard. Long-press the widget header → Configure for its own group, selected buttons, title, columns, button height, accent, transparency and dimensions. Save commits the draft; Cancel discards it. Add custom button and button overrides belong to that instance only. Put Rocket League on one page and Fortnite on another, or hotkeys and sounds together. Page columns support 2–8 with minimum touch-size adaptation; inner buttons 1–6 columns. Long-press header to move/resize, including while collapsed; long-press individual buttons to edit their inner arrangement. No six-button limit is imposed.

Existing outputs include quick chat, macros, text/channel/timing, Fortnite slots, mining, Stop/release, simulation and advertised fixed Windows hotkeys. Arbitrary scripts/paths are unsupported. Soundboard uses original ICARUS IDs and playback endpoints; output/favorite configuration remains on the server. [Current details](WIDGETS31_REPORT.md).

Requests are authenticated, bounded, cancellable, timeout-limited, and never follow redirects carrying credentials. Repeated in-flight taps are dropped. HTTP acknowledgment is not proof of game execution; simulation reports its queue acknowledgment as pending PC execution. No local edit/import automatically executes a command or modifies server files. See [ICARUS_OUTPUTS.md](ICARUS_OUTPUTS.md).

Home's Remote Deck HEAD check measures HTTP reachability only. Native PC/simulation telemetry uses real responses and labels unavailable data. Optional 30–300 second native refresh runs only while visible and stops under power/thermal restrictions. No inactive continuous polling, analytics or wake locks are introduced. The optional user-enabled Recents accessibility service only handles explicit taps.

## Widgets, appearance, motion, and status

Built-ins include Digital, Terminal, Analog, Segmented, and Date/time clocks; calendar; real battery/system data; weather; and ICARUS controls. Clock format, seconds, accent, transparency, and dimensions are configurable through long-press. Functional clock ticks continue with optional motion off and pause when inactive/obscured.

Weather uses documented [Open-Meteo forecast](https://open-meteo.com/en/docs) and [geocoding](https://open-meteo.com/en/docs/geocoding-api) APIs, attributed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Choose a city manually or request a one-shot approximate location, then Celsius/Fahrenheit. Only the selected query/coordinates go to the provider. Current/high-low/hourly/five-day values and fetch time are real; a 30-minute cache retains dated offline data up to seven days. No location is configured by default, and no background weather polling occurs. Observe the provider's terms before commercial distribution.

Third-party widgets use Android's AppWidgetHost binding/provider-configuration flow, native views and PendingIntents, persistent host IDs, and provider-aware sizing. Short clicks/scrolling remain native; providers may consume their own long-press. Host long-click accessibility actions also expose editing. Imports strip foreign host IDs and require rebinding. Proprietary Samsung/work-profile providers and oversized layouts need physical verification.

**Visual Detail** Minimal / Enhanced (default) / Cinematic controls cached static industrial structure independently from motion. Adaptive (default), Cinematic, Minimal, master, intensity, and all effect/transition switches persist independently. Power saver, low battery, reduced motion, thermal state, and screen power still gate optional motion. Appearance → Transitions retains measured-icon native app scale-up/clip-reveal/fade fallback, shared folder/widget expansion, and restrained Command Center/panel transitions. Samsung ultimately controls cross-app and gesture-return choreography; exact One UI parity is not claimed.

Settings has a compact title and an identity/version/build footer at the bottom of its scroll content. **Display → Status Panel** stores separate context preferences, with Applications and Settings off by default. The previous global status-panel preference remains the master gate. Hiding it reclaims space without changing Android notifications or immersive settings.

## Build and documentation

Open this `umbra-mobile/` folder in Android Studio. Install Android SDK Platform 35, Build Tools 35.0.0, and JDK 17 or 21; accept SDK licenses. Studio creates ignored `local.properties`, or use `ANDROID_HOME`. Set `JAVA_HOME` or add Java to PATH. Run **build_umbra.bat** on Windows. First use requires Internet for Gradle/Maven/Robolectric dependencies. Windows batch execution is not verified in this Linux environment.

```sh
./gradlew --no-daemon -Pkotlin.compiler.execution.strategy=in-process :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
```

Verified 3.3 results are recorded in [the executed evidence](verification/host33/RESULTS.txt): Android host tests, lint, app and device-test APK builds. The distributed signing certificate is preserved. Top-level requested permissions remain unchanged; an optional manually enabled Accessibility service is added for Recent apps. See [exact current results](verification/host33/RESULTS.txt).

Debug APK: `app/build/outputs/apk/debug/app-debug.apk`. Device instrumentation requires a real device/working emulator: `./gradlew :app:connectedDebugAndroidTest`. Compilation of its APK is not proof of execution.

- [3.3 fullscreen, custom icons and paired Sonar/Moments actions](HOST33_REPORT.md)
- [3.2 full-page HOME, mixed controls and category colors](HOME32_REPORT.md)
- [3.1 independent widgets, PIN, Recents and PC bulk upload](WIDGETS31_REPORT.md)
- [Phase 3 Engineering / shared connection / migration](PHASE3_REPORT.md)
- [Phase 2.3 implementation, executed verification, limits, next steps](PHASE23_REPORT.md)
- [Layout migration, editing, Undo, backup, and storage limits](LAYOUT_MIGRATION.md)
- [Configuration schema and privacy](CONFIGURATION.md)
- [Instant Buttons and exact server output contract](ICARUS_OUTPUTS.md)
- [Regression / physical S24+ acceptance checklist](TESTING.md)

Full configuration export uses Android's file picker and includes versioned layouts, selections, and preferences; credentials and portable widget bindings are excluded. Back up before large edits or imports. Weather locations/private URLs in an export should be shared deliberately. Corrupt/invalid storage recovers safely; failed writes remain visible. No QUERY_ALL_PACKAGES, precise/background location, broad storage, privileged status-bar or global-brightness permission is requested. Optional approximate location, notification listener access and the narrowly scoped Recents Accessibility service remain user-controlled. The Recents service cannot retrieve screen content or perform gestures.

Physical S24+/One UI behavior, native provider compatibility, live ICARUS/Tailscale/game execution, real Keystore, and measured performance remain device acceptance items. Historical reports/evidence for earlier phases are retained separately.
