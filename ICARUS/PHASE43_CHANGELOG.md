# Phase 4.3 Living Ship Operations changelog

Baseline: verified Phase4.2B d5add5b, with main f5d63a4 approved backlog merged in24e11f9. Initial integration f203314, reliability refinement127bda0, recovery correction13ab447. Exact tested/final package provenance is in PHASE43_VALIDATION.md and BUILD_MANIFEST.json.

## Implemented

- Actual artificial-gravity generator at C07, six topology-derived independent zones, bounded targets0–1.2g, physical field ramps, separate gravity/electrical isolation and real power/condition limits.
- Additive ship component registry with persistent health/wear/load/available power/status, source-backed fault reports, diagnostics, bounded repair history and adapters over existing equipment health.
- Finite paid electrical load; local effects on lights/cameras, powered hatches/lift, environmental regulation, production, labs, propulsion controls and launch readiness. Existing generation source can black-start downstream equipment. Oxygen/pressure/temperature remain real existing compartment variables; unsupported CO2 is labeled unavailable.
- Gravity-dependent graph travel, handhold/float/light-step poses, work anchoring, actual discovered unsecured containers/samples, consistent fall energy and conditional harm through existing injury rules. No decorative incidents or rigid-body replacement.
- Informed qualified autonomous engineers physically collect tools/spares, travel, diagnose, service-isolate, repair condition with paid work, test and record actual outcomes. Jobs support shortages, unsafe access, higher duties, reassignment and save/reload without duplicated supply payments.
- Existing local and paired Engineering pages receive compact gravity controls, actual target/output/power, warnings, orders and diagnostics. Commands retain pairing, authoritative validation and deduplication; phones load no simulation engine.
- Existing detailed cameras retain their art/topology/privacy/Follow Crew behavior and show actual gravity/motion, local lighting and engineering work. Engineering readings retain measured timestamps and explicit stale status if the control bus fails.
- Fixed two real defects found in campaign validation: low-gravity work restrictions could permanently freeze rest/recovery timers, and component-assignment filtering could prevent emergency preemption. New regressions preserve finite danger while allowing genuine recovery. See PHASE43_RECOVERY_INVESTIGATION.md.

## Files changed

New runtime modules: `web/ship-systems.js`, `web/gravity-motion.js`, `web/systems-maintenance.js`, `web/engineering-ui.js`.

Engine integration: `web/icarus.html`, `economy.js`, `repair-policy.js`, `research.js`, `transit.js`, `navigation.js`, `frontier.js`, `teams.js`, `crew-life.js`, `relationships.js`.

Observation/integration: `web/cinema.js`, `classified-ops.js`, `companion-view.js`, `observation-model.js`, `observation-ui.js`, `pixel-camera.js`, `ship-schematic.js`, `operational-ui.js`, `index.html`; authoritative command whitelist in `server.py`.

Verification/development: `test_ship_systems.js`, `test_operations_integration.py`, `test_operations_remote.py`, `operations_campaign.py`, `package_phase43.py`, phase plan/progress/architecture/validation/limits/security/installation/investigation docs, roadmap/backlog/handoff and source-based delivery artifacts. Development tools/tests/raw reports are excluded from Lite.

## Preserved boundaries

No new voyage, crew regeneration, simulation clock/rate rewrite, new map/universe, expedition/drone/creature expansion, AI takeover system or interface redesign. Calendar, save writer/backup codecs, TV service, BridgeService, installed/native Android source/APKs and existing source-backed storytelling remain. Existing final-art/crowd/cabin-recovery and hardware-validation limits remain open.

This batch moves the final design toward a coherent inhabited spacecraft: the same people, places, sources and finite supplies now govern observed engineering work and environmental consequences. It does not declare the final game complete because automated checks pass.
