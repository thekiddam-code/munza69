# ICARUS 4.6 — Startup Size Hotfix

A targeted correction to the Phase 4.6 Boot Hotfix Lite build. No new gameplay, save reset, schema change, or clock change.

## Install on the existing Windows host

1. Keep your existing complete backup and the old application folder. Stop its server and close its ICARUS tabs.
2. Extract `ICARUS_Phase4_6_Startup_Size_Hotfix_Lite.zip` into a **separate folder**. Keep the same Windows Python environment, browser profile, hostname and port used by your voyage. Saves belong to that browser origin/profile, not to the application folder. Changing origin/profile can make a different empty installation appear; it does not migrate your voyage.
3. Transfer optional private pairing/TV configuration only as described in `README_PHASE46.md`, with both servers stopped. This ZIP contains no personal save, authorization key or pairing secrets.
4. Run `Start_Remote_Deck.bat`. Use the existing local host URL; refresh updated assets with Ctrl+F5 if needed. **Do not clear site data or IndexedDB. Do not select New Voyage.** Your existing world should restore automatically.
5. The boot screen stays open. WAITING FOR WRITER means existing storage/server ownership protections are still active; let them resolve. Keep the authorization field available and use the normal key verification if needed. Do not alter lock records or bypass ownership.
6. Wait for ICARUS ONLINE and select **ENTER ICARUS** yourself. Confirm your original crew, episode and history. Open the paired UMBRA remote: it should show the same host world. A limited remote history preview is labeled; the complete history and recordings remain on the host.
7. To inspect a received drone recording locally, open Exploration's recording selector. Captured frames are loaded for playback on selection. State-only frames remain explicitly labeled reconstructions.

If an actual error occurs, retain its message. Request-size errors now identify the endpoint and byte limit. A telemetry-preview error no longer falsely declares writer ownership lost. Authentication errors, competing writers and genuinely lost ownership remain protected. Retry initialization after resolving an actual startup problem; this reloads the existing world.

## Backup and rollback

Export a full backup before upgrading and after confirming the voyage. The hotfix never converts, reduces or clears your save. If you need to restore manually, use the existing full-backup import UI with your retained backup; do not overwrite an unrelated voyage unintentionally.

For rollback, stop the hotfix server, close its tabs, reopen the retained Boot Hotfix folder using the same origin/profile, and restore your retained pre-upgrade backup only if needed. The original download is unchanged. Native Android functionality remains; original Android Studio source recovery and physical-device validation remain separate work.

See `STARTUP_SIZE_REPORT.md` for the reproduced cause, precise verification scope and remaining limits.
