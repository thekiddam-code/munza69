# ICARUS Phase 4.7 — Development Checkpoint

**Phase4.7 is NOT complete. This is a review checkpoint, not the finished Forward Operations release.** The previous Phase4.6 Startup Size Hotfix remains unchanged. Do not interpret passing selected tests as satisfying the missing camp/deployment acceptance gates.

[Download checkpoint ZIP](https://raw.githubusercontent.com/thekiddam-code/munza69/codex/forward-operations-phase4-7/downloads/phase47-checkpoint/ICARUS_Phase4_7_Development_Checkpoint_Lite.zip) · [SHA-256](SHA256SUMS.txt) · [Package verification](package_verification.json)

Implemented: persistent original FOC-01 at C03, scaled cargo exterior view and real crew inspection; every retained local archive ID and captured-frame playback controls; received surveillance categories/current drone views; physical ship-dock escort controller; cooperative catch-up yielding.

**Not implemented:** truck-sized freight/transport/deployment, persistent field camp, camp occupancy/equipment, camp docks/rotations/maintenance, ATVs and camp medical/logistics. Full remote historical media and higher-cadence encoded video remain unfinished. There is no cosmetic camp-deployment action.

529 case executions passed on the frozen source, including the supplied private voyage, Records1–12 access, full snapshot/history preservation and the 49-case remote suite. Another12 checks passed on this extracted ZIP (four running renderer/engine cases and eight boot/writer cases). There is inherited suite overlap. All229 ZIP entries/228 source-file hashes and141 runtime hashes verified. No private save, credentials, tests, raw test reports or packaging tools are included.

Earlier concurrent runs had one remoteCore snapshot difference and a TV tap timeout. Unchanged isolated/serial retries passed, but the load-sensitive snapshot finding remains unlocalized. See the detailed validation report; this is an additional production-readiness concern, not an asserted fixed defect. Physical Windows/Android/TV/Tailscale/antivirus validation was unavailable. Native APK source recovery remains pending.

Before trying a checkpoint, retain a complete pre-upgrade backup and the stable application folder. Stop the old server and host tabs. Extract into a separate folder, retain the same Python environment/browser profile/host/port, run Start_Remote_Deck.bat, wait for genuine readiness and choose ENTER. **Do not clear site data, delete writer records or start a new voyage.** The ZIP includes README_PHASE47_CHECKPOINT.md with backup, migration, configuration transfer and rollback instructions. Older builds require the pre-checkpoint backup for rollback of new task domains.

[Implementation/progress](../../ICARUS/PHASE47_PROGRESS.md) · [Acceptance/results/limitations](../../ICARUS/PHASE47_VALIDATION.md) · [Architecture](../../ICARUS/PHASE47_ARCHITECTURE.md) · [Actual screenshots](../../ICARUS/reports/phase47/screenshots) · [Source results](../../ICARUS/reports/phase47/accepted_summary.json)

The screenshots are actual running renderer captures from explicit technical fixtures, not events claimed from the user's voyage and not conceptual mockups. The original private backup remains unchanged and is not published.

SHA-256: `4631ea53713175fb84d9535edf439d33c8060b603b5af2a5b480ccf27276b9ab`
