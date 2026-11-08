ICARUS + REMOTE DECK BRIDGE v0.93.1

1. On Windows install requirements and run Start_Remote_Deck.bat.
2. On the PC (not tablet), open http://127.0.0.1:8765/icarus.html
3. Enter the ICARUS host key shown in the server console. This key is stored only in PC browser sessionStorage.
4. On Galaxy Tab S5e open the Remote Deck URL shown in the console and pair normally.
5. Select ICARUS tab for telemetry, crew, recent events and pause/resume/speed/save commands.

IMPORTANT: The PC ICARUS browser is authoritative. Keep it open to run the simulation.
ICARUS is NOT synchronized across two simulation browser copies. Remote Deck is a monitor/controller only.
Remote telemetry is kept in memory on the server, not written to disk.
Existing ICARUS localStorage saves are origin-specific. Opening through localhost:8765 starts a new save namespace; export your old ICARUS backup and restore it in the hosted version if you need continuity.
Host key is printed on PC and never sent to tablet. Pairing tokens remain managed by existing Remote Deck.
Only use on a trusted home network.

ICARUS v0.93.2 fix: Bridge code now executes inside the simulation closure, fixing "state is not defined". Replace the previous extracted folder with this package.
