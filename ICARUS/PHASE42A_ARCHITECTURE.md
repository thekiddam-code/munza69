# Observation Protocol architecture

## Baseline and boundaries

Engine baseline is Phase 4.2 `7f3fb0d`; main `0ce493c` supplied only additive UMBRA Android launcher/source/downloads and the ideas backlog. The dedicated branch merges those without replacing the newer ICARUS engine with main's older engine. The 112-file test runtime is pinned independently of docs and packaging. Crew identities, existing namespaces/schema-1 saves, histories, routes, resource/repair/medical/science/creature authorities, knowledge and calendar remain.

Canvas 2D was chosen after official LittleJS/Phaser/examples/Excalibur/Pixelorama research. No new rendering dependency, external artwork, copied game assets or independent engine was installed. See RENDERING_DECISION_PHASE42A.md.

## Rendering and real intent

- `observation-model.js` is a pure, bounded projection of existing rooms, equipment, atmosphere and actually observed crew. It separates room instrumentation from camera visibility. Private A05/A06 quarters, A07 executive suite and A10 hygiene have no ordinary camera actors or camera-bank entry. Biological sensors are explicitly unavailable; unknown signatures are not read from hidden organisms.
- `pixel-camera.js` draws original layered pixel interiors at 384×216 and cached reusable 36×54 character frames. Roles/identity details are stable. Work, carrying, care, eating, rest, search and conversation cues derive from actual tasks and physical state. Powered consoles animate without manufacturing malfunctions. Pixel scaling uses nearest-neighbor and aspect-preserving fit, inside camera scenes only.
- `crew-observation.js` advances only at physical simulation steps. A conversation seeker looks, chooses an actual eligible co-located partner, approaches for actual simulated time, asks through the established CrewLife/Knowledge path, talks only after a genuine recorded interaction, or waits/gives up/interruption. No view chooses partners or advances tasks. Actual speakers/listeners face each other at shared interaction anchors; real route/capacity/supply authorities stay upstream.
- Room anchors are a compatible presentation layer, not new authoritative coordinate physics. Walk-only interpolation uses previous/current received positions in the same node and never predicts movement through rooms/doors. Cross-room changes and work-state changes snap to their authoritative state. Advanced furniture/crowd collision remains limited.
- Corridor follow is a navigation-derived procedural reconstruction. It is separate from ordinary rotating cameras and never a claim of recorded corridor video. Historical movement replay retains the original schematic path and explicit reconstruction labeling.

## Surveillance and interfaces

`observation-ui.js` drives one main scene and four previews from one projection, with 12-second bank rotation, pause/resume, next/previous bank, pins, manual promotion and separate local UI preferences. Manual selection stops AUTO direction and remains held until another user selection. Main animation is capped; previews refresh at lower frequency. Visibility/reduced/minimal/paused presentation settings do not affect simulation ticks. The original camera is retained, with a classic schematic option for its sector/scan controls and old style choices. Those sector controls are explicitly disabled in pixel mode rather than pretending to pan an unrelated scene.

The UMBRA browser receives the same `observation` projection through existing fenced telemetry/SSE. It loads rendering/projection UI code only, never the simulation. Stale feeds clear live actors and show stale/unavailable status. No remote world uploads or alternate save namespace are introduced.

`ship-schematic.js` presents real atmospheric temperature, pressure/oxygen, existing equipment/door/hazard status and effective lighting. Zoom/scroll/focus are presentation only. Lighting uses additive persistent `roomLighting` with finite 0–1 values, gated by existing ship power. It changes illumination; it is not a new HVAC/circuit/economy controller. Unsupported CO₂, biological sensing, HVAC target control, circuit switching and suppression remain explicitly unavailable. No secret camera implementation.

Crew quick actions open source-limited received personnel/assessment/history/relationship information and available cameras. Bridge never receives private psych scores/preferences. Creator retains existing private inspection; menus do not confer additional permissions.

Home headers now toggle collapse with click/Enter/Space using the existing per-screen layout store. Separate collapse buttons are removed; embedded controls do not collapse headers. The broad status strip is compact/non-sticky so it does not overlap Focus. Themed scrollbars retain scroll chaining. Pause/Resume is intentionally Bridge-accessible under the new approved specification; speed/test/reset/debug remain Creator-only.

## Protocol and persistence

The richer projection exceeded the old modern host packet limit in a real late-save fixture: 78,632-byte request. The dedicated authenticated host publish cap is now 128 KiB. Other command requests remain 4 KiB; legacy telemetry remains bounded to 14,000 serialized characters. `observation` and `operations` are removed from the legacy projection, preserving installed-client response shape. Pairing, host ownership, heartbeat, stale detection, command deduplication and save fencing remain; room-light commands use a strict whitelist and normal dispatch/ack path.

New saved fields are additive (`socialSearch`, conversation facing/point, observation tick, optional roomLighting). UI bank/pin/style/layout preferences remain outside world saves. Old work is adopted; no voyage reset or crew generation. The known 20× timing issue remains deferred to Phase 4.1.1; the actual normal/holiday production timer tests are retained.

## Android boundary

Main now contains a separate Galaxy S24+ Kotlin/Compose launcher project and existing APK/source downloads; they are retained byte-identically. It opens the configured Remote Deck in the browser and is not the original installed Tab S5e project. That older project's recovery/identity remains separate. This batch changes browser/server functionality only and does not replace or rebuild either installed app.
