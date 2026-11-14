# ICARUS / UMBRA — Phase 4.5 Visual Overhaul & System Boot

This build improves the **running detailed surveillance cameras** with distinctive ship interiors, taller articulated crew, coherent wheelchairs, actual lounge/table/bunk approaches and a real-event startup display. It preserves your voyage and Phase4.3/4.4 operations. A03 stays Observation Lounge; the gym is deferred as you requested. A09 becomes Crew Lounge.

## Install without losing your voyage

1. In the working installation pause and export a complete backup **including history**. Keep the old folder and backup untouched, outside the new folder.
2. Close every old host tab and stop the old server. Do not run competing hosts; old versions may not share all current ownership protections.
3. Extract the Lite ZIP into a new folder. Keep all root runtime files and the complete `web` folder together.
4. On Windows run `Start_Remote_Deck.bat`. Existing Python3.11+ and requirements apply; if necessary use `py -m pip install -r requirements.txt` in that folder. Original pairing/network/TV/Tailscale setup remains in README_PHASE41.md.
   To retain pairing/settings, with both servers stopped copy your own `config.json`, `paired_devices.json` and `samsung_tv.json` (if present) from the old folder into the new one. Keep backups and do not publish private TV/pairing files. Otherwise pair the phone again using the new PIN. The host key changes on server restart; localhost bootstrap verifies the current key automatically.
5. Use the same laptop browser/profile/origin as your current voyage. If a new world appears at another address, stop and import your own complete backup through the existing interface; do not replace the old backup with that new world.
6. Boot shows actual persistence, connection, world/kernel, ship systems, authorization and camera setup. Healthy local bootstrap verifies automatically. The optional recovery field accepts the **Windows host key**, not the phone pairing PIN. A correct key still cannot bypass exclusive storage/server ownership.
7. Check crew names/date/history/resources/active missions before resuming. Migration adds persistent public appearance and optional ordinary room-interaction progress, without changing the save envelope or resetting crew/world. Existing expeditions and partial gravity/repair work remain.
8. Export a separately named post-upgrade backup after checking continuity. Keep the original untouched for rollback.
9. Open paired UMBRA on phone/tablet; it remains a received-data terminal. Never open a second host on the phone. The installed native app is not replaced; Tab S5e source recovery/build remains pending.

## See the new visuals

Choose **Operations → Watch** and the detailed pixel camera. If you previously selected the optional classic schematic, use **Use detailed pixel camera**. Visit A09 Crew Lounge, A08 Medical, B01/B05 Science, A01 Bridge, C07/C08 Engineering/Reactor, C03 Cargo, B07 Security and corridor/lift cameras. A03 remains Observation Lounge. Room identifiers and coverage are unchanged.

The new artwork is shared by primary/four previews, UMBRA and field camera characters. Quarters stay private in ordinary security; their room artwork is used only by existing authorized local restricted sensors. Do not alter privacy settings just to see a visual demonstration.

Autonomous crew approach ordinary lounge seating/dining/bunks when the task and readiness permit, then seat/work/rise over actual simulation minutes. Watching cannot cause an activity. Wheelchairs use accessible front space, never standing legs. Critical work keeps existing physical station/priority controls. No full collision simulator or gym/fitness benefit is claimed.

Boot automatically yields to the bridge when required startup is ready; authorization/read-only is separate. Reopen **ICARUS / System Status** in the header for actual stage diagnostics. During a failure use Retry after checking the original server/address/owner, or Observe read-only where available. Temporary disconnection does not reset saves. Do not treat an authentication acknowledgment as proof that another active owner has been displaced.

After upgrading, hard-refresh once if a browser shows old artwork; the new server revalidates static assets and the pixel import is versioned. Check the detailed/classic toggle and your actual URL before assuming a separate renderer. No service worker is installed.

## Manual Windows / phone / tablet checks

- Confirm identical existing crew, current tick/date, resources, active expedition/repair and received camera ID on laptop and UMBRA.
- Compare lounge, engineering, medical and corridors at normal zoom; check actual standing/seated/wheelchair silhouettes. Keep private-room coverage restrictions.
- Follow a crew member through room/corridor/lift and a genuine field mission. Check pause/reduced motion, manual selection and four previews; activities must match their source task.
- During ordinary lounge use, export/reload a complete backup and confirm the same approach/seat/task progress and appearance. Do not use provided fictional test worlds as your voyage.
- Open System Status, verify real stages and keyboard focus; during a temporary server/Wi-Fi outage confirm read-only/disconnected states, reconnect and unchanged world. Pair a phone using its PIN independently of host graphics loading.
- Test tablet/phone portrait and landscape, real LAN/Tailscale, installed APK and TV on actual devices. Automation here is Linux Chromium emulation/protocol, not physical certification.

## Rollback

Pause/export the updated voyage separately, close all hosts and stop the server. Restart the untouched previous folder at its old origin and import the **pre-upgrade backup** if needed. Older code does not advance new room interactions reliably. Keep both backup generations until rollback is confirmed.

## Verification from full source

Lite excludes test suites/reports/development tools; all runtime dependencies remain. The development branch contains the full tests and camera-capture tools. With Node, Python development Playwright and Chromium installed:

```
node --test ICARUS/test_*.js
python ICARUS/verify_operations.py --runtime PATH_TO_LITE --suite visual-focused --chromium PATH_TO_CHROMIUM --report visual.json
python ICARUS/verify_operations.py --runtime PATH_TO_LITE --suite visual-remote-focused --chromium PATH_TO_CHROMIUM --report remote.json
python ICARUS/verify_operations.py --runtime PATH_TO_LITE --suite field --chromium PATH_TO_CHROMIUM --report expedition.json
```

Use `visual`/`visual-remote` for full inherited suites, plus `clock`/`legacy`. Archived import tests require the labeled `--v13-web`, `--phase41-backup` and `--phase4-backup` fixtures in the evidence bundle. Missing fixtures are explicit failures. `capture_visual45.py`, `capture_boot45.py` and `capture_restricted45.py` capture actual current feeds/startup in labeled isolated examples. PHASE45_VALIDATION.md records exact source commits and actual results; PHASE45_LIMITATIONS.md describes unfinished scope and hardware gates. Passing automation alone does not finish the final game.
