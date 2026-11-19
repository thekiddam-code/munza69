# UMBRA 4.8C — Preservation and safe audio foundation

This build preserves the 4.8B server library and adds verified backups, opt-in input measurement/clip normalization, Sonar endpoint diagnostics/Aux clip-output selection, and historical Easter egg component palettes. **Full 4.8C acceptance remains pending actual Windows/Sonar testing and review of any external routing changes.** It does not automatically change your current Sonar Microphone chat input or your Sonar mixer.

## First: protect the sounds already imported

Your original Windows library is not in the development workspace. It has **not** been remotely backed up or counted here. Before updating:

1. Keep the existing installation. Stop its server and close authoritative tabs after exporting a voyage backup.
2. Copy ONLY `sound_backup.py` and `Backup_Existing_Soundboard.bat` from the separate Backup Tool ZIP into the **existing folder containing server.py and soundboard_data**. These are new helpers, not replacement application files.
3. Run Backup_Existing_Soundboard.bat. It reads that folder, makes a ZIP in the neighboring soundboard_backups folder, verifies CRC and every SHA-256, and checks originals stayed unchanged. It never deletes originals. It rejects an empty/wrong folder as a backup of your existing imported library.
4. Require `created: true`, `verified: true`, a nonzero `source.sounds` matching your library and no `source.errors`. Keep both the original folder and ZIP. A missing/hash-damaged clip is copied as found but blocks upgrading; do not reset it. You can share the result's count/verification/error summary without uploading private audio.
5. Extract the new application separately. While stopped, copy the **entire soundboard_data folder**, private config.json, paired_devices.json and samsung_tv.json if present. Keep the same browser profile, hostname and port. Do not clear IndexedDB or writer locks. Run Start_Remote_Deck.bat and explicitly ENTER after readiness.

The first server-side library/profile write in this build also requires a verified preservation snapshot. A failed backup blocks writes, never resets the library. Backups are private and are not automatically deleted. Manage/move old backups manually if disk space is limited. Standalone helper uses Python standard library only, no pip install/admin rights.

## Where storage lives

- Authoritative Windows server: `soundboard_data/<sound-id>.wav` holds the imported canonical audio. `soundboard_data/library.json` holds the schema-1 IDs, names, array order/button assignments, icons, categories, favorites, per-sound volumes and selected clip render output.
- New optional C processing: `soundboard_data/audio_profile.json` stores measured loudness/settings only. No recorded voice is stored. Existing WAV/JSON library fields are not migrated, rewritten or renumbered by calibration.
- Tablet/phone/PC browsers: `umbra-sound-library-v1` IndexedDB holds cache metadata/blobs. It is not the authority. All paired terminals connected to the same companion server use the same library.
- Sound backups are separate from ICARUS voyage backups. Keep both. A terminal with a populated cache will refuse to replace/prune it if the host library is missing or its revision is older; recover/copy the old server folder instead of importing a new empty collection.

No migration from Myinstants/Chrome/browser-only storage is required for sounds successfully saved through 4.8B Add Sound. The actual on-PC library must still be audited with the helper; code inspection and synthetic tests cannot prove its current disk state.

## Audio controls

Inside Instant Buttons, open **Audio calibration / Sonar / verified backup**. Inspect host endpoints. The input selector is for measurement only, not changing the physical mic chosen in Sonar. Legacy Windows names can be truncated; ambiguous roles must be checked locally. UMBRA does not infer the actual Windows defaults or per-app chat input from endpoint names.

On the PC (paired localhost interface), explicitly consent to a five-second sample. UMBRA verifies preservation before opening the input. Speak normally for calibration. Samples are analyzed in memory and discarded; only metrics reach the UI. Remote phones/tablets cannot start PC capture. Emergency Reset cancels even a measurement waiting for backup, so it cannot open the mic later.

**Calibrate speaking loudness** saves a reference. **Measure input / combined-mix levels** is a separate level-only check and does not replace that reference; a nonzero signal alone does not prove that both sources reached game chat. Input busy/removed/unsupported errors never cause fallback to another microphone or a device-default change.

Normalization stays OFF until explicitly enabled. It uses mono K-weighted, gated integrated loudness, defaults to effects 3 dB below the measured reference, limits boost to 6 dB, and applies 10 ms lookahead/2 ms attack/80 ms release peak protection with a -1 dBFS sample ceiling. The retained 35% per-sound volume is the nominal reference; other saved volumes are relative adjustments. Short effects/peak limiting may fall below target. This is not certified multichannel R128/true-peak processing. Stored clips stay byte-identical; processing is transient and bounded.

A saved clip's private preview and host playback use the same processed PCM. Private preview is still terminal-only, never a host-play command. Unsaved candidate preview is raw gain; save then hold to hear calibrated processing. If processing is enabled and the host is unavailable, processed preview fails explicitly rather than secretly playing a louder raw version. With processing OFF, the original B offline-cache preview remains.

**Emergency Audio Reset** stops UMBRA clips, requests input cancellation and disables its processing. It cannot undo manual Sonar/Discord settings UMBRA never changed. Ordinary shutdown releases only owned resources and preserves saved processing preferences. No normal voice passes through UMBRA.

## Sonar route: explicit external decisions still required

SteelSeries documents mixing Mic plus Aux via **Sonar Stream Mix**, with the receiving application using **Sonar - Stream**. Your reported input is **Sonar - Microphone**. They are different endpoints. No verified automatic injection into that unchanged microphone endpoint has been demonstrated here.

The UI can select a uniquely detected Sonar Aux as UMBRA's clip output after confirmation; this changes only UMBRA's output preference. It does **not** enable Streamer mode, change mix membership, select a physical mic in Sonar, change Windows defaults or switch game/Discord input. To adopt the optional Stream Mix route, first record your current external settings, review the official guide and deliberately configure only intended Mic/Aux sources. Exclude Game/Chat/Media as appropriate to avoid broadcasting unrelated audio/feedback. Those are persistent external choices, not automatic upgrade steps.

If you keep the current Sonar configuration/input unchanged, normal voice stays independent and soundboard clips remain render-only until a compatible route is actually verified. No extra virtual driver or serial UMBRA microphone mixer is installed. Follow SONAR_ROUTING_AND_VALIDATION.md for the actual hardware gates; do not treat endpoint detection or a level meter as proof.

## Easter egg palettes and rollback

The palette-only file restores source-backed amber tag/hazard stripes, mint readout and full-strength original specimen colors. Global UMBRA colors, triggers, preferences, histories and all original GIF/PNG bytes stay unchanged. See EASTER_PALETTE_RESTORATION.md.

For rollback, export the current voyage and stop this server/tabs. Keep the old installation, the entire private soundboard_data directory and verified backups. B ignores the optional C profile file and retains the schema-1 sounds. External Sonar/game settings, if you manually changed them, must be restored manually from your notes; closing UMBRA never claimed to revert them. Native APK source recovery and physical Samsung/TV/Tailscale checks remain pending.
