# ICARUS Phase 4.7A — Field Deployment Checkpoint

This continues the existing voyage and the verified catch-up hotfix. It implements physical FOC-01 deployment and recovery at Landing Shelf0. The whole Phase4.7 release remains incomplete: camp-based drone services, ATV travel, medical support and further logistics are next.

## Install and preserve your voyage

1. Export a complete backup from your current host. Keep it and the previous application folder.
2. Stop the old server and close its authoritative host tabs. Extract this build into a separate permanent folder. Transfer existing private configuration/pairing only with both servers stopped, as described in README_PHASE46.md.
3. Keep the same browser profile, hostname and port so the existing IndexedDB voyage remains accessible. Run `Start_Remote_Deck.bat`, refresh with Ctrl+F5 if needed, wait for actual readiness, then select **ENTER ICARUS**.
4. Do not clear site data, delete locks, create a new voyage or import a backup merely because the folder changed. The authorization field and writer ownership remain independent. Existing Windows-host/UMBRA pairing and remote-only operation are preserved.

The ZIP contains no personal voyage or credentials. Native Android rebuilding remains pending source recovery; existing browser/Android web interfaces have not been removed.

## Observe or request deployment

Open **Missions → Active → UMBRA // SURVEILLANCE**. FOC-01 remains parked in C03 until actual preparation and travel occur. Use **Request camp deployment** for an optional captain-directed request. This queues the same autonomous engineering/team controller rather than spawning a camp.

An available engineer must physically reach C03, inspect the vehicle, install the freight interface and test it. The refit requires six spare parts, two tools and four ship energy. Existing emergency, access and crew-priority rules can postpone it. The accepted mission needs a fit engineer/scientist team, suits, carried supplies, safe ship systems, a received Landing Shelf survey and an available shared lander. Blockers are reported; resources and crew are not fabricated to satisfy a request.

Crew collect supplies at C04, reach the C03 freight lock, load the vehicle, complete checks/pressure cycling, travel for the existing fifty minutes, unload and erect the actual equipment. Watch C03 for loading/empty parking; an available suit or drone camera at the Landing Shelf can show the exterior camp. There is no omniscient fixed camp camera. Medical/sleeping tents have no invented occupants or interior feeds.

Actual long-range expedition evidence can justify autonomous deployment when unfinished observed frontier work remains. The same completed mission cannot keep triggering redeployment. **Hold future deployments** prevents new autonomous requests; its release restores the evidence-driven policy. An active expedition uses its ordinary **Recall active team** control, including actual communications and return constraints.

**Request camp recovery** sends another physically prepared team to pack the equipment and load FOC-01. It must travel back, repressurize and be physically re-secured in C03. Recovering a camp does not copy its equipment or reset its battery. No free field replenishment occurs.

## What this camp can do now

Its equipment persists as actual erected/recoverable objects, with a finite vehicle power bank driving standby relay/floodlight state. Empty tents stay empty. Setup and packing work uses actual crew task poses in existing cameras. Radio loss preserves uncertainty: field status appears only after legitimate communication or returned-crew debrief. Unknown conditions are labeled unreported.

Camp-based drone charging/maintenance/rotations, medical treatment, overnight occupants, ATV driving, security patrols, resupply and off-shelf relocation are **not implemented in this milestone**. Those controls are not offered as if they work. Existing ship-based drone operations remain available. Only Landing Shelf0 is freight-rated; no truck travels through unmeasured tunnels. The architecture document records the new explicit engineering geometry and its abstraction limits.

## Saves, pacing and rollback

The existing world/schema/storage namespace and IDs remain. An optional deployment subdomain stores refit costs/progress, transport reservation, vehicle/camp location, equipment, battery and report references. Mid-load, transit and camp saves resume; Monday boundaries preserve ongoing work. The selected rate, holiday synchronization, catch-up worker, canonical IndexedDB saves, preview size cap and writer locks remain unchanged.

For rollback, export a complete post-deployment backup and retain it separately. **Pause this current build and import your pre-deployment backup here first**, using the ordinary explicit restore workflow; verify the original parked voyage. Then stop the server, close its host tabs and reopen the retained earlier build at the same origin. Earlier builds do not understand active freight/camp state, so do not open them against that active state first. Keep both backups for returning to this build; do not clear storage or bypass writer protections.

See PHASE47A_DEPLOYMENT_ARCHITECTURE.md, PHASE47A_DEPLOYMENT_PROGRESS.md and PHASE47A_DEPLOYMENT_VALIDATION.md for source boundaries, actual verification and remaining work. Physical Windows/Samsung/TV/Tailscale/antivirus tests are not implied by browser emulation.
