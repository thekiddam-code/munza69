# ICARUS Phase 4A — SOL Command Interface and Usability

**Implementation status:** specification only, NOT coded. **Branch:** `codex/sol-interface-phase4` based on `codex/cinematic-refinement-phase3-5`.

## User-approved direction
Prioritize the **graphic interface** and ease of learning before additional world simulation features. Existing UI has accumulated controls, many unclear or scattered. Organize **separate tabs** with clear responsibilities, simplify navigation, and add contextual explanations. The user plays **SOL, the ship's AI**, while SOL's established autonomous controller continues running the ship. Preserve a safe **20× testing speed**, distinct from normal 4× and nine synchronized holiday 1× pacing.

## Baseline audit and source of truth
Read `AGENTS.md`, `FINAL_DESIGN.md`, `PHASE35_VALIDATION.md`, `PHASE35_LIMITATIONS.md`, `PHASE35_ARCHITECTURE.md`, `FINAL_RELEASE_ROADMAP.md`, `README_PHASE35.md`, and current `web/icarus.html`, `web/unified-ui.js`, `web/cinema-ui.js`, `web/writer-ui.js`, `web/backup-ui.js`, `web/calendar.js`, `web/anthology-ui.js`, `web/film-ui.js`, `web/frontier-ui.js`, `web/living-frontier-ui.js` and existing browser/Node tests.

Observed current UI: `icarus.html` is a very large integrated document with an existing six-page menu (Home, Operations, Personnel, Notes & Records, Upgrades, Settings), separate location navigation, a dynamically relocated live-widget Home, many nested panels and remote controls. Normal `#speed` click is **disabled outside `__icarusSoakMode`**; in soak mode it cycles 1/5/20, while `renderUnifiedClock()` labels production Automatic 4×/holiday 1×. Do **not** claim that ordinary user-facing 20× currently works. Existing captain/SOL authority labels and actions need a coherent player-facing SOL interpretation, not a world rewrite.

## Guiding product concept: the user IS SOL
SOL is a **single intelligence** with two control layers:
- **Autonomous SOL:** existing decision engines operate ship, staff, repair, travel, science and emergencies without waiting for clicks.
- **Operator-directed SOL:** the human user can observe, investigate, adjust priorities, authorize feasible actions and override temporarily. Returning control to autonomy is clear and immediate.
- Do not invent a second independent SOL, rewrite ship/crew lore or alter saved source authorship. Keep legacy captain data/API semantics compatible, but re-label user-facing controls as **SOL directive**, **Release to autonomy**, **Explain decision** etc. Where an in-world captain/crew command role exists, preserve it as an NPC role; do not silently erase or merge characters.
- Provide a visible **AUTONOMOUS / DIRECTIVE ACTIVE** indicator, explanation of actual current controller, scope, and release behavior. Every command retains physical safety checks, permissions, actual resource costs and audit provenance. No unrestricted AI text generation, real host commands or network expansion.

## IA and interaction architecture
Implement a clear main navigation with seven distinct destinations, using concise labels and responsive layout (tablet scrollable or compact menu, not overlapping buttons):
1. **Bridge** — the default landing view: ship status, active risks, current autonomous decisions, short event feed, one primary live camera, quick inspect, and pause/time status. No huge wall of cards.
2. **Ship** — physical cutaway, rooms, systems, atmosphere, equipment, doors, repairs, camera/surveillance; secondary tabs for **Overview / Systems / Cameras**.
3. **Crew** — roster, health/availability, locations, relationships, activity/memory inspector; secondary tabs **Roster / Activity / Medical / Social**.
4. **Missions** — local destinations, actual expedition planning, docking, field operations, assignments and safe SOL directives; secondary tabs **Active / Destinations / Logistics**.
5. **Research** — experiments, samples, source-backed knowledge, science archives, LAZARUS (with clear safety context); secondary tabs **Projects / Evidence / LAZARUS**.
6. **Chronicles** — recent events, source-labeled replays, Sunday films, historical archives, personal/crew records and optional ideas backlog; secondary tabs **Timeline / Sunday / Archives**.
7. **Settings** — interface appearance, accessibility, help, clock/testing, backups, pairing, advanced diagnostics, creator/private-canon configuration; secondary tabs **General / Data / Testing / Advanced**.

This is a *proposed information architecture*, not a demand to duplicate components. Audit actual existing controls and map **every reachable function** into one logical home. Preserve existing real DOM nodes/event handlers where possible; avoid relocating the same live node between tabs during an active interaction or causing hidden reparenting side effects. Avoid duplicate controls that perform different actions with the same label. Keep dangerous actions (New Voyage, import, reset, overwrite) clearly isolated and confirmed. Show emergencies from any tab via a compact persistent status/alert area, with click-through to source context. No unrelated tab should visually bleed into another. Distinguish global navigation from within-tab subnavigation and location selection.

## Interface treatment
- Retain established Alien/Nostromo/Weyland-Yutani corporate industrial look, angular instrumentation, restrained amber/cyan/green, red only for real hazards. Refine visual hierarchy, spacing, typography, contrast, touch target size and predictable back navigation. A cleaner interface, **not** a blank reskin or an invented new 3D world.
- Prefer human-friendly labels and short explanations with expandable technical details. Explain: what this system does, what SOL is doing now, why a command is blocked, what happens on click. Tooltips plus accessible inline help and a concise first-run guided tour that can be reopened. Keep experienced-user fast access.
- Use real source-backed live state, no fake dashboard data, no new telemetry or omniscient views. Camera source labels (LIVE STATE PROJECTION / RECORDED SCHEMATIC SNAPSHOT / RECONSTRUCTION / TELEMETRY) remain accurate.
- Responsive 1920×1080 desktop and physical Tab S5e landscape target (emulation is not physical validation). Keyboard tab order/focus, screen reader labels, touch targets, reduced motion, no accidental double scrolling; avoid enormous nested disclosure stacks.
- Preserve optional HUD density, visual modes, widget preferences and Remote Deck pairing; migrate old per-device UI settings safely. The paired Android tablet remains a thin client, not an authoritative simulation host.

## 20× safe testing mode
- Add a clearly labeled **TEST MODE** UI in Settings > Testing, with **1× / 5× / 20×** options (or 20× toggle plus intermediate choice) and a prominent persistent TEST banner and return-to-normal action. Default normal live voyage remains automatic 4× (1× on nine synchronized holidays).
- Existing `__icarusSoakMode` and `#speed` are diagnostic-only; inspect actual clock code. Build a user-accessible, tested path instead of simply changing button text. 20× must actually accelerate **physical simulation progression** with correct resource, movement, health, ecology, job, mission, knowledge, and source-event accounting, deterministic tick bounds, no skipped decisions or retroactive history, no reentrancy/CPU freeze, and safe paused behavior. Do not accidentally speed up Sunday wall-calendar week boundaries or reinterpret synchronized holidays.
- **Safest default:** create an isolated **test copy of the voyage** (separate namespace/session or explicit snapshot restore) before acceleration. Never silently run a 20× test against the user's sole persistent save; allow intentional testing of an imported copy, clearly identify which voyage is active, and provide a verified return to the original live voyage. Ensure backup/export/test records are labeled so a test cannot silently replace the canonical voyage. If architecture prevents safe clone/ownership, implement a safe alternate test workflow and document limitations rather than compromising data.
- Real-time and test-clock transitions must not double count elapsed wall time or rewrite saved history. One authoritative writer per voyage, atomic durable saves and backup/cancel protection remain. Test while 20× and pause/resume, switch back to normal, save/reload, crash recovery, holiday crossing, Monday boundary, and large archives. Test mode must not invoke extra host/TV commands.
- Keep the production real-week archive policy unchanged. If test-copy simulation uses accelerated physical minutes while the real week stays fixed, explicitly show both clocks and prevent fabricated Sunday archive triggers.

## Acceptance criteria and testing
1. Inventory existing controls and create `PHASE4_UI_CONTROL_MAP.md`: existing ID/handler, new page/subtab, explanation, preserved behavior. No feature disappearance. Screenshot/snapshot baseline before redesign.
2. Implement **Bridge** first as a usable SOL landing screen, then migrate Ship, Crew, Missions, Research, Chronicles, Settings in independently tested batches. Avoid documentation-only completion.
3. Every tab/subtab has clear scope, browser back/forward or stable state navigation, no duplicate or unreachable controls, predictable scrolling, keyboard and touch support. Keep all underlying simulation, crew, archives, resource, calendar, backup and Remote Deck functionality unchanged unless explicitly approved.
4. Verify autonomous SOL continues operating while browsing; directives are attributed to SOL, audit logged, physically constrained, and can be released without creating a second decision engine.
5. Implement and prove user-facing isolated 20× test path with actual tick measurements and invariants. Normal 4×/holiday 1× must remain identical; prove real Monday boundaries and six-hour offline catch-up are not corrupted.
6. Re-run existing Node, cinematic/stability/compatibility/production/bridge, mobile emulation, save migrations, full history/source/resource audits and representative 7/30-real-day campaigns. Add UI browser tests for tab isolation, all controls, onboarding, SOL role, and 20×/normal transitions. Use screenshots of each major desktop and tablet-emulated tab; capture no fictitious visual claims.
7. Document exact commits, real results, failed/superseded tests and remaining native Windows/Tab S5e/TV/AV/human usability gates in `PHASE4_UI_PROGRESS.md`, `PHASE4_UI_VALIDATION.md`, `PHASE4_UI_LIMITATIONS.md`, and update roadmap.
8. Produce source-only **ICARUS_SOL_Command_Interface_Phase4_Lite.zip**, SHA-256, manifest and install/migration/rollback instructions after independent extracted ZIP verification. Preserve untouched 3.5 Lite folder and complete pre-upgrade backup. No AV bypass or unverified device certification.

## Development workflow
Start implementation now with UI control inventory and working Bridge screen, not only documents. Continue in large, independently tested, committed batches. Stop and explicitly report a blocker if safety, save isolation or time semantics cannot be maintained. No universe expansion, forced events, character rewrites, new network services or new graphics engine. Focus on an understandable, visually coherent interface where **SOL runs the ship and the user can step in as SOL**.
