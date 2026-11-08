# ICARUS: Codex handoff

This folder contains the intact ICARUS v0.94.8 Remote Deck source plus `AGENTS.md` engineering instructions.

## Fastest route on Windows
1. Extract this ZIP to a persistent folder, for example `Documents\ICARUS`.
2. Open that folder in Codex (desktop app or an IDE with Codex). Use the extracted project root, not an individual HTML file.
3. If Git is installed, run `git init`, `git add .`, and `git commit -m "Baseline ICARUS v0.94.8"` from the project root. Do not commit secrets or generated reports.
4. Ask Codex to read `AGENTS.md` and `CODEX_START_HERE.md`, inspect the source, and implement v0.94.9 in small tested commits.
5. For browser testing: `python -m pip install playwright`, `python -m playwright install chromium`, then `python soak_test.py --days 7`.

## Copy/paste first Codex prompt
Read AGENTS.md and CODEX_START_HERE.md. Audit the existing ICARUS v0.94.8 source and tests first. Then implement v0.94.9 Scientific Reasoning and Research Programs. Preserve full autonomous mission authorization with player intervention. Tie hypotheses, research programs and experiments to recorded case evidence; include uncertainty, resource/crew/safety constraints, save compatibility, and regression tests. Run the seven-day browser soak test if the environment supports it. Do not claim a pass without actually running it. Summarize changed files, test outcomes, and remaining risks.

## Important
The original v0.94.8 seven-day report passed, with six completed missions and one science case analyzed. That is a historical baseline, not proof that new changes pass.
