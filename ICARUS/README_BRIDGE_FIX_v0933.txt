Remote Deck bridge v0.93.3 repair

Fix: bridge UI is now in the DOM before the simulation script executes.
Fix: bridge logic remains inside the same simulation closure as state.

Extract into a NEW folder, stop old server, run Start_Remote_Deck.bat from the NEW folder.
Open http://127.0.0.1:8765/icarus.html?v=0933 and hard-refresh (Ctrl+F5).
Confirm the footer says v0.93.3 before testing.
Pair using host key printed by the server.

This repairs the browser initialization sequence; live device connectivity is not verified.
