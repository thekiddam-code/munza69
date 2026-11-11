# Phase 4 UI control map

Baseline: 32fa18e; inventory uses an isolated paused voyage. All 106 baseline controls with IDs still exist. 100 ID controls (including new controls) were visibly reached across all sections; closed-dialog/file inputs remain behind their existing launchers. Full before/after inventory is reports/phase4/control_inventory.json. The inventory asserts no world-state change from inspection.

Navigation retains internal `operations`, `personnel`, `records` keys for existing callers; labels are Bridge, Crew, Chronicles. Old Upgrades links resolve to Ship / Systems. No simulation controller is replaced.

| Existing component / handler | Logical home | Explanation and preserved behavior |
| --- | --- | --- |
| Home `homeLayout`, `renderHome`, widget handlers | Home | Existing device keys, order, sizes, live canvas/handlers retained. A deliberate page change restores nodes to their origin markers. |
| `frontierCommand`, `data-nav` | Bridge / Watch; Missions / Logistics | Hold, release, recall and feasible course retain fuel/access/rescue checks. New operator-layer audit metadata does not rewrite captain history. |
| `setLocation`, `data-remote-tab`, `data-remote-action`, `data-device`, `data-wy-camera` | Missions / Destinations | Existing local field consoles, expedition controls, equipment/sensors, docking, recovered cameras and finite maps. No new universe. |
| `missionIntervene` / mission director | Missions / Active | Existing explain, recall, abort, command and release API codes; SOL-facing labels. |
| `drawHologram`, room/deck/hatch/atmosphere handlers | Ship / Overview | Real cutaway and existing control nodes; same physical authority. |
| maintenance/dependency/supplies/audit readouts | Ship / Systems | Existing condition, paid repair and finite store views. |
| `renderCamera`, CinemaUI | Bridge / Watch; explicit Ship / Cameras link | One live camera, read-only manual/AUTO controls, accurate provenance. |
| crew roster / detail, recordings, impact, psychology | Crew / Roster, Activity, Medical, Social | Existing inspectors and actual health/fatigue overview; no new character behavior. |
| `sciencePanel`, `knowledge-read/report`, Lazarus handlers | Research / Projects, Evidence, LAZARUS | Existing uncertain programs, individual acquired records and safety-restricted procedures. Home Lazarus remains supported without duplicate IDs. |
| anthology sources, log filters, episode archives, replay handlers | Chronicles / Timeline, Sunday, Archives | Actual events, source labels, optional player, existing archive/idea tools. |
| `save`, durable-save, backup/import/checkpoint, bridge pairing | Settings / Data | Existing persistence and single-writer protocol; no backup redesign. |
| `configure`, creator/personal profile, director | Settings / Testing, Advanced | Calendar unchanged; explicit legacy creator incident tools stay separate from autonomous SOL. |
| HUD density, visual/reduced-motion/neon preferences | Settings / General | Existing per-device keys and handlers preserved. |

## Baseline ID inventory

All old IDs exist. Routes below come from the actual DOM after visiting every section. Closed dialogs and file inputs retain their original launchers; hidden header IDs remain compatibility entry points. Delegated handlers stay with their component. Dynamic field-console action families are mapped above.

| ID | Logical home / launcher | Behavior |
| --- | --- | --- |
| `pause` | Global status / hidden legacy launcher | Existing callback / component delegation retained |
| `speed` | Global status / hidden legacy launcher | Existing callback / component delegation retained |
| `save` | area-settings-data | Existing callback / component delegation retained |
| `followoff` | area-operations-watch | Existing callback / component delegation retained |
| `settingsopen` | Global status / hidden legacy launcher | Existing callback / component delegation retained |
| `credits` | area-records-sunday | Existing callback / component delegation retained |
| `reset` | area-settings-testing | Existing callback / component delegation retained |
| `frontier-target` | area-missions-logistics | Existing callback / component delegation retained |
| `encounter-frequency` | area-settings-general | Existing callback / component delegation retained |
| `encounter-apply` | area-settings-general | Existing callback / component delegation retained |
| `entity-select` | area-missions-destinations | Existing callback / component delegation retained |
| `memory-person` | area-personnel-activity | Existing callback / component delegation retained |
| `chronicle-week` | area-records-sunday | Existing callback / component delegation retained |
| `durable-save` | area-settings-data | Existing callback / component delegation retained |
| `durable-export` | area-settings-data | Existing callback / component delegation retained |
| `knowledge-actor` | area-research-evidence | Existing callback / component delegation retained |
| `knowledge-read` | area-research-evidence | Existing callback / component delegation retained |
| `knowledge-report` | area-research-evidence | Existing callback / component delegation retained |
| `cutawaymode` | area-ship-overview | Existing callback / component delegation retained |
| `holo-explode` | area-ship-overview | Existing callback / component delegation retained |
| `holo-deck` | area-ship-overview | Existing callback / component delegation retained |
| `holo-detail` | area-ship-overview | Existing callback / component delegation retained |
| `holo-crew` | area-ship-overview | Existing callback / component delegation retained |
| `holo-damage` | area-ship-overview | Existing callback / component delegation retained |
| `holo-atmosphere` | area-ship-overview | Existing callback / component delegation retained |
| `holo-routes` | area-ship-overview | Existing callback / component delegation retained |
| `holo-access` | area-ship-overview | Existing callback / component delegation retained |
| `holo-reset` | area-ship-overview | Existing callback / component delegation retained |
| `hatch-room` | area-ship-overview | Existing callback / component delegation retained |
| `hatch-toggle` | area-ship-overview | Existing callback / component delegation retained |
| `hatch-clear` | area-ship-overview | Existing callback / component delegation retained |
| `atmo-room` | area-ship-overview | Existing callback / component delegation retained |
| `dock-start` | area-missions-destinations | Existing callback / component delegation retained |
| `dock-release` | area-missions-destinations | Existing callback / component delegation retained |
| `camfollow` | area-operations-watch | Existing callback / component delegation retained |
| `camroom` | area-operations-watch | Existing callback / component delegation retained |
| `camreview` | area-operations-watch | Existing callback / component delegation retained |
| `camcycle` | area-operations-watch | Existing callback / component delegation retained |
| `camscan` | area-operations-watch | Existing callback / component delegation retained |
| `camzoom` | area-operations-watch | Existing callback / component delegation retained |
| `bridge-spectator` | area-operations-watch | Existing callback / component delegation retained |
| `spectator-next` | area-operations-watch | Existing callback / component delegation retained |
| `film-episode` | area-records-sunday | Existing callback / component delegation retained |
| `film-load` | area-records-sunday | Existing callback / component delegation retained |
| `film-prev` | area-records-sunday | Existing callback / component delegation retained |
| `film-play` | area-records-sunday | Existing callback / component delegation retained |
| `film-next` | area-records-sunday | Existing callback / component delegation retained |
| `film-seek` | area-records-sunday | Existing callback / component delegation retained |
| `home-edit` | Home | Existing callback / component delegation retained |
| `obsreplay` | area-personnel-activity | Existing callback / component delegation retained |
| `obsplay` | area-personnel-activity | Existing callback / component delegation retained |
| `obsback` | area-personnel-activity | Existing callback / component delegation retained |
| `obsnext` | area-personnel-activity | Existing callback / component delegation retained |
| `obsrate` | area-personnel-activity | Existing callback / component delegation retained |
| `obsseek` | area-personnel-activity | Existing callback / component delegation retained |
| `filterall` | area-records-timeline | Existing callback / component delegation retained |
| `filterlittle` | area-records-timeline | Existing callback / component delegation retained |
| `filtersocial` | area-records-timeline | Existing callback / component delegation retained |
| `filtersystem` | area-records-timeline | Existing callback / component delegation retained |
| `filteremergency` | area-records-timeline | Existing callback / component delegation retained |
| `rd-host-key` | area-settings-data | Existing callback / component delegation retained |
| `rd-connect` | area-settings-data | Existing callback / component delegation retained |
| `settingsclose` | area-settings-general | Existing callback / component delegation retained |
| `visualmode` | area-settings-general | Existing callback / component delegation retained |
| `reduced-motion` | area-settings-general | Existing callback / component delegation retained |
| `exportbackup` | area-settings-data | Existing callback / component delegation retained |
| `importbackup` | area-settings-data | Existing callback / component delegation retained |
| `backupfile` | area-settings-data | Existing callback / component delegation retained |
| `checkpointnow` | area-settings-data | Existing callback / component delegation retained |
| `export-stream` | area-settings-data | Existing callback / component delegation retained |
| `backup-cancel` | area-settings-data | Existing callback / component delegation retained |
| `exportarchives` | area-records-archives | Existing callback / component delegation retained |
| `ideatitle` | area-records-archives | Existing callback / component delegation retained |
| `ideacategory` | area-records-archives | Existing callback / component delegation retained |
| `ideabody` | area-records-archives | Existing callback / component delegation retained |
| `ideasave` | area-records-archives | Existing callback / component delegation retained |
| `ideacancel` | area-records-archives | Existing callback / component delegation retained |
| `exportideas` | area-records-archives | Existing callback / component delegation retained |
| `importideas` | area-records-archives | Existing callback / component delegation retained |
| `ideasfile` | area-records-archives | Existing callback / component delegation retained |
| `calendar-zone` | area-settings-testing | Existing callback / component delegation retained |
| `calendar-apply` | area-settings-testing | Existing callback / component delegation retained |
| `canon-key` | area-settings-advanced | Existing callback / component delegation retained |
| `canon-text` | area-settings-advanced | Existing callback / component delegation retained |
| `canon-save` | area-settings-advanced | Existing callback / component delegation retained |
| `personal-name` | area-settings-advanced | Existing callback / component delegation retained |
| `personal-shipwide` | area-settings-advanced | Existing callback / component delegation retained |
| `personal-dates` | area-settings-advanced | Existing callback / component delegation retained |
| `body-build` | area-settings-advanced | Existing callback / component delegation retained |
| `body-motion` | area-settings-advanced | Existing callback / component delegation retained |
| `personal-save` | area-settings-advanced | Existing callback / component delegation retained |
| `director-entry` | area-settings-advanced | Existing callback / component delegation retained |
| `hud-density` | area-settings-general | Existing callback / component delegation retained |
| `close` | modal | Existing callback / component delegation retained |
| `replayclose` | replaymodal | Existing callback / component delegation retained |
| `replayseek` | replaymodal | Existing callback / component delegation retained |
| `replayplay` | replaymodal | Existing callback / component delegation retained |
| `replayback` | replaymodal | Existing callback / component delegation retained |
| `replayforward` | replaymodal | Existing callback / component delegation retained |
| `replayspeed` | replaymodal | Existing callback / component delegation retained |
| `director-close` | director-modal | Existing callback / component delegation retained |
| `director-room` | director-modal | Existing callback / component delegation retained |
| `director-severity` | director-modal | Existing callback / component delegation retained |
| `director-execute` | director-modal | Existing callback / component delegation retained |
| `director-reset` | director-modal | Existing callback / component delegation retained |
| `director-quit` | director-modal | Existing callback / component delegation retained |
