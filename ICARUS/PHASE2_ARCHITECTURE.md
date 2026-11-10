# Phase 2 Living World architecture

Baseline: approved plan at 5b14078, runtime inherited from the user's working Phase 1 Lite source c73c7da. The ship, existing two field grids, equipment, custody, economy, research and original crew remain authoritative. No second universe, truth store, navigator or population generator was added.

## Knowledge and communications

`knowledge.js` owns optional version-1 `state.knowledge`: immutable source-backed facts and per-actor acquisition entries, message queue and migration metadata. Entries retain source ID, acquisition/observation tick, physical location, method, confidence, disclosure and sender/delivery timestamps. Observation admission checks the canonical event and actual witnesses. Inference requires known premises and cannot increase their certainty. Private facts require explicit consent to queue; canon cannot be admitted as an observation. Dead senders retain records but cannot transmit; recovery requires a live actor at the actual recorded body location.

`knowledge-runtime.js` adapts that ledger to existing physical channels. Conversation requires a stationary shared node. Radio requires the working ICARUS receiver, power and existing uninterrupted relay/field hardware. Returning carriers can hand over records at actual ship terminals; an old room label while in a corridor is insufficient. Delayed reports stay pending across saves; tick processing delivers at most eight messages per physical minute. Existing review/research tasks may read shared records at working terminals, and staging teams read delivered charts before departure. Captain archive controls use the same checked APIs. NPC registries gain actor records only after a real existing contact execution; no canon knowledge is seeded into them.

Private local events are retained in full source history, but `story.js` and `chronicles.js` withhold them from public recaps until an actual delivery creates a public report. Delivered reports reference both original source and fact, preserve uncertainty and publish once. Public field maps use delivered observations and last received position, not the hidden physical exploration flags. Research intake requires received evidence and retains material custody checks. Military archives reuse their existing IDs and actual room surveys.

Migration preserves old charts and already published archives as explicitly **legacy records**, without inventing original crew witnesses. Archive knowledge IDs are additive. Current knowledge is not reseeded on reload. Knowledge/dead-carrier state survives real Monday boundaries, exports and durable reloads. This is epistemic simulation in a single-player application, not encrypted access control: captain perspective, creator editor, full backups and debug inspectors can reveal private state.

## Organisms and ecology

`creatures.js` updates existing `unifiedWorld.organisms`, not a duplicate registry. Active adult/juvenile decisions occur every five physical minutes using keyed seeded draws. A sealed or dormant organism cannot pursue. Local perception reaches only its current node and an adjacent accessible node; routes reuse real ship hatches/bulkheads/lifts and asteroid/derelict grid barriers. There is no global prey search, encounter quota or scheduled release.

Finite health, energy and stamina constrain hiding, sensing, pursuit, attacks, retreat/rest and feeding. Rest spends energy; feeding debits bounded biomass of a real co-located deceased body. Low pressure and severe fire harm active organisms under an explicit gameplay species rule, not a claim of real biology. Movement traverses at most one graph edge per decision. Attacks require co-location, a cooldown, energy and a seeded decision; injury records link the actual encounter source. Existing medical recovery, permanent death and memorial systems remain authoritative. State-transition traces retain at most 64 entries.

Existing egg exposure, android host exclusion and 240-minute incubation/180-minute maturation remain. Birth uses the physical host body independently of whether that actor is alive. An offspring born inside an active transport remains there until recorded arrival; an unrecovered vehicle does not teleport to the ship. Ambiguous legacy field organism locations remain preserved and immobile pending explicit location recovery.

## Embodiment and calendar

`embodiment.js` is a read-only projection of existing navigation, task, interaction, medical and carried-supply state. It refines existing schematic sprites rather than replacing either art mode. Actual nodes drive corridor/deck markers; waiting, work, conversation, rest, carrying, treatment and alarm response have readable cues. Build, wheelchair and prosthetic cues are schematic. Reduced motion persists in the browser and respects OS settings. Docking telemetry connection mutations now belong to simulation ticks, not rendering.

`lunar.js` uses the unchanged MIT Astronomy Engine 2.1.19 vendored source. It computes geocentric phases offline and marks the configured timezone's date containing the full-moon instant, within declared UTC years 2000–2100. The bounded month cache and presentation flags never drive incidents or pacing. See LUNAR_MODEL.md for independent NASA checks and tolerances. Individual observances use explicit annual, absolute or bounded multiday dates, with opt-out and real already-paid meal requirements.

The production 4×/nine-holiday 1× clock, eight recognized observances, real Monday–Sunday episodes, six-hour recovery cap, monotonic world clock and existing namespace are unchanged. `world-schema.js` validates the optional new groups; old saves need not contain them. The Python host, launcher, configuration, requirements and Android thin-client authority remain unchanged.

## Validation boundaries

Daily diagnostics add knowledge/creature audits and measured counts without changing inherited fields. Campaigns use the real calendar controller and ordinary simulation steps, hourly wall-clock progression, fixed seed/timezone and explicit checkpoint reloads; automatic per-step autosave is disabled in the test driver. Adverse fixtures are labeled separately. PHASE2_VALIDATION.md reports actual results. Runtime ZIPs contain all loaded assets and licenses; test runners and packaging tools stay in source/evidence, outside Lite.
