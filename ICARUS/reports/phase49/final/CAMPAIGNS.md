# Phase 4.9 actual campaign measurements

All nine prefix checkpoints use the same corrected 172-file runtime. Each seed is one continuous 90 simulated day voyage with actual save/reload at7/30/90 days. No normal-campaign biological incidents/findings were injected. Audits cover biology, resources, creatures, ship systems, expeditions, drones, knowledge and transit. All reported audits are empty and all reload comparisons exact. Ordinary quiet outcomes are valid.

| Seed | Days | Crew alive/dead | Collected | Observations | Care | Enclosure repairs | Escapes | Biological injuries/deaths | Manifest launches | Existing science experiments complete | Bio extension KiB | Diagnostic snapshot MiB | Wall seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10101 | 7 | 20/0 | 0 | 1 | 0 | 0 | 0 | 0/0 | 12 | 65 | 5.3 | 5.81 | 68.0 |
| 10101 | 30 | 20/0 | 0 | 1 | 0 | 0 | 0 | 0/0 | 12 | 65 | 5.1 | 11.04 | 295.4 |
| 10101 | 90 | 20/0 | 0 | 1 | 0 | 0 | 0 | 0/0 | 12 | 65 | 5.1 | 23.74 | 1316.1 |
| 4242 | 7 | 20/0 | 2 | 59 | 2 | 0 | 0 | 0/0 | 13 | 66 | 19.1 | 6.49 | 73.3 |
| 4242 | 30 | 20/0 | 2 | 337 | 14 | 0 | 0 | 0/0 | 13 | 66 | 19.2 | 13.15 | 369.6 |
| 4242 | 90 | 20/0 | 2 | 1053 | 42 | 2 | 0 | 0/0 | 13 | 66 | 19.4 | 30.05 | 2027.1 |
| 2026 | 7 | 20/0 | 1 | 26 | 1 | 0 | 0 | 0/0 | 12 | 55 | 14.3 | 6.87 | 81.1 |
| 2026 | 30 | 20/0 | 1 | 158 | 7 | 0 | 0 | 0/0 | 12 | 55 | 19.3 | 12.94 | 329.9 |
| 2026 | 90 | 20/0 | 1 | 494 | 21 | 1 | 0 | 0/0 | 12 | 55 | 19.4 | 27.87 | 1895.5 |

Observations are witness/report events, not distinct species or guaranteed scientific conclusions. Science counts include the existing research system, not just new biological work. Mission counts are teamLog manifest authorizations, not guaranteed completed objectives; raw reports retain registry outcomes. Retained event_kinds cover the current chronicle window, not every source ever archived.

Resource reports retain actual water/oxygen/energy stock and whole-economy conservation audit results. Other stores remain in their existing domains; resource_stock is not presented as a complete inventory listing. Paid preparation/care/repair is separately tested with the real Economy adapter and exact interrupted-work restoration. No resources were granted in normal campaigns.

Times include concurrent headless workers, snapshot diagnostics and save/reload. The technical advance API executes every step/field minute but bypasses wall-clock pumping and its regular 15-minute autosave schedule; durable saves/reloads run at the explicit checkpoints plus normal page/visibility hooks. Separate production-clock and interrupted-save fixtures cover those boundaries. UI is backgrounded through existing visibility guards while every causal minute still runs. These are throughput observations, not isolated PC benchmarks. Full historical archives are intentionally retained and can grow. biological_state_bytes measures the biologicalLife49 extension only; ordinary organism entities/traces are stored in unifiedWorld.organisms and counted in the whole diagnostic snapshot, not that subdomain figure. Bounds on habitats/fixtures/history/sightings/traces are also regression audited. 90 simulated days do not replace real-world calendar, hardware or human playability testing.
