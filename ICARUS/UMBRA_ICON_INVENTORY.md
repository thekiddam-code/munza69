# Offline icon / asset inventory

`web/umbra/icons.js` includes stable SVG paths for power, mute, volume, channel, up/down/left/right/OK, home, back, source, play/pause/stop/rewind/forward, timer, camera, crew, connection, edit/save, settings/info/game and a neutral fallback. Labels remain plain text and accessible. Critical glyph rendering no longer depends on emoji/icon fonts/CDNs. The WY mark remains local inline SVG; PWA icons are local SVG plus 192/512 PNG. Browser-generated/user message text remains text nodes, not trusted HTML.

Source audit found numerous font-dependent glyphs (including combining mute/arrow symbols) and an empty original manifest icon list. Bundled web icons address those confirmed dependencies. Native red-X root cause still needs original APK source/WebView/drawable inspection; no physical fix is asserted.

Six supplied GIFs under UMBRA/assets/arcade-kill-cam are copied byte-for-byte to web/umbra/arcade and retain their fictional manifest/provenance. Each is GIF89a 128×72, 12 frames at 240 ms; static PNGs decode the actual first frame. They are not footage or game events. The loaded client validates/caches the six bounded pairs for disconnected playback, and reduced motion uses PNG. First browser bootstrap/reload needs the existing server; no native bundling/offline installation is claimed before recovering the Android project.
