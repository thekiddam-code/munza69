# ICARUS / UMBRA Phase 4.2A — Observation Protocol

Use the existing Windows host and existing voyage. This release adds original pixel-art surveillance, four rotating previews, actual visible conversation-seeking phases, a room-instrumentation schematic, persistent lighting controls and accessible bridge/dashboard repairs. It does not create a separate world on the phone.

## Safe update on Windows

1. Export a **complete** backup from the old running host and confirm the JSON download exists. Retain the entire old folder and private pairing/config files.
2. Verify the supplied ZIP SHA-256 with PowerShell `Get-FileHash .\ICARUS_Phase4_2A_Observation_Protocol_Lite.zip -Algorithm SHA256`. Extract beside the old installation, not over its only copy.
3. Close all old simulation tabs and stop the previous server. Keep the same Windows/browser profile, host URL and port to retain browser storage. Do not clear site data.
4. Start `Start_Remote_Deck.bat` using the existing procedure. Retained Python requirements and host launcher are unchanged. Retain your private pairing/TV/game settings; do not publish them.
5. Open the authoritative laptop host. Existing saves gain missing fields without resetting crew, history, relationships, missions, research or calendar. If using a new browser/origin, import the complete backup through Settings > Data. Save/reload and check identities before resuming.
6. Open the existing UMBRA phone/tablet URL and pair if necessary. Confirm HOST CONNECTED or SIMULATION PAUSED and matching ship time. Remote pages must not open a second simulation. Retain installed Android apps. The separately preserved native S24+ launcher can open your existing configured Remote Deck URL; it was not rebuilt in this batch.

## Observe and operate

Bridge > Watch retains the primary camera. The original pixel renderer is default; classic schematic mode retains the previous camera-sector/style/replay behavior. Four previews rotate every 12 seconds; pause, step banks or pin individual previews. Select a preview to promote it; primary selection stays fixed until you change it. Private quarters/executive/hygiene rooms never appear in ordinary camera selection. Camera images are procedural simulation views, not recorded video.

Ship > Overview adds an instrumentation schematic. Select a room to inspect real atmosphere/equipment/access readings, control lighting or focus an available camera. Biological sensing and unsupported controls are labeled unavailable. No sensor can identify hidden organisms merely from internal simulation data.

Open Crew Location's ⋯ menus for available cameras or authorized records. Bridge profiles show received evidence, not private thoughts. Ctrl+Shift+F12 retains Creator Mode for private/debug inspection. Pause/Resume and ship clock are accessible in normal Bridge Mode; test speeds remain Creator-only. The 20× issue is not changed.

Click or keyboard-activate Home widget headers to collapse/expand. Focus, layout customization, presets and separate mobile layout remain. Full/reduced/minimal motion settings still apply.

## Backup and rollback

Export another complete backup before rollback. Close the new host/server, launch the untouched prior folder at the same origin and explicitly restore the **pre-upgrade** complete JSON. Keep newer progress separately; an older build may ignore new observation fields. Never run both versions as writers.

## Check the installed devices

Use PHASE41_DEVICE_TESTING.md plus the A–H cases/manual watch in PHASE42A_VALIDATION.md. Check phone/laptop matching ticks, stale/reconnect behavior, commands affecting the correct host once, usable menus/scrolling, private-room exclusion, preview pinning and source labels. Physical Windows/Android/TV/Tailscale/antivirus tests were not performed here. Do not disable antivirus.

Read PHASE42A_ARCHITECTURE.md and PHASE42A_LIMITATIONS.md for the bounded implementation and unfinished art/crowd/sensor/device work. Machine-readable reports and isolated test-world evidence live in the repository/separate verification archive, not this Lite runtime ZIP.
