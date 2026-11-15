# Phase 4.7C engineering notes

## Dispatch root cause and repair

The legacy Field Operations panel rebuilt `fieldcrew` on refresh, discarded its value, and ignored `launchTeamJob()`'s rejection. A preferred scientist also filled a preferred slot and then the science slot again; the resulting two-scientist team failed the required-engineer check. These are independent faults, not evidence that crew should teleport or readiness checks should be bypassed.

Selection is now a per-destination localStorage interface preference. Focused native selection defers the legacy redraw. The dispatch helper fences writer/backup state, chooses the actual direct proposal, reports results, persists the proposal/preference and uses the existing manifest/crew routing. Required roles already filled are skipped; an off-role preferred person needs three actual eligible crew. Early orbital/shared-launch blockers are explicit. Existing Economy, Teams, ExpeditionOps and Knowledge own actual departure, gear, fifty-minute transit, field work and debrief.

## Rendering

`ForwardArt.rover` is one pure exterior asset, shared by cargo and field renderers. The vehicle's6.2×2.5×3.1m state and equipment are not migrated or replaced. New captured images use the new art; original stored PNGs remain untouched. `FieldArt` varies structural presentation from the observed terrain kind, purpose/name, depth and camera state. It does not look up undiscovered global rooms or add lore/evidence through rendering.

## Optional event media

`event-camera.js` samples the actual displayed available drone canvas. Per-camera ephemeral prebuffers hold at most three samples; active event jobs cap at four, seen IDs at64. New optional `clip.motion` is attached only to an actual recent event. It carries source camera, event ID, simulation ticks, monotonic capture times and PNG pixels. Maximum10 frames/96KiB, with PNG/type/tick/ordering validation in DroneSchema. Existing motion is never overwritten after reopening. Original minute frames and existing clip/host retention bounds remain.

The optional burst lasts roughly625ms after its first observed event sample; actual cadence follows full/reduced/minimal rendering. Completion schedules one fenced ordinary save. No high-rate capture occurs while paused, catching up, hidden or optically disconnected. This is a short captured procedural sequence, not physical recorded footage, encoded video/audio, continuous background recording or invented recovery of absent pixels. Static scenes can legitimately yield static clips. Existing onboard minute captures continue independently and preserve custody.

Local/remote playback selects retained motion frames when present, otherwise original captured minute frames, otherwise labeled source-state reconstructions. Selecting a different record invalidates an older asynchronous load. The UI never presents another record's pixels as a missing record. Large media are omitted from projections, not from the world/save. The telemetry preview remains bounded at110,000 bytes; its server publication guard remains131,072 bytes.

## Received archive transfer

`record_service.py` and `record-transfer.js` implement a separate read path:

| Endpoint | Authority | Purpose |
| --- | --- | --- |
| GET `/api/icarus/record?id=…` | Existing paired token; ID advertised in received telemetry | Queue/poll full original public record |
| GET `/api/icarus/host/record-requests` | Existing host key and current owner/generation lease | Read pending requests |
| POST `/api/icarus/host/record-chunk` | Existing host key and current owner/generation lease | Supply one bounded chunk |

Host reads use `DroneOps.receivedRecord`, never raw onboard clips. Generation changes clear transfer state. Four jobs,60-second TTL,48000-character base64 chunks, at most16 chunks and512KiB decoded JSON bound memory and work. Completed cache entries can be evicted for later requests. Missing/oversized originals report an error; no source recording is deleted or renumbered. Repeated chunks are idempotent. The server keeps no new persistent world/media files. Existing commands and heartbeats are independent of this read service.

No new external service, executable, system modification or runtime dependency is added; the server addition uses Python's standard library. New POST bodies have a65536-byte endpoint-specific cap, below the unchanged publication cap. Unpaired reads, unadvertised IDs, expired tokens/generations, spoofed record IDs, malformed chunks and oversized assemblies are rejected.

## Compatibility and boundaries

The existing voyage/database namespace, writer locking, canonical IndexedDB snapshots, compatibility worker, original records and calendars remain. Old clips with no motion property are valid. There is no forced discovery/encounter/death or altered simulation multiplier. New UI preferences are separate from saves.

The latest available source is Phase4.7A plus the existing ship-dock escorts. No independent Phase4.7B code was present on GitHub. Compatibility with an unpublished B build cannot be asserted; merge into that source before replacing such an installation. Documented camp-based services remain incomplete, as do native APK rebuilding and physical-device validation. The whole Phase4.7 release is not declared complete by these surveillance changes.
