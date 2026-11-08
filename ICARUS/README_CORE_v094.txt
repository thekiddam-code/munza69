ICARUS CORE v0.94.0 - Unified Remote Operations (first foundation build)

Changes:
- Remote expedition controller state now lives in the saved episode under state.remoteCore.
- Derelict and asteroid mission controller state survives local saves, checkpoints and JSON exports.
- Field operations advance once per simulated minute, in the same timer as the ship.
- Pause, 1x, 5x, 20x now drive both ship and field simulation in lockstep.
- Save restoration rebinds the remote controller to the restored episode.
- NIGHTGRID design and existing Remote Deck server/tablet controls unchanged.

Compatibility:
- Existing v0.93.4 saves load; missing remoteCore is initialized with defaults.
- Old saves cannot reconstruct remote mission controller state that was never stored.
- Backup your current episode before replacing the application.

Test:
1. Start_Remote_Deck.bat and open http://127.0.0.1:8765/icarus.html?v=0940
2. Verify tablet LINKED and pause/speed controls.
3. Begin an expedition, save/export, reload and verify its mission status.
4. Pause during an expedition and confirm its progress stops.

This is a foundation build, NOT a completed 7-day stability certification.
