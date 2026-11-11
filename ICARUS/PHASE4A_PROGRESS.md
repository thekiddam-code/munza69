# Phase 4A UMBRA companion progress

Authority: latest PHASE4_SOL_INTERFACE_PLAN.md, additions through e9ad213, and user clarification to preserve installed Android functionality. Branch codex/sol-interface-phase4. Baseline published Phase 4: 190cb41; instruction/assets baseline e9ad213.

Native Android Studio sources are absent from inspected tracked working/remote-branch trees. The working Samsung Tab S5e APK remains an existing supported integration; rebuilding/updating its native package is **pending source recovery**, not permanently unsupported. No replacement APK is created. Existing root URL, port 8765, pairing/token protocol, action endpoints and allowlisted TV keys remain. Browser/server work proceeds independently.

Milestone 1: reusable existing TV transport, explicit volatile server-managed sleep timer with exactly-once/cancellation/reconfiguration/unpair guards, truthful send-vs-execution status, authenticated capability/timer endpoints. Six deterministic service tests pass. Shared original ICARUS standard/51st-State camera sprite functions are extracted without output changes; read-only bounded companion projection filters unavailable cameras, secret field positions, unreceived deaths and private events. Five Node tests pass, including byte-equivalence of existing sprites and purity/privacy cases. No physical Android/TV test is claimed. Native sleep timer, power-on, app launch and advanced picture/sound/long-press remain unverified/unavailable capabilities.

Next: implement modular UMBRA browser layouts, profile editor, real camera/crew feed and offline optional arcade; validate existing functions plus new adversarial cases before packaging. Full Phase 4A acceptance is not yet claimed.
