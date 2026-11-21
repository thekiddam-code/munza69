# UMBRA Mobile Phase 2 engineering report

## Stage A — inspected baseline

Repository baseline: `110ff857ed4db70a98bebaec642c8339b0a06b12`. Android source is `UMBRA/umbra-mobile/`; ICARUS is a sibling directory. Phase 1 source had not changed since its delivery. The untouched baseline passed `testDebugUnitTest`, `lintDebug`, and `assembleDebug`; eight JVM tests passed. Evidence: `verification/phase2/stage-a-baseline.log`.

Phase 1 provided app discovery/search/favorites, browser Remote Deck access, bounded HTTP HEAD checks, persistent Preferences DataStore, three motion profiles, five effects, local device indicators, and HOME integration. Runtime acceptance was not previously established because the software emulator failed Android service initialization.

Deficiencies addressed during Phase 2: canceled package refreshes could publish stale data; startup/transitions shared one switch; no immersive controller, independent status indicators, Command Center, native authenticated ICARUS modules, import/export, or full appearance/layout configuration existed. Phase 1 stored settings are migrated rather than discarded.

## Inspected ICARUS contract

Existing `ICARUS/server.py` supports PIN pairing (`POST /api/pair`), bearer-authenticated PC status (`GET /api/status`), simulation snapshots (`GET /api/icarus/telemetry`), queued simulation commands (`POST /api/icarus/command`), TV keys (`POST /api/tv/key`), and configured quick chat/macros/emotes (`POST /api/action`). Pairing belongs to this phone's native client; browser tokens are not read. The privileged host-key endpoints are not used by Android. No server/simulation source changes are required. No arbitrary command execution, invented sensor data, or unverified TV app IDs are added.

Implementation and validation results are appended as the stages complete.

## Delivered stages and functional scope

| Stage | Implementation | Verification |
| --- | --- | --- |
| A Foundation | Phase 1 preserved; canceled app queries cannot publish stale results | Untouched baseline build, eight original tests; expanded regressions retained |
| B Immersive display | WindowInsetsController requests, edge-to-edge safe insets, cutouts, focus/resume restoration, visible-bar feedback, persistent emergency restore, independent real status indicators | Compile/unit pass; host Android UI exercises restoring bar preferences; actual OEM bar policy is a phone check |
| C Command Center | Native scrollable modules; down/up handles and overscroll navigation; bottom Deck shortcut; module layout, tiles, labels; device snapshots; native settings shortcuts; optional authorized notification count | Compile/unit pass; actual Compose gesture and fallback flows pass under host Android 11 and 14 |
| D Visual engine | Nine independent switches; master preserves selections; intensity; Adaptive/Cinematic/Minimal; power/reduced-motion/screen/thermal constraints; no inactive decoration | Policy, persistence, and independent-transition tests; host UI toggles master and persists Minimal across recreation |
| E ICARUS | Native PIN pairing, Keystore-encrypted server-bound token, real status/bridge snapshots, existing TV keys and configured game actions, honest unsupported/offline handling, visible-only optional intervals | Four local HTTP contract/security tests plus HEAD lifecycle regression; real PC/Tailscale and hardware Keystore remain device checks |
| F Studio | Appearance/density/layout/status/gesture controls; bounded typed schema 2 import/export with preview and atomic replacement; category resets; static lock wallpaper export/apply and manual Samsung guidance | Strict schema/migration/category tests, DataStore recreation, native PNG decode/dimension check, Studio host UI; SAF/OEM application remain phone checks |
| G Validation | Full host tests, lint, app/device-test APKs, signature/metadata checks, host-rendered previews, delivery documentation | Final results below; no physical-device acceptance claim |

### Fullscreen and notification boundaries

Default settings are full UMBRA shell, Adaptive, immersive ON, both bar-hide requests ON, status panel ON. Android controls actual hiding. Transient swipe behavior belongs to the OS; there is no repeated force-hide timer, reflection call, accessibility bypass, kiosk restriction, global animation-scale write, or replacement keyguard. The header's Android bars button always remains accessible and restores persistent standard presentation. Setting changes are applied only when display policy changes or the window resumes/regains focus, after attachment.

Ordinary third-party HOME apps lack a supported public notification-shade expansion API. The second downward pull therefore offers a truthful fallback: use the protected top-edge gesture, or restore Android bars. The native shade and Quick Settings remain available. Optional notification count requires an explicit Android listener grant, is off by default, excludes group summaries, and never reads titles, text, extras, or people. The OS-bound listener is optional and distinct from an unnecessary decorative foreground service.

### ICARUS protocol and security

The native client uses the inspected existing PIN/bearer contract. Authenticated JSON is bounded to 128 KiB; calls use 1–30 second timeouts and lifecycle cancellation. Redirects are not followed. Tokens are AES/GCM encrypted under Android Keystore, bound to canonical scheme/host/port/base path, held outside DataStore in no-backup storage, and never exported/logged. Browser pairing remains separate. No private address or credential is hardcoded.

Simulation actions report **queued**, not executed. TV configuration is server-reported, not proof the TV is powered/reachable. PC macro/game buttons come from actual server status. No arbitrary command console, unverified TV app-launch button, fabricated telemetry, host publisher key, or publicly exposed server endpoint is introduced. The inspected web UI has no supported section deep-link contract, so optional browser module URLs are user-configured and otherwise open Remote Deck.

### Privacy, configuration, and performance design

Schema 2 validates types (including rejection of quoted booleans), version, URLs, color contrast, collections, IDs, ordering, label lengths, ranges, and total 64 KiB size before replacement. Phase 1 preferences migrate. Full reset clears local pairing; category reset is scoped. Imports never carry credentials or notification/device data.

Device status uses supported Android APIs. Unavailable readings are distinct from zero. Storage/memory/uptime refresh on visibility entry or manual refresh; power, thermal, network, and battery use observers. Per-window brightness does not alter global brightness. Decorative updates are limited to 8/12 scheduled updates per second and stop while inactive; this is an implementation limit, not a measured frame rate. Periodic ICARUS refresh is opt-in, 30–300 seconds, visible-screen only, and reduced under power/screen/thermal conditions. No wake lock, analytics, broad package visibility, external-storage permission, global system-write permission, or permanent foreground service is added.

## Acceptance checklist

| # | Requirement | Status / remaining validation |
| --- | --- | --- |
| 1 | Working Phase 1 features preserved | Baseline regressions, search/Back/persistence host UI pass; real installed-app launch on S24+ remains manual |
| 2 | Edge-to-edge | Implemented and host rendered; camera cutout/rounded-corner device check remains |
| 3 | Supported immersive fullscreen | Native requests and escape implemented; host action tested; OEM policy remains physical |
| 4 | System gestures usable | No protected-edge interception; Samsung gesture/Recents validation remains physical |
| 5 | Real custom status panel | Actual APIs with unavailable markers; optional listener grant/count requires device validation |
| 6 | Swipe down opens Command Center | Host Android 11 and 14 UI pass |
| 7 | Swipe up closes Command Center | Host Android 11 and 14 UI pass |
| 8 | Native Android notifications available | Supported system edge gesture preserved; native fallback/restore dialog host UI pass |
| 9 | Command Center actions | Native implementation, discovered app tiles, supported settings intents, existing HTTP contracts; physical external targets remain manual |
| 10 | Adaptive behavior | Power/accessibility/interaction/thermal policy tests pass; real callbacks/performance remain hardware checks |
| 11 | Independent categories | Nine settings and independent command/terminal transitions tested |
| 12 | Master override | UI on/off and persisted independent selections tested |
| 13 | Intensity survives restarts | JSON round trip and on-disk DataStore recreation tested |
| 14 | Actual ICARUS connectivity | Real local HTTP contract tests pass; live server/Tailscale requires user's environment |
| 15 | Supported telemetry | Implemented, host rendered, explicit unavailable handling; compare actual phone readings manually |
| 16 | Persistent settings | Store recreation, Phase 1 migration, and activity recreation pass |
| 17 | All animations disabled | Actual host UI navigation/gestures work with master off and Minimal |
| 18 | One UI fallback | Android Home settings shortcut/instructions preserved; actual selection remains physical |
| 19 | ICARUS unchanged | Android delivery is restricted to UMBRA; ICARUS source remains unchanged by this work |
| 20 | APK builds | Verified Gradle debug build and signature; metadata version 2.0 / code 2, min 29, target 35, ARM64 |

## Test environment and limits

Validation date: 2026-11-20 (America/Chicago); build logs/host-rendered clock use the host's UTC clock. Build host uses JDK 21, Gradle 8.9, AGP 8.7.3, Kotlin 2.0.21, Android Platform 35 / Build Tools 35.0.0. App ID is unchanged, and its signing certificate matches the Phase 1 debug APK for in-place updates.

A full emulator was attempted with installed emulator 37 and official stable 35.4.9. The environment has no `/dev/kvm`; both require a roughly 7.3 GB userdata allocation despite the configured smaller partition, exceeding available disk. No device UI tests ran in a full emulator or on physical Samsung hardware. A device-test APK, including a real Android Keystore isolation/encryption test, is compiled for later execution.

Robolectric native graphics under SDK 30 and SDK 34 runs the actual Activity/Compose screens, not a WebView or visual mock. It supplies host Android service implementations, so its unknown battery/storage readings and synthetic framework network defaults in previews are not phone telemetry. The suite explicitly models the normal install-time grant of the application's own signature broadcast permission and pumps the paused Android main looper for lifecycle/network assertions. Real local HTTP sockets are used by network tests. Tests verify visible HEAD requests, no extra request while stopped, and a fresh request after resume. Wallpaper PNG generation is decoded back and checked at 1440×3120. Host screenshots are labeled as such and are not physical-device screenshots.

Physical acceptance remains required for actual default-Home selection, protected/Samsung gestures, notification special access/counts, hardware Keystore, wallpaper application and native clock/Good Lock, calls/fingerprint/keyguard, real ICARUS/Tailscale commands, and power/frame profiling. Windows native test runtime is included by the dependency, but this session does not execute the batch script on Windows. No measured frame-rate, thermal-temperature, or battery-savings claims are made.

## Phase 3 recommendations

1. Finish the S24+ checklist in TESTING.md and profile actual frame timing, idle/background drain, large fonts, TalkBack, and One UI updates.
2. Add LauncherApps-based managed profiles/private space, Android widgets, folders, icon packs, user image import, and drag/drop layouts.
3. Add server capability/version negotiation and verified TV application IDs if the existing server later exposes them; preserve authenticated private connectivity.
4. Add device CI/emulator storage/KVM capacity and production release signing/distribution. Keep key material out of source.
5. Refine measured visual performance and richer startup/parallax behavior within battery/accessibility limits; avoid claiming a replacement for Samsung's secure system UI.

## Final executed results

```text
./gradlew --no-daemon -Pkotlin.compiler.execution.strategy=in-process :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
BUILD SUCCESSFUL
```

The in-process Kotlin switch addresses the cloud host compiler-daemon setup; it is not required by the application. Final suite: **24 passed, 0 failures, 0 errors, 0 skipped**. Lint: **0 errors, 10 dependency-update advisories** for deliberately pinned Android/test libraries. App APK and device-test APK both compile. The device-test APK was not executed on a full emulator/phone.

| Suite | Passing cases |
| --- | ---: |
| AnimationEngineTest | 2 |
| ConfigurationV2Test | 6 |
| DeckTest | 2 |
| IcarusClientTest | 4 |
| LauncherHostUiTest | 2 |
| PersistenceTest | 1 |
| PolicyTest | 5 |
| RefreshGateTest | 2 |

Signature: Android APK v2 verification passed, with the same certificate as the Phase 1 debug APK. Metadata: `com.umbra.mobile`, version `2.0`, code `2`, min API `29`, target `35`, native ARM64 support. Packaged HOME and optional notification-listener declarations were checked; there is no broad package query, wake-lock, global system-write, accessibility-service, or device-owner permission.

Output: `app/build/outputs/apk/debug/app-debug.apk`. GitHub downloads retain their established names under `UMBRA/downloads/`: APK, APK ZIP, source ZIP, coordinated PNG, and SHA256SUMS. Source packaging excludes local SDK paths, Gradle/build caches, signing keys, credentials, and generated app data. Host UI previews/evidence are included under `verification/phase2/` and explicitly labeled as host renders.

APK SHA-256: `a3a6c0bfd95fc823094c557f9e4e410acbff79a8ba8469c6440dc54a1c6a012d`
