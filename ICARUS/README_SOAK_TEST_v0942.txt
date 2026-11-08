ICARUS v0.94.2 | SEVEN-DAY SOAK TEST HARNESS (experimental)

This package retains the v0.94.1 engine and Remote Deck unchanged.
Adds soak_test.py to drive real step() and fieldTick() calls through a browser,
checking resources, crew bounds, mission references, save and reload.

Install on PC (Python required):
  pip install playwright
  python -m playwright install chromium
  python soak_test.py --days 7

Outputs soak_report.json in remote_deck folder.
Do not run against a live episode: the harness starts a separate browser profile.
The browser is opened against a temporary localhost server on port 18765.

KNOWN LIMITATIONS:
- This is an automated stress-test runner, NOT a deterministic replay engine.
- Randomness still uses Math.random.
- This runner does not guarantee all mission types are triggered.
- Browser execution could not be verified in the build environment because
  browser navigation was blocked by administrator policy. No soak pass is claimed.
