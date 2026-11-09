# ICARUS — Final Core Design

Status: governing product direction from v1.4. This document defines the destination, not a claim that the current build is a finished commercial release. Changes must show how they deepen or finish this experience. Depth before breadth. Cohesion before expansion. Completion before additional scope.

## 1. Identity and player experience

**Official title:** ICARUS. **Genre:** Autonomous Science-Fiction Anthology Simulation.

A persistent spaceship, its established crew and the autonomous corporate AI SOL provide continuity through unpredictable, sometimes interconnected deep-space stories. The player can observe quietly or intervene as captain. The ship continues operating without a mandatory dispatcher, dialogue choice, daily checklist or encounter quota.

A good session can contain a satisfying ordinary watch, a humorous communication, friendship, a scientific uncertainty, philosophical disagreement, a frightening incident or a bittersweet departure. Danger is one possibility. An uneventful passage is valid. The final game must remain interesting through people, observation and consequences, rather than an escalating supply of emergencies or map cells.

## 2. Essential final-release systems

- One continuous world clock and durable crew, relationships, health, memory, resources, research, missions, unresolved incidents and source history.
- Autonomous crew life, maintenance, finite resource handling, feasible expeditions and emergencies; coherent SOL prioritization and optional captain overrides.
- Local signals, visitors, salvage, derelicts, scientific observations and ordinary encounters with finite opportunities and recorded causes.
- A causal anthology engine supporting overlapping, interrupted and unresolved threads, with persistent consequences rather than forced weekly endings.
- Evidence-based science, replication and uncertainty. Lazarus remains optional and cannot guarantee resurrection or a revelation.
- A unified observer/captain Remote Deck, accurate chronicles, accessible controls and a tested save/export/recovery workflow.

An implemented formula or passing test is only part of completion. Balance, legibility, variety, content quality, performance and sustained human play review must meet the intended experience.

## 3. Visual design and interface

Retain the existing dark shipboard corporate instrumentation: restrained cyan/green information, amber attention, red for actual danger, consistent type scale, angular panels and familiar ship/crew views. ICARUS remains the title; avoid multiplying competing product names. Operations is a single ship-and-story overview, with local logistics and preferences disclosed on demand. Existing specialist research, crew and medical views remain, progressively consolidated rather than replaced by disconnected dashboards.

Every important status should explain its cause and offer appropriate optional intervention. Preserve tablet-sized touch controls, readable contrast, keyboard focus, reduced motion and nonmodal observation. A cinematic layer must never hide critical controls or imply an event that did not happen. Full archive/export lives on the authoritative PC; the paired tablet is a thin observer/controller.

## 4. SOL and the captain

SOL operates ship systems, weighs actual survival and staffing needs, authorizes safe missions and research, and records the reason for decisions. Its corporate restraint permits dry humor, curiosity and recognition of people. Unusual does not mean hostile. Commentary must remain bounded by received information and actual outcomes.

The captain can hold/release local travel, override a feasible local course, recall expeditions, inspect evidence, attempt feasible rescue and alter existing protocols. Refusal must explain the physical or safety constraint. Silence is a supported player choice; the simulation must not stop waiting for routine approval.

## 5. Autonomous crew life

The established people keep their identities, personalities, jobs and relationship history. Physical location, health, fatigue, stress, morale, skills, gear, social needs and availability matter. A communication duty uses available time; it cannot make someone aboard while they are away or replace an emergency responder. Positive shared experiences can affect morale, trust and willingness. Injuries, treatment, loss, failed work and memories have lasting state-backed consequences. Death is permanent under current evidence; no repopulating weekly cast.

The target is recognizable individuals with believable, sometimes ordinary lives. Numeric experience is the present implementation, not a substitute for deeper characterization and human review.

## 6. Anthology lifecycle

A beginning needs a real observation, recorded crew behavior, ship operation, research result, unresolved situation or plausible seeded external signal. Each thread retains its source IDs and affected people/actors. Development uses actual available work, received information and existing conditions; complications require observed constraints, not a dramatic timer.

Threads may overlap, wait for staffing or scientific results, resume, end quietly, be declined, remain unresolved or end because of real loss. Sunday never forces closure. A later observation can reference an earlier actor or question. A remembered positive moment can become an optional tradition; its recurrence needs actual participants and paid provisions. No category is guaranteed each week.

Core breadth stays small: local contexts and a varied library of state-conditioned interactions. Improve specificity, consequences and presentation before adding another system.

## 7. Science and Lazarus

Keep observations, hypotheses, experiment outcomes and confirmed conclusions distinct. Experiments consume laboratory resources and eligible crew time. Failed, contradictory and inconclusive work is normal. Major claims need supporting independent evidence/replication under existing research rules.

An anthology thread can follow an unresolved experiment and later recorded results, but it never promotes its own narration to a scientific conclusion. Lazarus is one possible long-running research thread. Many stories never involve it. Unknown identity, viability and reconstruction questions remain unknown unless the scientific model actually supports an advance.

## 8. Sunday chronicles

Weekly presentation selects actual crew, encounter, research, relationship, operational and emergency records. Tone should follow what occurred: positive, ordinary, character-focused, mysterious, mixed or tragic. Open threads carry forward, with explicit source references. Selection is a view of the history, not a replacement for the world or a complete transcript.

Event cards and incident replays are labeled **reconstructions**. Actual recording metadata must be identified separately; never invent footage. Optional anthology endings summarize current state. Legendary Kill Cam eligibility remains rare and requires documented extraordinary lethal encounter evidence and matching recording/causal references. Never create violence for the feature.

## 9. Complete and playable

Final readiness requires stable continuous autonomy; recognizable persistent individuals; varied, coherent stories with consequences; engaging evidence-bounded SOL; optional rather than mandatory captain work; polished consistent UI; accurate chronicles; durable extended play; balanced interesting quiet periods; and understandable onboarding/recovery.

Verification combines deterministic/adverse/long-run tests with sustained human observation, usability and content review. Ship survival, a test count or a long duration alone cannot establish a good anthology or final-release readiness. FINAL_RELEASE_ROADMAP.md must expose incomplete and unverified areas.

## 10. Core exclusions / Extended Universe boundary

Procedural planet/star-system expansion, galaxy maps as progression, territorial faction management, autonomous civilizations, galactic markets and large-scale economic simulation belong to the separately preserved Extended Universe edition. Do not activate them in core without explicit user approval.

Also excluded from the present core definition: mandatory combat, unrestricted generated dialogue, multiplayer, recruiting an unlimited population, cloud-service dependence and manufactured cinematic footage. A bounded local schematic, finite salvage and believable travel/supply context remain valid supporting tools. New unrelated scope requires a clear player-experience benefit and explicit reconsideration of this boundary.
