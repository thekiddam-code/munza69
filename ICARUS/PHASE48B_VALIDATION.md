# Phase 4.8B verification and pending hardware gates

**599 selected case executions passed**, with inherited overlap. This is the soundboard software stage and a separate confirmed Easter egg repair, not completion of Phase4.8 or hardware certification.

| Suite | Passing executions |
| --- | ---: |
| Node simulation/gesture suite |460|
|archive_http|1|
|boot|8|
|dispatch|3|
|easter|3|
|remote|49|
|services|59|
|soundboard|7|
|voyage|4|
|windows|5|

Services include 19 new sound cases plus 40 inherited Windows/bridge/TV/archive cases. Seven final soundboard cases exercise real HTTP, browser decoding/AudioContext, local WAV upload and owned generated MP3 link response, pre-save preview, saved edits/order/favorites/categories/volume, deletion, reload, offline IndexedDB preview, no microphone API calls, explicit host-output dispatch, no host play on hold, cancellation/ghost clicks, delayed bytes after release, stale import replacement, 10 imports with bounded hot cache, responsive Simulator/SOL availability and authenticated errors/unpairing. Host render hardware is an explicit fixture. ffmpeg was used only to generate an owned test MP3; it is not a runtime dependency.

The separate three Easter egg cases fail twice against the unrepaired app.js/CSS from `73c2028` and pass with restored styles/timers, opt-in/reduced-motion/Bridge-only gates, persistence and unchanged arcade assets. All 13 original arcade files match `65e68f1`. Read EASTER_EGG_VISUAL_INVESTIGATION.md for exact causes/repair. Diagnostic pre-fix failures are retained and excluded from passing totals.

All 49 inherited remote, eight boot/writer, three dispatch/render/media, one original-record HTTP playback and four supplied-voyage cases passed. The private Episode2 input retains SHA-256 `888ea1574d2b24ae6e4f7911b29dbf2c22079fbbaa4f34cd64f350afbbff7d75`; crew/maps/knowledge/history/received recordings survive actual isolated restart. No live Windows installation was accessed or reset; no private save/audio/configuration is bundled.

Broad regression runtime began at `7f2c78bc3407f17f30b4e3c139ee6ed02da26ccb`. Afterwards only `web/umbra/soundboard.js` was hardened for the tested pending-import controls, memory bounds and unpair visibility. Final runtime is `73ace07148a73114ff0a5c04fd8db0dd1123117f`; all final seven soundboard tests reran successfully, including post-start output errors and failed persistent-cache clearing. Other 161 runtime hashes are unchanged; final 162 hashes are in reports/phase48b/scope.json. The ZIP directory records additional extracted-package checks, CRC/checksum and source lineage.

A deliberately pending-import test failed before the form reset repair and passed afterwards; late results are discarded. Gesture tests prevent two ghost clicks from routing publicly after a hold. Cache stress proves excess hot entries are evicted without deleting the durable library. An initial microphone trap accidentally returned a function to Playwright, which invoked it itself; the corrected no-return fixture counts actual calls and reports zero. No production assertion or writer protection was removed. The archive image test waits for actual decoding; timer verification observes real DOM changes under the installed clock.

## Live Myinstants check

A public homepage and sound page returned usable HTML, and the current parser found the page's main audio metadata. No copyrighted audio was downloaded or published in that live check; details are in live_source_check.json. End-to-end decoding/import tests instead used owned WAV/MP3 fixtures. Website layouts, access restrictions and licensing can change. Import failures are explicit, never bypassed; local file upload is available. A user's own permitted Myinstants clip still needs a manual live import check.

## Actual Windows / tablet / audio checklist — PENDING

No real Windows audio device, Alienware PC, SteelSeries Sonar, physical Samsung tablet/TV, microphone loopback meter or antivirus engine was available. The native APK cannot be rebuilt without source recovery. No physical output/private leakage/voice-survival result is inferred from mocks. Do not begin 4.8C routing on an unverified serial voice path.

1. Back up the voyage, private companion configuration and (on later B upgrades) the entire soundboard_data folder while stopped. Follow README_PHASE48B.md. Keep the same origin/profile; never clear the world database or writer locks.
2. Verify normal voice already works through the existing SteelSeries Sonar - Microphone input. Start UMBRA. Confirm Windows defaults/Sonar/microphone settings remain unchanged. Select only the intended explicit render output in the soundboard; this is a clip-output preference, not a Windows default-device change.
3. Import an owned WAV/MP3, preview it before saving, then import a Myinstants page you have permission to use. Test unsupported/oversized/missing audio errors. Rename/category/icon/favorite/volume/reorder/delete, restart the server and verify the library. Close Myinstants and Chrome on the PC; play from the paired tablet. Internet access should no longer be needed for the imported clip.
4. Tap and verify sound reaches the selected Windows render device. B does **not** promise game-chat injection: confirm that separately only when implementing C. Use headphones and keep the clip quiet; volume is not speech-calibrated/loudness-normalized yet.
5. Hold on the tablet and verify only its headphones play. Monitor Discord/game-chat input and any OBS/Sonar loopback: it must not contain preview. If it does, stop and isolate the terminal's existing output outside UMBRA before relying on privacy. UMBRA does not silently change that route. Preview on a Windows browser can follow an already-captured Windows default output; hardware verification is required.
6. Release, scroll, drag away, cancel touch, switch apps/tabs, close the drawer and lock the screen; preview must stop and must never fall through to public playback. Test a slow network response arriving after release. Normal tap remains distinct; no offline host command is queued.
7. Disconnect the terminal network while the page is loaded: cached private previews remain local; host-play failures are clear. A fully unloaded page cannot be reopened from a dead server without an app-shell cache, which B does not add. Reconnect without changing the output route. Stop all soundboard audio and verify release of UMBRA-owned output; if the host is unreachable, the last nonlooping clip can finish (max 30s).
8. Stop/restart and, separately, force-terminate the server. Normal microphone audio must remain independent. These physical tests remain pending even though B opens no capture devices. Do not claim voice continuity or isolation based only on software tests.
9. Verify existing Windows hotkeys/apps, TV, ICARUS host/remote, expedition/camera/backup behavior on the actual devices. Tailscale, native APK, antivirus and sustained gaming performance are separate hardware/manual gates.
10. Follow the separate Easter egg checklist. Existing world/discovery history must remain; these optional fictional effects never produce a simulated incident.

## Remaining limitations

Phase4.8C is **not started**: no capture, Sonar routing, virtual device, microphone calibration, perceived-loudness normalization, game-chat mixer or default-device changes. Normal tap is explicit Windows render playback; private preview is the terminal's current output. Their software paths are separate and tested; actual physical isolation is not certified. Default sound gain 35% and 10ms fades are not LUFS matching or a full limiter.

Library bounds: 64 sounds / 64 MiB, 30 seconds each, canonical 24 kHz mono PCM16. Original compressed uploads are not retained separately. WAV/MP3 conversion was exercised; other codecs depend on the browser. Simultaneous different sounds replace the previous host clip. Device name/index mismatches require reselection. A driver that refuses buffer release disables further playback until restart. Terminal cached copies cannot be remotely erased after export/revocation; sync prunes stale records, and Clear terminal sound cache affects only that database. A full voyage backup excludes the separate soundboard library: copy its folder while stopped.

Physical/native/TV/Tailscale/antivirus checks, full historical Python matrix and long-duration soaks were not run. Existing dependencies remain; no new runtime pip package/driver/PowerShell/audio-routing command was added. No antivirus protection, power setting, default audio or Sonar configuration was changed. See README_PHASE48B.md, PHASE48B_ARCHITECTURE.md and the separate Easter egg investigation.
