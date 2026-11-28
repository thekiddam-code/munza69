# Rocket League chat → sound update (UMBRA Mobile 3.4)

This incremental PC update runs the existing Rocket League quick/text action and then calls the existing authenticated SoundService playback mechanism. It adds no audio engine, catalog copy, microphone routing or independent output settings. The phone saves only the chosen existing sound ID with each button/widget override.

## Install

1. This package requires the **3.3 Phase 4.9 host-actions update** already installed. If needed, first apply the adjacent `phase49-host-actions` package (`umbra-pc-phase49-host-actions.zip`). Keep the original installation and data; do not replace it with main's older ICARUS server.
2. Save the current voyage and stop the companion normally. Extract this ZIP to a separate folder, run `apply_chat_sounds.bat`, and enter the original ICARUS folder containing `server.py`. CLI: `py -3 apply_chat_sounds.py "C:\path\to\ICARUS"`.
3. The installer checks exact source hashes, backs up the old code/private settings, replaces only server.py and adds umbra_chat_sounds.py. Changed/partial installations are refused. Restart the same companion normally.
4. Install the matching Mobile 3.4 APK over UMBRA. On HOME, long-press a Rocket League button inside a Button/Mixed widget, choose Configure, scroll to **Sound after chat**, tap **Sync sound choices**, choose a sound, and save the UMBRA override. Select **None** to disable. Existing buttons remain None by default. The sound chooser lists all synced entries in a scrollable list, without a six-entry limit.

The current soundboard's saved output/volume/processing remain authoritative. Output setup stays in CONFIG → ICARUS → Soundboard → Audio Output. This does not inject sound into game voice chat or alter Sonar, VoiceMeeter, microphones or Windows default devices. Ensure the chosen output is audible where desired.

## Behavior and API

`POST /api/rocket/chat-sound` uses the existing paired bearer token, origin check and request-size limit. Allowed payloads:

```json
{"action":"text","text":"Nice shot!","channel":"team","speed":"balanced","sound_id":"<existing 32-hex ID>","requestId":"<UUID>"}
```

```json
{"action":"quick","name":"Nice shot!","sound_id":"<existing 32-hex ID>","requestId":"<UUID>"}
```

The host serializes the sequence on the original input lock. The unchanged text action opens chat, types and presses Enter; only after it returns does the wrapper call `SoundService.post('play', ...)` with the same request identity/owner. Quick-chat sequences also finish before playback. No phone-side timer, arbitrary script/keys, audio uploads or new polling loop is added.

Input failure skips sound. A missing/deleted sound or unavailable output reports successful input completion plus playback failure and **never resends chat**. Responses distinguish `chat_input_completed` and `sound_started`; playback acknowledgment is not proof that someone heard it. An old server returns an explicit missing-update error; Android does not silently send chat without its configured sound or retry.

Receipts are bounded to 128 IDs/ten minutes in PC memory, scoped per paired owner. Repeated identical IDs within that window return the stored outcome, including partial input failures; changed bodies with the same ID are refused. Android uses a fresh ID for each deliberate tap and never retries automatically. Restart/expiry removes this temporary guard; this is not permanent delivery tracking. Rapid taps while the phone is busy are ignored by its existing gate. Long messages plus playback may exceed a short configured network timeout; raise the existing ICARUS timeout if needed, and check the outcome before deliberately tapping again.

Buttons with None use the original `/api/action` unchanged. Only QuickChat/Text outputs use the attachment; switching the editor to another output leaves the ID saved but inactive until returning to chat. Per-widget selections, positions and inactive presets are retained through existing DataStore/export handling; old files without the optional field default to None. Older apps may reject exports containing the new field; keep the current build when importing them.

## Rollback / verification

Stop normally. `py -3 apply_chat_sounds.py "C:\path\to\ICARUS" --restore-code "C:\path\to\umbra_host_code_backups\<backup>"` restores checked previous code and removes the newly added module. Private settings, clips, audio library and voyage data stay intact. Set attached sounds to None before using a rolled-back server.

Reproduce fixture checks with `ICARUS_PHASE49_REFERENCE` pointing to an original Phase 4.9 checkout and the adjacent host-actions package present, then run `python -m unittest discover -s <this-package> -p "test_*.py" -v`. Tests use fake keys/playback and isolated settings, plus the actual companion authenticated HTTP handler. They do not certify Rocket League game acceptance or physical audio output. No live PC deployment or actual game/audio testing occurred in the cloud.
