ICARUS CORE v0.94.1 | WORLD-STATE SAVE RELIABILITY

Based on v0.94.0. Remote Deck controls and NIGHTGRID interface retained.

Changes:
- Save snapshots are checked for core schema integrity before writing.
- The previous valid browser snapshot is retained as a recovery slot.
- If the main browser save is unreadable at startup, a verified recovery snapshot is loaded, with a warning in the event log.
- Automatic saves occur after both ship and field operation ticks finish, preventing a partially advanced expedition snapshot.
- Backup import uses the same validation and refreshes the existing remote controller object without leaving stale keys.
- Manual Save now reports storage failures instead of claiming success.
- New episode transitions reset the remote controller in place, avoiding stale expedition references.

IMPORTANT: The recovery slot is in the SAME browser storage. It is NOT a substitute for downloading JSON backups.
The simulation still uses Math.random and does not support deterministic replay. A seven-day soak test is NOT included in this build.

INSTALL:
1. Export your current episode JSON from the old build first.
2. Extract this ZIP into a new folder and run Start_Remote_Deck.bat.
3. Open http://127.0.0.1:8765/icarus.html?v=0941
4. Import your episode backup if the new browser origin has no saved episode.
5. Test saving and reloading during a live expedition, then confirm ship resources, crew tasks and expedition progress.

Technical checks performed: HTML embedded JavaScript syntax via node --check; Python server syntax via py_compile.
