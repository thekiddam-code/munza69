# ICARUS / UMBRA Phase 4A — browser Remote Deck and Windows server

This update extends the existing UMBRA browser app. UMBRA is the Weyland-Yutani vessel OS; SOL is its source-grounded ICARUS companion module. ICARUS's existing simulation, saves, crew/history and calendar remain. **The installed Android APK is not removed/replaced. Its native rebuild is pending recovery of the original Android Studio project.** No replacement APK is included.

## Install without losing the voyage or pairing

1. Export a complete voyage backup in the existing ICARUS build. Keep the old folder and backup. Close all old simulation tabs and stop the old Windows server.
2. Extract this ZIP to a new folder. Before starting it, copy your existing `config.json`, `paired_devices.json` and `samsung_tv.json`, **if present**, from the old server folder into this new server folder. Keep these files local/private; do not upload them to GitHub. They preserve configured game controls, paired-device token hashes and the Samsung address/approval token. Do not copy old web/runtime code over this build.
3. Run `Start_Remote_Deck.bat`. A working installation needs no new pip dependency. A new PC needs Python and `py -m pip install -r requirements.txt`.
4. Use the same browser/profile/PC address/port as before. The voyage stays in its existing browser save namespace. Do not clear browser data or click New Voyage for recovery. Enter the current startup ICARUS host key on the authoritative PC if the old key expired after server restart.
5. Existing paired clients/installed APK keep their original URLs and endpoints. Whether the APK displays these new web screens automatically depends on whether it loads the PC page or bundles its own assets; that requires recovering its source to establish. Server API compatibility is tested; native binary/device behavior is not claimed tested.

## Browser features

Engineering, Lounge, Simulator games, Armory and existing settings/actions remain. UMBRA has a cool navy/slate/violet/silver WY interface, local SVG icons, distinct phone/tablet layouts and a tablet right-hand remote. Lounge offers existing protocol keys, bounded repeat and local editable profiles for tablet-landscape and phone-portrait. Edit/drag or use labeled row/column/size/command controls; Save/Cancel/Undo/Reset/Lock; restore Factory at any time. Profiles never change the voyage. Orientation retains unfinished drafts separately.

The **UMBRA-managed sleep timer** uses the existing TV Power Off key after 15/30/60/90/120 real minutes. It is not a native TV timer. The Windows server and TV connection must remain available. Server restart cancels it; cancellation, target change and owner unpair invalidate old callbacks. A failed send is not retried later; a callback over 60 seconds late after server suspension expires without a surprise shutdown. A socket send is not a confirmed TV execution. The host PC is never powered off by this timer.

SOL shows real received state/events and existing covered ship cameras; field/private/unknown locations are not invented. Follow Crew uses a covering camera only, otherwise explicit unknown/no-camera. Standard and 51st State reuse the same original ICARUS sprite renderer and real state; these are schematic projections, **not video recordings**. Freshness and source IDs remain visible. Native video/actual Kill Cam capture remains deferred.

Settings → Appearance has independent **Corporate Anomalies** and **Arcade Kill Cam**, both OFF by default. Manual archive has six original bundled fictional pixel GIFs and static reduced-motion previews. Loaded clients cache the small collection for disconnected playback; first page load/reload still needs the existing PC web server (no offline installer/service worker is claimed). Rare automatic decoration is confined to idle UMBRA Bridge, guarded against editing, TV timers, crew follow and genuine alerts. It never creates ICARUS events or sends game/TV/host commands. No audio is generated.

## Backup / rollback / verification

Keep the untouched previous folder and pre-upgrade complete backup. To roll back, close this server/tabs, restart the old folder at the same origin/profile and restore the pre-upgrade backup if needed. Reuse your private configuration/pairing files locally. Do not delete browser databases. New per-client UMBRA profiles are simply ignored by older web code.

Compare `Get-FileHash .\ICARUS_SOL_Command_Interface_Phase4_Lite.zip -Algorithm SHA256` with the supplied `.sha256`. BUILD_MANIFEST.json identifies every retained committed source file. Lite excludes tests/reports/development tools; all runtime modules/assets, including `tv_service.py`, are retained. Do not disable antivirus. See PHASE4A_VALIDATION.md, SECURITY_PHASE4A.md, UMBRA_TV_CAPABILITIES.md and NATIVE_ANDROID_RECOVERY.md for actual tests and remaining gates.
