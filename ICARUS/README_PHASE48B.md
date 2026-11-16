# UMBRA Phase 4.8B — Native Instant Buttons

This extends the verified 4.8A software checkpoint. ICARUS worlds, saves, clock, crew, recordings, Remote Deck, TV, Windows monitoring, launchers and existing macros remain. The soundboard uses UMBRA's dark angular materials; no Myinstants theme or browser-extension integration is used.

## Install, backup and rollback

Export a full ICARUS backup and retain the previous application folder/configuration. Stop its server and close authoritative tabs. Extract the Lite ZIP separately; retain/copy your private config.json, paired_devices.json and samsung_tv.json if present. On future B upgrades also copy the entire private **soundboard_data** directory while stopped. It contains library.json, PCM clips and the clip-output preference and is intentionally excluded from Git and distributions.

Use the same browser profile, hostname and port to preserve origin-bound saves/preferences. Run Start_Remote_Deck.bat normally. Requirements.txt is unchanged; no new runtime pip dependency or administrator access is needed. Refresh browser assets; wait for real readiness and select ENTER ICARUS. Do not clear IndexedDB, reset the voyage or bypass writer protections. Native APK rebuilding remains pending source recovery; existing web URLs/contracts remain.

To roll back, export a post-update voyage backup, stop this server/close its tabs, and run the retained prior folder using the same origin. No ICARUS save migration is introduced. Keep the private soundboard_data directory separately: A does not understand it, and must not overwrite it. Keep both voyage backups and the existing 4.7C media-compatibility limitations.

## Add and customize sounds

Open Simulator → Rocket League/Fortnite/Minecraft, or the ICARUS/SOL remote tab. **Instant Buttons** opens a compact drawer without leaving the activity. Use **Add Sound** directly inside UMBRA.

- Upload a local audio file (up to 8 MiB) or paste a supported public HTTPS Myinstants sound-page URL. Confirm permission to store/use the audio. The public page's main audio is selected, never a related sound recommendation. Access errors/restrictions are reported; no bypass or Chrome extension API is used. Local upload remains the fallback.
- The browser checks duration, decodes supported audio, and converts it to 24 kHz mono PCM16 WAV, at most 30 seconds. Preview before saving. The canonical converted clip is stored; the original encoded file is **not** separately retained. Keep your original file if needed. WAV/MP3 were exercised; other formats depend on browser codecs and fail explicitly when unsupported.
- Set name, category, icon, favorite and per-sound volume. Default gain is 35%. This is not speech calibration or perceived-loudness normalization; those are 4.8C.
- Customize any saved button; rename/change its settings, Move earlier/later to rearrange, or Delete with confirmation. Changes persist on the Windows server and are available to paired terminals. Concurrent edits use revisions and reject stale overwrites.

The library supports 64 sounds / 64 MiB. Imports are not unlimited archival storage. Sound audio/metadata are separate from all ICARUS saves/history. Back them up by copying soundboard_data while the server is stopped; a voyage backup does not contain this separate library.

## Tap versus hold — separate routes

**Tap** requests normal playback on an explicitly selected **Windows render output**. Expand Playback output, select the installed output and choose Use selected output. No default output is assumed. The stored device index AND name are checked again; unavailable/moved devices require reselection. One clip plays at a time; another tap replaces it. Status means driver playback/start/error, not certified delivery to Discord/game chat.

**Hold** (550 ms) previews only on the current terminal/browser output; release stops it. It sends no host playback command. Scrolling, cancellation, pointer loss, navigation, blur, hidden page or closing the drawer cancel preview. Delayed audio arriving after release cannot start it. Held/cancelled gestures suppress release/duplicate ghost clicks; normal keyboard activation remains available. Customize → Preview privately provides an accessible local preview control.

**Use terminal headphones.** This software route is separate from host playback and opens no microphone, but cannot certify your physical headphones, acoustic pickup, OBS loopback or pre-existing Sonar routing. Verify those on your actual equipment. Browser output uses the terminal's current output; B does not change system/default audio devices. Stop all soundboard audio stops this terminal's preview and sends an authenticated host-render stop; host disconnect errors are explicit.

Imported clips work without Myinstants or Chrome running on the PC: the server stores the audio and renders it directly through Windows waveOut. A browser is still the remote interface. Internet disconnection does not prevent LAN-host playback. If the PC server itself is unavailable, normal host playback cannot work and is not queued/replayed. Previously cached private previews can work on the loaded/reopened reachable UMBRA page without audio API access; there is no installed offline PWA/service-worker shell in this phase.

Terminal metadata/blobs persist in a dedicated sound-library IndexedDB database. Decoded buffers are bounded. Clear this terminal's sound cache affects only that cache, never ICARUS. Deleting a sound/revoking a device cannot erase already-downloaded offline copies on another terminal; refresh/prune or clear the cache on that terminal. Do not cache sensitive clips on untrusted devices.

## Audio boundary

**Phase 4.8C is not started.** No microphone device is opened, no Sonar/default audio configuration is changed, and no game-chat injection/mixer/voice normalization is claimed. Playing a Windows render output does not imply other players hear it. Physical Windows/Sonar/private-output isolation and microphone-before/after/shutdown/crash tests remain pending. B's separation and cancellation were tested in a real browser audio graph and authenticated HTTP with an explicit host-output fixture; native hardware still requires the checklist in PHASE48B_VALIDATION.md.

The Easter egg repair is separate; see EASTER_EGG_VISUAL_INVESTIGATION.md. Both opt-in visual settings and their existing client persistence remain. No fictional motif is a world event, discovery, alarm or recording.
