# ICARUS Phase 3.5 — Cinematic Refinement & Reliability

**Status:** authorized implementation assignment, not completed work. **Branch:** `codex/cinematic-refinement-phase3-5` from `codex/cinematic-living-world-phase3`.

## Purpose
Finish and refine existing Phase 3 systems before authorizing Phase 4 or any new universe scope. Preserve the user’s existing voyage and the functional Phase 3 Lite build.

## Source of truth and baseline
Read `AGENTS.md`, `FINAL_DESIGN.md`, `FINAL_RELEASE_ROADMAP.md`, `PHASE3_ARCHITECTURE.md`, `PHASE3_VALIDATION.md`, `PHASE3_LIMITATIONS.md`, `PHASE3_PROGRESS.md`, `ENGINEERING_PHASE3.md`, `SECURITY_PHASE3.md`, `README_PHASE3.md`, `PHASE2_LIMITATIONS.md` and actual source/tests. Baseline evidence: 241 Node, 55 cinematic Chromium, 30 stability, 44 compatibility, 2 production, 3 bridge, 15 emulated mobile; four 7/30-real-day campaigns. These are **baseline report claims, not Phase 3.5 results**. Validate the exact branch and package anew.

## Invariants
- Keep Phase 2 individual knowledge, source/privacy delivery, physical location, ecology, finite resource/paid repair, original military asteroid rooms 21–24, all crew/deaths/history, evidence custody and autonomous captain/SOL authority.
- Keep 4× real-time production clock, nine synchronized 1× holidays, real local Monday–Sunday archives, six-hour bounded offline recovery and source-labeled footage. Never rewind or fabricate state/history, footage, conversations, casualties, rescues or discoveries.
- No forced disasters, kill quotas, weekly narrative quotas, guaranteed Lazarus outcome, mandatory missions, additional procedural galaxy/factions/economy or new network/PC-control abilities for agents.
- Preserve existing browser origin, local port 8765, Android thin-client pairing, Windows launcher and legacy Core/Extended Universe isolation. No disabling security warnings, bypassing AV, opaque binaries or uncontrolled external dependencies.
- The captain may intervene; spectator controls never mutate the world. Reduced-motion and keyboard/touch access are mandatory considerations.

## Implementation order and acceptance gates

### 3.5A — Readable character animation and environment
- Audit existing embodiment, camera, spatial/nav, crew-life, equipment and treatment state. Implement more expressive **procedural 2D** pose transitions (walking, lift/ladder/wheelchair travel, carrying, tool use, repairing, medical work, rest, conversation, alarm response) sourced from actual actor location/task/equipment.
- Distinctive but restrained silhouettes and motion by build/mobility; no fictitious work gestures or invalid handoffs. Respect stationary/disabled actors, actual travel edges, and reduced-motion preference. Optimize render changes.
- Automated tests for animation-state mapping, location, pause, reduced-motion, item provenance, no render mutations, historical snapshot truth; browser screenshots for desktop and Tab S5e landscape emulation. Do not claim full anatomical 3D or authored art.

### 3.5B — Cinematic camera, provenance and replay
- Improve shot composition, camera transitions and readable overlays using only actual observed/recorded physical state. Camera cannot see inaccessible areas or create footage retroactively.
- Distinguish **LIVE**, **RECORDED STATE SNAPSHOT (schematic, not video)**, **RECONSTRUCTION (source-derived)**, and **TELEMETRY**. Preserve exact event/source IDs and source availability. Never label a generated scene as genuine video.
- Add skippable/pauseable playback, manual camera override and graceful no-camera/quiet scenarios. Avoid video export/encoding unless a complete tested pipeline is justified and labeled.
- Tests for provenance, missing frames, no duplicate source, reload, inaccessible view, pause, camera-only changes not advancing physical simulation.

### 3.5C — Sunday chronicles, grounded awards and rare Legendary Kill Cam
- Refine weekly 3–5-minute *target* pacing while allowing shorter sparse weeks. Archive true highlights, character relationships/fates, unresolved threads, SOL assessment, rolling credits. Retain 12-week film bound unless safely improved.
- Add **evidence-based** optional awards (rescue, service, scientific contribution, accidental achievement), without fictional achievements or obligatory awards.
- Build automatic extraordinary-lethal candidate classification **only from retained causal events** (danger, disadvantage, ingenuity, impact, rarity, corroborating evidence); no fabricated rarity score or kill footage. Eligible clip requires actual retained recorded state plus a corroborating public lethal source. If evidence absent, no Legendary segment; optionally describe a sourced event in ordinary chronicle with correct reconstruction label.
- Test ordinary death excluded, extraordinary fixture accepted, no-recording rejected, accidental sourced event, empty week, Monday boundary, archive/reload, privacy/source access.

### 3.5D — Crew individuality and SOL editorial quality
- Review actual repeated dialogue/memory outputs from deterministic campaigns. Improve contextual variety and character-specific observations using real experience/relationship/job/knowledge, not random conflict/romance or global omniscience.
- SOL commentary must be source-backed, uncertainty-aware, concise, sometimes dry, and appropriately quiet during uneventful periods. Avoid duplicate notices and emergency-inappropriate humor.
- Tests for delivered knowledge, private canon exclusion, social co-location, grief timing, repeat suppression, source provenance and persistence. Record quantitative repetition samples and human-review examples.

### 3.5E — Reliability, accessibility, release
- Design and implement incremental/streaming history export/import and large backup handling **without truncating history**, with transactional integrity and explicit progress/cancel/recovery. Protect against hostile concurrent same-origin tabs via a single-writer ownership policy; spectator tabs may be read-only. Prevent silent overwrite; test crash/restart and rollback.
- Verify keyboard focus, contrast, reduced motion, readable controls, touch landscape and responsive layouts. Measure rendering, memory and save growth. Do not claim hardware qualification from emulation.
- Re-run Node, Chromium cinematic/stability/compatibility/production/bridge suites, Android touch emulation, Phase 1/2/3 backup migrations, exact reload, and multi-seed 30-real-day + adverse campaigns. Add tests for single-writer collisions, interrupted import/export, corrupted chunks and long history.
- Record actual source commits, package file hashes, suite results, measured performance and failures in `PHASE35_PROGRESS.md`, `PHASE35_VALIDATION.md`, `PHASE35_LIMITATIONS.md`, `ENGINEERING_PHASE35.md`; update `FINAL_RELEASE_ROADMAP.md`.
- Prepare source-only `ICARUS_Cinematic_Refinement_Phase3_5_Lite.zip` and manifest/SHA-256 plus installation/rollback steps; no binary wrappers or unverified safety claims. Keep a pristine Phase 3 folder and pre-upgrade complete JSON backup.
- Native Windows launcher/input, actual Galaxy Tab S5e LAN/touch, Samsung TV, antivirus scan, sustained human story review and final authored audiovisual art remain **unverified until actually tested**. Explicitly mark blocked/unavailable gates rather than inventing success.

## Codex workflow
1. Start with **3.5A**, inspect architecture and tests before editing. Implement code and focused tests, commit verified batch. Continue through B–E in independently testable increments.
2. Prioritize working implementations over documentation. Fix defects before marking milestones complete. Keep original runtime intact until package/migration verified.
3. No claims of final release or complete cinematic video production unless evidenced. Report precise completed vs incomplete work and the next action.
