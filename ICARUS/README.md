# Remote Deck v0.1

A local-network Android browser controller and Windows Python receiver for Minecraft, Rocket League and general hotkeys.

## Windows setup

1. Install Python 3.11 or newer from python.org. Enable Add Python to PATH if prompted.
2. Extract this ZIP to a folder on your PC.
3. Open a terminal in that folder, then run:

   `py -m pip install -r requirements.txt`

   `py server.py`

4. Windows Firewall may ask for access. Allow on **Private networks only**. Do not expose port 8765 to the Internet.
5. Note the displayed `http://...:8765` address and pairing PIN.
6. On Android, connect to the same Wi-Fi and open the address in Chrome. Enter the PIN.
7. Keep the Windows terminal running while using the controller. Press Ctrl+C to shut down.

## Controls

- Minecraft: toggle left mouse button or hold W + left mouse button for up to 10 seconds.
- Rocket League native quick chat: configure the two-key sequences in `config.json` to match your game settings. The defaults are **examples, not guaranteed Rocket League bindings**.
- Rocket League custom chat: set `text_chat_open` in `config.json` to the key that opens your game's text chat. This feature works only if your game/platform/server permits text chat.
- Macros: edit `macros` in `config.json`. Entries are key combinations, not arbitrary scripts. Example: `"Copy": ["ctrl", "c"]`.
- PC monitor: CPU/RAM percentages.
- Emergency stop: releases keys/buttons held by this receiver. Also releases automatically after a maximum of 60 seconds.

## Notes and limitations

- This is a **local web controller**, not a native APK. Browsers may not offer install-to-home-screen for HTTP connections to a LAN IP. You can still use it in Chrome or add a bookmark. A packaged APK or HTTPS deployment can be added later.
- The PC receiver must run in the same logged-in Windows desktop session as the game, and simulated input may not be accepted by every game or fullscreen mode.
- The phone must be paired after every receiver restart. Pairing tokens are stored only in the phone's browser session and in receiver memory.
- Do not use on untrusted Wi-Fi. This is plain HTTP, so the PIN and commands are not encrypted in transit. Use a trusted private home network; do not forward ports or expose to the Internet.
- This starter does not include remote editing of macros or a full visual macro builder. Modify `config.json` and refresh the app.
- Server and game rules may restrict automation, even when Minecraft cheats remain off.
- No screen capture, remote shell, file access, or arbitrary command execution is included.
- Stop Minecraft mining before switching to another application, as held inputs target the active desktop.
