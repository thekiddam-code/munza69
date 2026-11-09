# ICARUS v1.4.1 — engineering changelog

## Scope and baseline

This is a stabilization of v1.4 602b4a2. FINAL_DESIGN.md remains authoritative: one persistent ship, autonomous crew and SOL, optional captain, causal anthology, finite resources, science/Lazarus and sourced chronicles. No universe expansion, new encounter catalog or unrelated gameplay system is added. Extended Universe stays independently recoverable on its existing branch/archive.

Read ROOT_CAUSE_v1.4.1.md for the original-profile seed-1001 reproduction, exact causal ticks, intended failure mechanics and confirmed defects. The original 101 unit cases pass before implementation. Read-only instrumentation is supplied through a replay HTTP handler; original source files remain unchanged and diagnostic reads consume no random draws.

## Targeted changes

`web/repair-policy.js` separates repair/access/reservation/forecast decisions from the oversized HTML integration layer. It uses existing crew, physical corridors, room hatches, maintenance orders, native incidents and economy APIs; it does not create another resource or mission economy.

- Emergency dispatch uses actual route feasibility from the worker's current navigation node, not the one-token `path()` helper. One native responder reservation per fault prevents a single inaccessible galley from reserving all four engineers. Life support and upstream production outrank less consequential equipment; depletion forecasts can further raise priority.
- A jammed hatch can be repaired from its reachable near-side corridor or by a worker already inside. Thirty paid work minutes are required. The worker remains outside until the actual hatch opens and physical travel completes. Fire/breach/pressure conditions can prevent clearance; a captain/safety seal is never opened by this policy.
- Every new jam resets that jam's clearance progress. A native machine incident is not declared fully resolved while its hatch remains damaged. Repair progress is retained across worker rotation and saves; near-complete floating-point work uses a small numerical completion tolerance.
- Native equipment and atmospheric responses pay real tools, spares and energy for applied progress. Budgeting checks all required pools first and limits work to affordable increments, so shortage cannot debit an unrelated pool without applying work. Resource access excludes expedition loans. No repair cost is paid twice merely because of save/reload.
- Distribution can be manually repaired during a blackout at half normal progress rate, using actual parts, a physically present fit engineer and personal effort. This produces no energy directly. Restored hardware can subsequently convert actual carried fuel or incident starlight through existing generation rules. Without material, access or capable crew, recovery can fail.
- Preventive maintenance uses actual routes, materials, fitness and dependency priority. Collected/paid spare allocation is retained on the order so a replacement worker does not purchase the same job allocation again. Older paid carrying tokens remain usable; existing completed progress is not retroactively charged.
- Obsolete maintenance reservations are detached when another goal or field/clinical assignment takes precedence. Detaching a reservation preserves the new route/task; an early regression that canceled boarding was caught and fixed before acceptance runs. Exhausted ordinary workstation/supply queues can yield to rest or medical recovery. Emergency/field/clinical controllers retain their own ownership. Arrival at quarters can display the existing recovery goal instead of the literal Resting task; energy recovery now recognizes both labels at the unchanged rate.
- Rolling sixty-minute measured production/consumption forecasts expose net depletion horizons. Actual upstream life-support faults are checked immediately. A measured critical condition suppresses optional research/launch spending and anthology liaison work; existing questions/arcs remain and resume under normal constraints. Forecasts neither grant supplies nor guarantee a future outcome.

## Costs and physical constraints

Per 100 units of native repair progress: one tool unit, one spare unit and two energy units. Blackout distribution repair substitutes slower personal work for unavailable electrical energy; parts still cost the same. Atmospheric work follows the same metered resource path. Per completed hatch clearance: 0.5 tools, 0.25 spares and 0.5 energy, plus worker effort. Preventive work retains the existing one prepaid spare allocation and meters 0.5 tools/one energy per 100 progress. Early completion uses only applied work; all charges use the existing compensated economy ledger.

These are normalized game units, not a claim of engineering mass/thermodynamic fidelity. Inventory conservation and source/consumption totals are audited separately. Progress is not a free inventory source. Existing reactor/reclamation/fabrication dependencies, hull loss, injuries, exhaustion, grief and permanent death remain.

## Integration and persistence

`web/icarus.html` supplies physical callbacks and integrates the policy into existing maintenance, native emergency, atmospheric and movement functions. Goal-node handling distinguishes waiting at the near-side hatch from entering the room. Changing a repair target retains the known navigation node. The existing maintenance summary carries the latest SOL explanation; there is no new interrupting dashboard.

The optional `repairControl` save group holds bounded recent decisions/notices, cumulative counters and a rolling sample/forecast. It initializes on existing v1.4 saves without resetting crew, jobs, research, maps or inventory. Added order/incident paid-progress fields persist normally. Existing IndexedDB transactions, history archive, core save namespace and explicit Extended Universe import remain in use. No automatic population or weekly-world reset is introduced.

`stability-diagnostics.js` and the existing daily diagnostic row add equipment, incidents, policy decisions, paid-work counts and forecasts. These diagnostics are test-only/read-only. `stability_soak.py` retains older report fields and adds native repair/maintenance detail; it uses production codec order rather than preinstalling the codec in the browser. The legacy codec/checkpoint profile is explicitly retained for reproducing the original v1.4 run, whose primary-cache size diagnostic could otherwise report zero.

## Tests and reproducible investigation

- `investigate_stability.py`: original or current source, passive instrumentation, detailed thirty-minute causal captures, declared original checkpoint profile, real saved states and history.
- `recover_cascade.py`: exact captured-world counterfactual; initial state SHA, crew and inventory match before advancing. No materials or favorable actors are injected.
- `test_repair_policy.js`: route/seal safety, finite paid physical clearance, materials/fitness rejection, dependency priorities, blackout work, stale/duplicate assignment release, reserved-boarding preservation, depletion forecasts and exhausted queues.
- `test_stability_integration.py`: inherited default-core anthology tests plus physical hatch work, impossible/unfunded work, interrupted maintenance, queue/rest, mid-hatch save/reload, completion safety and diagnostic purity.
- `stability_adverse.py`: explicitly installed and verified adverse starting conditions, including funded blackout, unfunded sealed life support, injured engineers and unsafe pressure/jam; permanent losses and exact reload are retained.
- `stability_soak.py`: fresh deterministic 30/90/180/365-day milestones over multiple seeds, full reload equality, daily clock/identity/resource/source audits and actual activity metrics.

Large counterfactual files are passed by file path; browser state is transported as JSON strings to avoid expanded-protocol memory growth. One adverse-fixture attempt was invalidated because pagehide saving overwrote live storage edits; final fixtures install before bootstrap and verify exact inventory/hardware before simulation. Failed setup and introduced-regression attempts are not acceptance results.

Final test counts, source hashes, counterfactual outcomes, long-duration incident/maintenance/resource/crew statistics, honest limitations and unresolved issues are in VALIDATION_v1.4.1.md and packaged reports. Survival alone never closes the acceptance gate; the audit must show feasible assignments, real paid work, meaningful anthology/science continuity, conserved inventory and coherent failures.


Additional verified queue defects: station admission previously bypassed supply acquisition, returning workers could overbook capacity, routine queued maintenance could work without tools, and the actual `Recover social needs` meal goal was not recognized by social recovery. Four focused browser cases fail against unchanged 602b4a2 and pass the corrections; this strengthens the galley-prevention analysis without claiming every original queue event caused the decisive jam. Returning paid allocations now respect capacity, admitted workers share the existing supply path, and paid meal activity satisfies the existing social need.

An intermediate full-year campaign revealed hundreds of alternating relay/hull trips after two recorded failures exhausted each extraction objective. Core route selection ignored the frontier controller's two-failure objective limit, burning finite fuel without actionable field work. The route selector now uses those same recorded limits and rejects field-only travel without return-capable transport. Captain course overrides remain available. These superseded runs are diagnostic evidence, not final acceptance; the complete campaigns are repeated after the fixes.


## Verified release scope and remaining balance work

VALIDATION_v1.4.1.md records all 12 cumulative milestone results from three complete normal-frequency years, the identical-world counterfactual and four adverse outcomes. The original failure is repaired without reviving already-dead crew. The final source/resource audit separates fresh finite field returns from inherited process-scrap recycling; gross recovered ore is not a mining statistic. Normal campaigns prevent native machinery faults through actual maintenance, while captured-world and adverse regressions explicitly exercise failed machinery. Small repeated harvests after new measured ore deficits remain inefficient balance behavior, distinct from the fixed travel loop after exhausted objectives; batching and expedition-overhead forecasting are recommended refinement, not claimed complete. The release remains a targeted core stabilization, not final commercial readiness.
