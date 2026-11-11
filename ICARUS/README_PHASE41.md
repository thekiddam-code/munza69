# ICARUS / UMBRA Phase 4.1 Command Bridge

This is the browser Remote Deck and Windows Python host update. The existing Android APK is preserved. Native rebuild remains pending recovery of its Android Studio source; no replacement APK is provided. Read this guide first; included Phase 4A guides describe retained TV/profile/arcade features and are historical for host startup.

## Safe upgrade and Windows launch

1. In the existing voyage, export a **complete** backup. Keep the old installation. Note the exact PC browser URL/profile (localhost, 127.0.0.1 and a LAN IP have separate browser databases). Close all old simulation tabs and stop the old server; older code cannot retroactively enforce this new host lease.
2. Extract Lite alongside the old folder. Copy existing local `config.json`, `paired_devices.json` and `samsung_tv.json` if present into the new folder. Keep these private; never publish pairing/TV tokens. Do not copy old web/server code over the update.
3. Run `Start_Remote_Deck.bat`. Python and the same requirements.txt dependencies are needed; an already working installation needs no new pip dependency. A new installation can use `py -m pip install -r requirements.txt`. The server keeps port 8765 and opens the local host-launch page in the default browser.
4. The launch page reports whether voyage data exists at that browser origin. **Use your original PC URL/profile** before opening the host, or restore your complete backup using Settings → Data. If the old URL used the laptop's own LAN IP, opening that same URL on the laptop remains supported. The launch page will not silently assume a different origin contains your voyage. Do not clear browser data or use New Voyage for recovery.
5. Open `/icarus.html` on the laptop through that server. Host authentication is automatic for genuine local-PC requests. Keep this page running; it owns simulation and saves. Another local browser/origin cannot acquire the active server lease; another same-origin tab also cannot acquire the existing IDB writer fence. An ownership-losing page stops advancing/saving and requires deliberate reload after resolving the competing host.
6. On the phone/tablet open the existing UMBRA address, e.g. `http://LAPTOP-LAN-IP:8765/`. Pair using the console PIN if needed. Open ICARUS. It must show HOST CONNECTED or SIMULATION PAUSED and the matching host tick. Opening `/icarus.html` from a remote peer redirects to UMBRA before loading simulation code. Do not use file:// to host; it opens the server launch guide.

The PC must remain awake, its server/browser running and reachable. Existing trusted-LAN firewall/network configuration still applies; this package does not change the firewall, install services or disable protection. Existing Tailscale routes can carry the same authenticated HTTP/SSE/command traffic, with no hardcoded remote IP or separate cloud world. Actual Tailscale deployment is not verified here. Never publicly forward port 8765.

## Bridge and Creator controls

Bridge Mode is default on every restart. Source-backed operational records, engineering, crew observation, mission navigation/recall, actual security projections, chronicles and ordinary settings remain available. Private numerical psychology and raw movement/world inspectors belong to Creator Mode. Absence of an assessment means unknown, not healthy. Current field location/progress requires received evidence; no omniscient tracker is added.

Press **Ctrl + Shift + F12** on the host to toggle Creator Mode. Its banner is explicit. Existing test clocks, pause/resume, global autonomy release, direct psychology/lore/observance configuration, incident injection and debug controls remain there. New Voyage is still explicitly confirmed. Mode is not saved. Legacy Android pause/speed requests now require host Creator Mode too; this is an intentional permission change, not an APK rebuild. Ordinary navigation holds, course selection and feasible recall remain in-universe operations. Normal 4×, synchronized holiday 1× and real Monday–Sunday weeks are unchanged.

## Custom command workspace

Home is the modular command workspace. Customize Layout enables drag handles, keyboard arrow reorder, pointer corner resize and labeled width/height inputs. Lock Layout ends editing. Collapse/Focus/Hide apply per module; Escape leaves Focus. Module library uses existing widget checkboxes, including received crew records and the security camera wall. Hidden components are restored from the library, not deleted. Existing Home choices are imported. Save up to eight named presets per screen arrangement; Reset Layout confirms and affects only that screen layout. Desktop and mobile store separate orders/sizes; these preferences never enter the voyage save.

The original hologram is compact, with its real room selection, deck/condition/atmosphere/access/route overlays, drag orbit and pinch zoom. Zoom/rotation buttons are keyboard accessible. Normal wheel scroll goes through the page; Ctrl/Alt+wheel zooms intentionally. Detailed view expands it. Animation settings offer Full/Reduced/Minimal; existing effect toggles and OS reduced motion remain. Camera walls choose up to 12 actual rooms and columns, allow tile resize/focus and explicitly show unavailable/stale coverage. They are **schematic state projections**, not video. Existing incident playback is labeled reconstruction; genuine host archives are not invented or streamed as film.

## Connection and troubleshooting

HOST CONNECTED: fresh authoritative telemetry. SIMULATION PAUSED: host is connected and intentionally paused. RECONNECTING: network/report freshness interrupted. HOST OFFLINE: no current authoritative host. Last received reports can remain, clearly stale; cameras become unavailable and remote operations disable. Reconnection retries automatically with bounded backoff; Reconnect is available. A phone never uploads a world/save.

If offline, check the laptop's bridge status, server console, exact same PC browser URL/profile, duplicate tabs, pairing token and network reachability. If ownership is lost, resolve the competing host and reload rather than forcing a stale takeover. A server restart creates a fresh key/session: reload the genuine host page to bootstrap it; remote terminals then reconnect. No command is automatically replayed into a new host session. A queued request is not proof of execution; commands expire after 30 seconds, and physical safety rules may reject an operation.

## Backup / rollback / verification

Save schema/namespace and backup format remain unchanged. Keep the pre-upgrade backup and old folder. To roll back, close the new host/server, restart the old folder at the original origin/profile, and restore the pre-upgrade backup if needed. Do not mix runtime files or delete databases. New UI preferences are ignored by older builds. Existing APK/application/signing identity and local pairing files remain untouched.

Compare `Get-FileHash .\ICARUS_Phase4_1_Command_Bridge_Lite.zip -Algorithm SHA256` with the supplied checksum. BUILD_MANIFEST.json records committed source hashes. See PHASE41_VALIDATION.md for executed tests and PHASE41_LIMITATIONS.md for native/physical/human gates. Automated browser tests do not certify Windows input, Android/WebView, TV power behavior, antivirus or human usability.
