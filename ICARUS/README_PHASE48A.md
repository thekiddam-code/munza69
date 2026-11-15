# UMBRA Phase 4.8A — Windows Command & Control

This is the Engineering/Hotkeys stage of PHASE48_IMPLEMENTATION_BRIEF.md, based on the verified Phase 4.7C source `20a0a25`. The user confirmed the preceding differently named Field Deployment ZIP was their installed baseline; no additional B source is required to establish that lineage. Previously documented unfinished camp services remain unfinished, rather than being removed by this update.

## Update without losing the voyage

1. Export a complete ICARUS backup and retain your current installation folder. Keep private config.json, paired_devices.json and samsung_tv.json if present. Never publish those files or your backup.
2. Close authoritative tabs and stop the old server. Extract the Lite ZIP to a separate folder. Copy your private companion configuration into it while the server is stopped. Do not overwrite your only old copy.
3. Keep the same browser profile, hostname and port as before: IndexedDB and UI settings are origin-bound. Do not clear browser storage or delete writer locks. No world migration/reset is required by 4.8A.
4. On the Windows PC run `Start_Remote_Deck.bat` as before. Existing requirements.txt is unchanged. If dependencies are missing, install them with `py -m pip install -r requirements.txt` in that folder. No administrator privileges or execution-policy changes are needed for the new modules.
5. Refresh UMBRA with Ctrl+F5; reconnect the Samsung tablet/phone using the existing paired URL, LAN or Tailscale. The native APK is retained; rebuilding it still awaits original Android Studio source recovery.
6. Engineering now contains read-only Windows measurements. Armory / Hotkeys contains installed applications, Windows action categories and every existing config.json macro. ICARUS/SOL retains its original dashboard and receive-only remote architecture.

For rollback, export a post-update voyage backup, stop this server/close its tabs, and run the retained previous folder using the same origin. Phase 4.8A does not change ICARUS save fields. Keep the previous version's media compatibility rules: versions older than 4.7C may not accept its optional motion data. Preserve both backups.

## Engineering

Measurements are sampled in a background worker every three seconds and cached for all clients; slow optional vendor queries run at most every ten seconds. The UI polls only while Engineering is visible. CPU/RAM history is bounded to 60 host samples in memory; its display preference persists separately from the voyage. GPU temperatures/utilization/VRAM/clocks/power use an already-installed NVIDIA utility when available. Read-only Windows display registry entries provide model names otherwise. Unsupported CPU temperatures and vendor sensors say Unavailable. No driver installation is performed.

Storage, network rates, battery, uptime, power scheme and top-20 process CPU/RAM are provided where supported by psutil/Windows. First utilization/rate samples warm up rather than inventing measurements. Network connectivity means active link/assigned IPv4, not verified internet access. Disk activity is aggregate, not falsely attributed to individual volumes. The active power scheme is not necessarily Windows' separate power-mode overlay; that overlay is not measured. History/process data are not written to the voyage or exposed without pairing. No fan/thermal/power controls are added.

## Windows commands and installed apps

25 predefined Windows actions cover System, Windows, Utilities and Media. Tooltips, accessible names and hold descriptions explain the exact combination and focus/policy restrictions. Lock PC asks for confirmation. Existing user macros remain unchanged below the new controls.

Rocket League, Fortnite, Chrome, Bambu Studio and Minecraft are discovered from local Start menu/desktop shortcuts or registered packaged Start applications. Refresh installed applications rescans after installation/moves. Only the five fixed IDs can launch; the remote cannot provide a path or arguments. Trusted local shortcuts preserve their installed launch arguments. Steam/Epic .url launchers use a restricted protocol grammar. Network paths, script targets and arbitrary URLs are rejected. An installed app without a discoverable supported shortcut is explicitly not discovered; create its normal local Start-menu shortcut and rescan. There is no arbitrary remote file picker.

Icons come from the installed Windows Shell, not an online logo catalogue. Available icons render without labels/background tiles; missing icon extraction falls back to a clearly named text control, never an invented app logo. Windows Shell owns application startup/existing-instance behavior. A requested launch is not falsely reported as a verified running game: applications can focus an existing instance, start another window, or reject activation. Windows protected desktops/UAC cannot be controlled through these shortcuts.

## Windows hardware verification still required

Run the checklist in PHASE48A_VALIDATION.md on the actual Alienware m15 R7. Linux browser/service tests do not certify Windows sensor values, Shell icons, application activation, Samsung hardware, Tailscale routing or antivirus scans. Optional unsupported devices fail gracefully.

## Next stages

4.8B local sound library/import/playback/private-preview and 4.8C Sonar routing/calibration/mixing remain **not started** in this batch. No sound is injected, no microphone is opened, and no audio device/default/Sonar setting is changed. Do not infer audio fail-safe validation from this read-only monitoring stage. A safe independent voice path and separate private/public outputs are mandatory before implementing injection.
