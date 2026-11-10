# ICARUS: Unified World and Anthology Overhaul
## Phase 1 Codex Development Specification
**Status:** Design approved for implementation planning  
**Target:** Extend existing ICARUS v1.4.1 without discarding working systems.

### 1. Core Simulation

ICARUS is one persistent, autonomous science-fiction world consisting of a mobile research vessel, its crew, an asteroid formed from a destroyed mining planet, an abandoned Weyland-Yutani research derelict, and a crashed military warship.

SOL operates as the ship's corporate AI, with imperfect information and a distinctive personality.

The simulation must preserve character autonomy, causal consequences, ongoing missions, environmental hazards, relationships, discoveries, and permanent world changes.

Do not force disasters, deaths, encounters, or story conclusions to satisfy an episode schedule.

### 2. Time and Calendar Engine

**Normal simulation speed: 4×**

- One real-world hour equals four in-game hours.
- One real-world day equals four complete in-game days.
- Characters experience actual day/night cycles, shifts, meals, sleep, and activity schedules.
- In-game calendar dates advance with simulated time.
- Simulation time and real-world time must be maintained separately.

**Initial calendar alignment**

- The initial in-game date may be calculated dynamically to align with the next designated synchronized holiday.
- The simulation does not need to begin on the first of the current month.
- No fictional crew history is generated before the first simulation tick solely to fill a calendar gap.

**Holiday synchronization**

- At the beginning of a designated holiday in the user's configured local timezone, correct the displayed in-game date to match the actual holiday.
- Reduce simulation speed to 1× for the entire local holiday.
- Return to 4× after the holiday, unless another synchronized holiday immediately follows.
- Consecutive synchronized holidays, such as December 24 and 25, must remain continuous.
- Use the actual holiday date, not an alternate federal observance date, unless explicitly configured otherwise.

**Continuity safeguards**

Maintain two independent records:

1. Monotonically advancing simulation time and event history.
2. Adjustable displayed calendar date.

Calendar corrections must never rewind physical simulation state, reverse aging, resurrect characters, erase injuries, restore consumed resources, repeat completed missions, or delete memories.

Every holiday occurrence must have a unique real-world date identifier to prevent duplicate celebrations when the displayed calendar moves backward.

### 3. Official 1× Synchronized Holidays

The following nine dates are approved:

| Holiday | Date |
|---|---|
| New Year's Day | January 1 |
| Memorial Day | Last Monday in May |
| Independence Day | July 4 |
| Labor Day | First Monday in September |
| Halloween | October 31 |
| Veterans Day | November 11 |
| Thanksgiving | Fourth Thursday in November |
| Christmas Eve | December 24 |
| Christmas Day | December 25 |

Each receives one full real-world local day at 1× speed.

These holidays may influence crew activities, social gatherings, decorations, meals, remembrance, and personal traditions. They must not suspend essential operations or guarantee peaceful conditions.

### 4. Recognized Holidays at 4×

These observances do not change simulation speed:

- Martin Luther King Jr. Day
- Valentine's Day
- Presidents' Day
- St. Patrick's Day
- Easter
- Juneteenth
- Columbus Day / Indigenous Peoples' Day
- New Year's Eve

Crew members may acknowledge these dates through appropriate activities, discussions, ceremonies, decorations, or gatherings.

Participation is voluntary and based on established character preferences.

### 5. Individual Cultural and Religious Observances

Personal observances are distinct from the official shipwide time synchronization calendar.

Examples include Hanukkah, religious holidays, cultural traditions, birthdays, anniversaries, and personal remembrance days.

Hanukkah is **not** a global 1× synchronization holiday.

Character celebrations should reflect individual beliefs, preferences, relationships, and histories rather than assigning uniform behavior to an entire demographic.

Decorations and personal objects must exist as persistent world items. They may be placed, moved, stored, forgotten, gifted, or inherited.

### 6. Seasonal Atmosphere Engine

**October:** Elevated horror atmosphere throughout the real-world month, with Halloween as its culmination.

**Friday the 13th:** Heightened suspense during any real-world week containing Friday the 13th.

**Full moons:** Subtle eerie presentation and cultural references based on Earth's actual lunar cycle.

These modifiers may overlap.

They influence eligible environmental presentation, dialogue, pacing, and suspense, but must not automatically create enemies, disasters, temporal anomalies, or fatalities.

The real-world calendar determines these atmospheric effects, regardless of temporary differences in the ship's displayed date.

### 7. Seven-Day Anthology Episodes

- Each episode runs Monday through Sunday in the user's local timezone.
- Episode boundaries follow real-world time, independent of 4× simulation acceleration or holiday corrections.
- Crew, world conditions, and unfinished stories persist across episodes.
- Sunday recaps summarize actual recorded events.
- Recaps may use genuine camera footage or clearly labeled reconstructions.
- Extraordinary events may qualify for a rare Legendary Kill Cam.
- Never invent events solely to make a recap more dramatic.

### 8. Connected World Architecture

Preserve the existing three ICARUS decks and 30 named rooms.

Maintain one authoritative spatial state for corridors, rooms, lifts, airlocks, docking bridges, equipment, crew positions, and camera feeds.

Correct the existing discrepancy where the camera presentation depicts characters moving through successive rooms instead of their actual corridor routes.

The four primary environments are:

1. **ICARUS:** Command, habitation, research, containment, engineering, and docking.
2. **Asteroid 8847-A:** Surviving fragment of a destroyed, heavily mined planet, with caverns, a near-core borehole, atmospheric pockets, and hidden temporal anomalies.
3. **Weyland-Yutani Derelict:** Abandoned research vessel connected to Project Lazarus, biological preservation, and temporal research.
4. **Military Wreck:** Damaged warship containing finite salvage, recoverable power systems, equipment, vehicles, and concealed hazards.

Exploration must reveal information gradually. Do not expose undiscovered secrets in ordinary crew interfaces.

### 9. Character and Biological Systems

Preserve autonomous behavior, relationships, individual knowledge, injuries, physical limitations, and occupational responsibilities.

Support distinct body types, natural movement, prosthetics, wheelchair users, damaged androids, and alternative locomotion.

At initial simulation start:

- Exactly one fully developed Xenomorph exists, dormant and sealed in a concealed military chamber.
- Other Xenomorph presence is limited to dormant eggs.
- Additional Xenomorphs must emerge through causal host infection and development.
- Power restoration or exploration may create conditions for discovery or release, but neither is guaranteed.

A host-influenced Xenomorph generator must produce biologically coherent variants.

### 10. Lore and Discovery

Provide two separate systems:

**Settings: Lore Editor**

Creator-facing reference material and accepted ICARUS canon. Hidden world truths can be edited without exposing them to the crew.

**In-game Archives**

Only evidence, observations, documents, and discoveries actually acquired in the simulation.

Alien and Predator material may serve as biological and aesthetic reference, but film events are not automatically canonical to ICARUS.

### 11. Interface and Persistence

Preserve the existing industrial, restrained Weyland-Yutani visual direction, with amber and cyan interface accents.

Provide contextual controls, consistent ship holograms, resizable widgets, smooth character rendering, and synchronized camera/cutaway views.

Preserve existing UMBRA Remote Deck functionality and avoid breaking its PC, television, and gaming controls.

Persist the complete world state reliably across application restarts, including calendar mappings, event history, holiday completion markers, character memory, resources, and discovered lore.

Provide bounded, deterministic recovery and catch-up behavior after suspension without duplicating events.

### 12. Development and Validation

Before modifying the application, audit existing implementations and identify reusable systems.

Recommended implementation order:

1. Persistent simulation clock and calendar mapping.
2. Holiday synchronization and date correction.
3. Seven-day episode scheduling and evidence-based recaps.
4. Shared authoritative navigation and camera positioning.
5. Connected environment and character improvements.
6. Lore, discovery, and biological systems.
7. UI refinement and long-running stability tests.

**Required calendar tests**

- Four complete in-game days elapse during one uninterrupted real-world day at 4×.
- Every approved holiday aligns with its real-world date.
- Every approved holiday runs at 1× for the entire local day.
- December 24 and 25 remain consecutive without an intervening 4× period.
- Thanksgiving and other movable holidays resolve correctly each year.
- Calendar corrections never reverse simulation history or duplicate events.
- Recognized 4× holidays never trigger a global slowdown.
- Personal observances never trigger a global slowdown.
- October, Friday the 13th, and full-moon modifiers can overlap without forcing incidents.
- Episode boundaries remain tied to seven real-world days.
- Restart, timezone, daylight-saving, and suspension behavior remain consistent.

**Acceptance criteria**

The completed system must demonstrate persistent autonomous crew behavior, correct 4× time progression, reliable holiday synchronization, truthful episode recaps, coherent world navigation, stable save/load behavior, and no regression of previously working functionality.

---

**Approved design baseline:** This specification supersedes earlier conflicting calendar and simulation-speed proposals. The nine synchronized holidays and eight recognized 4× observances are finalized for Phase 1.