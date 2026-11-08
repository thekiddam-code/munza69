# Audit of v0.94.8 and v0.94.9 changes

Baseline Git commit: a85fa03099e4cd491fe84ceb015eb5e09ecf03d8.
Read AGENTS.md, CODEX_START_HERE.md, historical README documents, server.py, soak_test.py, and the relevant state, save, weekly rollover, mission, custody, science and rendering paths in web/icarus.html.

## Architecture and findings

The browser simulation uses private closure state, minute-based ship and field ticks, and an existing remoteCore tree for mission and science persistence. The Python server provides static assets and paired Remote Deck/host-key APIs, independent of scientific behavior. Science intake already deduplicates recovered findings, waits for physical transfer, holds custody exceptions, assigns eligible personnel, and performs preliminary metadata classification. Mission opportunities and outcomes use recorded exploration progress; research need not alter mission authorization.

The baseline had no structured scientific hypotheses, grouped programs, experiment costs, or experiment outcomes. Added web/research.js as a local, separately testable model; minimal integration calls it after existing scienceTick and displays its records in sciencePanel. Existing expedition decisions, autonomous captain/SOL authority and player intervention are preserved. New research has no network or command execution capability.

Automatic weekly rollover previously retained remote science while discarding specimenCustody, orphaning its evidence. Preserve custody across that automatic boundary; retain manual reset semantics. Existing save keys, core format, mission registry and original report fields are unchanged. The client footer reports v0.94.9.

## Automated coverage

Fifteen Node tests cover legacy initialization, grouped evidence provenance, resource charging and same-clock idempotency, custody/transfer/containment/lab/analyst/supply gates, pause/resume, active experiment serialization, finite failure/no-result states, loss of evidence support, and existing mission command/release/recall/abort behavior. Tests use the production model and production mission intervention function.

Two real Chromium seven-day runs exercise the integrated simulation. The ordinary run checks natural missions, crew energy/count, episode/tick continuity, archives, documented mission objectives, browser errors and exact save/reload snapshots. The explicitly seeded run additionally checks grouped cases, completed/failed/no-result experiments, hypothesis provenance and uncertainty, early save/reload during research, and specimen custody through weekly rollover. Both also verify the diagnostic clock remains paused without explicit advance calls. Raw reports and Node output are supplied separately, not committed as source.

Python server/runner compilation and all embedded JavaScript plus research.js syntax are checked. These checks establish syntax and the listed behaviors, not exhaustive coverage of every legacy visual/system interaction.

## Limits and unrun integrations

The simulation remains stochastic; no deterministic replay claim is made. Screens examine recorded specimen properties; no composition, viability or revival assay is implemented, and no Lazarus research is fabricated. Blocked hazardous specimens remain blocked pending a future safe protocol. Experiments cost laboratory supplies and serialize a research slot; they use existing crew eligibility without replacing normal crew scheduling. Physical Windows input/game controls, tablet pairing, and Samsung TV commands could not be exercised without those devices. Their server code is unchanged. Broad visual regression and every manual backup/reset UI path were not tested.
