# ICARUS Phase 4.7 — Development Checkpoint

**Phase 4.7 is not complete. This is not the finished Forward Operations release.**

Implemented: original FOC-01 parked aboard C03 with a scaled exterior camera and physical inspection; all retained local drone recording IDs/playback controls; source-limited surveillance filters; current-state animated drone rendering; ship-dock escort replacement logic; cooperative catch-up yielding. Vehicle transport and the persistent field camp are not implemented. Camp charging, camp rotations, ATVs and camp medical/logistical operation therefore remain unavailable.

See PHASE47_VALIDATION.md for the acceptance table, executed results and unresolved diagnostic findings. Do not infer full phase readiness from the passing selected suites.

## Run or review the checkpoint

Keep the Phase4.6 Startup Size Hotfix as the stable rollback build. Export and retain a complete backup before trying a development checkpoint. Stop the old server and close its authoritative host tabs before starting the new folder; do not bypass writer locks or run competing hosts for the same voyage.

Extract the checkpoint to a separate folder. Keep the same Python environment, browser profile, hostname and port to see the existing voyage. Run `Start_Remote_Deck.bat`. Refresh changed assets with Ctrl+F5 when needed. Do not clear site data/IndexedDB, select New Voyage, or delete writer records. The boot screen still waits for actual readiness and explicit ENTER. Optional private pairing/TV configuration transfer follows README_PHASE46.md with both servers stopped; no personal configuration is supplied here.

Use the existing Surveillance camera selector to choose C03 for the cargo establishing view. Missions → Active contains UMBRA // SURVEILLANCE, the FOC inspection request, received location filters, active drone view and archive. A queued inspection needs a physically available engineer and resumed simulation. The FOC status explicitly reports that transport/camp deployment are unavailable; no button pretends to deploy them.

All retained received recordings are listed locally, including Records1–12 if they exist in the host archive. Select a record, play/pause/replay its actual retained sequence. Captured frames and later source-state reconstructions stay separately labeled. Older full remote playback is not implemented: the paired terminal receives compact archive metadata and a bounded latest-record preview. Missing historical pixels are not invented.

Escort rotations need two actually assembled, charged, serviceable drones and a safe observed route to a currently reported expedition. Existing assembly, engineering and resource gates remain. A coverage gap is a valid outcome. These rotations use the ship dock; there is no forward camp dock yet.

## Saves and rollback

Legacy saves gain one optional original-equipment registration. Crew, history, maps, recordings, research, ship systems and calendar are retained. FOC inventory registration is an original-equipment asset, not a gift into ship resource stores. No new namespace or destructive schema migration is used.

To roll back, stop this server and close its tabs, reopen the retained stable Phase4.6 build at the same origin/profile, and restore the **pre-checkpoint complete backup** if necessary. Older builds cannot operate the new inspection/escort domain. Do not use clearing browser data as a rollback mechanism.

The supplied private voyage backup is neither modified nor included in this distribution. Native Android functionality is retained; APK rebuilding is still pending original Android Studio source recovery. Physical Windows/Samsung Android/TV/Tailscale and antivirus tests were unavailable. Screenshots in the source repository are actual running renderers over explicit technical fixtures, not footage from the user's voyage.
