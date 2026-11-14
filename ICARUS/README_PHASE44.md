# ICARUS / UMBRA — Phase 4.4 Expedition Operations Lite

This update extends your existing voyage with actual asteroid preparation, travel, field work and source-grounded observation. It preserves Phase4.3 ship engineering, Phase4.2B cameras/personality, UMBRA, save history and production calendar rules. The native installed Android app is not replaced.

## Install, back up and migrate

1. In your working installation, pause and export a complete backup **including history**. Keep an untouched copy of both the old installation and backup outside the new folder.
2. Close every old ICARUS host tab and stop the old companion server. Do not run old and new hosts simultaneously; older versions may not implement current writer fencing.
3. Extract the Lite ZIP into a **new folder**. Keep all six root runtime files and the complete `web` folder together. Never copy a test campaign save into your voyage.
4. On the Windows laptop run `Start_Remote_Deck.bat`. It uses `py server.py` or `python server.py`. If required, install the existing dependencies from that folder with `py -m pip install -r requirements.txt` (Python3.11+ recommended). Follow README_PHASE41.md for original network/configuration/pairing/Tailscale settings.
5. Use the same laptop browser/profile and server origin as before. Storage is origin-specific. If a new world appears, stop and import your own exported backup through the existing backup interface. Confirm crew names/history/date/resources before resuming.
6. Migration adds geometry, equipment/evidence metadata and optional field domains without replacing the voyage. Already-active legacy missions finish their existing controller; subsequent asteroid departures use the new physical workflow. Do not recall/relaunch merely to force migration.
7. Export a separately named post-upgrade backup after checking continuity. Keep the original backup unchanged.
8. On phone/tablet open your paired UMBRA address. It remains a remote terminal; do not open a second `icarus.html` host on the phone. Native Samsung Tab S5e source recovery/build remains pending, not unsupported.

## Observe or request an expedition

Open **Missions → Active** on host or paired UMBRA. The expedition section shows received maps, actual mission category/team, equipment/carry budget, pressure stage, last command result, safe return and received event records. Select a supported objective and a **known** target when appropriate, then Request. The host validates authorization, actual objective, supplies, team/readiness and shared transport. A request can be postponed; an acknowledgment is not a guarantee of immediate launch.

SOL's existing autonomy can authorize expeditions from real observed opportunities without intervention. A reported failed lift supply can justify a paid repair; remaining known unvisited routes justify survey. No quota requires continual missions. Finishing a repair does not consume unrelated exploration evidence.

Watch crew collect equipment in C04, brief/check protection in C01, reach C02, cycle the vestibule, take the shared shuttle and walk connected field passages. Return takes actual time too. Use Follow Crew or select the available **BODY** feed. During transit, range loss, damaged equipment or a receiver outage the field feed is unavailable rather than replaced by an omniscient scene. Information can arrive late.

Recall uses the actual communication channel. A pending request can wait for delivery; repeated clicks cannot magically recall an unreachable team. Environmental reserves can cause autonomous withdrawal. Repairs consume carried tools/spares/power and require a powered post-test. An unsafe C02 return hatch can hold the team; do not assume an infinite oxygen rescue guarantee.

Received event review offers actual saved source-state frames labeled **reconstruction — no recorded video**. It is not a video recording. Significance2/3 changes the threshold; ordinary walking only updates a bounded short ring. Lost-link local data remains on the device until legitimate transmission or surviving physical recovery/dock reading.

## Laptop / phone / tablet manual checks

- Confirm matching mission ID, ship tick, team, stage and received map between laptop and paired UMBRA. Remote must show no independent simulation and reconnect after temporary Wi-Fi loss.
- Request a real survey only if a valid objective and resources exist. Watch C04/C01/C02, actual travel and return; confirm reserves and ledger entries change consistently.
- Follow a real team member through ship/lift, shuttle-unavailable state and a BODY feed. Verify private ship-quarter camera rules remain unchanged.
- Pause, export backup during field travel, close/reopen host and import only if needed. Check exact team/location/progress, original voyage history, unchanged calendar and no duplicate supplies/records.
- Test portrait/landscape touch controls, field reconstruction slider, dropdowns, profiles, Bridge/Creator separation and saved desktop/mobile workspace arrangements.
- Verify existing TV and installed Android integrations separately on actual devices. Do not infer physical success from the automated protocol/emulation tests.

## Rollback

Pause/export the updated voyage separately, close all hosts and stop the server. Restart the preserved older installation at its old origin and import the **untouched pre-upgrade backup** if needed. Older code is not certified to advance new field manifests/evidence. Do not erase either backup generation until rollback is confirmed.

## Reproduce from full source

Lite excludes tests, reports and development/packaging tools, but retains every runtime dependency. The branch contains the full source. With Node and Python development Playwright/Chromium installed:

```
node --test ICARUS/test_*.js
python ICARUS/verify_operations.py --runtime PATH_TO_LITE --suite field --chromium PATH_TO_CHROMIUM --report field.json
python ICARUS/verify_operations.py --runtime PATH_TO_LITE --suite field-remote --chromium PATH_TO_CHROMIUM --report remote.json
```

Use `--suite expedition` for the full inherited browser suite and `expedition-remote` for all HTTP/emulated-phone cases; `clock` and `legacy` are separate. Archived migration cases need `--v13-web`, `--phase41-backup` and `--phase4-backup` pointing to the clearly labeled evidence fixtures. Missing fixtures fail explicitly. `expedition_campaign.py` uses ICARUS_RUNTIME_ROOT/ICARUS_CHROMIUM, --seed, --days, --scenario and --output; `summarize_expeditions.py` independently audits its actual artifacts. These are isolated fictional test worlds, never your voyage.

Read PHASE44_VALIDATION.md for exact results, PHASE44_ARCHITECTURE.md for migration/authority, PHASE44_LIMITATIONS.md for incomplete rescue/art/physics/native scope, and SECURITY_PHASE44.md for static review. Passing automation does not declare final-game readiness.
