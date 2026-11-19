# Phase 4.8C validation — foundation, not full acceptance

**Your installed Windows library was not accessible. Its actual backup has NOT been created or verified here.** Use the separate Backup Tool in the existing installation first; require created/verified=true, the expected nonzero sound count and no source errors. Keep originals. No migration/removal was performed. Storage audit is in reports/phase48c/storage_audit.json. Original B code is already server-backed; this does not convert authoritative data into browser storage.

**627 selected source/regression case executions passed** (inherited overlap, not unique tests):

| Suite | Passing executions |
| --- | ---: |
| Node simulation/gesture suite |460|
|archive_http|1|
|audio|6|
|boot|8|
|dispatch|3|
|easter|3|
|palettes|2|
|remote|49|
|services|79|
|soundboard|7|
|voyage|4|
|windows|5|

Services include 20 new preservation/audio foundation cases plus 59 inherited service cases. Six actual HTTP/Chromium C cases verify a populated B-format server library shared by PC/tablet/phone contexts; exact verified ZIP download/authentication; no capture without local consent; no delayed capture after Emergency Reset during backup; missing/older server metadata cannot prune a populated terminal cache; explicit Sonar-Aux **fixture** clip-output selection; untouched original WAVs/assignments; processed host/private-preview PCM equality; independent level metering and reset behavior. Native audio endpoints/input samples are controlled fixtures, not physical Windows observations.

Backup tests preserve unknown files too, check exact original inventories after export, detect corrupted archive/reference data, block writes if preservation fails, and test the standalone CLI with both a populated original fixture and an empty/wrong folder. Empty is not reported as a verified backup of imported sounds. Five-second voice sample data are not saved or returned; metrics only. Cancellation is checked before native input open/start, including after a slow preservation operation. Input busy/errors never switch defaults or select another mic.

DSP tests compare a known 1 kHz mono reference around -23 LUFS, gating across trailing silence, silent/clipped/invalid samples, bounded gain, sample peak protection, original byte/volume preservation and profile continuity. Level-only sampling cannot overwrite a speech reference. Normal shutdown preserves profile settings; explicit Emergency Reset disables only owned DSP and cancels input/output. A corrupt optional profile leaves the library readable/exportable and blocks unsafe processed preview.

Two palette tests fail against B styling with the new CSS suppressed, and pass after scoped restoration. Exact historical RGB/opacity/stripe geometry, unchanged global background, light/dark preference, reduced motion, mobile width and unfiltered arcade images are asserted. All 13 original arcade assets match their original hashes. See EASTER_PALETTE_RESTORATION.md and before/after screenshots. Trigger JavaScript/state is unchanged.

All 49 inherited remote checks, seven B soundboard browser cases, five Windows fixture cases, three existing Easter effect cases, eight boot/writer checks, three expedition/render/media cases, one full original-record HTTP playback case and four actual supplied-voyage restart/history/record checks passed. Private Episode2 SHA-256 remains `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`; private world/audio/configuration files are excluded from all distributions.

## Exact source lineage

Broad runtime `20b36ac5bcc7690471785e3221e6cd81eeff8969` was followed by the six-file CLI/capture-cancellation/level-only meter hardening. Final runtime is `12988bcc080ea50b7f7598d486ad41b6a83dd807`. Final 79 service and six C audio browser cases passed again; other 163 runtime file hashes are unchanged. All 169 final runtime hashes are in scope.json. Separate extracted-ZIP verification is in downloads/phase48c. Expected pre-fix palette failures and deliberate ZIP-tamper warnings are diagnostic, not final failures or fabricated results.

## Actual requirements still unverified / incomplete

- Actual imported library backup/count/hash validation needs the user's Windows directory. The development repository has no installed library. The helper and guarded writer are implemented/tested, but that is not a claim the real sounds were backed up.
- Actual Windows MME input/output/driver execution, both physical microphones and real loudness calibration were not run. The user must validate shared capture does not interfere with Sonar; an unavailable/exclusive input must be left alone.
- Official Sonar documentation supports Mic+Aux Stream Mix to a receiving app's Sonar Stream input. That differs from the user's reported Sonar Microphone input. No automatic/external Sonar/default/per-app setting is changed. Aux clip selection is functional, but routing/mix membership/combined game-chat delivery is not verified. Physical mic switching inside Sonar remains manual; no private/unsupported control API is guessed.
- Private terminal preview has a separate software path; headphone selection, acoustic/OBS/loopback leakage and combined receiving-mix audibility need physical tests. Level detection alone is not proof of both sources. Mic survival on normal close/crash/force termination has not been physically tested. Source architecture has no serial UMBRA voice branch, but code/fixtures do not certify hardware behavior.
- Peak protection is sample-peak, not certified true-peak/intersample limiting; short clips have approximate loudness. DSP stays opt-in; stored WAVs and old per-sound volume numbers stay unchanged. Enabled processed preview needs the host; no unsafe raw fallback when it is unavailable. Disabled B offline preview remains.
- Native APK rebuild/source recovery, physical Samsung phone/tablet/TV, Tailscale hardware, antivirus and sustained real gaming performance were unavailable. Full historical Python and long-duration campaigns were not rerun. Existing protocols/requirements remain; no new pip package, virtual driver, default audio/Sonar setting, power setting or antivirus modification.

Follow README_PHASE48C.md before upgrading and SONAR_ROUTING_AND_VALIDATION.md before any optional external routing change. Keep existing Sonar Microphone voice working until the real tests and user choices are complete. **Phase 4.8C is not declared complete.**
