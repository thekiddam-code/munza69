# Existing ICARUS soundboard integration

**3.1 navigation/storage update:** see [current report](WIDGETS31_REPORT.md). Soundboard is now in SIMULATOR; audio output is CONFIG → ICARUS → Soundboard. Dedicated Instant Buttons and Command library pages are removed. HOME Button/Soundboard widgets have independent configuration; schema 6 preserves existing data. The earlier contract and historical verification below remain applicable except where the current report supersedes navigation or limits.

Phase 3 moves the native soundboard to **DECK → Soundboard** and retains these same server-owned configuration/playback APIs. See [current Phase 3 report](PHASE3_REPORT.md). The original 2.3.1 verification below remains historical.

## Finding and scope

The native Phase 2.3 client discovered only `/api/status` text/macro/quick-chat mappings. It did not request ICARUS's separate sound library. The working implementation is on `codex/umbra-soundboard-phase4-8b` (`958f3efdb72e2998a1b741e7670703c69ada1569`), with a compatible catalog/playback contract on `codex/umbra-sonar-phase4-8c` (`ca2fcffab513aec65f1ff626c85b481de4c8a2f9`). The older ICARUS tree on main has no soundboard. This hotfix updates only the native launcher; it does not merge those branches, replace the user's running server, rebuild audio playback, or touch simulation saves.

Keep using the existing soundboard-capable ICARUS server and its existing private `soundboard_data` folder. Configure its address in UMBRA Settings → ICARUS, connect Tailscale, and pair the native phone using the server PIN. Browser pairing is separate. A 404 on `/api/sounds/library` means the configured server lacks the existing soundboard API; it is not a successful empty sync. Do not replace a working 4.8B/C installation with main's older server or copy an empty library over the existing one.

## Native use

Open **DECK → Soundboard**. Every parsed sound appears using its original ID and label; the scrollable grid has no six-button limit (ICARUS currently supports 64 clips). Tap to send the existing host-play command. Stop playback sends the existing host-stop command. The reported starting/playing/idle/error state comes from ICARUS, with one-second refresh only while playback is active and this panel is visible. This is driver/server feedback, not proof that another player heard it. No offline commands are queued or automatically replayed.

Long-press and drag any button to arrange it. Release a stationary hold to open existing grid options; Resize changes its grid size and Configure changes its shared Favorite flag. Holds and drags suppress playback. Positions/sizes/visibility use the existing local `gridLayouts["soundboard"]` DataStore entry with the same Undo/Done workflow and temporary amber placement guides. Long-press the SOUNDBOARD heading to restore hidden sounds. Existing layouts and animation preferences are preserved; no configuration schema change is needed. Text/quick-chat remains on separate tabs and never substitutes for the sound catalog.

## One authoritative audio configuration

Open **Settings → ICARUS → Soundboard → Audio Output**. UMBRA reads the saved render device and the actual available devices. Selecting a device saves the exact ID/name through ICARUS with the current library revision, then re-reads the catalog. It does not save a second audio-output preference in DataStore or configuration exports. The server checks identity again at playback; missing/moved devices require deliberate reselection and never silently fall back.

4.8B supports an explicit render-device selection and per-clip gain, with one clip at a time and replacement/stop semantics fixed by its existing player. It does **not** expose master volume, repeat, routing-mode or stop-behavior preferences, so this app does not invent those controls. Per-clip gain/import/rename remain available in the original Remote Deck. When 4.8C advertises a valid `audio_profile`, Settings additionally exposes its existing normalization enable, speech offset, ceiling and maximum boost, saved through its existing profile endpoint. Enabling requires an existing speech calibration; microphone calibration stays in Remote Deck. No Android microphone permission is requested and no Windows/Sonar defaults are changed.

### Existing definitions, storage and calls

| Responsibility | Existing ICARUS source / contract |
| --- | --- |
| Sound definitions and exact mappings | `sound_library.py`: `sounds[]` in `soundboard_data/library.json`, immutable sound ID → matching WAV |
| Playback | `sound_service.py` → `sound_output.py` Windows render backend; no client audio engine |
| Authentication | Existing `/api/pair` PIN and `Authorization: Bearer …`; server-bound encrypted Android Keystore token |
| Catalog, devices, saved output, player | `GET /api/sounds/library` |
| Play | `POST /api/sounds/play` with exactly `{id, requestId}`; unique request ID, no automatic retry |
| Stop | `POST /api/sounds/stop` with `{}` |
| Saved default render output | `POST /api/sounds/output` with `{device: {id,name}, revision}` |
| Shared favorites | `POST /api/sounds/edit` with `{id,fields,revision}`, preserving name/category/icon/volume |
| Optional 4.8C normalization | Advertised `audio_profile`, `POST /api/audio/profile` with exactly enabled/offset_db/ceiling_dbfs/max_boost_db; authoritative `soundboard_data/audio_profile.json` |

No server extension was necessary. ICARUS's existing atomic storage, revision conflicts, pairing/origin checks, request-ID deduplication and original Remote Deck remain authoritative. A conflict/error prompts refresh instead of overwriting another terminal or replacing the output. Audio settings always load from the server on entry; this naturally survives restarting UMBRA.

## Synchronization, privacy and lifecycle

Catalog sync has its own count, last successful full-parse timestamp, busy state and error, independent of text commands and ship telemetry. A failed/malformed catalog retains a clearly dated earlier snapshot, never advances its success timestamp and marks playback status unknown. Switching server bases hides the former catalog. HTTP requests are bounded to 128 KiB, use the existing timeout/cancellation/redirect restrictions and do not log URLs, tokens or labels. Playback feedback is not simulated. Screen actions and polls cancel when hidden/stopped; there is no service, wake lock, inactive polling, analytics or duplicate clip cache.

## Verification and remaining device checks

See `verification/soundboard/RESULTS.txt` for executed results and logs. Native tests use Android host runtimes and an isolated server fixture; the original server/browser tests use their existing generated audio and explicit fake Windows output, not the user's private library or live hardware.

Physical acceptance still requires the running ICARUS PC and phone: confirm every private library button appears, tap several IDs, hear the configured render output, verify Sonar/game routing separately, restart UMBRA, change output/favorites from Remote Deck and refresh UMBRA, disconnect the selected device, test long-press/resize and Android background/resume. Actual sound on Windows/S24+, microphone continuity and exact One UI behavior cannot be certified by these host tests. No claim of full hardware acceptance is made.

Phase 2 follow-up: optionally expose more audio controls only when the authoritative server supports them; add server push events if available, and perform the physical device/audio acceptance above. Preserve the same library and playback engine.
