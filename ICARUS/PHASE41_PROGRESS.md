# Phase 4.1 Command Bridge progress

Approved user specification: 2026-11-11 chat, stages A–F. Baseline 2436d4f (Phase 4A); branch codex/command-bridge-phase4-1. Preserve the installed Android APK; native rebuild pending original source recovery. Physical Windows/Android/TV/AV are separate unexecuted gates.

Audit: prior host publication is opt-in via a manually pasted session host key hidden in Settings, only works at the exact served /icarus.html path, and is entirely absent when opening a file. This explains a reproducible no-key offline condition; the user's actual Windows logs are unavailable, so no unique device-specific diagnosis is claimed. Serving the simulation to remote browsers also permits a separate local world. Destructive command dequeue loses requests on dropped delivery. Old cross-tab IDB ownership covers one origin, not two origins or clients.

Stage A implemented: loopback automatic host bootstrap, non-loopback /icarus.html redirect to UMBRA before simulation loading, server-monotonic 12-second fenced ownership plus shorter local write permission, heartbeat, bounded acknowledged commands and token-scoped request deduplication, opt-in SSE with paired authentication, existing native routes retained. Standard Windows launcher opens the authoritative loopback URL. Saves remain browser-owned; no remote save-upload route. Old static localhost test hosting still uses existing IDB ownership (no companion service there).

Executed initial validation: seven deterministic service unit cases and four real-HTTP/Chromium authority, protocol, duplicate-dispatch, source match and remote-gating integration cases pass. Later stages and full regressions follow; this is not final acceptance.
