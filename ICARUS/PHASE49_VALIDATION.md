# Phase 4.9 validation — Living Specimens & Frontier Encounters

The bounded Phase 4.9 software increment is implemented and verified on the available platform. This is not certification of physical Windows/Samsung/native/TV/audio hardware or ICARUS final-release readiness. Runtime freeze: `bb49916cea1202f9b5f1e6e7004529d450792971`. All 172 retained runtime hashes are in reports/phase49/runtime_scope.json; fingerprint `fdc239140c8ae786333f4e5997c00aa328a94d07604cbca5142bcac135b31342`. Final ZIP verification identifies the packaging/source commit separately. Later documentation commits do not change the frozen runtime.

## Executed results

| Group | Executed result | Actual coverage |
| --- | --- | --- |
| Node | 490 passed; 0 failed/skipped | Existing simulation domains plus 29 specimen/custody/care/evidence cases and combined payload boundary |
| Extracted Lite runtime | 50 passed; 0 failed/skipped | Six biological/physical/payload cases, two paired remote, two interrupted-care/source-state cases, boot 8, audio 10, Easter eggs3, palettes2, engineering 6, visuals 6, dispatch 3, deterministic full-engine/reload2 |
| Final-source compatibility browser | 22 passed; 0 failed/skipped | Expeditions 9, drones 7, knowledge 6; actual physical passages, finite repair, signals/custody, real-Monday transitions, delayed records and save/reload |
| Companion services | 79 passed; 0 failed/skipped | Bridge/TV/classified/media/Windows/sound/audio software and protocol cases; their code is unchanged after the run |
| Supplied historical voyage | Four passed on final source |19,257,662-byte private JSON;16,954 full history rows; crew/map/knowledge/research/media/history preservation, exact restart, deferred playback, paired telemetry and size-rejection recovery |
| Full browser campaigns | Nine checkpoints passed | Seeds10101/4242/2026; each one continuous 90 simulated day run, exact 7/30/90 saves/reloads, every causal minute counted |
| Package integrity | See downloads/phase49 verification | Source archive/CRC/file hashes, retained172-runtime equality, local entry-point assets, checksum and extracted final-archive smoke |

Raw case names, failures from earlier diagnostics and actual campaign statistics are retained in reports/phase49/final. Tests passed only where actually executed. The final package contains the exact tested172 runtime files; tests/reports/developer scripts stay in source. Release ZIP metadata/documentation can differ from the earlier extracted candidate; runtime equality is checked and final archive startup/acquisition is exercised again.

## What was corrected during verification

The original second-sortie assumptions first hit a legitimate resource-priority launch refusal. Tests now wait for actual readiness/conservation recovery and retry without granting stores or bypassing safety. This exposed a real stale-navigation defect: a crew member leaving C04 still had C04 as their last room ID, so staging chose an empty route despite the actual corridor node. physicalTaskRoute retains the required physical trip from the recorded node. The original cavern traversal and finite powered lift-repair tests pass after correction. See reports/phase49/STAGING_INVESTIGATION.md.

A later source review found inherited duplicate carriedMass properties: the specimen callback replaced the recovered-drone callback. The unified pure payload query now counts both, and the near 40-unit boundary plus actual host callback are regression tested. See reports/phase49/PAYLOAD_INVESTIGATION.md. Campaigns started before either correction are development evidence only; final nine-checkpoint acceptance uses the final freeze above.

An early historical-voyage import exceeded its unchanged120-second test timeout under concurrent campaigns. It passed the same assertions on rerun, then all four final-source historical startup checks passed when scheduled separately (129.301seconds for the full four-case suite). No import code change, database clearing or voyage reset was used to obtain that result. Large-save latency on the user's actual Windows installation remains unmeasured. The private backup's SHA-256 is retained in the integrity report; input bytes are unchanged and the file is not published. The current installed voyage/library is unavailable here.

## Actual campaign observations

See reports/phase49/final/CAMPAIGNS.md and its nine raw reports. Counts describe actual runs, not guaranteed outcomes. No specimens/findings/containment faults/injuries/deaths were injected into ordinary campaigns. Biological observations are witness/report events, not distinct new species. Completed science experiments include the existing research system and do not imply confirmed biological or Lazarus breakthroughs. Quiet missions are valid; launch counts plateau rather than manufacturing fresh objectives in exhausted local terrain.

All reported biology/resource/creature/systems/expedition/drone/knowledge/transit audits are empty, all checkpoints reached the requested monotonic tick, and all save/reload snapshots match exactly. The original canonical adult remains dormant. Normal-campaign escapes/injuries/deaths, if any, are reported as measured; breakout/recovery capability is separately exercised in explicitly labeled adverse fixtures rather than claimed as a natural campaign event.

Resource reports retain actual water/oxygen/energy stock plus the whole-economy conservation audit. These three stock fields are not a complete listing of every inventory domain. Paid collection, kits, care, repair and interrupted work use the existing Economy ledger; no normal campaign was granted replacement stores. New live biological history/sightings/fixtures/habitats are bounded; full historical archives are intentionally retained and can grow. biological_state_bytes measures only the biologicalLife49 extension, excluding ordinary organism entities/traces stored in unifiedWorld.organisms; those are included in the whole diagnostic snapshot. The subdomain metric is not presented as total added memory. Diagnostic snapshot bytes include test projections/aliases and are not labeled as save-file size.

## Timing and performance limits

These are full existing browser-engine technical campaigns, not90 real calendar days or a Windows performance benchmark. Explicit advancement executes step and fieldTick for every causal minute, with bounded120-minute chunks and exact returned-tick checks. Existing hidden-page guards suppress non-displayed presentation. Technical advancement bypasses wall-clock pumping and its regular 15-minute autosave cadence; durable saves/reloads occur at7/30/90 checkpoints plus normal page/visibility hooks. Production-clock/calendar and mid-activity persistence have separate regressions. Reported wall time includes concurrent headless workers, diagnostics, saving and reloading. No production speed multiplier was increased and no causal events were skipped. Native UI/audio/real-week/human playability acceptance is separate.

## Reproduce from source

```
node --test ICARUS/test_*.js
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_integration.py --report /tmp/specimens.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_remote.py --report /tmp/specimen_remote.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_acceptance.py --report /tmp/specimen_acceptance.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/soak_specimens.py --out /tmp/specimen_campaigns --seeds 10101 4242 2026 --days 7 30 90
python ICARUS/package_phase49.py --output /tmp/specimen_lite
```

Python Playwright/Chromium and Node are development dependencies, excluded from Lite. Supply a suitable browser executable on other systems; ICARUS_SPECIMEN_ARTIFACTS optionally selects the screenshot directory. The normal Windows launcher/runtime requirements are retained. Tests use isolated browser contexts; do not point destructive adverse fixtures at an installed voyage.

## Unverified or intentionally bounded

No physical Windows launch/display/audio, Samsung phone/tablet/native APK, TV, Fortnite/private-preview/VoiceMeeter close/crash, actual current library/backup, antivirus execution or human long-form art/story review was available. Viewport/protocol tests do not certify devices. Native APK rebuilding remains pending original source recovery. Audio routing/default devices/drivers and the current sound library were not changed.

Three lightweight families/four fixtures/finite local habitats are implemented, not a reproductive food web or invasive experimental choreography. Recovery is room/node based; precise mid-passage dropped-container salvage and full within-room collision/anchoring physics remain unimplemented. See README_PHASE49.md for those boundaries and PHASE49_SECURITY_REVIEW.md for source/network/system review. No gallery, galaxy expansion or gym conversion is included.

Forward migration is additive. **Older runtimes must not advance new species. Rollback requires the pre4.9 complete backup in a separate browser profile**, preserving the current profile/post-upgrade world and independent soundboard_data. Read the installation/backup instructions before upgrade.

Recommended next batch: observe this bounded build with actual Windows/phone/tablet hardware, measure current-voyage startup/long-session performance and review encounter/care balance; then refine the existing node-based recovery and specimen presentation. Depth/cohesion/polish take priority over more destinations, forced outbreaks or unrelated scope.

## Ninety day outcome summary

| Seed | Crew alive/dead | Collected | Care | Enclosure repairs | Escapes | Biological deaths | Diagnostic snapshot MiB | Wall seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10101 | 20/0 | 0 | 0 | 0 | 0 | 0 | 23.74 | 1316.1 |
| 4242 | 20/0 | 2 | 42 | 2 | 0 | 0 | 30.05 | 2027.1 |
| 2026 | 20/0 | 1 | 21 | 1 | 0 | 0 | 27.87 | 1895.5 |

Full raw reports and actual renderer captures: https://github.com/thekiddam-code/munza69/tree/codex/living-specimens-phase4-9/ICARUS/reports/phase49
