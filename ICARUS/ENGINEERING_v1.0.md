# ICARUS v1.0 — The Living Simulation

An integrated, bounded implementation of all five development phases, continuing v0.94.9 commit 08fd082. This build retains the NIGHTGRID interface, Remote Deck host, mission authority and captain controls. It does not claim exhaustive feature parity with a finished commercial simulation.

## Baseline and milestones

Read AGENTS.md, CODEX_START_HERE.md and the existing release documentation. Audited closure state, private social/learning systems, atmospheric survival and routed rescue, clinical tissue repair, Lazarus entities, maintenance/workstations, autonomous mission dispatch, evidence custody, saves and the Playwright runner. The untouched v0.94.9 baseline passed a seven-day browser run; its raw report is included.

1. Scientific discovery: finite experiments now have injected uncertainty, biological assays, conservative containment gates, recorded reviewer disagreements and an evidence-linked longitudinal Lazarus program. Missing activity data yields no result. Existing manual Lazarus procedures now retain a nonzero incomplete-reconstruction chance even at low risk. No living crew are revived by scientific metadata.
2. Living crew: persistent health, fatigue, morale, injury history and mission experience complement existing personality, trust and relationships. Hazard exposure and field accidents can injure or kill. Safe, powered, staffed medbay treatment consumes finite sterile cartridges; treatment improves relationships. Death records preserve the deceased crew member and cause, remove them from operational staffing and cause survivor grief. Zero survivors is saved and remains terminal.
3. Autonomous operations: existing SOL/captain dispatch and explain/recall/abort/command/release controls remain. Candidate fitness and recovery reservations constrain launch; risk assessments record condition, experience and support relationships. Risk affects field work rate and actual accident exposure. Debriefs retain evidence and crew condition. Maintenance ranks urgency and life support. Quartermaster transfers debit finite cargo reserves instead of manufacturing replenishment. Existing evidence-based opportunity gates prevent exhausted maps from generating weekly repeat expeditions.
4. Emergent storytelling: a persistent bounded journal records actual system, social, research, medical and casualty events. Recaps select character highlights, failures and relationship events with source IDs. Automatic archives retain episode recaps. Optional anthology endings summarize actual outcomes. Legendary selection requires an extraordinary lethal encounter plus a matching existing incident-record ID; ordinary environmental casualties do not qualify. All recap presentation is labeled as journal reconstruction, not footage.
5. Stability: seeded stochastic state is persisted. Deterministic unit tests and full-browser comparisons exercise identical seeds and save/reload continuation. Automatic weekly transitions preserve all surviving crew/personality, deceased registry, research/custody, Lazarus entities, finite reserves and explored field maps. Tests cover adverse conditions and legacy migration.

## Architecture

The legacy simulation remains in web/icarus.html. New domain logic is kept in small local modules with browser and CommonJS exports:

- web/research.js: hypotheses, case grouping, experiments, uncertainty, reviewer disagreements, long-term Lazarus evidence stages. One shared experiment slot. Prolonged blocked experiments terminate safely; analysts can be reassigned without paying twice.
- web/living.js: serializable RNG, vitals, injuries, clinical resources, death/grief, fitness/risk and campaign continuity capture/restore.
- web/operations.js: finite cargo transfers, maintenance priority, mission assessment, field accident/health withdrawal and debrief policy.
- web/story.js: bounded source journal, character and event selection, optional factual endings, strict legendary-record eligibility.

The HTML supplies existing state, real simulated minute ticks, atmosphere, crew, hardware and log callbacks. New modules make no network calls and execute no shell commands. The Python host and physical device handlers are unchanged. Script assets are local and compatible with the existing static server.

## Persistence and time

The existing version-2 save key and backup format remain. Old 20-person saves acquire vitals and research/journal defaults. New saves validate exactly 20 unique founding identities across survivors and the deceased registry. All terminal casualties remain serializable. Older application binaries cannot understand a reduced living roster; export backups before downgrading.

Automatic weekly transitions retain campaign crew and field consequences while preserving the legacy fresh ship-system episode initialization. Work routes and stale shipboard assignments are cleared; away crew retain expedition state. Manual New Episode remains an explicit full scenario reset and can restore the founding roster, as in the old interface. It is not an in-world resurrection mechanic.

Simulation randomness uses persisted seeded entropy. Independent equal-seed browser sessions and future evolution after save/reload are compared. Archive endedAt remains wall-clock metadata, so byte-for-byte archive wall timestamps are not a deterministic-replay guarantee. The existing weekly convention starts a new episode at 08:00: each episode spans 9,600 explicit advance minutes. The runner checks that convention at both durations. Existing directorClock-based deadlines retain the inherited weekly clock offset; see known limitations.

## Testing and evidence

Commands from ICARUS:

```
node --test test_*.js
python test_integration.py --report integration_report.json
python soak_test.py --days 7 --seed 1001 --report soak_report.json
python soak_test.py --days 30 --seed 1001 --report soak_30day.json
python soak_test.py --days 7 --seed 1001 --seed-science --report science_7day.json
python soak_test.py --days 30 --seed 1001 --seed-science --report science_30day.json
```

Playwright and Chromium are required for browser tests. Set ICARUS_CHROMIUM to an installed browser path if necessary; this build was tested with /usr/bin/chromium. Python runtime bridge dependencies remain in requirements.txt; Playwright is a development dependency.

Final results: 33 unit tests and 9 real-browser integration tests passed. Natural and synthetic-evidence runs passed at seven and thirty days, with zero browser JavaScript errors and exact final save/reload equality. Thirty-day runs completed four automatic transitions. Natural seed 1001 produced six justified, completed missions and no recovered science items; this is explicitly not evidence of research coverage. The labeled synthetic runs supply three geological specimens, cover completed/failed/no-result experiments and grouped programs, and verify research/custody persistence. Biological assays, disagreements, containment incidents and longitudinal Lazarus progression are covered by injected unit scenarios. Physical-device integrations were not run.

Fixes discovered by tests: zero-health patients must not be healed before death processing; extinct crews must remain valid saved states and never repopulate on weekly rollover; missing medbay hardware must be initialized explicitly in fixtures; unavailable analysts and unsafe specimens must not hold the shared research slot indefinitely. Final reports are authoritative; intermediate diagnostics are retained separately where useful.
