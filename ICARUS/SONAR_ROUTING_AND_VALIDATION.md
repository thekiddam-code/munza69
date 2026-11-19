# Sonar routing review — no automatic configuration change

## Evidence and design boundary

SteelSeries documents Game/Chat/Media/Aux as playback channels and Mic as input. Streamer mode mixes selected channels, including microphone, to the separate Sonar Stream endpoint. Its Discord guidance uses Stream as the application input. These documents do not demonstrate a supported injection API into the user's currently reported Sonar Microphone endpoint while leaving all mixer/app configuration unchanged.

Primary references checked November 19, 2026:

- [Setting up Sonar for Streaming](https://support.steelseries.com/hc/en-us/articles/13761015491725-Setting-up-Sonar-for-Streaming)
- [Personal and Stream Mix](https://support.steelseries.com/hc/en-us/articles/13761324882701-How-to-setup-personal-and-stream-mix)
- [Sharing music through the stream mix](https://support.steelseries.com/hc/en-us/articles/14660250166285-How-can-I-share-music-with-my-friends)
- [Discord routing and echo considerations](https://support.steelseries.com/hc/en-us/articles/35145998503181-Setup-Sonar-to-Stream-with-Discord-Without-Echo)

These are capabilities of Sonar, not observations of the user's installed configuration. No local Windows/Sonar session was accessible. No source claims actual game-chat injection, microphone survival or physical private-preview isolation has passed. The new tools keep `injection_verified: false`.

## Optional independent route

Physical microphone → existing Sonar Mic processing → Sonar Stream Mix → receiving application's Sonar Stream input.

UMBRA soundboard → explicit Sonar Aux render output → that same externally managed mix.

The first path never passes through UMBRA; stopping/crashing the clip branch cannot intentionally cut the voice path. Existing processing can remain in Sonar. However, enabling/changing the stream mix and switching a per-app input are persistent external changes and conflict with preserving the exact current configuration unless the user chooses them. This build only inspects endpoint names and, on explicit confirmation, selects Aux for its own clips. It never applies external changes or installs a virtual driver.

Do not select a physical microphone as an output. Do not assume that hearing a speaker clip feeds Sonar Microphone. Do not use UMBRA as a live serial mic mixer. No unsupported/private Sonar API or guessed configuration-file edit is used. Ambiguous/truncated device names require local inspection rather than automatic matching.

## Required actual Windows checks — not run here

1. Run the existing-library backup helper in the old folder. Verify the sound count/hashes and retain originals. Confirm imported clips/assignments match on PC/tablet/phone before any optional processing or external route change.
2. Note/screenshot the actual Sonar mic source, mix membership, Windows defaults and game/Discord input. Confirm natural voice works before launching UMBRA. Do not change these just to satisfy a test.
3. Inspect endpoints in UMBRA. Compare full names/roles in Windows/Sonar. Confirm both physical microphones independently; the UMBRA selector changes only a measurement source. If a driver rejects parallel measurement, leave voice intact and report the error, not a default-device workaround.
4. With local consent, measure representative speech and preview privately on terminal headphones. Enable normalization only after reviewing the measured level. Check actual clip loudness and peaks; verify no gain beyond the configured cap and keep human monitoring. Input/mix-level measurement does not save a new speech reference.
5. If the user chooses the optional Stream Mix route, manually include only intended Mic/Aux sources and choose the corresponding input in a test application. Avoid chat return/game/system audio and double monitoring. Do not disable existing processing or change defaults automatically. Keep recovery notes for every external change.
6. Before game use, listen at the actual receiving mix. Verify voice alone, clip alone, then both. Sonar's ordinary mic preview can be before the mix; it is not evidence that the clip reaches the receiving app. The UMBRA level meter cannot identify the two sources by itself.
7. Hold a private preview and check the receiving mix contains no preview. Verify terminal headphone selection, acoustic pickup and existing OBS/loopback routes. UMBRA only guarantees its distinct software functions; physical isolation needs this test.
8. Disconnect/reconnect the tablet. Stop the server normally and then test force termination separately. Voice must continue through the independent external route; no duplicate clip or unexpected device fallback should occur. Check Emergency Reset cancels pending capture/owned output and disables DSP. Native driver resource behavior cannot be certified from Linux fixtures.
9. Verify Windows/Sonar/default settings remain unchanged by UMBRA. If the optional external route was manually changed, restore it manually if rolling back; UMBRA never claims to revert a change it did not own.

No hardware results are fabricated. Full Phase 4.8C acceptance is blocked on actual library verification, Windows/Sonar endpoint review, explicit decisions about external routing, combined-signal/private isolation tests, and shutdown/crash voice continuity. Existing microphone configuration stays unchanged until then.
