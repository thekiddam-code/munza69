# Catch-up regression investigation and engineering notes

## Finding

The supplied voyage retains `calendar.selectedRate = 20`. The calendar still advances each physical simulation minute through the existing core and field logic. This was a throughput regression, not an intentional pacing reduction. On this machine the original checkpoint was faster than 1× simulation time, but much slower than the repaired implementation; the reported near-1× behavior on the user's Windows hardware was not directly measured.

The dominant measured cost was synchronous LZ-string encoding of the complete snapshot and preceding compatibility recovery snapshot on the browser main thread. In the matched 120-tick original run, eight save calls consumed 26.50 seconds of the 28.95-second processing window. CPU sampling attributed 23.05 seconds directly to `_compress`, before its wrapper/GC costs. Core and field processing together used about 374 ms. Cooperative catch-up yielding in the Phase 4.7 checkpoint exposed additional UI and preview work between these expensive saves. The compression cost predates Phase 4.7; profiling does not establish that vehicle code introduced it.

Vehicle registration/inspection, drone escorts, drone simulation and pathfinding were inspected and measured. In the same original 120-tick run, ForwardOps.tick used 1.8 ms, DroneEscort.tick 0.3 ms, and DroneOps.tick 7.0 ms; these were not the main bottleneck. Core timing includes crew routines, movement, engineering and psychology. Field timing includes science, research and mission selection. An inactive expedition has no active expedition tick cost. A separate actual preparation/travel/return fixture measured 227 active expedition calls totaling 35.5 ms (0.156 ms/call), plus 396 pathfinding calls totaling 28.5 ms. That technical fixture is separate from the matched private voyage. No vehicle deployment/camp implementation is implied by these measurements.

## Save path

`save()` used to synchronously decode/encode compatibility primary/recovery data before returning. The app-managed path now validates/serializes the same complete state and queues `ICARUSDurable.snapshot(raw)`. IndexedDB remains canonical, with the original three-revision retention and transaction fencing. Autosave cadence is unchanged. The pump pauses before consuming another calendar interval when two complete snapshot writes or four history transactions are outstanding. It resumes on normal cooperative callbacks, without consuming time or skipping physical events while blocked.

`save-cache-queue.js` allows one active and one latest pending compatibility job. `save-cache-worker.js` uses the existing vendored lossless codec off the main thread. Coalescing applies only to the derived cache, never the canonical snapshots or recorded events. A job includes its canonical predecessor so the recovery mirror is complete. Both local storage writes are fenced by current local/server authority, latest raw snapshot and database revision. Failed or late jobs cannot replace a new world. Worker errors leave IndexedDB and backup export usable, with a diagnostic warning. A reload before encoding completes restores the verified database without falsely forking event history.

The unchanged-history optimization caches at most 4096 committed row signatures; changed contents under the same ID still write. Signatures are acknowledged only after the history transaction commits and are invalidated after atomic import. Failed writes requeue rows without replacing newer queued content.

`ICARUSDurable.flush()` waits for canonical snapshots and history; `{cache:true}` additionally waits for the compatibility mirror. Only cache-editing technical fixtures need that extra wait. Manual backups still include full current state and indexed history. With unavailable IndexedDB the existing synchronous fallback remains; worker acceleration is not claimed there.

## Telemetry and presentation

The Remote Deck preview has a separate 110,000-byte budget, below the server's unchanged 131,072-byte request cap. Preview projections duplicate historical crew paragraphs, state frames and recording previews. The previous reducer could still exceed the preview budget after its last historical-detail reduction. This is not a limit on the actual world or backup file.

The reducer now batches historical trimming rather than repeatedly serializing the full envelope after every person, and can defer the remaining duplicated crew history. All live identities/conditions, source archive IDs, known map sectors and command acknowledgements remain. Deferred history is labeled; it is not represented as nonexistent. Source world and recordings are never modified. The supplied earlier backup did not reproduce every reported oversized essential payload; a deterministic oversized-history fixture reproduces the previous error, while an irreducible-essential-payload test proves truthful rejection/backoff rather than silent data corruption.

`telemetry-cadence.js` prepares previews at most every three seconds during catch-up and normally every 1.1 seconds, reuses unchanged prepared packets briefly, and backs off preview-size errors. Payload failures do not invalidate writer authority. Authorized command polling/application precedes preview preparation; Host's independent heartbeat remains unchanged. Real authentication, lease and network errors retain their existing behavior. Preview size limits were not increased.

Only presentation is throttled: clock DOM updates at most four times per second, general rendering/observation refresh every two seconds during catch-up, and hidden observation panels avoid redundant projections. Actual sensor observation, event-triggered capture, physical movement, research, gravity and field minute processing remain on the original causal loop. Camera renderers continue their existing visibility-aware drawing. No world events or recordings are removed as a performance shortcut.

## Diagnostics and boundaries

`runtime-diagnostics.js` stores bounded, nonpersistent counters and live throughput measurements, separate from voyage data. It reports selected/interval rates, backlog in wall seconds, simulation and wall-throughput, tick/save/telemetry timings, queue status and storage warnings. No network service, executable download, new dependency, external command, or system modification was introduced. The worker imports only the existing local codec. Server/network security and writer-lock mechanisms were not bypassed.

This targeted hotfix does not implement the unfinished Phase 4.7 camp, vehicle departure, camp-based drone rotations or new media transport. Those remain separate work. Physical-device performance and the user's current unsupplied live database remain unverified; the supplied Episode 2 backup was the common workload. See the verification report for actual timings and tests.
