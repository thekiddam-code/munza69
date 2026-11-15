# ICARUS Phase 4.7C — Dispatch, Rover & Surveillance

This build continues the latest available repository implementation, `codex/phase47a-field-deployment`, preserving the catch-up fix, saves, vehicle/camp lifecycle and ship-dock escorts. No separate Phase4.7B source was available on the remote branches. Compatibility with additional B code installed outside this repository is unverified; do not overwrite that installation. Camp-based medical/drone/ATV services were already documented as unfinished in the available source and have not been removed or claimed complete here.

## Install, backup and rollback

Export a complete backup and retain the previous application folder. Stop its server and close its authoritative tabs. Extract this ZIP separately, retain your private pairing configuration, and use the same browser profile, hostname and port only when upgrading the supported repository baseline. Run `Start_Remote_Deck.bat`, refresh assets with Ctrl+F5 if necessary, wait for actual startup readiness and select ENTER ICARUS. Do not clear IndexedDB, create another voyage, delete writer locks or disable antivirus.

If your current B build has additional unpublished source, merge these changes into that source first; test a backup copy in an isolated profile before pointing this build at its voyage. Nothing in this development task changed your Windows installation or original backup.

Before rollback, export a post-update backup. Pause this build and restore the pre-update backup here, then close its tabs/server and run the retained earlier build. Older validators do not understand new optional captured live-clip data. Keep both backups; do not use an old build to automatically recover or discard newer state.

## Expedition repair

Open **Missions → Destinations → Asteroid or Derelict → Expedition**. Your preferred specialist survives live refresh and restart as an interface preference. The native picker is not rebuilt while focused. Dispatch now reports acceptance, a queued proposal's blocker, or a writer/readiness/resource error. A preferred scientist fills the science role once; the team still needs engineering coverage. A preferred person outside the required roles needs a larger valid team, not a silent substitution. Pending proposals retain the chosen specialist and do not allocate cargo repeatedly.

Follow the real collection/staging/transit/field stages and source-limited crew status. A dispatch order is not an arrival. Paused simulation, unsafe systems, unavailable crew, occupied transport, insufficient suits/resources and exhausted objectives remain valid blockers. Read-only spectators cannot dispatch.

## Exterior redesign

FOC-01 now uses a shared angular industrial rover asset in C03 and field views: integrated cockpit, reinforced hull, three suspended axles, equipment bays, work lights, antennas and mismatched service panels. ID, nickname, dimensions, original stock, footprint, transport, camp and saved condition are unchanged. There are no new interiors. Existing captured PNGs are not repainted; later state reconstructions use the current renderer and remain labeled reconstructions.

## Surveillance and records

Live drone views update while visible, using actual received location, traversal, battery, optics, signal, lighting and nearby actors. Hidden panels avoid extra live draws; pause/reduced-motion settings remain respected. Sectors/Facilities/Drones organize received intelligence. A location with no current camera is labeled a report, not given a fake feed. Industrial mining, shafts, natural caverns, observed boreholes and actually accessed military/corporate facilities have distinct source-backed architecture. Unknown/sealed locations are not added for visual variety.

New meaningful drone events can retain short **captured live procedural clips** from the actually displayed stream, including a small pre-event buffer when available. Capture is best-effort, up to8 samples/second,2–10 retained frames and96KiB of PNG data per optional clip. It never advances the world, fabricates travel, records private/unreceived cameras, or continuously saves video. Paused/catching-up/hidden/unavailable views do not generate high-rate clips. Existing simulated-minute event PNG/state sequences remain the fallback and remain playable. There is no encoded audiovisual/WebM recorder or promise of cinematic motion in an event that was physically static.

Select a record or use **Load original record** before playback. Remote terminals retrieve full original received records on demand, separate from the110,000-byte telemetry preview. A record larger than512KiB must be viewed on the host. Transfers require the existing pairing/host lease, use chunks below the existing publication cap, and are bounded in memory and lifetime. A lost connection never turns an unreceived onboard clip into a public archive record. Play/pause/replay and scrubbing use retained images; state-only frames are explicitly reconstructed.

Records1–12 in the supplied Episode2 backup were retained but hidden by an old eight-record UI slice. They remain under their original IDs, together with all retained records. Missing pixels are not fabricated. Later retention evictions remain distinct from unseen/onboard data; existing24 host/8 onboard caps are unchanged.

See PHASE47C_VALIDATION.md for actual tests, screenshots, source hashes and limits. Physical Windows/Samsung/TV/Tailscale/antivirus and native APK rebuilds remain unverified; the existing web/native integration paths are preserved.
