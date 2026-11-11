# Phase 4 engineering changelog

## Player experience

Home stays the default customizable live dashboard; Bridge is a separate operational center. Eight destinations and scoped sections replace the accumulated six-page layout. Existing camera, cutaway, crew, incidents, science, knowledge, logistics, field consoles, creator settings, backups, pairing and archives remain reachable. Internal aliases and same-node Home widget handlers preserve compatibility. The control map and paused-world inventory document the retained controls.

The player operates SOL's directed layer. Actual autonomy/directive scope, route explanation, incident access and pause/time status are visible. Course/hold directives use SOL-facing provenance without rewriting old captain records. Global Release restores directed missions through their existing API plus navigation/field autonomy; it cannot teleport a team or waive safety.

Rectangular controls, square segmented interiors, muted translucent amber gradients, cool inactive gradients, restrained cyan surfaces, predictable spacing/focus, responsive navigation and orientation help retain the shipboard identity. Existing density, widget, lighting, visual and reduced-motion keys remain. Remote Deck host/pairing is unchanged.

## Clock and reliability

Explicit development 1×/5×/20× controls use the existing bounded physical-minute pump. Normal 4×/holiday 1× and real Monday–Sunday episodes are unchanged. Prior-rate elapsed time is settled at transitions; pause drops paused elapsed time. Testing is session-only, warns that the current voyage changes, and returns to normal on reload. Writer and backup-transfer guards remain; no new network/host operation or cloned-save system.

Confirmed regressions fixed during validation: inherited hidden location styles after relocation; stale imported preference callbacks/values; Home/Research Lazarus duplicate procedure IDs; insufficient location touch target; explicit selection refresh; scoped mission release; and accumulating relocated history sections. The last defect duplicated controls during real timer progression, so the regression suite now checks uniqueness after physical time passes. None of these fixes suppresses real simulation outcomes or alters the crew/ecology/research/resource controller models.

## Reviewable milestones

- `1f12f1f`: working eight-page SOL deck, retained Home, canonical controls and bounded user-facing test clock.
- `b42d8b2`: retained controls, source-backed specialist integration, imported bindings and UI inventory.
- `db2f955`: scope release and accurate new SOL command attribution.
- `d39f2d7`: replace refreshed relocated panels rather than accumulating duplicates; **final runtime revision**.
- `0835f14`: extra scope/rate/spectator regression cases; documentation/testing only.

Later documentation and package commits must retain all 65 tested runtime file hashes. Exact package source/hash and final results are in the manifest, verification report and PHASE4_UI_VALIDATION.md. Superseded/aborted runs are retained as diagnostics and excluded from accepted results.

## Tradeoffs and next work

This finishes a substantial implemented interface batch and brings the final design closer through cohesion and discoverability. It does not establish final native/human readiness. Some specialist field consoles retain legacy layout; the older panel CSS and integrated HTML remain large. Keep future work focused on sustained human desktop/tablet observation, measured accessibility, specialist dialog polish, then deferred backup/recovery stabilization. Do not add universe scope to address presentation gaps.
