# ICARUS v0.94.9 — Scientific Reasoning and Research Programs

The existing shipboard science queue now feeds persistent programs grouped by source location and preliminary material class. Every case has a tentative hypothesis with case/specimen provenance, supporting observations, custody objections and contamination confounders, numerical confidence, and explicit unknowns. Metadata alone is not a verified discovery.

SOL autonomously selects a custody review (30 minutes, one laboratory supply) followed by a non-invasive contamination screen (60 minutes, two supplies). There is one shared experiment slot. Custody, transfer, containment, lab power and available research personnel gate work; emergency responders cannot staff new research. Active work pauses if its analyst or safe conditions become unavailable, retaining progress and prepaid costs. Each case/method is attempted once, preventing automatic retry loops and supply exhaustion.

Outcomes are derived from existing specimen state: inadequate integrity fails; contamination can make screening inconclusive; a clean screen records the absence of recorded contamination, not composition or viability. Completed experiments retain a timestamped observation snapshot. Confidence remains tentative and capped at 45%; missing custody revokes support. Scientific results never create field missions or unlock Lazarus from metadata. Existing Lazarus gameplay is preserved; this milestone does not implement a revival assay.

Research appears below evidence on the remote expedition panels and remains in the existing save tree. Automatic weekly continuity now preserves specimen custody alongside retained science and missions. Manual New Episode keeps its intentional reset behavior. Existing saves and JSON backup format are retained.

## Validation

- `node --test test_research.js`
- `python soak_test.py --days 7`
- `python soak_test.py --days 7 --seed-science --report science_soak_report.json`

The browser runner requires Playwright and Chromium. Set `ICARUS_CHROMIUM` to an installed Chromium executable if needed. The optional seeded run uses an isolated browser profile and three explicitly synthetic specimens to exercise grouped research and all terminal outcomes. Existing report fields remain; research, provenance, custody, paused-clock and early save/reload diagnostics are additive. The seed is installed only by the test runner, never normal gameplay.
