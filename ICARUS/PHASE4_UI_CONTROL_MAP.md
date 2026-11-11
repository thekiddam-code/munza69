# Phase 4 UI control map

Baseline: 32fa18e; inventory uses an isolated paused voyage. All 106 baseline controls with IDs still exist. 104 ID controls (including new controls) were visibly reached across all sections; closed-dialog/file inputs remain behind their existing launchers. Full before/after inventory is reports/phase4/control_inventory.json. The inventory asserts no world-state change from inspection.

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

Each handler remains attached to the same node or uses the existing source renderer. Dynamic field-console action families are mapped above. A closed-dialog/file input entry is reached through its original launcher, rather than displayed on every page.

| ID | Page / section | Behavior |
| --- | --- | --- |
| `pause` | operations / watch | Existing callback retained |
| `speed` | operations / watch | Existing callback retained |
| `save` | settings / data | Existing callback retained |
| `followoff` | operations / watch | Existing callback retained |
| `settingsopen` | Home widget / launcher / compatibility node | Existing callback retained |
| `credits` | records / sunday | Existing callback retained |
| `reset` | settings / testing | Existing callback retained |
| `frontier-target` | missions / logistics | Existing callback retained |
| `encounter-frequency` | settings / general | Existing callback retained |
| `encounter-apply` | settings / general | Existing callback retained |
| `entity-select` | missions / destinations | Existing callback retained |
| `memory-person` | personnel / activity | Existing callback retained |
| `chronicle-week` | records / sunday | Existing callback retained |
| `durable-save` | settings / data | Existing callback retained |
| `durable-export` | settings / data | Existing callback retained |
| `knowledge-actor` | research / evidence | Existing callback retained |
| `knowledge-read` | research / evidence | Existing callback retained |
| `knowledge-report` | research / evidence | Existing callback retained |
| `cutawaymode` | ship / overview | Existing callback retained |
| `holo-explode` | ship / overview | Existing callback retained |
| `holo-deck` | ship / overview | Existing callback retained |
| `holo-detail` | ship / overview | Existing callback retained |
| `holo-crew` | ship / overview | Existing callback retained |
| `holo-damage` | ship / overview | Existing callback retained |
| `holo-atmosphere` | ship / overview | Existing callback retained |
| `holo-routes` | ship / overview | Existing callback retained |
| `holo-access` | ship / overview | Existing callback retained |
| `holo-reset` | ship / overview | Existing callback retained |
| `hatch-room` | ship / overview | Existing callback retained |
| `hatch-toggle` | ship / overview | Existing callback retained |
| `hatch-clear` | ship / overview | Existing callback retained |
| `atmo-room` | ship / overview | Existing callback retained |
| `dock-start` | missions / destinations | Existing callback retained |
| `dock-release` | missions / destinations | Existing callback retained |
| `camfollow` | operations / watch | Existing callback retained |
| `camroom` | operations / watch | Existing callback retained |
| `camreview` | operations / watch | Existing callback retained |
| `camcycle` | operations / watch | Existing callback retained |
| `camscan` | operations / watch | Existing callback retained |
| `camzoom` | operations / watch | Existing callback retained |
| `bridge-spectator` | operations / watch | Existing callback retained |
| `spectator-next` | operations / watch | Existing callback retained |
| `film-episode` | records / sunday | Existing callback retained |
| `film-load` | records / sunday | Existing callback retained |
| `film-prev` | records / sunday | Existing callback retained |
| `film-play` | records / sunday | Existing callback retained |
| `film-next` | records / sunday | Existing callback retained |
| `film-seek` | records / sunday | Existing callback retained |
| `home-edit` | Home widget / launcher / compatibility node | Existing callback retained |
| `obsreplay` | personnel / activity | Existing callback retained |
| `obsplay` | personnel / activity | Existing callback retained |
| `obsback` | personnel / activity | Existing callback retained |
| `obsnext` | personnel / activity | Existing callback retained |
| `obsrate` | personnel / activity | Existing callback retained |
| `obsseek` | personnel / activity | Existing callback retained |
| `filterall` | records / timeline | Existing callback retained |
| `filterlittle` | records / timeline | Existing callback retained |
| `filtersocial` | records / timeline | Existing callback retained |
| `filtersystem` | records / timeline | Existing callback retained |
| `filteremergency` | records / timeline | Existing callback retained |
| `rd-host-key` | settings / data | Existing callback retained |
| `rd-connect` | settings / data | Existing callback retained |
| `settingsclose` | Home widget / launcher / compatibility node | Existing callback retained |
| `visualmode` | settings / general | Existing callback retained |
| `reduced-motion` | settings / general | Existing callback retained |
| `exportbackup` | settings / data | Existing callback retained |
| `importbackup` | settings / data | Existing callback retained |
| `backupfile` | Home widget / launcher / compatibility node | Existing callback retained |
| `checkpointnow` | settings / data | Existing callback retained |
| `export-stream` | settings / data | Existing callback retained |
| `backup-cancel` | settings / data | Existing callback retained |
| `exportarchives` | records / archives | Existing callback retained |
| `ideatitle` | records / archives | Existing callback retained |
| `ideacategory` | records / archives | Existing callback retained |
| `ideabody` | records / archives | Existing callback retained |
| `ideasave` | records / archives | Existing callback retained |
| `ideacancel` | Home widget / launcher / compatibility node | Existing callback retained |
| `exportideas` | records / archives | Existing callback retained |
| `importideas` | records / archives | Existing callback retained |
| `ideasfile` | Home widget / launcher / compatibility node | Existing callback retained |
| `calendar-zone` | settings / testing | Existing callback retained |
| `calendar-apply` | settings / testing | Existing callback retained |
| `canon-key` | settings / advanced | Existing callback retained |
| `canon-text` | settings / advanced | Existing callback retained |
| `canon-save` | settings / advanced | Existing callback retained |
| `personal-name` | settings / advanced | Existing callback retained |
| `personal-shipwide` | settings / advanced | Existing callback retained |
| `personal-dates` | settings / advanced | Existing callback retained |
| `body-build` | settings / advanced | Existing callback retained |
| `body-motion` | settings / advanced | Existing callback retained |
| `personal-save` | settings / advanced | Existing callback retained |
| `director-entry` | settings / advanced | Existing callback retained |
| `hud-density` | settings / general | Existing callback retained |
| `close` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayclose` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayseek` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayplay` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayback` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayforward` | Home widget / launcher / compatibility node | Existing callback retained |
| `replayspeed` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-close` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-room` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-severity` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-execute` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-reset` | Home widget / launcher / compatibility node | Existing callback retained |
| `director-quit` | Home widget / launcher / compatibility node | Existing callback retained |
