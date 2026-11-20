# Expedition regression investigation

Two pre-existing browser scenarios initially failed after adding paid biological collection. The first request to launch a second survey, at minute260, was correctly rejected as `ship resource priority`. An earlier assertion assumed immediate repeated dispatch. The tests now retry only after actual simulated readiness/resource recovery, retaining the safety rejection and granting no resources.

That exposed a separate software defect: the next accepted mission (M-0002 at minute310 in the diagnostic) stayed in equipment collection. Engineer Sana Okafor's last room was C04, but her real navigation node was H:C:1 on an interrupted route toward B05. The staging callback used path(C04,C04), producing an empty route while the old navigation step remained active. Arrival validation correctly refused this false physical arrival. The crew waited, depleted readiness, and staging aborted; the two-sortie history assertion consequently remained at one return. Audits did not indicate inventory duplication.

The repair adds physicalTaskRoute for ordinary task assignment, expedition staging/movement and new biological work. It retains the actor's actual navigation node/lift state and assigns the requested destination even when it equals the last room ID. The existing travel engine then traverses the connected graph; the repair does not rewrite room, jump the actor to equipment, weaken the arrival check or override resource/crew safety. There is no timeout extension or free repair/resource grant in production.

A targeted real-browser fixture starts available specialists in C04's corridor on an existing route, dispatches, asserts the original corridor node plus a required C04 route, then requires actual progression beyond staging. The original two-sortie cavern traversal and finite powered lift-repair tests remain and are rerun. Initial failed reports are retained as diagnostic evidence rather than relabeled passes. Final validation records the actual rerun results.

Long-duration runs started before this repair are retained only as development prefixes. Final campaign acceptance must use the corrected runtime hashes.
