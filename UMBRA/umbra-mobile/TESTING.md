# Phase 1 verification

## Automated checks

Run `build_umbra.bat` on Windows or `./gradlew :app:testDebugUnitTest :app:lintDebug :app:assembleDebug` elsewhere. JVM tests cover URL acceptance/rejection, all animation restrictions, master override restoration, on-disk preferences after store recreation, favorite toggling, real local HTTP HEAD requests, response classification, redirects not followed, call timeout, and cancellation.

With an emulator or USB device connected, run `./gradlew :app:connectedDebugAndroidTest`. Device UI tests cover drawer search, Back to terminal, and master-switch persistence across activity recreation. These tests change the test installation's animation setting; use an emulator or dedicated test device.

## Galaxy S24+ acceptance checklist

Use the debug APK and record Android/One UI version, display resolution, font size, refresh-rate setting, test outcome, and any logcat crash stack. Do not share connection URLs, tokens, or browser authentication in logs.

- [ ] Install and open; confirm no runtime permission prompt.
- [ ] Select UMBRA in Settings → Apps → Choose default apps → Home app. Press Home from another app and from Config; verify the terminal appears.
- [ ] Launch Phone, Messages, Camera, Settings, and a third-party app through the drawer. Confirm alphabetic ordering and labels/icons. Install/uninstall an app while UMBRA is active and verify refresh; repeat while it is inactive.
- [ ] Search with mixed case, test no matches, star two apps, filter favorites, return Home, launch a favorite, and unstar it. Force stop/reopen and reboot; verify favorites persist.
- [ ] Select every profile. Toggle all five individual effects. Turn master off, switch screens, and confirm instant/static optional effects. Turn master on and verify prior individual selections return. Recreate the activity/rotate and reboot; check persistence.
- [ ] With effects enabled, activate Samsung power saving while UMBRA is visible. Confirm effects stop. Repeat with Android Developer options animator/window/transition scales set to zero and Accessibility → Visibility enhancements → Remove animations. Restore the original settings afterward.
- [ ] With charge at/below 20%, confirm no decorative motion. Check plugged/unplugged, Wi-Fi/cellular/VPN changes, airplane mode, date/time/time-zone changes, rotation, and split screen if supported.
- [ ] Configure the actual ICARUS URL over Tailscale. Test HTTPS success, disconnected tunnel, wrong host/port, authentication-required endpoint, and timeout. Confirm status reflects the response and Open deck uses the browser. Reconnect and tap Check. No ICARUS server changes should be needed.
- [ ] Enter an invalid/credential-bearing URL and invalid timeout. Verify Save is disabled and the saved working connection remains intact.
- [ ] Launch another app and inspect CPU/network in Android Studio Profiler: no decorative updates or network polling while UMBRA is stopped. Lock/unlock and confirm normal recovery. A request already in flight must cancel when stopped.
- [ ] Swipe notification shade, lock/unlock with fingerprint, place a call, use native Recents, gesture/three-button navigation, edge panel, and Samsung camera shortcut. Confirm normal system behavior.
- [ ] Turn on TalkBack and large text/display scaling. Verify navigation, labeled animation switches, app launch/favorite controls, scroll access, and readable status alerts.
- [ ] Restore One UI Home through system settings; press Home and confirm One UI. Return to UMBRA, then uninstall after restoring One UI.

## Performance follow-up

On the physical S24+, profile drawer scrolling with at least 100 launchable apps and run idle/interaction/background battery comparisons across profiles. Record frame timing and power measurements. Host tests cannot establish Samsung frame pacing, actual battery drain, gesture integration, or thermal behavior.
