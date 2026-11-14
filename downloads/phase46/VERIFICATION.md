# Phase 4.6 distribution verification

Lite source: `11c49af03292a5ab2dc62d8cb2c1625e69cf8aa5`. Tested immutable runtime: `a22f2aca871e988a94cdd5083f8c99022da53460`.

- All **137 runtime file hashes** match the tested export.
- All **215 retained source hashes** and **216 ZIP-entry CRCs** passed.
- Runtime dependencies remain; tests, development tools, packaging scripts, reports, credentials and test worlds are excluded.
- Lite size:946,603 bytes.
- SHA-256: `eae56476450a826825cdfecfe6a4303ab8b71de31fe3d15d6c3eae2fdde3d960`.

Windows checksum verification:

```powershell
Get-FileHash .\ICARUS_Phase4_6_Autonomous_Exploration_and_Drone_Reconnaissance_Lite.zip -Algorithm SHA256
```

Compare the entire result with SHA256SUMS.txt. No antivirus exceptions or protection changes are needed or introduced.

## Executed final-source suites

| Suite | Passed |
| --- | ---: |
| Deterministic Node models | 405 |
| Full browser integration | 100 |
| Real-HTTP/emulated remote | 49 |
| Ordinary production clock/calendar | 4 |
| Legacy continuity/adverse regressions | 19 |
| Bridge/TV/service units | 18 |
| **Source case executions** | **595** |

No final failures, errors or skips. Counts include separately executed inherited overlap. Earlier failed/interrupted candidate runs are retained as diagnostics and excluded from accepted counts.

**Against the extracted Lite ZIP:** seven drone, four remote/boot, nine expedition and six visual checks passed (26 additional executions). `package_verification.json` and `reports/phase46/accepted/package_*.json` record the exact package source/counts. The entire source suite was not repeated after packaging: all137 identical runtime hashes and these26 extracted-package checks verify the distribution boundary.

## Actual acceptance evidence

An existing engineer physically collected/assembled a paid drone; it charged, launched at tick263, surveyed Landing Shelf plus three previously unknown connected sectors, returned at tick412, retained four received records/18 captured procedural frames and passed exact save/reload equality. No drone, reading, map discovery or recording was injected. The fixture initially made the existing engineer available and held ship navigation. Normal campaigns independently exercised default autonomy without that placement.

Both fixed-seed normal1001 and explicit-adverse4807 campaigns ran seven real /25 ship days, reached episode2 and retained20 living crew/zero deaths. Each made five actual ship arrivals and seven completed drone sorties, received20 sector observations/20 records/98 PNG frames, then stopped at the finite reachable frontier. Landing Shelf was already charted and is not counted as a newly discovered global location. Military seal23 and initial dormant Xenomorph prerequisites stayed intact.

Battery inputs366.9 − use266.9 = final100; charging consumed36.69 finite ship energy units, plus paid assembly energy/components. Independent Python audits checked actual exported ship pools, battery conservation, source IDs, PNG signatures, pre/post bounds and receipt timestamps. Both checkpoint reloads matched exactly. Each campaign also completed two crew asteroid expeditions,18 science investigation cases (not guaranteed breakthroughs), one Sunday film and453/463 real conversations. Surviving alone was not the acceptance basis.

The adverse test explicitly initialized B07/C09/C07 damage and one injury; those are test conditions, not claimed spontaneous incidents. These are25-ship-day current campaigns, not newly run30/90/365-day certifications. Snapshot UTF-8 sizes were8,756,099 and9,071,499 bytes. Detailed outcomes, decisions, resources and histories are in the evidence archive and source reports.

## Screenshots, security and remaining gates

[Actual camera/boot captures and provenance](../../ICARUS/reports/phase46/SCREENSHOTS.md), [full validation](../../ICARUS/PHASE46_VALIDATION.md), [static security review](../../ICARUS/SECURITY_PHASE46.md) and [limitations](../../ICARUS/PHASE46_LIMITATIONS.md) accompany this build. The evidence ZIP includes original isolated exports, never the user's voyage. Its manifest hashes every included file; CRCs and all file hashes passed.

Not run: physical Windows laptop, Samsung phone/Tab S5e/TV, native APK rebuild, actual LAN/Tailscale, antivirus scan, hardware GPU/touch/accessibility and human visual/playability review. Native build remains pending source recovery. Gym, precise mid-passage salvage, encoded video and dedicated relay planning remain deferred. Source-backed recorded procedural images and later reconstruction are labeled distinctly; no physical footage is invented. Tests do not certify final-game readiness.
