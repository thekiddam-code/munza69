# Seed 1001 investigation — evidence and classifications

Baseline: ICARUS v1.4 commit 602b4a2. The read-only instrumented replay using the original seed and day-30/day-90 save/reload sequence reproduces all twenty deaths around elapsed day 347. A second uninterrupted seed-1001 replay survives the year; therefore the seed alone is not a complete replay specification. Both results and checkpoint profiles are retained. Instrumentation only reads state, never draws randomness, advances time or changes decisions.

## Recorded causal timeline (elapsed simulation minutes)

| Tick | Actual recorded transition | Classification |
| ---: | --- | --- |
| 486756–486898 | Fabricator fault is detected, dispatched and repaired | Normal recoverable wear/failure |
| 487284 | Galley equipment crosses its failure threshold; last unresolved galley fault begins | Intended deterioration; prevention/dispatch delay needs attention |
| 487523 | Frank is dispatched to the galley | Available crew exists; response is feasible before the jam |
| 487524 | Critical local degradation jams the galley hatch | Intended hazard; actual atmosphere remains pressure 100, oxygen 21, no fire/breach in captured state |
| 487547, 487619, 487763 | Jules, Theo and Tomas are also assigned to the same unreachable galley | Poor dispatch policy: en-route reservations ignored, all engineering capacity consumed |
| By tick 488160 (day 339 end) | All four engineers have null routes to A04, hundreds of minutes of navigation wait, and healthy energy reserves | Confirmed infeasible assignments; real pathfinding differs from placeholder `path()` distance |
| 488352 | Air scrubber fault begins with no free engineer | First unresolved upstream life-support fault |
| 488892–489156 | Research, fabricator and security faults accumulate | Unattended wear and operational cascade |
| 489612 | Power-distribution fault begins | Upstream production endangered despite finite fuel and parts remaining |
| 489832–489873 | Backup battery warning/critical transitions are recorded | Intended dependency cascade |
| 490620 | Cooling fault adds a further production dependency failure | Intended machinery dependency |
| Around days 344–347 | Stored water/oxygen/energy deplete; repeated shortage injuries precede permanent deaths | Coherent resource/medical consequences, not disappearing crew |

Exact source IDs, thirty-minute state transitions, assignments, inventory and death times are in the packaged investigation reports. Calendar ship-day labels include the initial eight-hour offset; the table uses monotonic elapsed ticks.

## Confirmed defects and policy failures

1. Native emergency selection uses `path()` (a high-level destination token), not the actual corridor/hatch pathfinder. The galley can be selected while actual navigation returns null.
2. A fault with an engineer already en route can attract another dispatch every 24 minutes. No reserved-responder cap or stalled-route release protects other life-support work.
3. Existing jam recovery requires an engineer already inside the inaccessible room. When all available engineers are outside, the repair predicate is circular. Fixing this must require physical access to the near-side hatch, real paid work and safe pressure/fire conditions; captain-sealed doors must remain sealed.
4. Maintenance reservations can outlive a changed goal or medical/rescue duty. The maintenance timer then prolongs an unrelated action. This is independently testable and a contributing scheduling risk, not a claim that every social interaction causes the cascade.
5. Existing native emergency work increments condition/progress without consuming tools, spares or energy. That is independently a conservation/feasibility defect; initial scarcity did not cause this particular failure because stocks were available.

6. The displayed rest task changes to its goal on arrival (`Recover energy`), but the former body loop replenished energy only for the literal `Resting` label. Arrival could therefore delay needed energy recovery until the next task assignment. The repair policy now recognizes the existing recovery goal; no extra recovery rate is granted. This is an independently tested scheduling defect, not a claim that it caused the initial galley jam.

## Captured-world intervention

The identical day-339 saved state has SHA-256 `b87ee10fa58f1153e6c7f0217f8c169f482bc07cf89a9b6d941442eac62aa690`. Both replay variants verify exact initial crew and inventory. Over twelve days, old rules lose all twenty crew; the repaired variant retains twenty, clears two hatches through 200 applied paid work units, completes eight native incidents and 77 preventive jobs in the recorded intermediate repaired run. Final-runtime results are separately retained; no material or favorable crew state is added to the captured case.

## Intended behavior retained

Finite stocks, wear, hazardous access, limited labor, production dependencies, exhaustion, injuries and permanent death remain valid. Repair prioritization cannot create tools, make an absent person physically present, clear a captain seal, negate a fire or guarantee survival. A no-tools/unsafe-access catastrophe must remain possible and explicitly recorded.

## Investigation boundaries

The different uninterrupted and checkpointed histories require reproducibility analysis; a fixed initial seed must always be reported with the same external actions/checkpoint profile. Additional repair/forecast changes will be tested with independent adverse fixtures and complete fresh campaigns. No repair is considered verified merely because a different seed survives.
