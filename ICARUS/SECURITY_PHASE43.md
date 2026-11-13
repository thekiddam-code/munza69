# Phase 4.3 static security and provenance review

Review scope: changes from verified Phase 4.2B d5add5b to corrected frozen runtime 13ab447, plus Lite file selection. This is a source review, not antivirus certification or a full penetration test.

The new ship-system/gravity/maintenance modules execute local simulation logic only. They do not invoke operating-system commands, install software, download code, open new network connections or modify system settings. Engineering UI sends fixed string commands through the existing authorized bridge; server-side ranges/zone/component whitelists reject arbitrary payloads. No command is evaluated as JavaScript or shell text. Actual remote tests cover unpaired rejection, invalid values, deduplication and matching host state.

The retained Windows launcher changes into its own folder and runs `py server.py` or `python server.py`. Users may need `py -m pip install -r requirements.txt`; this downloads the existing listed Python packages and modifies that Python environment. The launcher does not disable antivirus, change firewall rules, request administrator rights or install a service.

The unchanged companion server listens on `0.0.0.0` for LAN/Tailscale access and retains existing host fencing, pairing and command endpoints. Browser host/remote telemetry and commands use the existing HTTP/SSE routes; saved world state is never accepted from a stale remote panel. Retained pre-existing desktop/media automation can control the PC on explicitly paired user commands, and configured television integration connects to the selected TV address. These capabilities are potentially sensitive; use a trusted network, valid pairing and the existing settings. They are not new in-game agent OS permissions.

The TV service, BridgeService, calendar, voyage clock, host-authority, durable store and backup codecs/transfers are byte-identical to the baseline. Repository `UMBRA/` native source/APKs are also unchanged against main. No native project/installed APK was replaced. No new external analytics, cloud simulation, arbitrary agent network access or antivirus bypass was added.

The source-based Lite manifest records the exact source commit and SHA-256 for every retained file. Packaging excludes test suites, raw reports, development/campaign tools, packaging scripts, generated credentials and test worlds while retaining every runtime web dependency and all six host files. ZIP CRC and manifest hashes are checked separately. Package verification and executed tests are in PHASE43_VALIDATION.md and the evidence bundle.

Remaining review limits: no real Windows Defender/third-party antivirus scan, native APK analysis/rebuild, physical TV/network penetration test or independent security audit was performed. Antivirus was not disabled or circumvented.
