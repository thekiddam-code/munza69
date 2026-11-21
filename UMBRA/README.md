# UMBRA Mobile 2.0 — Phase 2

Native Kotlin / Jetpack Compose Android launcher for Samsung Galaxy S24+, alongside the existing ICARUS project.

## Download and install

- [Download Phase 2 debug APK](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-debug.apk)
- [Download APK ZIP](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-apk.zip) — extract before installing.
- [Download full Android Studio project](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-source.zip)
- [Download coordinated lock-screen wallpaper](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-lock-screen.png)
- [SHA-256 checksums](downloads/SHA256SUMS.txt)

Install over Phase 1 to preserve settings. Select **Settings → Apps → Choose default apps → Home app → UMBRA**. Choose **One UI Home** there to restore Samsung. The persistent **Android bars** header action exits immersive presentation.

## Phase 2

Supported immersive fullscreen; real configurable status panel; native swipe Command Center and system dashboard; nine independently controlled motion categories, profiles, intensity and master override; native ICARUS pairing/Engineering/Lounge/Simulator controls; Customization Studio; validated versioned settings import/export; coordinated static lock wallpaper.

ICARUS native pairing uses your existing server PIN and Android Keystore-encrypted local credentials. Keep Tailscale connected separately. No ICARUS server/simulation change is required. Native notifications, system gestures, keyguard, biometrics, calls, settings, and One UI fallback remain Android-managed.

## Source and documentation

Open [umbra-mobile](umbra-mobile/) in Android Studio. Windows: `umbra-mobile\build_umbra.bat` with JDK 17 or 21 and Android SDK 35.

- [Install, build, and operation guide](umbra-mobile/README.md)
- [Configuration schema and privacy](umbra-mobile/CONFIGURATION.md)
- [Phase 2 feature checklist, results, limitations, and Phase 3](umbra-mobile/PHASE2_REPORT.md)
- [Physical-device acceptance checklist](umbra-mobile/TESTING.md)

The debug APK builds successfully. Host Android 11/14 UI testing is distinct from physical Samsung acceptance. Device notification access, actual Keystore/wallpaper/system gestures, live ICARUS/Tailscale behavior, and measured performance remain phone checks. This is a development-signed build, not a store release.

## Host Android UI preview

These images render the actual Activity/Compose UI in Robolectric's host Android runtime; they are not physical phone screenshots. Missing host telemetry is displayed as unavailable.

<img src="umbra-mobile/verification/phase2/host-renders/home-sdk34.png" width="300" alt="UMBRA Home rendered by the host Android runtime">
<img src="umbra-mobile/verification/phase2/host-renders/command-center-sdk34.png" width="300" alt="UMBRA Command Center rendered by the host Android runtime">
