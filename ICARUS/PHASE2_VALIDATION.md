# Phase 2 Living World — measured validation

Status: the implemented increment is verified within the boundaries below. This is not final-release certification or a claim that every inherited controller is fully knowledge-based. See PHASE2_LIMITATIONS.md.

Runtime source: **113e79b7693db4c37c8519449339032cf2ed60a1**. The independent Lite extraction has all **49 runtime files** byte-identical to this commit. Subsequent test-harness fixes are in **177e367b2d7d516fb749c25b62e992191de19463** and do not alter runtime hashes. The manifest/ZIP source remains 113e79b. Detailed machine-readable evidence: [reports/phase2/accepted_summary.json](reports/phase2/accepted_summary.json), with the source/runtime hashes and campaign-specific source commits.

## Automated results against the extracted Lite ZIP

| Suite | Actual result |
| --- | --- |
| Node deterministic unit tests | 217 passed, 0 failed, 0 skipped; baseline 158 plus 59 added cases |
| Living World browser integration | 46 passed |
| Stability browser regression | 30 passed |
| Extended Universe compatibility browser regression | 44 passed; archived v1.3 fixture used only for migration testing |
| Ordinary production clock | 2 passed; real page timer, normal 4×, synchronized holiday 1×, pause/resume and old speed-button handling |
| Remote Deck bridge | 3 passed; real HTTP/Chromium, physical input stubbed |
| Pixel 5 touch/mobile flow | 15 checks passed; pairing, persistent hash/token, authoritative PC course/hold, thin-client layout, reconnect, Origin denial, allowlisted stub input/TV and unpair |
| Syntax/dependencies/package identity | All local script dependencies present; 46 script/Python syntax checks; 54 retained source-file hashes plus manifest verified |
| Historical Phase 1 Lite full backup | 10,659 history records preserved; every original compared domain unchanged apart from 24 verified additive archive knowledge IDs; exact reload; resumed tick 36,000 → 36,120 |
| New Phase 2 day-30 backup | 50,170 history records in the receiving browser, preserving all 50,169 campaign source records; knowledge/world domains exact; reload exact; resumed tick 160,920 → 161,040 |

The browser suites overlap inherited cases; their counts are executions per suite, not a claim of 125 distinct feature scenarios. Tests run outside Lite and point at its independently extracted assets. Test runners/reports/development tools are excluded from the runtime ZIP.

New regression coverage includes isolated observers, false witnesses, broken/restored radio, delayed and once-only delivery, private consent, canon exclusion, body record recovery, actor/backup continuity, clinical/creature privacy, informed bereavement, physical terminals, pending reports through a real Monday, actual barrier reporting, knowledge-graph reachability and autonomous departures. Ecology cases cover quiet/sealed adults, inaccessible routes, local pursuit, costly causal attacks, fatal injury/memorials, finite biomass/starvation recovery, environmental harm, vehicle containment and save determinism; android host exclusion and 240/180-minute development remain covered. Poses/physical nodes, waiting, treatment, carrying, item handoff, mobility and reduced-motion persistence are checked. Eighteen lunar tests include sixteen independently published NASA full-moon times, timezone boundaries and two full moons in May 2026.

## Final continuous campaigns

Start: **2026-10-28 00:00 UTC**, timezone **America/Chicago**. The ordinary simulation/calendar controllers process hourly wall-time intervals with fixed seeds. Per-step autosave is disabled in the explicit accelerated driver; saves and exact reloads are checked at recorded checkpoints. The nine approved holidays and real Monday–Sunday episodes stay active. Thirty real days yield **111.75 simulated days**, rather than 120, because synchronized holidays run at 1×; seven real days yield 25 simulated days.

| Profile | Real days | Simulated days | Alive / dead | Arrivals | Field / local frontier missions | Science cases | Actual creature attacks |
| --- | --- | --- | --- | --- | --- | --- | --- |
| normal_1001 | 30 | 111.75 | 20 / 0 | 5 | 14 / 5 | 26 | 0 |
| normal_4807 | 30 | 111.75 | 20 / 0 | 5 | 9 / 5 | 23 | 0 |
| compound_1001 | 7 | 25.0 | 20 / 0 | 5 | 8 / 5 | 15 | 0 |
| chamber_4807 | 7 | 25.0 | 20 / 0 | 5 | 10 / 5 | 23 | 5 |

All four final campaigns completed with zero resource, frontier, chronicle, knowledge or creature audit errors; no discarded/rolled-back wall time; all original crew identities accounted for; and exact checkpoint reloads. Each made five actual arrivals through the existing bounded local context. Ordinary voyages are rejected as evidence if they remain motionless. They had completed, evidence-justified field objectives and five local survey jobs, without forced incident or discovery quotas. Final zero staging failures do not erase the earlier regression that exposed incorrect failure handling.

The compound profile explicitly starts B07/C09/C07 at 10/32/45 condition and Frank at 55 health. The released-chamber profile starts the existing adult unsealed/awake in asteroid cell 23 with an already-onsite two-person team and supplies transferred from finite ship stock. Both use normal backup import, assert actual starting conditions before any tick, record the initial snapshot/payload hash, and assert daily saves. These are **adverse fixtures**, not natural release/injury claims. The released adult made 35 graph steps, produced five genuine attack source events, and ended at asteroid cell 6 with zero energy/starved; it did not receive free recovery. There were two documented team-safety withdrawals. Fatal and unrecoverable outcomes are tested separately; no campaign is called valid merely because all crew survived.

## Research, information, resources and growth

Ordinary seed 1001 retained 106 experiments: 74 complete, 28 no-result and 4 failed; seed 4807 retained 96: 72 complete, 22 no-result and 2 failed. These are experiment statuses, not automatic discoveries. Confirmed conclusion counts were 2 and 4, under the existing independent-evidence rules. Lazarus was not forced to succeed.

The ordinary runs ended with 284/257 source-backed facts and 364/335 deliveries across actors. No reports remained pending at the final checkpoints, but isolated/broken-channel tests verify they do stay pending when required. All fact sources resolve to retained actual history or explicitly labeled legacy charts. No private source ID enters public chronicle source lists; publication creates a separate delivered report. Attack counts exclude those later report copies. Full history retained 50,169/50,952 actual records in the ordinary runs.

The resource audit checks the existing inventory/production/consumption/feedstock/cargo identities at every daily sample. Ledger sources include incident starlight, finite reactor fuel conversion, ore-to-parts conversion, finite specimen bulk, nutrient/water medical culture and paid recycling. Cumulative recycled throughput is not net resource creation. Full conversion/consumption/transfer ledgers are retained in campaign backups; source totals appear in the JSON summary. No new economy or source-granting mechanism was added.

| Ordinary seed | Food | Water | Oxygen | Energy | Medical | Spares | Tools | Lab | Fuel spent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1001 | 159.99 | 152.84 | 110.19 | 179.85 | 20.00 | 69.73 | 69.99 | 80.00 | 1.9625 |
| 4807 | 159.33 | 153.07 | 111.33 | 179.84 | 20.00 | 70.00 | 70.00 | 80.00 | 1.9625 |

Primary compressed cache grew from 307,324 → 1,047,780 bytes (seed 1001), and 312,076 → 1,039,714 bytes (4807), over 111.75 simulated days. Persistent history/knowledge naturally grow with real records; this is measured growth, not a mathematical guarantee of bounded saves forever. Delivery receipt/organism traces are bounded, derived actor maps are not serialized, and streamed archival/indexing work remains open.

## Findings, rejected attempts and verification limits

Earlier stable-but-motionless campaigns were rejected: missing chart boundaries and failed-boarding accounting stalled departure. The fixes are documented in ENGINEERING_PHASE2.md and protected by the survey-to-navigation regression. Lethal emergence initially used an invalidated live-actor lookup; finite-food starvation recovery had an early-exit defect; both were corrected and retested. A transient syntax error during source editing did not recur on stable-source runs. A reduced-motion test initially asserted before asynchronous reload bootstrap was ready; its readiness synchronization was corrected and the full suite rerun.

Initial alleged adverse runs were also rejected because page-hide persistence overwrote cache-based setup. Their world audits passed but did not prove adverse survival. Only the final, asserted backup-import profiles above count. Superseded and interrupted attempts are separately labeled in the evidence bundle. No favorable result substitutes for an unavailable or failed test.

Environment: Linux-6.18.57-x86_64-with-glibc2.41; Python 3.12.14, Node v24.22.1, Chromium 156.0.8078.79 built on Debian GNU/Linux 13 (trixie), Playwright 1.62.0.

Not run:

- Native Windows BAT launcher and actual PyAutoGUI desktop/game input (Linux environment; input stubbed).
- Physical Android phone, Wi-Fi interruptions and Samsung TV hardware/TLS (mobile emulation and TV socket stub used).
- Firefox/Safari, hostile concurrent browser writers, exhaustive fuzzing/penetration and transitive dependency audit.
- Antivirus engine scan (clamscan/Windows Defender unavailable); no protection was disabled or bypassed.
- 180/365-day Phase 2 full-world campaigns; final tested durations are stated individually.
- The user's live Windows browser profile was not accessed; migration uses a real historical Phase 1 Lite campaign backup.

Static security review: SECURITY_PHASE2.md. No antivirus or Safe Browsing protection was disabled or bypassed. External contact knowledge currently represents entity-level radio endpoints; full individual background-NPC crew life/knowledge is not implemented. Human long-form story interest, final art, fully belief-based legacy social/contact controllers, autonomous body-record recovery and physical-device release qualification remain open. Next batch should refine those existing systems and save performance rather than expand the universe.
