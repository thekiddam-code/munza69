# ICARUS — Cinematic Refinement Phase 3.5 Lite

An autonomous science-fiction anthology simulation. This build refines the existing voyage: procedural activity animation, authentic source snapshots, optional Sunday awards/strict lethal eligibility, quieter individual-aware editorial, streamed backups and one protected writer tab. It adds no universe expansion, forced incident or guaranteed outcome. See PHASE35_VALIDATION.md and PHASE35_LIMITATIONS.md; automated verification is not native-device or human cinematic approval.

## Back up and install

1. In the working Phase 1/2/3 build, export a **complete JSON backup**. Confirm the file exists. Preserve an untouched copy of that working folder and this pre-upgrade backup.
2. Close all old simulation tabs and stop the old PC server. Extract the entire new Lite ZIP to a separate folder. Keep all web assets and the Python host together; do not mix individual files from different builds.
3. Copy your customized `config.json` and, when present, `paired_devices.json` and `samsung_tv.json` from the old folder. No generated credentials are shipped.
4. Start the unchanged `Start_Remote_Deck.bat`. Keep the **same browser profile, hostname and port 8765**. Existing core save keys and IndexedDB schema remain compatible. Do not click New Voyage to recover a save. If necessary import your complete backup in Settings.
5. Keep one simulation writer tab. Additional same-origin tabs show **READ-ONLY SPECTATOR** and cannot save, run the physical simulation or consume Remote Deck commands. Close the writer and reload the desired tab to take over; LAN lease fallback can require 15 seconds after a crashed writer. Different browser profiles/origins are separate voyages, as before.
6. Android remains the existing paired thin client. Use the PC host's LAN URL and existing pairing/normal PIN. Remote Deck bridge key controls are now in **Settings**, so their overlay no longer obstructs the camera. Host command capabilities, port and pairing data are unchanged.

No new Python dependency is needed for a working Lite installation. A new PC needs Python and `py -m pip install -r requirements.txt`. No installer, video encoder or executable wrapper is included. All local JS dependencies/licenses are retained. Never disable antivirus to run the build.

## Watching and playback

Operations retains manual camera controls, optional AUTO direction, actual physical nodes, procedural body/mobility cues and reduced motion. Manual camera choices stop AUTO. Pause/reduced motion stop character motion. Room visibility/hardware failures give telemetry, not imaginary occupants. Significant local source events can retain real schematic snapshots; older saves gain an empty buffer, never retroactive footage.

Sunday timelines remain optional, nonmodal and shorter for sparse weeks. Awards require actual documented achievements. Legendary eligibility requires retained causal evidence, a corroborated death, recorded intervention, measured adverse conditions and an observed rarity sample. Most encounters cannot qualify; zero clips is valid. Saved state snapshots explicitly say schematic/not video; other cards say RECONSTRUCTION. Arrows skip a focused card, Space plays/pauses, Escape closes; seek and touch buttons remain available. No camera control changes ship decisions.

## Large backups, migration and cancellation

Settings → Save Management → **Stream complete backup** writes `.ndjson`: world envelope, ordered SHA-256 history chunks and final manifest. Chromium's writable-file API writes incrementally where available. Other browsers download Blob parts, retaining encoded bytes until download. The original JSON export remains for compatibility/rescue; large full archives should use streaming.

**Import backup (.json / .ndjson)** accepts existing files and the new format. It validates the world, source availability, chunk hashes/order/IDs and final manifest, stages history, then commits world and history in one IndexedDB transaction. Progress and Cancel are visible; cancellation closes when atomic commit begins. Physical ticking is held during transfer, then existing bounded catch-up resumes. Failed/cancelled staging leaves the old world; after a crash, a new writer cleans abandoned staging. Keep backups outside browser storage.

Legacy JSON still requires whole-file parsing under the existing 128 MiB limit. New streamed files avoid loading the entire history array; individual lines have a 64 Mi UTF-16 code-unit buffer bound and history batches contain at most 128 rows. Old save-only files without a full archive import all records they actually contain and are explicitly labeled partial; unavailable older history is never invented. Import requires working IndexedDB; if storage fails, use the labeled JSON rescue export and restore in a functioning browser. SHA-256 detects corruption, not who authored a file.

## Rollback

Export the current voyage before rollback and retain it separately. Stop Phase 3.5, restart the untouched old folder at the original browser/profile/hostname/port, then import the **pre-upgrade complete JSON backup**. This restores that checkpoint, not a backward merge of subsequent events. New `.ndjson` files are not readable by older builds. No database-version bump or browser-storage deletion is needed. Keep both backups until verified.

## Verify

Use `Get-FileHash .\ICARUS_Cinematic_Refinement_Phase3_5_Lite.zip -Algorithm SHA256` on Windows and compare the supplied `.sha256`. BUILD_MANIFEST.json records the exact Git source commit and every retained file hash. Tests, reports, development utilities and packaging scripts stay in the repository/evidence archive, outside Lite runtime. Source: thekiddam-code/munza69, branch codex/cinematic-refinement-phase3-5.
