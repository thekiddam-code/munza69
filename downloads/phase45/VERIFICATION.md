# Phase 4.5 package verification

The immutable Lite ZIP was built from committed source `4592a904561e6325edd79176231f66c38312093e`. All **134 runtime files** match the independently frozen/tested runtime `4bd2dadbd6e6541ef118e04b50b30ddbf561ae19`. Every one of the 204 retained source-file hashes and all 205 ZIP-entry CRCs passed verification. The generated manifest pins each file. Tests, reports, development tools, packaging scripts, generated credentials and test worlds are excluded. Runtime dependencies remain included.

Lite SHA-256:

```text
5395c11cd8db4c421a089f042f31d54fadc203fd02ad7898eef231a4dd129efe
```

Windows verification:

```powershell
Get-FileHash .\ICARUS_Phase4_5_Visual_Overhaul_and_System_Boot_Lite.zip -Algorithm SHA256
```

Compare the entire result with the checksum above or `SHA256SUMS.txt`. Do not bypass antivirus protection.

## Executed tests

| Final source suite | Passed |
| --- | ---: |
| Node deterministic models | 384 |
| Full browser integration | 93 |
| Real-HTTP remote integration | 45 |
| Production clock/calendar | 4 |
| Legacy continuity | 19 |
| Server/services | 18 |
| **Source case executions** | **563** |

No final source failures, errors or skips. Counts include inherited tests executed independently across suites. Focused development reruns are excluded.

Against the **extracted ZIP**, an additional **6 visual + 6 remote/authorization + 9 expedition checks passed** (21 total; 26.599s, 27.090s and 155.984s respectively). See `package_verification.json` and evidence `reports/accepted/package_*.json`. The complete source suite was not repeated after packaging: exact byte identity of all runtime files plus these 21 extracted-package checks establish package provenance.

## Campaigns and observed behavior

Both fixed-seed campaigns ran 7 real days / 25 ship days, reached episode 2, preserved checkpoint reload state and made **five actual arrivals each**. Both retained 20 living crew, zero deaths, and passed resource/source, privacy, transit, engineering, gravity, knowledge, creature and expedition-custody audits.

| Metric | Normal 1001 | Explicit adverse 4807 |
| --- | ---: | ---: |
| Asteroid sorties | 4 | 5 |
| Visited field cells | 20 | 20 |
| Received records / frames | 32 / 152 | 37 / 175 |
| Science investigation cases (not breakthroughs) | 17 | 17 |
| Conversations | 449 | 456 |
| Source history records | 12,269 | 12,504 |
| Sunday films | 1 | 1 |
| Final snapshot bytes | 8,026,288 | 7,930,244 |

The adverse campaign explicitly initialized damaged B07/C09/C07 equipment and one injury through the actual backup interface. These were test conditions, not claimed spontaneous events. Reports retain the exact conditions, transitions, decisions and audits.

The actual-time watch used real wall/monotonic time: 122.8645s at measured 3.9067×, then 541.6641s at measured 20.0493×; reload preserved tick 99 and 20× selection. Paired-phone emulation disconnected/reconnected successfully. Eight BODY samples, two real conversations and 16 completed lift trips were observed; no duplicate sources or discarded wall time. Whole watch: 687.0646s. Post-reload cumulative canvas/UI work averaged approximately 0.880ms per counted canvas, with a retained 156.2ms maximum; this is not a physical-device FPS guarantee.

## Review and limits

[Static security review](../../ICARUS/SECURITY_PHASE45.md) documents local key authorization, existing paired control/network and PC/TV capabilities, launch/dependency commands, credentials and trust boundaries. No antivirus bypass or protection changes were introduced. [Architecture](../../ICARUS/PHASE45_ARCHITECTURE.md), [validation](../../ICARUS/PHASE45_VALIDATION.md), [limitations](../../ICARUS/PHASE45_LIMITATIONS.md) and [visual comparison provenance](../../ICARUS/reports/phase45/VISUAL_COMPARISONS.md) distinguish implemented behavior from incomplete work.

Not run: physical Windows laptop, Samsung phone/tablet/TV, native APK build, real LAN/Tailscale, antivirus scanning, human visual/accessibility/touch and device GPU testing. Native build remains pending source recovery. Gym is explicitly deferred; A03 is unchanged. These tests do not certify final art, a collision physics engine, 365-day stability or final release readiness. Earlier failed/interrupted runs are retained as diagnostics, not counted as passing acceptance runs.
