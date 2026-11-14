# ICARUS Phase 4.6 Lite — run, preserve, observe, recover

1. In your current ICARUS host, export a **complete backup**. Keep the old folder and backup for rollback. Close all old simulation tabs and stop the old server.
2. Extract the new Lite ZIP to a separate persistent Windows folder. Do not overwrite your only working installation. Python and the existing runtime dependencies are still required. Your working Phase4.5 environment should already contain them; if not, open a terminal in this folder and run `py -m pip install -r requirements.txt` before launching. The batch file itself does not install packages.
3. With both servers stopped, optionally copy your own config.json, paired_devices.json and samsung_tv.json from the old installation to preserve host/paired settings. Never copy generated test configurations or other people's keys. Otherwise re-pair the remote.
4. Run Start_Remote_Deck.bat. Use the **same browser profile, hostname and port** as before: browser storage is origin-specific. A missing voyage at a different origin is not a reason to start a replacement. Use your complete backup import if migration between origins is necessary.
5. The boot screen now stays visible throughout restoration and after readiness. Exclusive writer ownership and Bridge authorization have separate indicators. Key text remains available. Wait for actual readiness, then press **ENTER ICARUS**. A second owner stays read-only; close the old host rather than bypassing the lock. Keep Windows awake while it hosts the continuous simulation.
6. Open **Missions → Active → 8847-A / Drone Reconnaissance**. Observe autonomy or request assembly. Qualified engineers need real C04 components and must reach C01. A chassis starts empty and charges using actual ship energy. Maintenance/safety may postpone it. No free drone appears on upgrade.
7. Launch toward observed frontier or a received destination, inspect received map/readings, select the drone camera, or queue recall. Recall needs a working channel; onboard reserve return does not. Unknown sectors stay unknown until physical survey and receipt. A disconnected device shows stale last status, not its hidden true position.
8. The Bridge surveillance selector includes drone feeds alongside existing cameras. Received event playback labels captured procedural frames separately from later reconstruction. No physical video is claimed. Full captured records live in your host save; bandwidth-limited remote previews can use labeled source-state reconstruction.
9. Crew expeditions can physically recover a stationary co-located stranded drone when carrying space allows. It must actually return to a powered dock to transfer local evidence. Mid-segment and exterior-transit salvage remain limited; no teleport or automatic rescue.

## Save migration and rollback

The existing voyage namespace and schema1 durable envelope remain. The optional drone domain initializes empty, with existing crew/maps/history/military state intact. New work, physical segments, charge/condition, onboard/received knowledge and event records persist in normal saves and complete backups. Keep the same origin and only one authoritative host.

For rollback, stop the new host/tabs, start the retained old folder at the original origin, and restore the **pre-upgrade complete backup**. Do not ask an old version to advance a new drone save. Export a post-upgrade backup as well before experimenting. Neither the Lite ZIP nor automated fixtures contains your personal voyage.

## Testing your devices

On the laptop, verify boot stays ready while unattended, finish typing the key if needed, explicitly enter, check crew/history/calendar, let an engineer build/charge/launch, watch a connected survey and physical return, save/restart and confirm received findings remain. Disconnect/reconnect a phone: it should retain labeled stale data and reconnect to the same tick/world. A phone opening ICARUS remains a terminal, never a second world. Test optional controls against the authoritative host. Do not disable antivirus protection.

Physical Windows/Samsung/native/TV/LAN/Tailscale validation is pending. Existing installed Android and TV features are preserved; rebuilding the native APK awaits original source recovery. See PHASE46_VALIDATION.md, PHASE46_ARCHITECTURE.md, PHASE46_LIMITATIONS.md and SECURITY_PHASE46.md for evidence and boundaries.
