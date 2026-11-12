# ICARUS Phase 4.2 Living Ship Lite

Continue your existing voyage. This package preserves the Phase 4.1 Windows simulation host, UMBRA browser/Android integration, pairing, Remote Deck layout, physical environments and saves. See PHASE42_CHANGELOG.md, PHASE42_VALIDATION.md and PHASE42_LIMITATIONS.md. Development build; not the finished ICARUS final edition.

## Install and back up on Windows

1. In the old running host use Settings > Backups > complete backup export. Keep the JSON and an untouched copy of your previous application folder, including private settings/pairings. Confirm the download exists. Do not place credentials in GitHub.
2. Verify the supplied SHA-256 with PowerShell `Get-FileHash .\ICARUS_Phase4_2_Living_Ship_Lite.zip -Algorithm SHA256`. Extract to a new folder beside the old installation. Do not overwrite the old folder or copy someone else's saves.
3. Close all old ICARUS host tabs and stop the previous server before starting the new one. Use the same Windows account, browser profile, host URL and port as before to retain browser storage. Do not clear browser site data.
4. Double-click Start_Remote_Deck.bat. Existing launcher installs the retained Python runtime requirements. Open the laptop's authoritative local host through the server's launch instructions. Preserve original private pairing/configuration files according to README_PHASE41.md; do not replace working TV/Android credentials with sample defaults.
5. The host automatically adds absent activity/social fields. It does not reset crew, memories, relationships, resources, missions, calendar or history. If using a new browser/origin, import the complete backup through Settings; review the restore confirmation. Save, reload and check the actual voyage before resuming.
6. Open UMBRA on the existing phone/tablet LAN or Tailscale URL and pair if required. Confirm matching authoritative time/episode and HOST CONNECTED or SIMULATION PAUSED. Remote URLs must not start another world. Retain the installed native APK. Rebuilding it awaits recovery of the original Android Studio project.

## Observe the crew

Bridge Mode remains the default. Cameras show actual procedural activity and source-labeled reconstructions; SOL reports only received evidence. Ordinary shifts, downtime and quiet days are valid. Optional Ctrl+Shift+F12 opens Creator Mode. Crew > Roster shows private routine/social histories and optional adult/relationship-interest preferences. These preferences do not themselves create consent, conversations or couples; genuine repeated interaction and mutual autonomous agreement remain necessary. Unset preferences remain unset in old saves.

No clock fix is included: the known 20× issue belongs to Phase 4.1.1. Do not change clocks to test this update on your only copy of a voyage.

## Roll back

Pause and export a complete current backup first. Close the new host/server, start the retained prior version at the original origin, and explicitly restore your untouched **pre-upgrade** complete backup. Do not assume an older build understands new social state. Restoring an older backup intentionally discards later progress; retain the new backup separately. Never run both versions as writers.

## Device checks

Follow PHASE41_DEVICE_TESTING.md for Windows/phone/tablet, authority, pause/reconnect, command deduplication, cameras, saved layout and TV controls. Verify task motion follows actual location and work; private thoughts/bonds must not appear in Bridge/UMBRA. Inspect a backed-up voyage across a real Monday and reload during active work. Physical-device, antivirus and native APK validation have not been performed in this Linux environment. Do not disable antivirus protection.
