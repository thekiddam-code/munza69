# ICARUS — Phase 3 Cinematic Living World Lite

A tested development increment of the autonomous science-fiction anthology, not final-release certification. Individual routines and real conversations, optional bridge spectator direction, source-backed SOL watch notes and skippable Sunday timelines refine the existing living world. Quiet weeks remain valid. No drama, discovery, lethal encounter or Lazarus success is guaranteed. See PHASE3_LIMITATIONS.md and PHASE3_VALIDATION.md for evidence and unfinished work.

## Backup and install over a working Phase 1/2 Lite

1. In the working voyage use **Export complete backup**. Confirm the JSON exists in Downloads and keep it with an untouched copy of the old installation. Never start a new voyage to recover an old one.
2. Stop the old PC server. Extract the whole Phase 3 Lite ZIP to a **separate folder**. Keep `web`, `server.py`, `config.json`, requirements and launcher together. Do not copy selected JavaScript files over an older build.
3. Copy your customized `config.json` and, if present, `paired_devices.json` and `samsung_tv.json` from the old folder. These contain your local pairing/configuration; generated credentials are not included in the ZIP.
4. Run `Start_Remote_Deck.bat`. Use the **same PC browser profile, hostname and port 8765** as before. Folder changes do not alter browser origin; changing localhost to an IP or a different browser profile does. Persistent core save format/namespace is unchanged and migration adds empty new presentation/routine groups, without replacing the crew or world history.
5. If the voyage is not visible, reopen the original browser/origin or import the complete backup through Settings. Check crew, date, missions and history before continuing. Reconnect Android with the host's LAN URL and existing pairing or the normal PIN. The PC remains authoritative; the phone/tablet is a thin client.

For a working Phase 1/2 installation Python dependencies and launcher are unchanged. A new installation requires Python and `py -m pip install -r requirements.txt`. All JavaScript dependencies and licenses are included. There is no new runtime download, executable wrapper, video encoder or AI service. Never disable antivirus to run this build.

## Observing the new features

- Operations camera: optional **AUTO/MANUAL** spectator direction and Next shot. Manual camera and captain interventions remain available. Live state projections, telemetry and historical reconstruction have explicit labels. Camera selection and playback do not drive simulation decisions.
- Crew inspector: bounded routine choices and memories explain actual individual activity. Conversations need physical co-location and availability; support is personal, reports preserve source/confidence. No random conflict or romance schedules.
- Expand **SOL · sourced watch notes** near the camera for recent source/confidence-backed commentary. Silence can mean there is no new eligible shared record.
- Expand **Sunday cinematic archive** to select an episode, Load, Play/pause, Previous or Skip. Closing the panel pauses playback, not ship operations. Week archives are created at real Monday boundaries. Actual retained snapshots say **RECORDED STATE SNAPSHOT — schematic projection, not video**. Other cards say **RECONSTRUCTION**. Quiet weeks have shorter films. This is an in-app timeline, not an exported video.
- Reduced motion, original art modes, optional captain control, source perspectives, calendar and Remote Deck controls remain. The normal 4×, nine synchronized holiday 1×, real Monday–Sunday episodes and six-hour offline catch-up policy are unchanged.

## Rollback

Export a fresh complete backup before rollback and preserve it separately. Stop Phase 3, restart your untouched old folder at the same browser origin/profile/port, then import the **pre-upgrade backup**. Do not assume an older runtime understands a newer save. This intentionally restores the old checkpoint; later Phase 3 events are not merged backward. Keep both backups until verified. No installer overwrites browser storage automatically.

## Verify the download

Compare ZIP SHA-256 with its supplied `.sha256` file; on Windows use `Get-FileHash .\ICARUS_Cinematic_Living_World_Phase3_Lite.zip -Algorithm SHA256`. `BUILD_MANIFEST.json` inside lists the Git source commit and every retained file hash. Lite excludes tests/reports/development tools/packaging scripts but retains all runtime assets and license headers. Full engineering evidence is in this branch under `ICARUS/reports/phase3` and the accompanying evidence archive. Security behavior and unavailable native-device/antivirus checks are documented in SECURITY_PHASE3.md.
