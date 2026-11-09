# v1.3 → v1.4: explicit import, independent saves

The core edition starts a separate voyage unless you explicitly import a backup. Use the same port/origin to retain access to old browser data, but do not expect automatic cross-edition copying.

1. In v1.3, export a **complete JSON backup** and retain the entire v1.3 project. The independent archive/extended-universe-v1.3 branch points at ea984a8749c907fd373492283f085d769eebbd03. ICARUS_Extended_Universe_v1.3_Archive.zip is also supplied.
2. Extract the entire v1.4 project and launch the existing local server. Read README_v1.4.md. Core uses IndexedDB `icarus-anthology-v14` and physical cache `icarus-anthology-v14`; v1.3 retains `icarus-voyage` / `icarus-v02`. Recovery/checkpoint/cache metadata keys are also separated. Notes and interface preferences may remain shared.
3. Use Settings → save management → Import JSON backup. Confirm the concrete replacement of the **core** voyage. Import preserves old crew, science, inventories, missions, injuries, relationships, navigation and source history. Source-linked v1.4 story state initializes separately.
4. Old discovered destinations stay readable and conserved. Their sectors stop growing; no old map is erased. Existing transit completes physically and existing expeditions can return. Five finite local contexts are anchored at the migration position. New autonomous routes use those contexts; old planetary routes are not offered as core progression. No free replenishment is inserted into existing inventory.
5. Commit the core save and export another complete JSON backup. Keep the original v1.3 file. Returning to the preserved edition uses its independent browser database or original backup; do not import v1.4-only narrative state into an older executable and expect support.

Core export includes world plus indexed historical records, integrity information and visible warnings. Modern incomplete structures are rejected before replacement; a partial rescue backup is clearly labeled. Browser-origin/profile deletion still requires an off-device backup. Never open two writers for the same edition and assume concurrent-write arbitration.

## Recovering Extended Universe

`git switch archive/extended-universe-v1.3` restores the complete source at ea984a8, including working tests and original docs. Alternatively extract ICARUS_Extended_Universe_v1.3_Archive.zip; its original BUILD_MANIFEST and reports remain intact. This is the original v1.3 ZIP under a clearly labeled archive filename, not a stripped reconstruction.

Galaxy-generation/large-route modules: web/universe.js and web/navigation.js. Associated extraction/cargo/economy and registry policies: web/frontier.js, logistics.js, economy.js, entities.js, frontier-ui.js and their tests. The core reuses finite physical capabilities through core-context.js, which disables expanding scans and restricts new route choice. Full planetary exploration remains in the preserved edition. Core has no UI toggle that activates that edition. A soak-only test fixture exercises original compatibility behavior; it is not a player feature.
