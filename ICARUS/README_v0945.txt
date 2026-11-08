ICARUS v0.94.5 Autonomous Mission Director

Autonomous command generates documented mission objectives from unresolved derelict telemetry, resource shortages and follow-up asteroid findings. Existing transit, exploration and return simulation are preserved.

New in this build:
- Persistent mission registry, decisions and outcomes
- Mission-based dispatch with crew readiness and return recovery
- Manual Remote Deck recall, abort, takeover, release and request for SOL assessment
- Missions and mission records preserved at automatic weekly rollover; assigned expedition crew restored into new episode
- Onsite endurance safeguard 720 simulated minutes, with earlier return on crew exhaustion
- Diagnostic report records mission registry, transitions and persistence

Run: python soak_test.py --days 7
This is a prototype. Missions are still limited to derelict and asteroid, and advanced incident-specific decision trees are not implemented.
