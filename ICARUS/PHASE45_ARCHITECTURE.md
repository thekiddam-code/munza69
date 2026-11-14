# Phase 4.5 renderer, interaction and boot architecture

## Baseline and scope

Phase4.4 deliveryfd70501 was inspected against its verified128-file runtime34fd122. The running detailed surveillance path is ObservationModel → ObservationUI/OperationalUI → PixelCamera, including primary, four previews, field cameras and received field-state reconstructions. FieldArt introduced in4.4 was active on asteroid feeds; the ship still used the older generic walls/pipes/console arrangement and36×54 rig with wheelchair wheels appended to standing legs. No service worker exists. Static responses previously had no explicit revalidation policy.

This update changes that active path. It does not create a second simulation/showcase renderer, regenerate rooms or introduce a new scheduler. Optional classic schematic mode and existing chronicle presentation remain available. Final runtime4bd2dadbd6e6541ef118e04b50b30ddbf561ae19 contains134 runtime files. Complete final regression, source/provenance campaigns, actual-time watch, visual captures and extracted-package checks use this immutable export. Earlier7310ddc/f007166/6ee7c6d runs are diagnostics/refinement evidence, not silently substituted as final. Later docs/package commits must preserve all134 hashes; PHASE45_VALIDATION.md records exact results.

**Registry correction and explicit user choice:** the30-room registry has A09 Recreation and A03 Observation Lounge, not two Recreation rooms. User chose “Keep A03; defer gym conversion.” A09 becomes Crew Lounge; A03 remains Observation Lounge with its existing watching/meeting/quiet routines. No gym, exercise task, fitness score or replacement compartment is fabricated. IDs, door/lift topology, privacy and camera IDs are unchanged.

## Active visual modules

| Module | Responsibility |
| --- | --- |
| room-design.js | Existing ID→visual function mapping; actual lounge/table/bunk interaction points and a clear foreground approach lane. No new rooms or independent ship map. |
| room-art.js | Original cached384×216 structural, wall-equipment, furniture and thin foreground layers. Distinct bridge, communications, engineering/reactor/life-support/workshop, medical, science/containment, cargo/storage/archives, lounge/observation, quarters, airlock/hangar and corridor/lift silhouettes. |
| character-design.js | Original articulated60–62px default standing anatomy, persistent public appearance descriptors, build/clothing/hair/accessory/gait variation and coherent49px seated wheelchair rig. Pure rendering/descriptor projection plus explicit migration API. |
| room-interactions.js | Existing ordinary-task loop extension: approach, turn, seat, work and rise at registered lounge/table/bunk positions; persistent per-person progress and bounded placement. No renderer-side activity generation or new clock. |
| boot-screen.js / .css | Actual readiness-event modal, real stage count, early host-code verification, online/read-only/disconnected/failure status, retry/observe, keyboard/focus/inert handling and reopenable status control. |

PixelCamera delegates to these modules. Its former generic detailed room/sprite functions are removed, rather than remaining as an accidentally active parallel path. FieldArt remains the asteroid environment layer and draws the new character rigs through the same PixelCamera. Room background cache≤64, articulated sprite cache≤512. Caches contain presentation canvases only and are not serialized into world saves. Light/power/fault/door/lift changes invalidate relevant static layers. Live interfaces retain existing reduced/minimal/paused behavior; stride/rolling frames derive from actual displacement, not a visual movement timer.

Engineering and console anchors now meet the rebuilt floor plane. Medical/lab furniture work surfaces are proportioned against the taller rig. Sprite limbs are redrawn with articulated knees/arms; the old bitmap is not vertically stretched. Wheelchair geometry includes seat/back, supporting frame, rear wheels/spokes, front casters, footrests, arm supports and seated legs/hands. Roll/turn states never select standing legs. The side-view turn is a brief actual heading change, not a full3D turn animation.

## Grounded ordinary furniture work

The authoritative task loop calls RoomInteractions once per simulated minute. It uses actual room/target/route/task/readiness and existing Embodiment. Supported ordinary lounge recreation, dining and bunk rest approach through the clear foreground lane before the existing task timer runs. Wheelchairs stop at accessible front space instead of standing on a sofa. Existing seat claims prevent duplicate use of the same fixture; unavailable seating does not block an urgent task indefinitely.

Matching approach/turn counts as travel and seat/rise as waiting in CrewLife's existing ledger. New ordinary social commitments wait for those transitions; stale metadata from a changed task cannot suppress a new emergency/maintenance responsibility. Emergency, maintenance, research, medical, expedition, private-event, fatigue and low-gravity controllers retain priority. No unsupported fitness benefit or free food/resource is introduced. Existing rest/meal/social/economy consequences remain the source of benefits.

This is a bounded interaction extension. Critical engineering/medical/research work retains existing authoritative station controllers/anchors; no full per-pixel collision solver, metric interior walking mesh or measured chair turning-radius simulation is claimed. Decorative furniture stays behind the clear approach lane and does not add invisible topology obstacles. Existing wheelchair route restrictions, ladders, lift gates and travel costs are retained. See limitations for the physical precision boundary.

## Identity, history and save migration

`crew[].visualAppearance` version1 contains bounded public physical descriptor values, derived deterministically from stable identity only when absent. Existing supported descriptors are retained. Explicit bootstrap/backup-restore migration runs outside pure routine/view functions. Body/locomotion, names, memories, relationships, history and random entropy are not replaced. Observation DTOs and new field frames copy these public descriptors; old historical states fall back to deterministic identity for a clearly labeled reconstruction, never claimed original footage.

`crew[].roomInteraction` and `roomPlacement` preserve actual ordinary approach/heading/fixture progress. They are bounded scalar records, not unbounded histories. Optional schema checks reject malformed/future/out-of-range new descriptors/coordinates without requiring those fields on old saves. The existing schema1 save envelope, origin keys, history storage, atomic backup transfer and writer fencing remain. Old builds cannot reliably advance new interaction fields; rollback uses a pre-upgrade backup.

## Real boot and authority

Boot markup loads immediately in the host body, before the heavy simulation/persistence closure. Stages are driven by actual module load, Durable availability, restored/migrated world, ship-system initialization, Host bootstrap/claim/heartbeat and surveillance-UI installation. Progress counts confirmed events; no timed fictional progress, forced delay, invented sensor readiness or camera-dependent authorization.

`/api/icarus/host/auth` is a **read-only localhost + existing host-key check**. It reports verified credentials and never grants a lease, publishes telemetry, modifies saves or starts the simulation. Host.authorize can request ownership only after Durable confirms exclusive storage and only through the existing Host.acquire/server generation fence. Wrong codes and another owner remain read-only. The existing localhost bootstrap/automatic verification continues; Windows host key is distinct from the remote pairing PIN. Root canWriteWorld still requires both Host and Durable.

A pending connection, denied/lost ownership, outage or failed asset/init receives an explicit diagnostic. Retry reloads without replacing the world. Ready/read-only observation is separate from command authorization. Boot can reopen through System Status; its visible modal makes background controls inert and honors reduced motion. Core timing remains outside rendering. The existing static-development-server fallback is retained for legacy harness/production-clock tests and clearly labeled; it does not prove production server authorization.

UMBRA stays a thin terminal. Its existing pairing panel remains available before telemetry/cameras; it does not initialize a remote ship kernel or use the host code to create a second world. New room/character art is shared receive-only code on phone/tablet. Remote redirects, TV, desktop integrations and native app/source are preserved. Tailscale uses existing remote pairing and authority paths, not a cloud host. Actual hardware tests remain separate.

Static HTML/JS/CSS now requires cache revalidation and the updated pixel import has a version query. No service-worker cache or duplicate detailed renderer is introduced. Manual hard-refresh/cache/hardware validation remains an installation gate; source-file hash equality is not a claim about an untested physical browser cache.
