# UMBRA Phase 2 verification

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

## Physical Galaxy S24+ acceptance

Record Android/One UI version, display resolution, text/display scaling, navigation mode, battery state, and outcome. Do not share pairing PINs, tokens, private connection URLs, or authenticated browser state in logs/screenshots.

- [ ] Install Phase 2 over Phase 1 with the same key. Verify favorites, URL, profile, and individual effects migrate. Select UMBRA as default Home; press Home from other apps and Studio. Restore One UI Home and confirm recovery.
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

## Performance and limitations

Measure real S24+ drawer frame timing with ≥100 launchable apps and idle/interaction/background battery behavior across profiles. This environment has no KVM; stable and current emulator versions could not allocate their required data partition. Host Android UI tests provide useful regression coverage but do not establish Samsung gesture policy, special-access grants, real Keystore behavior, actual wallpaper application, live ICARUS/Tailscale compatibility, battery savings, or measured frame rates. See PHASE2_REPORT.md for the final executed results and outstanding acceptance items.
