# Phase 4.8C routing correction — local playback first

## Established voice chain and non-negotiable boundary

The user confirmed: Arctis Nova physical microphone → existing Sonar microphone processing → **SteelSeries Sonar - Microphone** → game voice input. The physical microphone is a capture endpoint, never a speaker/render destination. UMBRA must not change that physical selection, processing, Windows defaults or existing library. No actual Windows audio session or installed library was available in development.

## Investigation, checked November 20, 2026 (UTC)

SteelSeries describes Game/Chat/Media/Aux as output channels and Mic as an input channel. Its supported method for including application effects/music with voice is **Sonar for Streamers / Stream Mix**, with the receiving application's input set to **SteelSeries Sonar - Stream**. Including Aux in Stream Mix alone does not make Aux appear in the distinct Sonar - Microphone endpoint. Local hearing also requires the channel in Personal Mix and a valid headphone playback destination.

Primary references:

- https://support.steelseries.com/hc/en-us/articles/16954265292173-How-does-Sonar-work
- https://support.steelseries.com/hc/en-us/articles/14660250166285-How-can-I-share-music-with-my-friends
- https://support.steelseries.com/hc/en-us/articles/35145998503181-Setup-Sonar-to-Stream-with-Discord-Without-Echo
- https://learn.microsoft.com/en-us/windows/win32/coreaudio/enumerating-audio-devices
- https://vb-audio.com/Cable/
- https://vb-audio.com/Voicemeeter/

No supported public direct-injection API into Sonar - Microphone was identified. Windows audio render APIs send samples to render endpoints; capture APIs read microphone samples. A recording endpoint cannot simply be passed as a waveOut playback destination. UMBRA enumerates playback with waveOut and optional measurement inputs separately with waveIn; names do not override this direction.

## Local playback finding and implemented repair

The native waveOut path from B (`958f3ef`) remains intact. C added opt-in transient clip processing; it did not replace native rendering or automatically reconfigure Sonar. The prior optional Aux button changes the **single UMBRA clip output**. If chosen without Aux in Sonar Personal Mix, local headphone playback can become inaudible even though Windows accepts output. No actual installed endpoint selection or native failure could be inspected, so this is a verified architecture gap and plausible explanation, **not a reproduced diagnosis of the user's PC**.

Implemented in the existing soundboard, without a second mixer/library:

- A clearly labeled **Restore PC headphone playback** section with an explicit playback/render selector and save button. There is no guessed default or automatic microphone/output switching.
- The selector uses the actual render enumeration, starts blank if no valid prior selection exists, preserves an unsaved explicit selection during inspection, and matches both ID and name.
- Both the existing output picker and optional Aux button use the same validated soundboard output command and revision handling. A library/cache conflict blocks the new path too. The server revalidates render identity and performs its existing verified pre-write backup.
- The Aux confirmation explains it replaces local clip output, needs Personal Mix for local listening, and is **not** Sonar Microphone injection. Local restoration changes only library.json's output and revision; all sound IDs, audio bytes and button assignments remain.
- A normal tap plays through the selected PC output. A held private preview still uses only this terminal's Web Audio output and never issues a host-play command, even when host clips target Aux.

No real PC library was accessible or backed up here. Before upgrading, run the existing backup helper in the old installation and require created=true, verified=true, the expected nonzero sound count and empty source.errors. Keep originals. The automatic guard is additional protection, not proof the user's current library has already been backed up. No schema migration or original removal is needed.

## Microphone injection — decision required before implementation

| Route | Additional component | Required change | Current status |
| --- | --- | --- | --- |
| Existing Sonar Mic + Aux → Sonar Stream Mix → games | None beyond supported Sonar Streamer mode | Deliberate mix membership and games' input changed to Sonar - Stream; leave physical Arctis mic/processing unchanged | Documented vendor capability; not configured or hardware-tested here |
| Sonar - Microphone (processed voice) + effects → external mixer → virtual recording output → games | A virtual mixer such as Voicemeeter with its recording output; a separate cable only if the chosen topology needs it | Games must use the mixer's combined recording endpoint; adds driver/software, routing/latency and availability dependencies | Explained only; not installed, implemented, or claimed verified |
| Effects directly into unchanged Sonar - Microphone, without changing Sonar's physical input | No supported direct-injection API identified | Cannot satisfy through ordinary render-only playback; a cable by itself does not add a mix inlet to this endpoint | Unimplemented; exact requested endpoint constraint remains unresolved |

A plain VB-CABLE transports audio between its render and capture ends; it is not by itself a capture-plus-render mixer. Putting a mixer **before** Sonar and selecting it instead of Arctis as Sonar's input would violate the physical-input requirement and is excluded. A downstream mixer can preserve Sonar processing but becomes a dependency for the combined game stream; do not promise voice continuity if that mixer exits. UMBRA must remain a clip-only branch.

No new virtual driver, external mixer, private Sonar API, configuration-file edit, default-device change, game-input change or Sonar setting was applied. The next consequential choice is whether games may use Sonar - Stream while retaining the existing physical microphone and processing. Do not implement an external workaround before that choice.

## PC verification and rollback

After the verified old-library backup, extract the new package separately and copy the entire soundboard_data folder while both servers are stopped. Keep the old installation and private configuration; preserve hostname/port/browser profile and voyage storage. No simulation runtime or saved voyage schema changes in this correction.

Open Instant Buttons → Audio calibration / Sonar / verified backup → Restore PC headphone playback. Inspect the endpoint against Windows Playback devices. Choose the headphone **playback** device (possibly a Sonar playback channel already feeding headphones), save, and tap an existing sound at a safe volume. Confirm audible sound, voice still working, all imported buttons present, and selection retained after server/browser restart. If the error concerns DSP, use the existing explicit Emergency Audio Reset to disable UMBRA processing; do not change Sonar voice processing. Do not select any microphone input as an output.

Hold a sound to preview and release to stop. The preview uses the browser terminal's current output, so on a tablet/phone it plays there, not automatically on PC headphones. Real receiving-game/OBS/loopback and acoustic isolation must still be tested before calling it private on the user's installation. For a later broadcast test, check voice alone, effect alone, both together, private hold absent, disconnect, normal close and force termination at the actual receiving input. A level meter alone cannot distinguish those sources.

Rollback: stop the new server, retain the whole private library and backup, and start the old installation with the same library folder copied while stopped. Schema 1 stays compatible. This correction never changes external settings and cannot revert changes it did not own. Full C injection and physical audio acceptance remain incomplete.
