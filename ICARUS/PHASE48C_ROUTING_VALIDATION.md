# Routing correction validation

The runtime change is limited to web/umbra/audio-controls.js and web/umbra/soundboard.js. No simulation runtime, server endpoint, storage schema, native audio implementation, Easter egg trigger/palette/asset or external configuration is changed in this correction. Existing kernel/save continuity coverage is inherited, not newly rerun here.

Executed against the correction source:

- **56 selected cases passed**, no failures/errors/skips: 10 actual HTTP/Chromium audio-integration cases (including four new local-output/private-path checks), seven B soundboard browser cases and 39 existing sound-service/audio-foundation unit cases. Audio endpoint/native-driver responses are controlled fixtures, not actual Windows output.
- JavaScript syntax checks passed for both changed runtime files; git diff whitespace check passed.
- Four Node sound-gesture cases passed (tap/hold/release/cancellation). These overlap browser behavior and are additional executions, not 60 unique requirements.

The new cases demonstrate: explicit Aux→headphone render selection survives library recreation/browser reload; source WAVs, names/IDs/order/volumes stay unchanged; a verified two-sound preservation snapshot precedes output modification; backup failure leaves output/data unchanged; input-only microphone identities cannot be submitted as outputs; no default is implicitly chosen; unsaved local selection survives endpoint inspection; a held preview makes zero host-play requests with Aux selected. Existing cases retain the missing-server cache guard, authorization, consent, calibration/normalization, interruption cancellation, private PCM, imports/edits, reordering and restart behavior.

Machine-readable results: reports/phase48c_routing/source_tests.json and gestures.txt. Extracted-package checks and hashes, if published, are separately recorded in downloads/phase48c-routing/VERIFICATION.md. These results supersede no historical hardware gates or earlier run provenance.

**Not run / not complete:** actual Windows audible headphone playback, real Sonar endpoint/mix behavior, processed voice + effect at a receiving game input, hardware private-preview/OBS/acoustic isolation, normal-close/force-kill voice continuity, physical Samsung/native APK/TV and antivirus checks. No actual installed sound library was accessible; its preservation backup is not verified by fixture tests. Full historical regression matrix and long-duration soaks were not rerun for this two-file companion UI correction. Direct injection into unchanged Sonar - Microphone remains unimplemented; no external mixer/cable workaround is installed or tested. Resolve the documented receiving-input decision before proceeding.
