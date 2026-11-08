ICARUS v0.94.3 Patch 3: diagnostic-only timer isolation and error stack traces.
The normal app is unchanged unless loaded with ?icarus_soak=1.
Run python soak_test.py --days 7 from remote_deck.
The test disables autonomous clock ticks and startup crew task reassignment in diagnostic mode, so it can distinguish save corruption from legitimate gameplay scheduling.
