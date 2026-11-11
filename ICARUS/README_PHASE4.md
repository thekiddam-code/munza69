# ICARUS — SOL Command Interface / Phase 4 Lite

ICARUS is an autonomous science-fiction anthology simulation. This build reorganizes the existing interface; it does not reset the voyage, create new worlds or replace the autonomous controllers. Full final release/native-device acceptance remains open.

## Install and keep your voyage

1. In the existing build, export a complete backup; keep the old folder and backup outside browser storage. Do not clear browser data.
2. Close every existing ICARUS simulation tab and stop the old server. Older builds may not honor writer ownership.
3. Extract this ZIP into a new folder. Run `Start_Remote_Deck.bat` on Windows. An existing working Lite installation needs no new Python dependency; a new PC needs Python and `py -m pip install -r requirements.txt`.
4. Use the same browser, profile, host address and port as before. Existing core save namespace and IndexedDB schema remain unchanged. Check the crew and voyage before proceeding. Do not use New Voyage to recover an old save.
5. Android stays the paired thin client. Open the existing PC LAN URL and use the existing pairing workflow. Bridge-key configuration is in Settings → Data. Keep one authoritative PC simulation tab.

## Find your controls

Home remains the default personal dashboard. Customize widgets preserves the existing device layout/order/sizes and live interactions. Bridge contains cameras, actual decisions and SOL directives. Ship has the cutaway, systems and a link to the single live camera. Crew contains roster, activities, health and social views. Missions has active objectives, local field consoles and finite logistics. Research contains projects, individual acquired evidence and LAZARUS. Chronicles contains the actual journal, Sunday players and archives. Settings separates preferences, data/pairing, testing and creator tools.

You operate the directed layer of the same SOL intelligence. NPC captain roles and old source authorship are preserved. The control bar identifies autonomy/directive scope, explains current route decisions and links to incidents. Release restores autonomous choices; it cannot teleport crew or cancel physical travel. Arrow keys navigate focused main/section buttons; browser Back/Forward retains routes. Guided help can be reopened in Settings → General. Reduced motion and device preferences remain available.

## Development testing

Settings → Testing offers normal automatic 4× / synchronized holiday 1× and explicitly warned TEST 1×/5×/20×. These change the **current voyage**, including resource consumption, injuries and outcomes. Every simulated minute runs the existing controllers. Real local Monday–Sunday episodes do not accelerate, and never reset the world automatically.

Pause/resume and a persistent TEST indicator are visible. Return to normal restores holiday-aware pacing. Reload defaults to normal; test acceleration is session-only. New voyage / reset experiment requires deliberate confirmation and starts a new world. Backups remain functional; elaborate backup/migration polish is deferred to pre-release stabilization.

## Rollback and verification

Keep the original folder and pre-upgrade backup. Stop this server/tabs, restart the untouched previous folder using the original browser origin/profile, and restore that pre-upgrade complete backup if required. This returns to that checkpoint; it does not merge later events backward. Never delete the browser database as an upgrade step.

Compare `Get-FileHash .\ICARUS_SOL_Command_Interface_Phase4_Lite.zip -Algorithm SHA256` with the supplied checksum. BUILD_MANIFEST.json lists the exact source commit and every retained file hash. Lite excludes development tools/tests/reports. Host input/TV capabilities are the existing Remote Deck implementation; do not disable antivirus. See PHASE4_UI_VALIDATION.md and PHASE4_UI_LIMITATIONS.md for actual verification limits.
