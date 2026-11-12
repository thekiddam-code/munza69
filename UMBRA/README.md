# UMBRA Mobile

Native Android launcher for Samsung Galaxy S24+, built with Kotlin and Jetpack Compose. This folder is separate from the existing ICARUS application.

## Download

These links download files from GitHub rather than ChatGPT artifacts:

- [Download debug APK](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-debug.apk)
- [Download APK as ZIP](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-apk.zip) — extract the APK before installing.
- [Download Android Studio source ZIP](https://github.com/thekiddam-code/munza69/raw/refs/heads/main/UMBRA/downloads/umbra-mobile-source.zip)
- [SHA-256 checksums](downloads/SHA256SUMS.txt)

## Install

Transfer the APK to your phone and open it. Allow installation from the file manager when Android asks. Then choose **Settings → Apps → Choose default apps → Home app → UMBRA**. To restore Samsung, select **One UI Home** in that same screen.

Keep Tailscale connected separately. Configure your own Remote Deck URL in UMBRA's Config screen. No ICARUS server change is required.

## Build and documentation

Open [umbra-mobile](umbra-mobile/) in Android Studio. On Windows, run `umbra-mobile\build_umbra.bat` with JDK 17 or 21 and Android SDK 35 configured.

- [Installation, configuration, and build guide](umbra-mobile/README.md)
- [Implementation and limitation report](umbra-mobile/PHASE1_REPORT.md)
- [Device acceptance checklist](umbra-mobile/TESTING.md)

The debug APK was successfully built with Gradle. Eight host tests passed; Android lint passed with zero errors. The APK signature was verified. Native UI tests could not execute because the cloud emulator's Package Manager failed to initialize. Physical Galaxy S24+/One UI and live ICARUS/Tailscale acceptance testing remain required. This is a development-signed APK, not a store release.
