# Phase 4.9 host actions for UMBRA Mobile 3.3

This update **creates** the paired-host Sonar/Moments endpoints; they did not exist in the inspected Phase 4.9 companion. Apply locally on the Windows PC. The cloud environment could not reach the private PC and has not deployed or hardware-tested this package.

## Install without replacing your working installation

1. Save/export the current voyage and keep your private backups. Stop the existing companion normally and close its authoritative tab after saving. Keep the same installation, browser profile, hostname and port 8765.
2. Extract this ZIP into a separate folder. Run `apply_host_actions.bat` and enter the original ICARUS folder containing `server.py`. Alternatively run `py -3 apply_host_actions.py "C:\path\to\ICARUS"` then `py -3 configure_host_actions.py "C:\path\to\ICARUS"`.
3. The installer verifies the original Phase 4.9 server checksum, adds one module and backs up the old code plus private settings before writing. Different/partial source is refused. Existing bulk/volume fixes remain compatible when their server.py is unchanged. **Do not copy main's older ICARUS server over the working Phase 4.9 installation.**
4. The local setup helper asks for the **existing** folder shown by GG → Settings → Moments → Clip Settings → Storage Location. It does not create a new recording directory or move/delete clips. Enter the saved Save Clip binding if needed, e.g. `alt+s`; blank keeps it unchanged. Match that binding in GG's Shortcuts. The helper edits only `config.json.macros["Save Clip"]` when explicitly supplied and `umbra_host_actions.json.moments_clip_directory` when explicitly supplied, retaining other fields and private backups.
5. Restart the same companion normally. Install the matching Mobile 3.3 APK over the existing installation. Configure a mixed widget, select the two silver Host action entries and Save. An old green generic Save Clip macro may still appear in the picker; choose the silver entry to use request/file verification.

No driver/package, Windows default device, VoiceMeeter configuration, microphone input/processing, soundboard output/profile/library, TV backend, world/save or simulation runtime is replaced. New settings and code/settings backups stay private on the PC; never upload them or your clips to public GitHub.

`--check` validates source without modifying it. An already fully installed patch is a no-op. Rollback code while stopped with `py -3 apply_host_actions.py "C:\path\to\ICARUS" --restore-code "C:\path\to\umbra_host_code_backups\<backup>"`. It verifies hashes, restores server.py and removes only the newly installed module. Private configuration is retained. Code rollback does **not** undo a deliberate successful Sonar output switch; restore outputs through Sonar if desired.

## Sonar contract

All endpoints below are behind the original bearer-token pairing and origin checks. No second authentication/connection system is introduced.

`POST /api/sonar/arctis` accepts only `{ "requestId": "<new UUID>", "output_id": "<optional returned id>" }`.

- The host discovers GG via its existing ProgramData coreProps file and `/subApps`, validates loopback-only addresses, refuses redirects and disables proxies. GG Core's self-signed TLS is accepted only for the validated localhost connection; Android's remote TLS policy is unchanged.
- The current adapter requires **Sonar Classic mode** and a known routing response containing Game, Chat, Media, Aux and Mic. Streamer/unknown modes and changed API shapes are rejected without switching mode or attempting writes. The routing interface is GG's internal API and may change with GG updates.
- Candidates must be reported physical **render** endpoints with Arctis names. Capture, Sonar virtual, VoiceMeeter and unavailable endpoints are excluded. No candidate means an error. Multiple candidates return `state: selection_required`, `outputs: [{id,name}]`, `verified:false`; no route is changed until selection. A previously remembered available identity is reused.
- Only the four playback route setters are callable. Before/after Mic route IDs are compared; no Mic, mode, volume, EQ, stream-mix, app-routing or Windows-default setter is exposed. All four output IDs must match the selected endpoint before returning `state: verified`, `verified:true`, `routes:{game,chat,media,aux}`, `output:{id,name}`, and `microphone_preserved:true`.
- A verified target is remembered in the PC's private `umbra_host_actions.json`, shared across phone restarts. A save failure is reported separately. Removed devices require a new available selection. On failure, the host attempts to restore only its own changed output routes, and only when they still match its target; it never overwrites an externally changed Mic route. Failure/rollback readback is returned without claiming success.
- UUID results are cached per paired owner. Repeating the same request does not repeat a switch; reusing an ID for different data is rejected. No automatic retries are made after uncertain transport outcomes.

Operational Sonar failures may be a `state:error`, `verified:false` envelope with `error`, `routes` and `rollback`; clients must check verification, not HTTP 200 alone. Invalid fields/authorization/setup errors use HTTP error responses.

## Save Clip contract and the rejected-digital-hotkey limitation

`POST /api/moments/save-clip` accepts only `{ "requestId": "<new UUID>" }`. It reads the current **Save Clip** entry from the original `config.json.macros` for each request. Android never sends Alt+S or maintains another key binding.

The earlier host action used PyAutoGUI virtual-key events. This endpoint uses **Windows SendInput scan codes**, a bounded hold, and verified insertion/key-release counts. It refuses a physically held shortcut/modifier and attempts release of every inserted key even on partial failure. It does not install drivers, escalate privilege, alter GG, enable recording or bypass Windows input restrictions. Supported saved bindings are 1–4 named modifiers, letters/digits, arrows, Enter/Space/Tab/Escape or F1–F24. Other ordinary macros retain their original executor.

**This remains synthetic input. GG can still reject it.** Microsoft documents that SendInput is subject to integrity-level restrictions and does not guarantee acceptance by another application. The new API is a command/verification boundary, not a claim of a confirmed public GG manual-capture endpoint. SteelSeries' documented GameSense autoclip API is for registered game events; this update does not register a fictitious game or change detection/capture settings to simulate manual capture.

The host requires the real, already existing Moments clip folder and takes a bounded metadata baseline **before** sending. One requested check watches that folder for at most 30 seconds; no idle clip scanning service is added. Existing/growing files, symlinks/reparse points, unsupported/deep/oversized folder scans and invalid containers cannot produce a positive result. A new nonempty file with a video-container signature must be stable over successive observations.

The initial result is `state:pending`, `hotkey_sent:true`, `clip_file_verified:false`, `request_id`. `POST /api/moments/clip-status` with the same UUID reads its owner's result and never resends input. Android polls only while the initiating widget is visible/started. One in-flight capture request is allowed; results are bounded/expire.

- `state:clip_detected`, `clip_file_verified:true`, `clip:{name,bytes}` means a **new stable video file was observed**. It is not proof of playable content, Gallery registration or causation if an automatic clip happened concurrently. The UI explicitly asks to confirm in Moments.
- `state:unverified`, `clip_file_verified:false` means no file was confirmed or observation failed. Input acknowledgment alone is never called “clip saved.”
- `capture_active:null` is deliberate: this adapter cannot reliably certify the running GG version's capture state. Enable/verify actual capture in GG before testing. No footage, clip contents or folder listing is sent to third parties; the paired response contains only the detected basename and size.

If the physical saved shortcut works but injected scan codes still do not, this GG/session combination remains unsupported by this method. Verify the foreground game/capture state and matching session/integrity levels manually. Do not infer that renaming a hotkey call to an API bypasses GG's input filtering. Actual Windows/Android clip creation remains required acceptance.

`POST /api/host-actions/status` with `{}` exposes only protocol version and whether the saved macro/verification folder are configured. It neither switches devices nor presses keys.

## Verification and primary references

The included tests exercise fixture Sonar routing/readback/rollback, remembered identity, excluded capture/virtual outputs, per-owner UUID guards, changed saved bindings, new-file observation versus old/growing files, timeout/no-clip outcomes, fake Win32 structure/scan-code/release behavior, actual companion HTTP authentication/origin/field guards, and installer/setup preservation. These are software fixtures, not actual GG/Windows audio or recording certification.

Reproduce with Python and the original isolated Phase 4.9 source checkout: set `ICARUS_PHASE49_REFERENCE` to its repository root, then run `python -m unittest discover -s <this-package> -p "test_*.py" -v`. HTTP tests need local socket access and the original Phase 4.9 modules/dependencies. `manifest.json` identifies exact source and payload hashes. The Windows BAT was not executed on this Linux host.

References inspected for interoperability, not copied implementations:

- [SteelSeries: channel roles and playback devices](https://support.steelseries.com/hc/en-us/articles/16954265292173-How-does-Sonar-work)
- [Community primary-source GG routing observations](https://github.com/hardtekpt/steelseries_gg_py/blob/main/docs/gg_spec.md) — internal discovery, device identities and classic redirection contracts; version compatibility is not guaranteed.
- [Microsoft SendInput](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput) and [KEYBDINPUT scan codes](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput)
- [SteelSeries: clipping checks](https://support.steelseries.com/hc/en-us/articles/360060109772-Having-Issues-Capturing-Clips), [storage location](https://support.steelseries.com/hc/en-us/articles/24542109368973-Getting-to-know-Moments), and [GameSense autoclip contract](https://github.com/SteelSeries/gamesense-sdk/blob/master/doc/api/sending-moments-events.md)
