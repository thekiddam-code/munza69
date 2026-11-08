# ICARUS v1.0 — The Living Simulation

This build continues v0.94.9 with integrated research uncertainty, durable crew health and personality, risk-aware autonomous operations, finite reserves and source-linked weekly recaps. See ENGINEERING_v1.0.md for the changelog and architecture; KNOWN_LIMITATIONS_v1.0.md includes reduced scope and the recommended next batch.

## Run

On Windows, extract the complete ICARUS folder, install the existing runtime dependencies with `py -m pip install -r requirements.txt`, then run Start_Remote_Deck.bat. Open the ICARUS PC URL printed by the server. Keep the full web directory together; the new JavaScript modules are required. The static browser simulation can also run on a local HTTP server; physical Remote Deck controls require the existing Python host.

Export a backup from your previous build before upgrading. Browser saves belong to the origin/port where they were created. Old saves migrate into this build; retain your old ZIP and exported backup for downgrade. Automatic weeks now preserve crew and expedition consequences. The New Episode button remains a deliberate full scenario reset.

## Observe the new systems

- Remote expedition evidence panels show program hypotheses, uncertainty, scientific disagreements and experiment progress/results. Biological evidence may establish a longitudinal Lazarus research program, without automatic revival.
- Personnel details show health, fatigue and morale. Injury recovery uses the existing routed medical/clinical systems and finite cartridges. Casualties remain in the memorial registry and influence survivors.
- Mission panels retain captain intervention and display dispatch risk assessments and debrief condition. SOL still selects justified opportunities autonomously; exhausted field maps do not produce arbitrary weekly sorties.
- Sunday Credits opens a journal-grounded recap. Optional anthology endings and legendary encounter selection are saved preferences. No combat producer is implemented, so the legendary selection normally has no eligible footage.

## Validation bundle

The packaged reports directory contains natural seven-day and thirty-day reports, separate labeled synthetic-science runs at both durations, baseline v0.94.9 results, unit output, browser integration results, syntax checks and a test summary. The ordinary seed-1001 runs recover no scientific evidence; the synthetic runs and focused tests supply science coverage explicitly.

Test commands and their prerequisites are in ENGINEERING_v1.0.md. Physical device integrations were not tested in this Linux build environment.
