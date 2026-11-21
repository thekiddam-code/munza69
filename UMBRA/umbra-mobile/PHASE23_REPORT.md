# UMBRA Mobile 2.3 implementation report

This increment extends the existing Phase 2.1 launcher at `5c08c9e` in `UMBRA/umbra-mobile/`; no separate 2.2 source was present on the selected GitHub branch. Package `com.umbra.mobile`, version **2.3 (4)**, Kotlin/Jetpack Compose, min SDK 29, target/compile SDK 35. The original terminal appearance, native launcher APIs, unified transitions, Enhanced detail, animation profiles, folders/pages, clocks/weather, widget host, pairing, native system shortcuts, and One UI recovery are retained.

## Implemented

- Shared collision-aware snap grids for Home items, module headers, Instant Buttons, native system controls, ICARUS shortcuts, Engineering actions, Lounge TV keys, Simulator/Rocket League controls, and Device Status. Stable IDs, responsive spans, contextual resize, explicit and adjacent-page movement, optional haptics, one-level arrangement Undo, and versioned persistence.
- Collapsed module headers can be held and dragged without expansion. Positions, expanded sizes, visibility, and collapsed states persist. Collapse is independent per module, with no forced accordion. Collapsed layout compacts to header rows without large empty panels.
- Command Center stores its last Compact/Expanded mode separately from module state. Native Wi-Fi/Bluetooth/sound/display/battery/media interfaces and UMBRA-only brightness controls remain truthful about Android restrictions.
- Available grid positions illuminate subtly in amber during drag/resize. Drag guides clear on release/cancel; ending editing clears guides and arrangement controls immediately. These are functional guides and work with motion on or off.
- Arrangement controls are contextual. The permanent Home Folder/Widget/Pages toolbar and per-widget Widget Options rows are replaced with long-press editing. The Arrange toolbar is absent during normal use; accessible long-click/reordering actions remain available.
- A dedicated native Instant Buttons page restores create/edit/delete/rename/icon/output configuration, explicit testing, save/load, widget selection, wrapping/scrolling, search, Select all, and Deselect all. Compact widgets no longer truncate to six controls. Existing catalog names, selections, and custom labels migrate. Local overrides preserve placement and do not overwrite PC mappings.
- Full typed output configuration uses the inspected authenticated server contracts. Unsupported generic press/release/script protocols are identified, never fabricated. Repeated execution is gated and responses/queued acknowledgments are distinguished from verified downstream execution.
- Settings uses a compact title and a scroll-content footer with the UMBRA icon, installed package version, and debug/release information. Independent status-panel choices cover Home/information/ICARUS sections, Applications, Settings, and Command Center; they reclaim space without changing immersive preferences or protected Android notifications.

See [LAYOUT_MIGRATION.md](LAYOUT_MIGRATION.md) for storage, migration, layout limits, and recovery; [ICARUS_OUTPUTS.md](ICARUS_OUTPUTS.md) for the exact native editor/server contract. Existing schema 2/3 imports and Phase 1 migration remain supported. Local widget IDs are retained; portable widget imports still require Android rebinding.

## Verification

The untouched baseline passed before changes (`verification/phase23/baseline.log`). Grid/editor integration compiled incrementally. Intermediate failed checks are retained separately from final results. The environment lacked the JDK image tool needed by newly generated Java; build information instead uses Android's installed package metadata, retaining the Kotlin-only build pipeline.

The final command is:

```sh
./gradlew --no-daemon -Pkotlin.compiler.execution.strategy=in-process :app:testDebugUnitTest :app:lintDebug :app:assembleDebug :app:assembleDebugAndroidTest
```

**Final result: BUILD SUCCESSFUL in 2m 32s; all 68 tests passed with zero failures, errors, or skips. Android lint reported zero errors and 13 warnings (11 dependency-update notices and two notices about deliberately durable pending-widget SharedPreferences commits). The app and device-test APKs both assembled; APK signature verification passed and the certificate matches the published Phase 2.1 build.**

Final executed counts (`RESULTS.txt`), the successful command log (`final-checks.log`), JUnit/lint XML, manifest/signature metadata, and fresh host renders are recorded under `verification/phase23/`. Host tests run actual Activity/Compose UI and native graphics on Android 11/14 (SDK 30/34), with real local sockets for HTTP contracts. Compiling a device-test APK is not executing it. Windows batch execution and physical-device profiling are not claimed.

## Limits and physical acceptance

- Physical Galaxy S24+/One UI launcher selection, gesture behavior, native widget-provider compatibility/configuration, notification grants, real Keystore, actual TV/game execution, and live Tailscale remain phone/PC checks. No exact Samsung transition parity or measured frame/battery performance is asserted.
- Standard Android third-party widget clicks and provider binding/configuration remain native. Providers may handle their own long-press; accessible host editing is also available. Proprietary Samsung-only, work-profile/private-space, and oversized providers remain outside verified support.
- The grid is an adaptive ordered integer-cell workspace, not a pixel editor. Larger spans may need internal scrolling; clipped cells cannot paint over neighbors. Data/file limits are documented. Button files save local output definitions; full Settings exports additionally preserve grids and selections.
- Adjacent-page dragging and the contextual page chooser preserve stable item IDs. Native widget removal releases its binding; an imported/restored reference can require rebinding. Undo is one-level and process-local, not an indefinite history or substitute for export backups.
- Compact mode prioritizes dense module headers/system controls while retaining the user's individual flags. Hiding modules can be undone or restored through contextual Configure / advanced Settings. Functional clocks/alerts remain independent of optional motion.
- Server-catalog references depend on synchronization; missing selections are retained/reported. Local command definitions are stored on the phone, not silently written to the shared PC configuration. HTTP acknowledgments cannot prove downstream execution, and cancelled requests cannot undo commands already delivered.

Next priorities: perform the S24+ acceptance checklist, profile a large catalog and several real widget providers with Android Studio/Perfetto, then refine device-specific input/resize behavior. No server or protected-system modifications are necessary for this increment.
