# TV adapter capability / validation matrix

Scope: existing Windows server's private-LAN Samsung Tizen WSS port 8002, original allowlisted `ms.remote.control` Click keys and stored approval token. No physical TV is attached here. **Every device/firmware result below is NOT RUN**; protocol tests use an explicit socket stub. An existing protocol key is not a claim of physical model verification or native APK functionality elsewhere.

| Requested action | Existing protocol / implementation | Actual physical result |
| --- | --- | --- |
| Power Off | KEY_POWEROFF, retained; no host shutdown | Not run |
| Power On / wake | Not implemented/verified by this adapter; no blind wake sequences | Not run |
| D-pad / OK, Home / Back | Existing KEY_UP/DOWN/LEFT/RIGHT/ENTER/HOME/RETURN | Not run |
| Volume / mute / channels | Existing KEY_VOLUP/VOLDOWN/MUTE/CHUP/CHDOWN | Not run |
| Repeat | Bounded client repeated Click, 250 ms, at most 12 repeat sends/hold; cancellation/blur/visibility guarded | Not run; not a native long-press claim |
| Source/input | Existing KEY_SOURCE opens TV source menu; direct input selection unverified | Not run |
| Playback | Existing PLAY/PAUSE/STOP/REWIND/FF; old play_pause alias remains KEY_PLAY | Not run; no toggle acknowledgment claim |
| Settings/menu/info/exit | Existing MENU/INFO/EXIT allowlist; advanced section labels protocol scope | Not run |
| Stremio / TV Plus apps | Existing shortcut behavior is honestly labeled “Open TV Home for …”; direct app IDs/launch not implemented | Not run |
| TV Plus channel shortcuts | Not verified/implemented | Not run |
| Picture/sound modes | Not verified/implemented | Not run |
| Native sleep timer | No supported native API established in available source; no SmartThings service added | Not run; native capability unknown |
| UMBRA-managed timer | 15/30/60/90/120 real minutes; server must stay running/connected; one existing Power Off attempt | Not run physically; scheduling/cancel/expiry/failure tests executed |
| Long-press key protocol | Not verified/implemented; no guessed Press/Release sequences | Not run |
| Pairing/session | Original token storage/approval handshake; socket reused, idle reconnection after 120 s; denial/errors surfaced | Not run physically |

Timer state is deliberately volatile: restart cancels, config change and owner unpair invalidate callbacks, cancellation/replacement generations prevent old sends. Failed sends never retry later, and callbacks more than 60 seconds late after server suspension expire without sending. Browser/server countdown tests do not advance real television behavior. Send success only means socket transmission; this protocol implementation does not confirm device execution/power state. Cached socket status is not a liveness probe.

The current adapter's false/unavailable capability flags mean “not established/implemented here,” **not** “the user's TV or working native APK can never support it.” Recovery of native integration sources/model/firmware and physical validation can establish further supported functions later. Original allowlisted key names and the legacy TV response body remain compatible.
