# UMBRA Phase 4.8A Lite software checkpoint

[Download ZIP](UMBRA_Phase4_8A_Windows_Command_Checkpoint_Lite.zip) · [SHA-256](SHA256SUMS.txt)

This is the Engineering/Hotkeys stage, with actual Windows acceptance pending. Phase 4.8 as a whole is **not complete**. 4.8B/C sound library and Sonar routing are not started. No microphone, audio defaults, power settings or antivirus protection were changed.

Source `04b0231665abf55aa68bb9b2b52743e6dfe1a4ca`; tested runtime `73f5504f618e570169c94ebfcd91a9416491e59b`. ZIP 1,058,574 bytes, 254 retained source files plus manifest. CRC, all source hashes and all 154 runtime hashes passed. Tests/reports/tools/private data excluded; existing runtime dependencies retained. No new pip dependencies.

SHA-256: `da8953275b540ef44dec9845208dca644ee97a55bb46f2c5142c95a815a20088`.

**583 selected case executions passed**: 566 source/regression executions plus 17 extracted-ZIP executions (5 new Windows HTTP/browser fixture tests, 8 writer/boot, 3 dispatch/render/media, 1 paired original-record playback/pause/scrub). Inherited overlap means these are not 583 unique tests. The original supplied voyage passed four actual isolated restart/history/media/paired-terminal checks and its input hash remains unchanged. Raw private data are excluded.

[Full validation and Windows checklist](../../ICARUS/PHASE48A_VALIDATION.md) · [Architecture/security/files](../../ICARUS/PHASE48A_ARCHITECTURE.md) · [Install/backup/rollback](../../ICARUS/README_PHASE48A.md) · [Raw selected results](../../ICARUS/reports/phase48a)

## Implemented

Cached read-only Windows CPU/GPU/RAM/storage/network/system/process measurements with honest unavailable fields; bounded optional history inside Engineering only. Existing server pairing and command mechanism retained. 25 predefined Windows actions with categories/context notes, accessible icons/text and hold descriptions. Five-app local Start menu/desktop/Store discovery with installed Shell icons, fixed remote IDs, revalidation, bounded duplicate protection and actionable status/errors. Existing config macros, chat, TV, ICARUS and saves preserved.

## Pending physical checks and limits

Actual Windows 11 sensor readings, native Shell icon extraction, installed-app activation and key effects were not executed here. Windows APIs/input used controlled fixtures in Linux Chromium. Screenshots in the source reports are explicitly fixture-backed UI tests, not readings from the Alienware PC. Physical Samsung tablet/phone/TV, native APK rebuild, Tailscale hardware and antivirus scans were unavailable. Full historical/campaign matrix was not repeated. CPU temperatures, non-NVIDIA GPU performance and Windows overlay power mode may be unavailable. Windows Shell owns already-running app activation; 'requested' does not mean a game is ready. Missing icons use text fallback.

## Update and rollback

Export a full ICARUS backup and retain the old installation/configuration. Stop its server and close authoritative tabs. Extract separately; copy private config.json/paired_devices.json/samsung_tv.json if present while stopped. Use the same browser profile, hostname and port. Run Start_Remote_Deck.bat, refresh assets and select ENTER ICARUS after actual readiness. Do not clear IndexedDB or bypass writer protection. No save migration is needed for 4.8A. For rollback, export a post-update backup and return to the retained prior 4.7C folder using the same origin. Keep both backups and older media-compatibility limitations. Native Android source recovery remains pending; existing URLs/contracts are retained.

Follow the exact PC checklist in PHASE48A_VALIDATION.md before treating the Windows feature set as hardware verified. Audio/private-preview/game-chat/microphone-survival acceptance belongs to later B/C implementation and must be physically tested, not inferred from these software tests.
