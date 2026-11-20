# Phase 4.9 validation

Validation is in progress. This document will be finalized with the actual completed test/campaign reports before publication. Runtime freeze: d2bf219e9bbbedf22c145fd38b7129c9e4bfc410; later commits currently change documentation/test tooling only. All 172 runtime hashes are in reports/phase49/runtime_scope.json.

Executed so far: 489 Node tests passed with zero failures/skips. The eight focused source-browser tests passed (four specimen/camera/migration, two paired remote/protocol, two interrupted-care/source-state acceptance). Broader regression execution and extracted-package testing are ongoing. Two old repeat-expedition timing assertions failed initially and are under investigation; a historical-voyage startup attempt timed out and is being checked. These are not counted as passing.

Final-source full-browser campaigns use seeds10101,4242,2026 and checkpoints7/30/90 simulated days. Reports retain actual completed checkpoints, causal minute counts, crew continuity, scientific activity, paid biological work, finite-resource audits, exact save/reload comparisons and state size. No biological discoveries, enclosures, failures, encounters, injuries or deaths are injected in ordinary campaigns. Quiet results are valid. Fault injections occur only in labeled adverse fixtures. Final results pending.

The supplied historical voyage is private and excluded from the package. Its import/restart tests are separate from isolated seeded worlds. The current installed PC voyage and private sound library are unavailable, so their current contents/backup cannot be certified. Keep pre-upgrade backups as described in README_PHASE49.md.

Run from the source checkout (test tools are excluded from Lite):

```
node --test ICARUS/test_*.js
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_integration.py --report /tmp/specimens.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_remote.py --report /tmp/specimen_remote.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/test_specimen_acceptance.py --report /tmp/specimen_acceptance.json
ICARUS_CHROMIUM=/usr/bin/chromium python ICARUS/soak_specimens.py --out /tmp/specimen_campaigns --seeds 10101 4242 2026 --days 7 30 90
```

Python Playwright is a development dependency; use its installed Chromium or supply the executable path. The harness uses isolated browser contexts and real simulation ticks. It does not connect to or modify an installed Windows voyage. The normal production clock/holiday/real Monday–Sunday rules are unchanged. Accelerating90 simulated days is not90 real days of calendar observation; explicit real-Monday regression tests cover that boundary separately.

Unavailable: physical Windows launch/display/audio, Samsung phone/tablet/native APK, TV, Fortnite/private-preview/VoiceMeeter shutdown or crash, actual current voyage/library, antivirus execution, human long-form art/story/playability assessment. Browser viewport/protocol checks do not certify these devices. Read PHASE49_SECURITY_REVIEW.md for static review and inherited privileged/network capabilities. The phase is not certified complete while validation remains pending, and ICARUS final-release readiness is not established solely by passing tests.
