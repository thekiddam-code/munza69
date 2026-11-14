# ICARUS 4.6 — targeted boot hotfix

Baseline: completed Phase4.6 branch at4899cae; baseline runtime a22f2aca. Hotfix runtime:fc8ce280689fda785a34d046f1187d5fcd6aee55. This is a bug fix, not a new phase or exploration update.

## Reproduced causes

The inspected Phase4.6 source already had explicit ENTER and no fixed dismissal timeout. The reproduced defect was that completed browser initialization displayed “ICARUS ONLINE · READ-ONLY ACCESS” while the server writer was still unavailable. Any initial409 ownership conflict set a permanent lost flag even though this instance had never owned a server generation. Heartbeat retry required an existing generation, so an initial waiting instance did not acquire the lease when a departed owner's lease naturally expired. Claim errors also wrote the authorization row even when credentials remained valid, conflating independent states. The publish loop attempted generation-zero publication while waiting, adding misleading errors.

The before-fix regression fails on the inaccurate ONLINE state. Additional real-HTTP tests demonstrate delayed lease resolution, live-owner protection and independent credential state. No fictional timeout cause or Windows-specific diagnosis is claimed.

## Changes (four runtime files only)

- `web/boot-screen.js`: actual INITIALIZING / WAITING FOR WRITER / ICARUS ONLINE and error states; writer state derives from both original ownership checks. Inputs are retained DOM nodes. A small status observer updates visible progress only; it never dismisses the screen, acquires storage, advances the world or grants permission. ENTER appears near the startup heading and stays accessible when scrolling after actual browser initialization; dismissal is still only its explicit user action. Read-only observation remains protected. Verified-key feedback follows actual writer readiness rather than retaining an obsolete waiting message. Retry authorization retains the key field; initialization retry reloads the saved world.
- `web/host-authority.js`: credential verification is independent of lease state. Preserve actual service/error text. Serialize initial claim requests. An instance with **no previously held generation**, verified credentials and actual Durable ownership may retry the original server claim endpoint with its same identity. It waits for the server to grant access normally; it cannot expire or displace another owner. A conflict after a generation was held stays latched/fenced until reload. No established host automatically reclaims ownership after loss.
- `web/icarus.html`: one startup bridge guard prevents publish/command polling before a server generation exists. No simulation, clock, crew, map, research or drone logic changes.
- `web/boot-screen.css`: prominent ENTER action and scrollable startup presentation.

The other133 runtime files match Phase4.6 byte-for-byte, including durable-store.js, bridge_service.py, server.py, all drone/exploration modules, persistence, calendar and world systems. The original lock tokens, generation checks, expiry values and authorization endpoints remain. No lease record is deleted, forced, expired or bypassed by production code. No new dependencies, system modifications or network endpoints.

## Executed verification

Accepted per-case JSON/logs are under reports/boot_hotfix/accepted. Counts are executions including separately run inherited overlap, not unique new tests. Earlier failing reproduction and a corrected test-fixture diagnostic are retained separately.

Eight focused real-HTTP/Chromium startup cases cover:

1. A departed server's actual12-second lease stays protected, then naturally expires; this same waiting instance obtains a new grant, retains typing/focus, preserves the existing voyage, and enters only on explicit selection.
2. An8-second delayed real asset response cannot hide startup, clear the key or claim early readiness.
3. Wrong key → actual rejection → corrected key retry, independent of writer state, with no early ONLINE or automatic dismissal.
4. A live owner remains protected across retries.
5. A real failed script load shows its actual error; initialization retry preserves the existing saved voyage and still requires ENTER.
6. A host that loses an already-held generation never silently reacquires or overwrites the replacement owner.
7. Delayed native IndexedDB open completion retains the original browser lock/storage code and keeps authorization/key input independent; release allows actual restoration/ownership and explicit entry.
8. An actual503 bootstrap error is displayed, and valid authorization recovers without a world reset.

Regression checks additionally cover the complete existing49-case real-HTTP remote suite, seven autonomous drone/exploration cases, six visual/save cases, four ordinary production-clock cases,405 deterministic model cases and18 service cases. All **497 final-source case executions passed**, with no failures/errors/skips:8 startup +49 remote +7 drone +6 visual +4 clock +405 models +18 services. Exact per-case results are in accepted/verification_summary.json. An earlier candidate run had one timeout waiting for a stubbed TV key response; the unchanged test passed in isolation and in the full final49-case run. No TV code or assertions were changed. Node tests use byte-identical current source; browser/service tests target the frozen hotfix runtime. Distribution hashes/CRC and extracted-package checks are reported separately with the hotfix download.

The startup test fixture initially used a completely new read-only world before first writer grant. Its following first writable reload legitimately initialized existing chronicle presentation metadata, so strict equality to the pre-first-writer empty metadata was inappropriate for the user's existing-voyage case. The corrected test first creates and saves a genuine voyage, then simulates a departed server lease. Full snapshot equality remains required before/after grant and reload; assertions were not removed or narrowed. No game logic was changed to alter chronology.

Actual captures in reports/boot_hotfix/screenshots show native storage waiting with a verified key, followed by ONLINE with explicit ENTER still visible. The input is a masked test credential, not a user secret. These are Linux Chromium/local HTTP tests, not physical Windows screenshots.

## Limits and omitted tests

No new long-duration campaigns, physical Windows/Samsung phone/Tab S5e/TV, native APK rebuild, actual LAN/Tailscale, hardware GPU/touch/accessibility, human play review or antivirus scan was run for this targeted hotfix. Prior Phase4.6 campaign reports remain historical and are not presented as new hotfix campaigns. The eight startup cases and focused preservation regressions are the relevant new evidence. No antivirus protection was disabled. No unrelated game features or deferred gym work were added.

Installation, backup and rollback are in README_BOOT_HOTFIX.md. Older Phase4.6 saves retain the same namespace and schema; no migration/reset is necessary. Use one authoritative host and wait for actual protected readiness.
