# CODEX IMPLEMENTATION BRIEF
# UMBRA PHASE 4.8 — WINDOWS COMMAND & CONTROL

## Primary Objective

Upgrade the existing UMBRA Remote Deck and Windows companion server into a more capable Windows 11 command-and-control interface.

This phase focuses on:

1. Engineering system monitoring.
2. Instant Buttons soundboard integration.
3. SteelSeries Sonar microphone and game-chat audio routing.
4. Expanded Windows hotkeys.
5. Application launchers.
6. Reliability, persistence, and remote-control security.

**Do not rebuild UMBRA from scratch. Preserve the existing architecture, styling, tabs, controls, ICARUS simulation integration, and working functionality.**

The target PC is an Alienware m15 R7 running Windows 11. UMBRA is accessed through a Samsung Galaxy Tab S5e and mobile devices, including remotely over Tailscale.

Inspect the repository and existing implementations before modifying anything.

---

## 1. ENGINEERING — WINDOWS SYSTEM MONITORING

Expand the existing Engineering tab into a comprehensive Windows performance dashboard.

### Required telemetry

Collect actual Windows system measurements where supported:

**Processor**
- CPU model and core/thread count.
- Total CPU utilization.
- Per-core utilization if practical.
- Current CPU frequency.
- CPU temperature where available.

**Graphics**
- GPU model.
- GPU utilization.
- Dedicated VRAM usage.
- GPU temperature.
- GPU clock and power information where supported.

**Memory**
- Total installed RAM.
- Used and available RAM.
- Memory utilization percentage.

**Storage**
- Drive names and capacities.
- Used and available space.
- Disk activity where supported.

**Network**
- Active network interface.
- Upload/download throughput.
- Local IP address.
- Network connectivity status.

**System**
- Windows version.
- System uptime.
- Battery percentage and charging status.
- Current Windows power mode when detectable.
- Running processes and their CPU/RAM usage.

Use appropriate Windows APIs, performance counters, or established monitoring libraries.

Never fabricate unavailable measurements. Display "Unavailable" or hide unsupported sensors gracefully.

### Interface

Maintain UMBRA's existing industrial science-fiction design language:

- Near-black surfaces.
- Subtle cyan, mint, and amber accents.
- Clean typography.
- Angular panels and restrained borders.
- Responsive layouts for tablet and phone.
- Smooth, lightweight animations.

Include clear utilization indicators and optional short-term performance history.

### Important boundary

**Engineering monitoring must remain inside the Engineering tab.**

Do not add floating performance overlays to Simulation, Lounge, Hotkeys, or other sections.

Alienware Command Center already manages hardware performance behavior. Avoid competing fan, thermal, or performance controls.

Do not alter existing Windows power-management settings.

---

## 2. INSTANT BUTTONS — UMBRA SOUNDBOARD

Build a soundboard system into the existing UMBRA interface.

The user currently uses:

https://www.myinstants.com/en/index/us/

Myinstants is accessed through Chrome, a downloaded website shortcut, and a Chrome extension.

The user has only one saved sound, so there is no need to build a complicated account migration system.

### Architecture

Use an UMBRA-managed local sound library.

Myinstants serves as a sound-discovery and import source, not a required runtime dependency.

Avoid relying on undocumented Chrome extension APIs or fragile browser automation.

### Importing sounds

Provide an **Add Sound** action.

Allow the user to:

1. Paste a Myinstants sound-page URL.
2. Retrieve available sound metadata and audio when technically supported and permitted.
3. Preview the sound.
4. Import the audio into UMBRA's local library.
5. Assign a name and optional icon.
6. Choose a category.
7. Save the sound.

Also support importing local audio files.

Handle unsupported links, unavailable audio, and import failures with clear messages.

Respect website terms and audio licensing. Do not bypass access restrictions.

### Soundboard library

Support:

- Customizable sound buttons.
- Reordering.
- Renaming.
- Categories.
- Favorites.
- Deleting sounds.
- Adjustable per-sound volume.
- Local storage and offline playback.
- Persistent settings across restarts.
- A shortcut to open Myinstants for discovering sounds.

The soundboard must remain functional without Chrome or Myinstants running after supported sounds have been imported.

### Availability throughout Simulation

Make Instant Buttons accessible from every Simulation/Simulator subtab without requiring the user to leave the current activity.

Preserve the existing Simulation controls and navigation.

Use a compact, accessible panel or drawer that works on the Samsung tablet and phone.

### Button behavior

**Normal tap**
- Immediately play the selected sound through the configured Windows audio/game-chat mix.
- Provide subtle visual feedback.
- Prevent accidental duplicate triggers from touch events.

**Press and hold**
- Preview the sound privately through the configured local headphones or monitoring output.
- Do not send private preview audio into the game microphone feed.
- Show a distinct preview state.
- Stop preview on release.
- Never trigger public playback when releasing after a long press.

Implement reliable pointer/touch cancellation and a configurable hold threshold if useful.

Private preview and public playback must have separately validated audio paths.

---

## 3. AUDIO ENGINE — STEELSERIES SONAR INTEGRATION

The user has two physical microphones.

The current game/Discord input device is:

**SteelSeries Sonar - Microphone**

The objective is to let other players hear both the user's natural microphone audio and selected Instant Buttons sounds.

### Microphone selection

Provide a settings panel that can:

- Detect available Windows recording devices.
- Identify the two physical microphones.
- Show the current input and output devices.
- Select or configure the desired microphone when supported.
- Display the active audio routing configuration.
- Test microphone capture.
- Test soundboard playback.
- Test the combined game-chat signal.

Do not silently change the user's Windows default recording device.

### Audio mixing

Investigate the existing SteelSeries Sonar configuration and supported audio-routing options.

Prefer a Sonar-compatible route that preserves the user's current microphone processing and existing game/Discord input selection.

If Sonar cannot directly mix the soundboard into its microphone output, investigate a compatible virtual audio routing solution.

Do not assume that playing sound through the speakers automatically sends it into the microphone.

Document the chosen routing method and its limitations.

### Voice-matched loudness

Implement sound-effect loudness normalization.

Requirements:

- Provide a microphone calibration function.
- Measure representative speaking loudness.
- Normalize imported sound clips using a suitable perceived-loudness metric.
- Provide an adjustable soundboard-to-voice loudness offset.
- Default sound effects to approximately 3 dB quieter than calibrated speech.
- Apply a peak limiter and smoothing to reduce abrupt loudness spikes.
- Provide per-sound volume adjustments.
- Allow private preview before public playback.

Do not confuse peak normalization with perceived loudness matching.

Use sensible safety limits and avoid excessive gain on quiet recordings.

### Critical microphone fail-safe

**UMBRA must never become a required serial component in the user's normal microphone path.**

If the UMBRA server:

- Closes normally.
- Crashes.
- Disconnects.
- Loses network connectivity.
- Encounters an audio playback error.

The user's normal microphone must continue working through the existing SteelSeries Sonar setup.

Prefer optional soundboard injection into an otherwise independent microphone path.

Avoid persistent changes to default Windows audio devices or Sonar settings wherever possible.

If a persistent routing change is unavoidable, explicitly disclose it, provide a recovery procedure, and do not claim that shutting down UMBRA automatically restores it.

Include an **Emergency Audio Reset** action that stops soundboard playback, releases UMBRA-owned audio resources, and restores any temporary settings that UMBRA actually controls.

### Required audio tests

Verify:

1. Microphone works before starting UMBRA.
2. Normal voice works with UMBRA running.
3. Soundboard audio reaches the intended game-chat input.
4. Private preview is not transmitted to game chat.
5. Soundboard effects remain at controlled loudness.
6. Closing UMBRA does not interrupt normal voice.
7. Force-terminating the UMBRA server does not interrupt normal voice.
8. Reconnecting the tablet does not change the audio routing unexpectedly.

If an audio routing requirement cannot be met safely, do not force an unreliable implementation. Report the limitation and preserve the existing microphone configuration.

---

## 4. HOTKEYS — CLEAN ICON-FIRST DESIGN

Expand the existing Hotkeys tab.

Preserve every currently working hotkey and shortcut.

### Visual design

Use a minimalist, icon-first interface.

**Application shortcuts**
- Display the actual recognizable application icon.
- Prefer icons with transparent backgrounds.
- No visible application name underneath.
- No "Shortcut" label.
- No unnecessary colored square background.
- Preserve natural icon proportions.
- Use subtle hover, focus, and pressed-state effects.

**Windows hotkeys**
- Use recognizable native or established icons when suitable icons exist.
- Show icon-only buttons for those actions.
- For actions without a suitable icon, use clean text-labeled buttons.
- Do not invent arbitrary icons just to eliminate text.
- Do not show redundant labels underneath icon-only buttons.

Provide accessible names, tooltips, keyboard navigation, and long-press descriptions.

Make touch targets comfortable on the tablet.

### Windows shortcut coverage

Add verified Windows 11 hotkeys organized into categories:

**System**
- Start menu.
- Settings.
- File Explorer.
- Task Manager.
- Lock PC.
- Show desktop.

**Window management**
- Task View.
- Switch applications.
- Snap windows.
- Minimize/maximize.
- Virtual desktop navigation.

**Utilities**
- Snipping Tool.
- Clipboard history.
- Emoji panel.
- Search.
- Run dialog.

**Media**
- Volume controls.
- Mute.
- Playback controls where supported.

Verify actual Windows key combinations.

Identify context-dependent shortcuts rather than presenting them as universally functional.

Use the existing authenticated Windows companion command mechanism.

---

## 5. APPLICATION LAUNCHERS

Add application launch tiles to the Hotkeys tab.

Initial applications:

1. Rocket League.
2. Fortnite.
3. Google Chrome.
4. Bambu Studio.
5. Minecraft.

### Requirements

- Discover installed applications and their launch methods.
- Use actual installed application icons.
- Launch applications through the authorized Windows companion service.
- Support normal desktop executables and registered Windows/Store application launch mechanisms where applicable.
- Preserve any existing launcher controls.
- Show launch status and actionable errors.
- Handle applications that are missing, moved, or already running.

Do not hardcode unverified installation paths.

Do not accept arbitrary executable paths or command-line arguments from unauthenticated remote requests.

### Appearance

Launcher tiles must follow the same minimalist style as the rest of Hotkeys:

- Icon only.
- Transparent background when possible.
- No application name underneath.
- No "Shortcut" tag.
- Subtle UMBRA interaction feedback.

---

## 6. REMOTE ACCESS, SECURITY, AND RELIABILITY

Preserve the existing UMBRA Windows companion server, Remote Deck Bridge, pairing system, and Tailscale connectivity.

Ensure that Windows commands, soundboard playback, and application launches require appropriate authentication and authorization.

Requirements:

- No arbitrary remote code execution.
- No unauthenticated application launches.
- No unrestricted file-system access.
- No unintended microphone recording or transmission.
- No exposing local audio files or telemetry publicly.
- Appropriate validation of imported sound URLs and file types.
- Clear errors rather than silent failures.
- Reliable reconnection after network interruptions.
- Persistent user preferences.
- Graceful behavior when optional dependencies are unavailable.

Do not break existing ICARUS simulation features.

Keep resource usage reasonable so UMBRA monitoring and audio functions do not noticeably interfere with gaming.

---

## 7. TELEMETRY REDESIGN — DEFERRED

Do not redesign the existing ICARUS telemetry dashboard in Phase 4.8.

The user wants to review its contents separately and decide which information should be retained, removed, or reorganized.

Only make minimal compatibility or stability repairs if necessary.

Do not merge ICARUS simulation telemetry with the new Windows Engineering dashboard.

---

## 8. IMPLEMENTATION ORDER

Implement in controlled stages.

### Phase 4.8A — Engineering and Hotkeys

- Windows performance monitoring.
- Engineering dashboard.
- Verified Windows shortcuts.
- Minimalist icon-first Hotkeys redesign.
- Application launchers.

Test and preserve existing functionality.

### Phase 4.8B — Soundboard Library

- Local sound library.
- Myinstants URL import where supported.
- Local audio import.
- Categories, favorites, and editing.
- Persistent soundboard controls.
- Soundboard availability across Simulation.
- Tap-to-play and press-and-hold private preview.

Initially validate local playback and private preview independently of microphone injection.

### Phase 4.8C — Audio Routing and Sonar

- Device detection.
- Microphone selection/settings.
- Safe Sonar-compatible routing.
- Game-chat audio injection.
- Loudness calibration and normalization.
- Peak limiting.
- Emergency Audio Reset.
- Microphone fail-safe testing.

Do not proceed with a routing approach that makes normal voice dependent on UMBRA staying online.

---

## 9. FINAL ACCEPTANCE TESTS

Before declaring Phase 4.8 complete, verify:

- Engineering shows real, updated Windows data.
- Unsupported sensors fail gracefully.
- No performance overlay appears outside Engineering.
- Existing Hotkeys still work.
- New Windows shortcuts perform their documented actions.
- Application launchers use correct icons and launch installed programs.
- App icons have no visible text labels or unnecessary backgrounds.
- Imported sound files persist after restart.
- Soundboard works without Myinstants or Chrome open.
- Normal tap triggers public playback.
- Press-and-hold triggers private preview only.
- Private preview cannot leak into the configured game-chat input.
- Sound effects are appropriately normalized and limited.
- Normal microphone audio survives UMBRA shutdown and forced termination.
- Tablet and phone interfaces remain responsive.
- Existing ICARUS simulation functionality remains intact.
- Existing pairing and Tailscale access continue working.

Test failure cases, not just successful interactions.

---

## 10. DELIVERY REQUIREMENTS

At the end of each implementation stage, provide:

1. Summary of completed changes.
2. Files modified.
3. Dependencies added.
4. Installation or update instructions.
5. Any required Windows or Sonar configuration.
6. Test results.
7. Known limitations.
8. Remaining work.

Do not claim that a feature has been tested unless it was actually exercised.

If physical audio hardware, SteelSeries Sonar, or a running Windows environment is unavailable, report those tests as pending and provide exact steps for the user to verify them.

Preserve the existing UMBRA installation, configuration, and user data.

**Begin by inspecting the current repository and identifying the existing Engineering, Hotkeys, Instant Buttons, Windows companion, and audio components. Then implement Phase 4.8A first.**