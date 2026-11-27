# UMBRA Phase 2.3 verification

## Automated commands

```sh
./gradlew --no-daemon :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
```

Host tests include Phase 1 HTTP/policy/persistence regressions, strict schema/URL/layout validation, Phase 1→2 DataStore migration, independent animation controls, zero intensity and power/accessibility/thermal overrides, category resets, request refresh gating, and the actual existing ICARUS HTTP contract against MockWebServer. Redirects must not forward bearer tokens; cancellation, response size, unavailable readings, pairing, and action formats are checked.

Robolectric runs the **actual MainActivity and Compose UI** with native graphics under Android 11 (SDK 30) and Android 14 (SDK 34) at an S24+-sized logical viewport. It models Android's automatic grant of this application's own signature broadcast permission. UI regression covers search, Back, Command Center down/up gestures, native-notification fallback, persistent Android-bar restoration, master on/off, Minimal profile, activity recreation, and access to unpaired ICARUS. The test also exercises real local HTTP HEAD lifecycle transitions and validates generated wallpaper PNG dimensions. Host-rendered images are written to `app/build/reports/ui/`. These are host Android renders, **not physical phone screenshots or performance measurements**.

The suite's paused host Android main looper is explicitly advanced for lifecycle/network callbacks; real OkHttp request threads still use actual local sockets. Android runtime/graphics dependencies are downloaded by the test runner on first use.

For a working emulator or dedicated device:

```sh
./gradlew :app:connectedDebugAndroidTest
```

Device tests include launcher navigation/settings recreation and a Keystore AES/GCM pairing test. The Keystore test uses an isolated temporary private directory. Launcher UI tests change the test installation's preferences, so use a dedicated test installation/device. Compiling a device-test APK is not proof those tests ran.

## Phase 2.1 regression coverage

The final suite adds strict schema 3 / legacy schema 2 compatibility; independent Visual Detail and transitions; per-category and master transition gating; folder creation/moves/page removal with stable IDs; on-disk workspace and native widget ID survival; portable export/import stripping host IDs; actual `ActivityOptions` bundle bounds and immediate native launch intents; zero-resource launch fallback with master off; Open-Meteo HTTP formats, units, provider failures, private-cache recreation/TTL/offline expiry; authenticated instant catalog/action requests, feedback, server binding, and concurrent-tap suppression.

Final executed result: **48 tests passed, zero failures/errors/skips; lint zero errors (13 warnings); app and device-test APKs built**. See `verification/phase21/RESULTS.txt` and `final-checks.log`.

Additional SDK 30/34 Activity/Compose regression verifies real touch drag-to-folder, adding a page and an Analog widget, and opens/closes folders and clock details with master off, swipes home pages, returns from Apps without losing the selected page, changes widget settings, recreates the Activity, renames a folder, and exercises both system-bar requests with persisted preferences. Clock seconds are functional updates, independent of optional motion. Host tests do not prove Samsung’s cross-activity compositor behavior or compatibility with any third-party widget provider.

Executed logs, JUnit summaries, lint output, artifact inspection, and fresh host renders are in `verification/phase21/`. `verification/phase2/` remains the historical baseline. Intermediate failed regression logs are retained alongside the final successful run so fixes remain reviewable.

## Physical Galaxy S24+ acceptance

Record Android/One UI version, display resolution, text/display scaling, navigation mode, battery state, and outcome. Do not share pairing PINs, tokens, private connection URLs, or authenticated browser state in logs/screenshots.

- [ ] Install Phase 2.1 over Phase 1/2 with the same key. Verify favorites, URL, profile, and individual effects migrate. Select UMBRA as default Home; press Home from other apps and Studio. Restore One UI Home and confirm recovery.
- [ ] Discover/launch Phone, Messages, Camera, Settings, and third-party apps. Search, favorite/unfavorite, filter, install/uninstall while visible/backgrounded, and use customized quick labels/order.
- [ ] Verify immersive defaults, cutout and corner safe areas, transient bar reveal/auto-hide, keyboard entry, protected edge gestures, Back, Recents, and the header's Android bars emergency escape. Check actual bar visibility feedback where Android retains them.
- [ ] Swipe down on Home/overscroll at its top, swipe up on Command Center header/overscroll at its bottom, second swipe native-notification fallback, and all corresponding buttons with animation off. Body scrolling must remain usable.
- [ ] Reorder/hide every module, adjust tile sizes, reorder/rename quick apps, reset layout, recreate/reboot, and confirm persistence.
- [ ] Check real battery/charging, Wi-Fi/cellular/VPN, airplane mode, power saver, storage/memory refresh, and uptime. Unavailable values must not appear as zero. Compare to Android Settings where practical.
- [ ] Use per-window brightness and confirm global brightness is unchanged outside UMBRA; open sound/Wi-Fi/Bluetooth/display/battery settings.
- [ ] Without notification access, show unavailable/authorization instructions. Grant access deliberately, check summary counts/group handling, disable local counting, revoke access, and verify no notification content appears anywhere.
- [ ] Enable all effects, then test every independent switch, master off/on, intensity 0/100, all profiles, active interaction, screen lock/off, battery ≤20%, power saver, and Android Remove animations / zero animation scales. Restore any Developer options changed for testing.
- [ ] Pair the native client to the actual ICARUS server via Tailscale. Verify PC readings and simulation snapshot ages, known queued commands, configured TV keys, configured game shortcuts, target-game focus, authentication failure, offline/reconnect, wrong host/port, and timeout. Do not treat queue acknowledgment as command execution.
- [ ] Confirm server-base changes never reuse a token for another base, redirects are refused, Forget pairing works, and local clear remains possible offline. Run the actual Keystore device test.
- [ ] Test resume/network refresh switches, manual Check, optional foreground intervals, background/lock cancellation, and no requests/animations while stopped. Use Android Studio Profiler/Network Inspector for the real device.
- [ ] Export/import all categories, cancel document pickers, reject malformed/oversized/wrong-version/wrong-type files without changing current data, reset individual categories, and restore defaults.
- [ ] Export/apply the coordinated lock wallpaper, configure Samsung's native clock/Good Lock manually, and confirm secure keyguard/fingerprint behavior is unchanged. Test OEM wallpaper restrictions/fallback.
- [ ] Test TalkBack, large fonts/display scaling, rotation, keyboard, calls, notifications, Samsung edge panels, biometric unlock, gesture/three-button navigation, and One UI fallback.

## Phase 2.1 physical acceptance additions

- [ ] Confirm Enhanced default on migration; select all detail/motion combinations and recreate/reboot. Master off must retain Cinematic detail and every individual transition choice.
- [ ] Launch apps from Home, drawer, folder, and Command Center. Check supported icon-origin scale-up/clip reveal, fallback, reduced motion, power saving, native return gestures, cold/warm tasks, portrait/landscape, and animation interruption. Record One UI version; do not label the result exact Samsung parity.
- [ ] Open/close folders from measured icon positions, move them across pages, rotate, and close using Back. Open/close UMBRA widget details from actual bounds. Rapidly open/close Command Center and settings; ensure inputs are not delayed or lost.
- [ ] Drag app-to-app and app-to-folder; reorder, move at page edges or through explicit management, rename folders, reorder/remove members, delete folders, hide/unhide apps, customize drawer order, delete/reorder pages, and confirm all saved positions after reboot.
- [ ] Test five clock styles, 12/24-hour, AM/PM, seconds, accent, transparent panels, dimensions, screen-off/locked states, master off, and large fonts. Verify date/time changes and timezone updates.
- [ ] Choose a real weather city; verify current/high-low/hourly/daily values with Open-Meteo, C/F and last-updated time. Test permission denial, approximate location timeout, offline cache ages, malformed response, location/unit changes, visible refresh, and no stopped/background polling.
- [ ] Add a compatible third-party widget through Android binding, including a provider configuration Activity. Cancel/deny/rotate/restart mid-flow, resize with provider restrictions, remove, recreate/reboot, uninstall provider, and import/rebind. Confirm native clicks, embedded scrolling, and PendingIntent actions are not intercepted by UMBRA.
- [ ] Toggle header bars in both directions including during transient visibility, keyboard use, calls, and three-button/gesture navigation. Confirm settings values and Home fallback remain accessible even when One UI retains protected bars.
- [ ] Pair the actual server, Sync controls, compare four configured Rocket League names/mappings and ten saved messages with current PC config, change a PC mapping then invoke by name, refresh changed text/labels, favorite/reorder/relabel locally, and confirm repeated in-flight taps are dropped. Test missing actions, auth expiry, server switch, cancellation, and game focus. No server files should change.

## Performance and limitations

Measure real S24+ drawer frame timing with ≥100 launchable apps and idle/interaction/background battery behavior across profiles. This environment has no KVM; stable and current emulator versions could not allocate their required data partition. Host Android UI tests provide useful regression coverage but do not establish Samsung gesture policy, special-access grants, real Keystore behavior, actual wallpaper application, live ICARUS/Tailscale compatibility, battery savings, or measured frame rates. See PHASE21_REPORT.md for the final executed results and outstanding acceptance items.

## Phase 2.3 execution and physical checklist

Current executed results are in `verification/phase23/` and [PHASE23_REPORT.md](PHASE23_REPORT.md); earlier Phase 2.1 counts above describe historical coverage. New tests exercise mixed-span collision invariants across densities, collapsed header sizes/order, strict schema 4 imports, schema 3 native-widget ID migration, persistent module flags/mode/status choices, more-than-six/all/explicit-empty selections, all supported output payloads, local overrides preserving placement/widget references, button files rejecting unsupported protocols, and real authenticated command/queued/error responses.

SDK 30/34 native UI tests physically hold and drag collapsed Command Center headers with motion enabled and disabled; assert no expansion, amber guides while dragging and none afterward, hidden normal-use arrangement controls, Undo, independent module expansion, and Compact mode after Activity recreation. They also verify per-tab status space, compact Settings/footer, selection of 14 buttons, and long-press editing without executing a command. Earlier Home/folder/widget tests use the new contextual entry points while retaining persistence and touch assertions. The paused host Android event loop is explicitly processed for asynchronous storage/network callbacks.

Physical S24+ checks remain separate:

- [ ] Upgrade the existing signed installation without uninstalling. Compare all pages, folder membership, widget IDs/binding/configuration, favorite/button assignments, URLs, motion/detail choices, and weather location before/after.
- [ ] Drag collapsed headers, expand multiple modules, resize/hide/restore, switch Compact/Expanded, then rotate/restart/reboot. Test all combinations of master off/on, intensity zero, profiles, Android reduced motion, and power saving.
- [ ] Confirm amber guides appear only for active editing, clear on release/cancel/Back/Done, and never remain after navigation. Test interrupted/rapid and two-finger gestures. Verify no command fires from long-press, drag, resize, or import.
- [ ] Move apps/folders/widgets/controls across free and occupied cells, use adjacent-page dragging and direct page chooser, resize mixed spans, and Undo. Verify TalkBack alternatives, large fonts, landscape, and no overlapping interactive controls.
- [ ] Create/edit/delete/rename/icon-select Instant Buttons, test each supported output against the actual paired server and target app/game, export/import, create local overrides, and confirm shared PC mappings never change. Distinguish acknowledgment/queued state from real execution.
- [ ] Select a catalog larger than six, search/filter, Select all/Deselect all, customize each widget independently, scroll to the final selected entry, hide/restore, and synchronize removed/renamed server references without losing retained assignments.
- [ ] Check compatible native widget short clicks, scrolls, long-press handling, bind/configuration cancellation, provider resize constraints, lifecycle stops, and rebinding after portable import. OEM-only/work-profile providers remain unverified.
- [ ] Compare status preferences on every tab, confirm Settings has only a compact title and scroll footer, and verify native system bars/notifications, calls, keyguard, gestures, media/system interfaces, and One UI Home recovery.
- [ ] Profile frame timing, large catalogs, real providers, idle/background/network activity, and battery behavior with Android Studio/Perfetto. Host tests do not establish performance measurements.

## 2.3.1 soundboard hotfix

See [executed results](verification/soundboard/RESULTS.txt) and [integration / physical acceptance](SOUNDBOARD_INTEGRATION.md). `SoundboardTest` covers the real catalog/play/stop/edit/output contracts and server-only preferences; `SoundboardHostUiTest` runs native SDK 30/34 grid and Settings flows. The existing full suite still passes. ICARUS 4.8B service and Chromium/HTTP tests pass in an isolated reference checkout without modifying the main server or private library. Generated fixtures and mocked Windows rendering do not establish actual audible output or physical S24+ acceptance.

## Phase 3 acceptance

See [Phase 3 report](PHASE3_REPORT.md) and [executed results](verification/phase3/RESULTS.txt). New native SDK 30/34 tests exercise six-tab/header presence, persisted indicator visibility, real HTTP fixture telemetry shared by two HOME widgets, independent resizing/collapse, preset restoration and cancellation while stopped. Pure tests cover inert legacy TV mappings, older schemas, native widget binding retention/export, exact Windows contracts, supported old-server fallback, request interruption, sample ages and conservative connection classification. Physical PC/S24+ sensors, Tailscale route, game/audio delivery, native HOME selection, gestures and battery consumption still need real-device acceptance.

## 3.1 current verification

See [executed results](verification/widgets31/RESULTS.txt) and [current setup/limits](WIDGETS31_REPORT.md). The final full run has 97 Android test executions. New tests cover independent widgets and schema-5 selection migration, owned command definitions/overrides, exact Windows hotkey and sound endpoints, a 512-entry catalog, PIN field without export leakage and the optional Recents setup/privacy declaration. SDK 30/34 host flows use generated HTTP fixtures, not the user's PC. PC update evidence records 42 service + 10 Chromium + 4 installer tests.

Physical checks: upgrade without uninstalling; compare all existing presets; add independent Rocket/Fortnite and sound widgets; configure/save/cancel and resize; test scrolling at dense/large-font layouts; verify animations off; pair using the real PIN; manually enable optional Recents and verify native Samsung behavior/gestures; apply PC installer to the stopped exact Phase 4.9 installation after verified backups; import actual files and verify output, existing sounds and voyage preservation. No live PC deployment or device acceptance is implied by host tests.

## 3.2 current acceptance

[Executed build/test evidence](verification/home32/RESULTS.txt) and [current setup/limits](HOME32_REPORT.md). New native host tests run on SDK30/34, exercise independent header/footer recovery and activity recreation, verify reclaimed viewport height without page-data changes, show 13 command/sound controls in one fill-page widget, confirm separate authenticated command/sound playback routes and unchanged audio output, then stop the launcher and assert no idle requests. A native SDK34 landscape-tablet case asserts 12 controls in the same row of one full-width widget. Pure tests cover schema6-to7 defaults, strict booleans, dynamic sizing/collisions without saved-grid mutation, row-major new-button packing with retained explicit positions and static category palettes.

Physical acceptance: upgrade the previous APK without uninstalling; compare presets and widget IDs; collapse each section and both, restore Tabs/Header, swipe pages, rotate, reboot and test animations off/on; configure a mixed widget with actual quick chat, emotes, mining/hotkeys and sounds; long-press rearrange/resize and verify no unintended playback; confirm actual PC output remains unchanged. Test large fonts/landscape/third-party widgets/native gestures/Recents and measure performance. No live PC or Samsung hardware verification is implied by host fixtures.
