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
1. **Home** — the **default landing page** and customizable personal SOL dashboard. Preserve existing user-configurable live widgets (ship hologram, diagnostics, crew locations, psychological climate, incidents, recent records, equipment, atmosphere, cameras, LAZARUS), their preferences and event handlers. Make layout editing straightforward. Provide a concise overview, optional quick links and no overwhelming wall of cards. **Do not remove Home or replace it with Bridge.**
2. **Bridge** — the ship's dedicated operational command center: current autonomous decisions, ship command state, priority alerts, live camera, SOL directives, quick inspect, and pause/time status.
3. **Ship** — physical cutaway, rooms, systems, atmosphere, equipment, doors, repairs, camera/surveillance; secondary tabs for **Overview / Systems / Cameras**.
4. **Crew** — roster, health/availability, locations, relationships, activity/memory inspector; secondary tabs **Roster / Activity / Medical / Social**.
5. **Missions** — local destinations, actual expedition planning, docking, field operations, assignments and safe SOL directives; secondary tabs **Active / Destinations / Logistics**.
6. **Research** — experiments, samples, source-backed knowledge, science archives, LAZARUS (with clear safety context); secondary tabs **Projects / Evidence / LAZARUS**.
7. **Chronicles** — recent events, source-labeled replays, Sunday films, historical archives, personal/crew records and optional ideas backlog; secondary tabs **Timeline / Sunday / Archives**.
8. **Settings** — interface appearance, accessibility, help, clock/testing, backups, pairing, advanced diagnostics, creator/private-canon configuration; secondary tabs **General / Data / Testing / Advanced**.

This is a *proposed information architecture*, not a demand to duplicate components. Audit actual existing controls and map **every reachable function** into one logical home. Preserve existing real DOM nodes/event handlers where possible; avoid relocating the same live node between tabs during an active interaction or causing hidden reparenting side effects. Avoid duplicate controls that perform different actions with the same label. Keep dangerous actions (New Voyage, import, reset, overwrite) clearly isolated and confirmed. Show emergencies from any tab via a compact persistent status/alert area, with click-through to source context. No unrelated tab should visually bleed into another. Distinguish global navigation from within-tab subnavigation and location selection.

## Interface treatment
- Retain established Alien/Nostromo/Weyland-Yutani corporate industrial look, angular instrumentation, restrained amber/cyan/green, red only for real hazards. Refine visual hierarchy, spacing, typography, contrast, touch target size and predictable back navigation. A cleaner interface, **not** a blank reskin or an invented new 3D world.
- Prefer human-friendly labels and short explanations with expandable technical details. Explain: what this system does, what SOL is doing now, why a command is blocked, what happens on click. Tooltips plus accessible inline help and a concise first-run guided tour that can be reopened. Keep experienced-user fast access.
- Use real source-backed live state, no fake dashboard data, no new telemetry or omniscient views. Camera source labels (LIVE STATE PROJECTION / RECORDED SCHEMATIC SNAPSHOT / RECONSTRUCTION / TELEMETRY) remain accurate.
- Responsive 1920×1080 desktop and physical Tab S5e landscape target (emulation is not physical validation). Keyboard tab order/focus, screen reader labels, touch targets, reduced motion, no accidental double scrolling; avoid enormous nested disclosure stacks.
- Preserve optional HUD density, visual modes, widget preferences and Remote Deck pairing; migrate old per-device UI settings safely. The paired Android tablet remains a thin client, not an authoritative simulation host.

## Button geometry and layout audit — user screenshot requirement

User provided a real screenshot of the current ICARUS / WY DERELICT / ASTEROID location row and the three large **Hold local position / Release to SOL / Recall expeditions** commands. These controls have inconsistent trapezoidal/slanted outlines, disproportionate widths, uneven spacing, and over-dominant visual weight. Similar defects exist across many controls. The user specifically wants **the middle/interior buttons square/rectangular**, and many buttons reorganized into cleaner layouts.

- Audit CSS cascade in `web/icarus.html` before editing: many successive `clip-path:polygon(...)`, `border-radius:0!important`, `--hud-cut`, `--ng-control-cut`, `--lt-cut`, `--ng-corner` and button overrides conflict. Fix the root design tokens and component classes instead of adding more global `!important` patches.
- **Segmented groups:** use square, straight-edged *interior* segments; consistent heights, seams and borders; optional restrained angular cuts only on the **outside** ends. The selected segment must be legible without oversized skewed shapes. Do not force every button to be a perfect square; 'square' here means **straight rectangular edges/corners**, especially middle buttons.
- **Action buttons:** rectangular geometry with modest, consistent corner treatment, content-based width or a measured responsive grid; do not stretch three unrelated commands into giant equal-width trapezoids. Group primary/secondary/destructive actions by function and importance, with predictable gaps, wrapping and alignment.
- **Navigation vs actions:** preserve subtle shipboard visual identity for top-level location/navigation controls, but remove gratuitous slants from ordinary commands, selects, disclosure rows and toolbars. Avoid decorative shapes that clip labels, borders, focus rings or hit targets.
- **Screenshot area:** make ICARUS/WY DERELICT/ASTEROID a compact consistent location switcher within its appropriate Ship/Missions context; present the three local-travel commands as a coherent compact directive toolbar; show orbital location, fuel and travel hold reason as readable secondary status; move verbose story ARC records into Chronicles, retaining quick summaries/links.
- Audit all major pages, nested tabs, modals, Remote Deck controls, home widgets and tablet layouts for overflowing rows, orphaned controls, uneven heights and misaligned groups. Define reusable button sizes, spacing, layout grids, states, focus outlines and touch targets. Test at desktop 1920×1080, narrower desktop, and Tab S5e landscape emulation. Capture before/after screenshots, including the screenshot's location/command region, and prove the CSS change is not confined to one row.
- Preserve all existing actions and disabled/active/hover/focus semantics; no blanket CSS hiding or action removal.

## Muted amber selected-state styling — user-approved

The user specifically finds the existing **bright orange/amber active navigation buttons** too visually dominant (visible on the ICARUS location button in the screenshot). **Tone down amber, make active fills translucent, and reduce glow** across main navigation, location selectors, subtabs, toggles and ordinary selected buttons.

- Establish shared theme tokens, e.g. `--ui-active-amber-fill: rgba(171,117,57,.19)`, `--ui-active-amber-border: rgba(194,147,83,.58)`, `--ui-active-amber-text: #e0c49c`, with adjusted values as needed for real contrast and dark background. These are **starting targets**, not hardcoded requirements.
- Use subtle active borders/indicator strips and readable text instead of bright solid orange fills or heavy neon box shadows. Preserve a clear active/inactive distinction under color-vision differences and reduced motion.
- Reserve strong amber for genuine warnings and red for critical hazards; selected tabs should never compete with emergency signals.
- Apply consistently to **Home/Bridge/Ship/Crew/Missions/Research/Chronicles/Settings**, location buttons, segmented controls and all nested tabs. Hover/focus/disabled states remain visually distinguishable and accessible.
- Fix conflicting CSS rules at their source rather than piling more global `!important` overrides. Add desktop/tablet visual regression screenshots and check text contrast.

## Preserve gradients and subtle color — explicit user clarification

**Do not flatten the interface into monochrome or solid-color rectangles.** User explicitly wants the existing soft gradients, slight color variation and understated illuminated sci-fi edges preserved. Refine rather than remove them:
- Inactive controls: restrained dark teal/cyan-to-navy gradient, low saturation, subtle cool border.
- Selected controls: **translucent muted amber gradient**, not a flat orange block; use layered alpha over the dark base and a legible warm label. Example design target: linear-gradient(145deg, rgba(180,126,65,.30), rgba(116,79,43,.19) 55%, rgba(28,45,48,.85)), with accessible contrast adjustments.
- Panels/backgrounds: layered dark blue-green gradient, slight ambient cyan edge glow, consistent depth and angular industrial feel.
- Remove *excessive* glow and saturated solid fills, not all lighting or visual texture. Retain active/inactive differentiation and reserved strong hazard signaling.
- Preserve rectangular straight-sided interior segments and tidy responsive geometry independently of gradient styling. Validate real browser screenshots on desktop and tablet emulation.

## 20× safe testing mode
- Add a clearly labeled **TEST MODE** UI in Settings > Testing, with **1× / 5× / 20×** options (or 20× toggle plus intermediate choice) and a prominent persistent TEST banner and return-to-normal action. **Primary goal is fast, observable functional testing during active development**. Full save/backup UX hardening is deferred until closer to final release, not permanently discarded. Provide a clear test reset and diagnostic readout (ticks, simulated minutes, active jobs, warnings, errors, actual decisions). Default normal live voyage remains automatic 4× (1× on nine synchronized holidays).
- Existing `__icarusSoakMode` and `#speed` are diagnostic-only; inspect actual clock code. Build a user-accessible, tested path instead of simply changing button text. 20× must actually accelerate **physical simulation progression** with correct resource, movement, health, ecology, job, mission, knowledge, and source-event accounting, deterministic tick bounds, no skipped decisions or retroactive history, no reentrancy/CPU freeze, and safe paused behavior. Do not accidentally speed up Sunday wall-calendar week boundaries or reinterpret synchronized holidays.
- **Revised user priority:** while ICARUS is **still being built**, the user wants to **defer save, backup and progress-preservation polish**, not eliminate persistence from the final product. Use the simplest reliable 20× development-testing implementation, with a clear warning that accelerated tests can alter the current voyage and an easy deliberate reset. A separate test-copy/clone system is **not required for this phase**. Retain existing basic persistence, recovery and single-writer protections; avoid silent corruption, but do not delay the visual interface with complex save namespaces, transactional export redesigns or migration UX. Revisit full backup/recovery hardening before final release.
- Real-time and test-clock transitions must not double count elapsed wall time or rewrite recorded history. Keep existing single-writer and basic automatic recovery safeguards; don't introduce elaborate backup UI as a Phase 4 deliverable. Test 20×, pause/resume, switch back to normal, restart, holiday crossing and Monday boundary. Test mode must not invoke extra host/TV commands.
- Keep the production real-week archive policy unchanged. If test-copy simulation uses accelerated physical minutes while the real week stays fixed, explicitly show both clocks and prevent fabricated Sunday archive triggers.

## Acceptance criteria and testing
1. Inventory existing controls and create `PHASE4_UI_CONTROL_MAP.md`: existing ID/handler, new page/subtab, explanation, preserved behavior. No feature disappearance. Screenshot/snapshot baseline before redesign.
2. Preserve and simplify **Home** first as the default customizable landing screen, implement a distinct usable **Bridge** command screen, then migrate Ship, Crew, Missions, Research, Chronicles, Settings in independently tested batches. Avoid documentation-only completion.
3. Every tab/subtab has clear scope, browser back/forward or stable state navigation, no duplicate or unreachable controls, predictable scrolling, keyboard and touch support. Keep all underlying simulation, crew, archives, resource, calendar, backup and Remote Deck functionality unchanged unless explicitly approved.
4. Verify autonomous SOL continues operating while browsing; directives are attributed to SOL, audit logged, physically constrained, and can be released without creating a second decision engine.
5. Implement and prove user-facing 20× test path with actual tick measurements, visible diagnostics and invariants. No test-voyage cloning requirement. Normal 4×/holiday 1× must remain identical; prove real Monday boundaries and six-hour offline catch-up are not corrupted.
6. Re-run existing Node, cinematic/stability/compatibility/production/bridge, mobile emulation, save migrations, full history/source/resource audits and representative 7/30-real-day campaigns. Add UI browser tests for tab isolation, all controls, onboarding, SOL role, and 20×/normal transitions. Use screenshots of each major desktop and tablet-emulated tab; capture no fictitious visual claims.
7. Document exact commits, real results, failed/superseded tests and remaining native Windows/Tab S5e/TV/AV/human usability gates in `PHASE4_UI_PROGRESS.md`, `PHASE4_UI_VALIDATION.md`, `PHASE4_UI_LIMITATIONS.md`, and update roadmap.
8. Produce source-only **ICARUS_SOL_Command_Interface_Phase4_Lite.zip**, SHA-256, manifest and concise installation instructions after independent extracted ZIP verification. Existing simple recovery remains, but **backup/migration polish is deferred to pre-release stabilization, not canceled**. No AV bypass or unverified device certification.

## Weekly anthology clarification

The user expects **new episodes each week** with the **same persistent crew and world**. The user is comfortable resetting experimental builds during development, but does not want weekly story resets. Preserve existing Monday–Sunday episode boundaries and continuous character consequences unless the user explicitly chooses a new voyage. Focus testing on whether each weekly chronicle actually reflects the autonomous world and whether the user can see and diagnose its operation. Do not invent weekly plot events to meet a quota.

## Development workflow
Start implementation now with UI control inventory, retained/improved Home and a distinct working Bridge screen, not only documents. Continue in large, independently tested, committed batches. Stop and explicitly report a blocker if safety, save isolation or time semantics cannot be maintained. No universe expansion, forced events, character rewrites, new network services or new graphics engine. Focus on an understandable, visually coherent interface where **SOL runs the ship and the user can step in as SOL**.
