# Known limitations, unresolved scope and next batch

## Complete bounded behavior in this build

Research supports finite, uncertain local experiments and honest no-results; crew injury, treatment, death and continuity have real consequences; SOL runs the existing mission/maintenance/emergency systems with new fitness/risk/resource policies; recaps select actual journal evidence. Tests and both requested simulation durations were executed. These systems are integrated into the existing gameplay rather than independent demos.

## Reduced or deferred scope

- Independent biological activity acquisition, composition instrumentation, viability replication and safe revival protocols are not implemented. Longitudinal Lazarus research collects real case references and requests replication only when recorded activity exists. It cannot guarantee a breakthrough. Existing manual specimen reconstruction gameplay is retained and remains a separate apparatus; research does not resurrect dead crew.
- No combat, wildlife damage, tactical kill recording or rendered kill-camera animation was added. Legendary recap eligibility is implemented and tested, but no current combat producer creates such records. Environmental deaths remain excluded. Incident visuals and recaps remain labeled reconstructions.
- Expedition transport still carries one field crew member. Relationships with shipboard support influence assessment; multi-person field tactics are deferred. New health/risk mechanics supplement existing personality/experience decisions rather than replacing every legacy task choice. Routine schedules still exist; consequences and recaps derive from actual state.
- Treatment shares existing clinical hardware and cartridges with legacy energy-stabilization cycles. There is no detailed organ model, disability-specific navigation, surgical scheduling or disease propagation.
- Cargo reserves are finite starting stores and persist across weeks. This batch does not implement a market, farming, manufacturing supply chain or off-ship food procurement. Empty reserves block resupply and research; critical ship consumable economics need longer balance work.
- Automatic episodes deliberately retain legacy ship-system resets, while crew and field history persist. This is campaign continuity with periodic ship-system refresh, not a physically continuous unlimited voyage. Manual New Episode remains a full explicit scenario reset.
- The inherited directorClock adds a 480-minute offset at automatic episode rollover. Research progress and new experiment timeout/reassignment counters advance by explicit ticks. Legacy mission cooldown deadlines can expire earlier across that boundary. Current seven/thirty-day clock checks validate the legacy convention, not a unified elapsed-time redesign. A versioned migration of old mission timestamps is deferred to avoid silently reinterpreting existing saves.
- Journal retention is bounded at 4,000 events; archived recaps retain selected sources. Detailed old events and live-only movement frames can age out. The optional ending is a factual text anthology, not generated film or voiceover.
- Seeded browser tests verify same-seed simulation and future continuation after reload. No promise of bit-identical saves across browser versions, wall-clock archive timestamps or user interaction sequences is made. Long-duration coverage uses seed 1001, plus injected adversarial scenarios, not exhaustive Monte Carlo coverage.
- Windows input/game controls, physical tablet pairing, Samsung TV commands and broad visual snapshot regressions were not exercised in this Linux environment. Server syntax was checked and the device host was left unchanged. Test coverage does not prove every legacy UI flow.

## Recommended next development batch

1. Introduce versioned continuous elapsed time and migrate all mission/research deadlines with legacy timestamp fixtures; eliminate the weekly deadline offset without losing old campaign history.
2. Add actual non-invasive instrument measurements and independently replicated assays, scientist peer review and safe protocol development. Keep custody/uncertainty provenance and avoid scripted Lazarus success.
3. Add finite resource procurement/manufacturing based on newly recovered material, medical triage staffing and multi-crew expeditions; measure balance over many seeded 90-day runs.
4. Extract legacy atmosphere, rescue and maintenance logic into tested modules; extend browser tests to captain controls, backup import, manual scenario resets and physical-device test stubs.
5. Add structured encounter producers and recording provenance before implementing any lethal encounter playback. Keep extraordinary selection rare and optional.
