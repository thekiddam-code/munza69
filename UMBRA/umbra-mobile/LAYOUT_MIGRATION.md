# Phase 2.3 layout and editing configuration

UMBRA upgrades the existing private Preferences DataStore envelope from schema 2/3 to **schema 4** on the next successful write. It keeps the `config_v2` storage key and still reads Phase 1 scalar preferences. No destructive reset or eager rewrite is performed. Existing desktop schema 1 pages/items/folders/widgets, native widget IDs, favorites, custom labels, server URLs/timeouts, motion choices, weather location, and Keystore pairing are retained.

## Shared grids

`gridLayouts` maps stable surface IDs to version 1 grids. Examples: `home:<page ID>`, `command`, `icarus`, `system-controls`, `engineering-actions`, `lounge-controls`, `instant-page`, and `instant-widget:<widget ID>`. Each grid stores its reference column count and cells with stable `id`, integer `x`/`y`, width `w`, expanded height `h`, `hidden`, and `collapsed`.

Existing Home pages seed grids from item order, their configured columns, and widget spans. Existing Command Center module order/hidden choices seed the module grid. Once edited, integer grid positions control arrangement. Existing desktop objects remain authoritative for app/folder membership and Android widget binding. Missing server-control references keep their stored metadata, rather than being silently deleted while offline. Returning catalog entries can recover their placement.

The shared collision engine packs mixed spans, snaps dropped controls, displaces occupied cells without overlapping, scales spans across available widths, and compacts module rows after collapse. A collapsed module occupies a single header row while retaining its expanded size. Multiple modules can stay expanded. Home and module layouts share this engine; buttons and native system shortcuts use it too. Large button grids compose the viewport plus a small overscan, and cache resolved placement until their inputs change. No frame-rate or battery measurements are implied by these implementation choices.

Limits protect local data and rendering: a 1 MiB configuration envelope, up to 128 saved grid surfaces, 2,048 cells per grid, reference density 1–8 columns, height 1–24 rows per grid item, and existing desktop limits (12 pages / 256 total items / 96 items per page / 64 folder members). Clock and Android widget configuration retains its existing 1–5 column / 1–6 row controls and provider restrictions. Invalid edits/imports are rejected without replacing the prior configuration. Limits never silently truncate selected controls to six.

## Interaction and recovery

- Tap performs the usual action. Tap a deck header to expand/collapse it.
- Long-press an item or a module header to edit. Drag while holding, then release to snap/save. A collapsed header can move without expanding.
- Only the active drag/resize shows amber free-cell guides; release/cancel removes drag guides immediately. Visual Detail and motion switches do not control these functional editing guides.
- The contextual Arrange toolbar provides Options, one-level Undo, and Done. Back or tapping blank space exits editing. There is no permanent Widget Options row or normal-use arrangement toolbar.
- Contextual actions include configure, resize handles, remove/hide, duplication where supported, and explicit page movement. Android widgets use their provider-aware configuration for resizing and cannot be duplicated with the same host ID.
- Drag near a Home page edge to move to an adjacent page; the contextual page chooser can move directly to any page. Cross-page movement preserves the item ID and widget binding.
- TalkBack exposes long-click editing and Move earlier / Move later actions. Manual folder/page editors remain available after entering editing.
- To add widgets/folders/pages, long-press the Home page title. To restore hidden deck controls, use Settings → Command Center → Restore all hidden modules and controls, or a module's contextual Configure panel.

Undo covers the latest arrangement in the current launcher process; saved layouts themselves survive process death. Export a full configuration in Settings → Configuration before imports, resets, or large edits. A configuration import is a validated replacement with a preview. Android widget IDs are retained locally but stripped from portable exports/imports, so imported providers must be rebound through Android. Removing a native widget releases its binding; restoring a prior reference may require rebinding.

## Mode and status panel preferences

`commandExpanded` records Compact versus Expanded independently from each module's `collapsed` flag. Expanded is the migration default, matching the prior full Command Center. Compact shows a denser presentation without overwriting individual expansion preferences. Grid moves, sizes, visibility, and collapsed state persist independently of animation settings.

`statusTabs` stores independent choices for Main Home, Applications, Information Deck, ICARUS, Engineering, Lounge, Simulator, Instant Buttons, Settings, and Command Center. Applications and Settings default off; other contexts default on. `statusPanel` remains the overall master gate and preserves the user's prior value. The active Home page kind identifies its terminal/information/ICARUS context; native ICARUS uses its selected section. Hiding the panel reclaims layout space and does not change immersive bar preferences or Android notifications.

`deckColumns` controls density; `editHaptics` defaults off. Android system preferences still govern haptic availability. Motion profiles, master/intensity, per-effect switches, and Visual Detail keep their existing independent persistence and power/accessibility behavior.

## Buttons and files

`customButtons` contains local typed output definitions; `instantSelection` distinguishes inherit/legacy-all (`null`) from an explicit empty selection. Legacy nonempty `instantFavorites` remains the selection until an explicit new choice is made. `widgetButtonSelections` stores optional independent lists by stable widget item ID; absent entries inherit the global selection. All selected controls wrap and scroll, and missing references are reported and retained. Select all adds available entries; Deselect all explicitly clears the selection.

A configured override of a server-catalog button creates a local UMBRA definition, transfers its grid placement and widget references, and changes the UMBRA selection without modifying PC mappings. Local button identity survives rename/output changes. Deleting a local definition removes its UMBRA references; removing a tile from one widget changes only that widget's selection. Duplicating an ICARUS widget copies its selected-button configuration.

Button-only JSON files store versioned local output definitions and exclude connection credentials. Loading merges stable button IDs after a preview and offers a backup first; it never executes anything. Full Settings export additionally backs up grids, selections, labels, and all other launcher preferences. See ICARUS_OUTPUTS.md for the exact supported output contract.
