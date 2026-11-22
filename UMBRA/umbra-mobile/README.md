# UMBRA Mobile 3.0

A native Kotlin / Jetpack Compose Android HOME launcher for Samsung Galaxy S24+, package `com.umbra.mobile`. Android 10+ (API 29), target/compile API 35. This increment preserves the existing industrial terminal interface and native Android functions while moving arrangement controls out of normal use.

## Phase 3

**HOME | APPS | DECK | SIMULATOR | ICARUS | CONFIG**. Engineering has its own DECK section and six HOME widget types, backed by the existing shared Windows companion. Named HOME presets retain independent layouts and widget settings. A compact, optional PC status indicator appears across all tabs; tap for status, reported PC name, detected address class, HTTP latency and Reconnect. CONFIG → ICARUS hides it. TV controls are retired; existing mappings are retained as inert migration data. Soundboard audio settings stay on ICARUS. See [Phase 3 setup, migration, APIs, verification and limits](PHASE3_REPORT.md).

## Install / update / recover

Download `umbra-mobile-debug.apk` from the sibling [GitHub downloads folder](https://github.com/thekiddam-code/munza69/tree/main/UMBRA/downloads), or extract the APK ZIP first. Open the APK on the phone and grant the opening file manager/browser installation permission when Android requests it. ADB alternative: `adb install -r umbra-mobile-debug.apk`.

Version **3.0 (code 6)** updates the previous signed build without requiring an uninstall. Keep the same signing key when building future updates; a build signed on another computer may need your consistent key or an uninstall, which clears local data. The distributed debug build is for development, not store distribution.

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

Home, module headers, Instant Buttons, system controls, Engineering, Lounge TV keys, Simulator/Rocket League controls, ICARUS shortcuts, and Device Status use the same collision-aware grid. Reference density adapts to available width/orientation; mixed spans cannot paint across neighboring controls. Expanded sizes, positions, hidden flags, and collapsed flags persist. TalkBack exposes long-click and accessible reordering alternatives without permanent arrangement buttons.

Wi-Fi, Bluetooth, sound, display, battery, media, and device controls open their supported Android interfaces. Brightness applies to **UMBRA's window only**, with Use system brightness recovery. No restricted system setting is reported changed merely because a shortcut was tapped. Android notifications remain native; optional notification counts require explicit OS listener authorization and exclude notification content.

## ICARUS soundboard hotfix

Open **DECK → Soundboard** for the existing server sound library. Output selection is now under **Settings → DECK → Soundboard → Audio Output**, saved on ICARUS and shared with Remote Deck. Keep using the working soundboard-capable 4.8B/C server; main’s older server has no soundboard API. See [integration, storage, exact APIs and verification](SOUNDBOARD_INTEGRATION.md).

## Instant Buttons / ICARUS

Keep Tailscale connected separately. In **Settings → ICARUS**, configure the existing Remote Deck URL and optional server base, timeout, and refresh behavior. Native pairing uses the current server PIN via `POST /api/pair`. Browser authentication is separate. One server-bound token is AES/GCM encrypted with Android Keystore in private no-backup storage, excluded from exports. Changing servers never forwards the prior token to the new base.

Open **DECK → Instant Buttons**. Long-press its title to create buttons, select/search the catalog, Select all/Deselect all, save/load button definitions, and restore hidden entries. Long-press buttons to configure, rename, choose an icon, change supported output parameters, duplicate, remove, resize, or drag. Test command is explicit and shows actual response/error feedback. Configuring a discovered server reference creates a UMBRA override with preserved placement while leaving PC mappings unchanged.

Supported existing outputs are quick chat by current name, named macros, text/channel/timing, configured Fortnite slots, mining toggle, timed forward mining, Stop/release, and simulation commands. Generic arbitrary press/release/script protocols are unsupported. The complete selected set wraps and scrolls; there is **no six-button truncation**. Each ICARUS widget can have independent selected buttons. Missing catalog references remain retained and reported. Sync displays the actual snapshot time; PC key arrays stay server-resolved at execution.

Requests are authenticated, bounded, cancellable, timeout-limited, and never follow redirects carrying credentials. Repeated in-flight taps are dropped. HTTP acknowledgment is not proof of game execution; simulation reports its queue acknowledgment as pending PC execution. No local edit/import automatically executes a command or modifies server files. See [ICARUS_OUTPUTS.md](ICARUS_OUTPUTS.md).

Home's Remote Deck HEAD check measures HTTP reachability only. Native PC/simulation telemetry uses real responses and labels unavailable data. Optional 30–300 second native refresh runs only while visible and stops under power/thermal restrictions. No inactive continuous polling, analytics, wake locks, or new persistent service is introduced.

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

Verified 3.0 result: **89 Android tests passed; lint zero errors (13 warnings); app and device-test APKs built**. The previous signing certificate, permissions and native-library list are preserved. See [Phase 3 results and hardware limits](verification/phase3/RESULTS.txt).

Debug APK: `app/build/outputs/apk/debug/app-debug.apk`. Device instrumentation requires a real device/working emulator: `./gradlew :app:connectedDebugAndroidTest`. Compilation of its APK is not proof of execution.

- [Phase 3 Engineering / shared connection / migration](PHASE3_REPORT.md)
- [Phase 2.3 implementation, executed verification, limits, next steps](PHASE23_REPORT.md)
- [Layout migration, editing, Undo, backup, and storage limits](LAYOUT_MIGRATION.md)
- [Configuration schema and privacy](CONFIGURATION.md)
- [Instant Buttons and exact server output contract](ICARUS_OUTPUTS.md)
- [Regression / physical S24+ acceptance checklist](TESTING.md)

Full configuration export uses Android's file picker and includes versioned layouts, selections, and preferences; credentials and portable widget bindings are excluded. Back up before large edits or imports. Weather locations/private URLs in an export should be shared deliberately. Corrupt/invalid storage recovers safely; failed writes remain visible. No QUERY_ALL_PACKAGES, precise/background location, storage, privileged status-bar, accessibility-service, or global-brightness permission is requested. Optional approximate location and notification listener access remain user-controlled.

Physical S24+/One UI behavior, native provider compatibility, live ICARUS/Tailscale/game execution, real Keystore, and measured performance remain device acceptance items. Historical reports/evidence for earlier phases are retained separately.
