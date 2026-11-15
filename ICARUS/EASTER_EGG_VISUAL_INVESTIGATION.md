# Separate investigation: corporate Easter egg visual regression

## Confirmed scope and baseline

The user confirmed the missing visuals were the UMBRA acid drips, biological growth, radar sweep/pings and short interference/readout effects. This repair is separate from the 4.8B soundboard (separate implementation commit `7f2c78b`). No additional art, lore, creature behavior or forced incident was introduced.

Compared the current 4.8A baseline `73c2028` with the working inline styles/callbacks in the parent of `65e68f1` (Phase4A extraction). Also inspected `65e68f1` and the later offline/native-contract correction `3b6d986`. The relevant original assets and authored CSS/keyframes are recoverable in Git; no replacement visuals were necessary.

## Actual causes

1. The Phase4A stylesheet replacement set `.umbra-orb,.wy-bio-stain,.umbra-acid,.wy-glitch{display:none}`. It did not carry over the acid drip keyframes/rules, growth opacity/background rules, radar sweep/ping pseudo-elements or conditional glitch-layer override. Existing DOM spans and saved preference controls remained. Turning infestation/acid/growth on could still update attributes, but the rendering rules no longer existed and the layers stayed hidden. This was a CSS extraction regression, not lost discovery state, missing footage or a graphics-driver assumption.
2. The old 24-second fictional readout and 18-second interference callbacks were removed from index.html and replaced by a comment delegating optional decoration to the new companion module. That module implemented a separate rare generic/arcade decoration but did not restore those callbacks. The `eggs` and `glitch` checkboxes still persisted, but no longer activated their original effects. This was missing activation logic in addition to the CSS regression.
3. The newer Corporate Anomalies master toggle intentionally defaults OFF, and reduced-motion/privacy/critical-operation gates intentionally suppress some effects. Those are preserved design requirements, not bugs to bypass. Changing only an infestation intensity while leaving the master OFF must still produce no effects.

## Repairs and source conservation

Restored the original acid gradient/drip geometry/keyframes, growth stain/opacity, radar sweep/ping geometry/keyframes and transient glitch layer from Git, scoped to the opt-in UMBRA Bridge. Restored the original readout/glitch timing and probability levels, adding the established newer idle/critical-operation gates. Readouts are explicitly prefixed FICTIONAL MOTIF and never pretend to be telemetry. Interference remains brief, pointer-transparent and disabled for reduced motion. There are no spontaneous effects in the ICARUS simulation or source-backed camera/recording views.

No master toggle is silently enabled. Existing `umbraPrefs` and `umbra-companion-appearance-v1` keys remain, with no reset or migration. These client decorations have no simulated discovery ledger to regenerate. No world/save/history/calendar/crew/discovery/incident file or field was modified. The authentic Legendary Kill Cam remains distinct from fictional arcade decoration.

All **13** original bundled arcade files (six GIFs, six static PNGs, manifest) match commit `65e68f1` byte-for-byte; see reports/phase48b/easter_assets.json. The manual archive and reduced-motion static substitution remain. No asset was fabricated or substituted. The decorative orb was intentionally hidden by the newer design and is not among the user-confirmed missing effects; it was not redesigned/restored as unrelated scope.

## Reproduction and tests

The same final three browser cases were run against an isolated runtime with only app.js and umbra.css restored to `73c2028`: **two failed as expected**, one passed (safety gates). Failures prove the acid/growth layer remained hidden and the readout/interference callbacks did not activate. See eggs_before.json. Running them with the repairs passed all three: visible acid sampled at its actual animation phase, expected growth opacity/radar animation, persisted preferences after reload, hidden effects away from Bridge, master OFF/reduced-motion behavior, observed real timer-driven DOM changes under a controlled random/idle clock, and unchanged playable arcade assets. Controlled test probability does not alter production encounter odds or fabricate simulation events.

The initial callback-inspection test was revised to observe actual DOM timer effects, because Playwright's installed clock replaces interval wrappers. The archive check waits for its actual image decode. No source assertion was removed to conceal a runtime defect.

The screenshots in reports/phase48b/screenshots show the actual running procedural browser layer, with the drip paused at a known CSS-animation phase for visibility. They are UI captures, not recorded ship footage. Physical Samsung/Windows visual review remains pending, as do antivirus/native-device checks. Full results/source lineage are in PHASE48B_VALIDATION.md.

To verify manually: Settings → Appearance → enable Corporate Anomalies; select Active/Outbreak and enable the acid/growth/optional interference/Easter-egg controls. Return to Bridge. Drips and radar animate intermittently; growth appears. Transient readouts/interference remain probabilistic, idle-only and clearly fictional. Disabling the master, leaving Bridge or enabling reduced motion must retain the documented safety behavior. Do not trigger any world event or reset a voyage to inspect decoration.
