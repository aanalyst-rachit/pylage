# PyLage V2 — Final Phase-Wise Roadmap

## PHASE 0 — V2 Preparation & Baseline
Goal: V2 development start hone se pehle V1 ko frozen baseline banana.

0.1 V1 baseline:
- V1.0.2 stable
- Existing API frozen
- Existing tests green
- Performance baseline recorded
- Current demo verified
- Current protocol documented

0.2 Architecture freeze:
- Granian
- ASGI
- server-driven UI
- differential rendering
- session-based runtime
- file-based routing
- Python-first developer experience

0.3 Regression baseline:
- full test count
- performance benchmarks
- protocol behavior
- rendering behavior
- public API compatibility

0.4 Playground V1 completion:
- modern PyLage landing page
- live Python-to-UI playground
- two-pane editor and live preview
- browser-side Pyodide runtime
- current V1 PyLage API execution
- demo components and reactive examples
- loading and error handling
- responsive desktop/mobile layout
- MkDocs integration
- GitHub Pages deployment verified
- deployment and focused Playground tests verified

Exit Gate: V1 stable → Baseline recorded → Playground V1 complete → V2 architecture frozen → PHASE 1.

## PHASE 1 — Foundation & Runtime Migration 🔴 CRITICAL
Goal: PyLage proper multi-user production runtime.

1.1 ASGI Adapter — IMPLEMENTED (Option B):
- ASGI adapter provides unified HTTP + WebSocket transport
- WebSocketServer reactive/event machinery is reused behind the ASGI boundary
- Granian runs the importable ASGI application factory
- Real Granian HTTP, WebSocket handshake, and event round-trip smoke verified
- Existing Runtime + LocalServer remain as the compatibility/local path during staged migration
- Full regression gate: 1109 passed, 1 skipped

1.2 Per-Session State Isolation:
Connection → Session → State → DependencyGraph → Scheduler → Component Tree
No global user state.

1.3 Session Resumption — IMPLEMENTED:
Browser → session token → disconnect → reconnect → same session restored.
- Secure session token handshake
- Client stores session token
- Reconnect resumes the same WebSocketServer/session
- Unknown or stale token creates a fresh session
- Retained sessions are cleaned up during ASGI lifespan shutdown
- Full regression: 1126 passed, 1 skipped

1.4 SessionStore — IMPLEMENTED:
- in-memory SessionStore is the default runtime store
- TTL eviction with expired-session cleanup
- swappable SessionStore interface with ASGI injection
- ASGI shutdown clears the session store
- Redis later only when horizontal scaling requires it

1.5 WebSocket Heartbeat — IMPLEMENTED:
- configurable heartbeat interval
- server ping / client pong verification
- dead connection detection
- dead connection cleanup
- WebSocket regression: 28 passed

1.6 Migration Test Gate — IMPLEMENTED:
- transport tests
- session isolation
- two-tab/session coverage
- reconnect/resumption test
- no cross-user state leakage
- TTL/expiration coverage
- focused migration gate: 42 passed
- full regression: 1129 passed, 1 skipped

Exit: ASGI + Session Isolation + Session Resume + TTL + Heartbeat + Regression — PASS.

## PHASE 2 — Protocol & Performance 🔴 CRITICAL
Goal: existing fast reactive engine also fast at network level.

2.1 Binary Protocol:
- JSON → MessagePack
- changed props only
- metadata caching
- smaller payloads
- faster serialization/deserialization

2.2 CSS Deduplication:
StyleCollector → unique CSS → shared stylesheet

2.3 Static/Dynamic Template Split ⭐ — IMPLEMENTED:
- Component → IR → Static Template + Dynamic Slots → state change → changed slots only.
- Component trees compile into compiler-layer IR.
- Static props and reactive dynamic bindings are separated.
- Renderer compiles the template without changing existing HTML output.
- Existing changed-prop/differential update machinery remains intact.
- Custom registered renderers remain compatible.
- IR + renderer regression coverage added.
- Full regression: 1172 passed, 1 skipped.

2.4 Event Loop Optimization ⭐ — IMPLEMENTED:
- Granian ASGI runtime supports explicit event-loop selection.
- uvloop is available through the optional performance dependency.
- asyncio compatibility is preserved.
- 5-run benchmark completed with 500 sequential HTTP requests per run.
- uvloop mean throughput: 765.803 req/s vs asyncio 724.777 req/s.
- Mean throughput gain: 5.66%.
- Mean latency reduction: 5.48%.
- Benchmark evidence saved to test/performance/granian_event_loop_benchmark_output.txt.
- Focused event-loop regression: 33 passed.
- Full regression: 1175 passed, 1 skipped.

2.5 Native Hot Path — OPTIONAL — COMPLETED:
Profile-first optimization was completed before considering native code.
- cProfile identified redundant per-render static/dynamic template compilation as the dominant renderer hot path.
- Removed the unused renderer-side compile_static_dynamic_template call and related state.
- Preserved the Phase 2.3 IR compiler implementation in pylage/ENGINE/core/ir.py.
- Post-optimization cProfile render workload dropped from 22.64s to 3.75s; remaining costs are genuine renderer/style/theme work.
- Focused performance regression: 6 passed.
- Full regression: 1175 passed, 1 skipped.
- git diff --check: clean.
- Rust/PyO3/Cython was not introduced because profiling did not justify a native extension; Python remains sufficient for the current V2 performance target.

Exit: Binary protocol + CSS dedup + Static/dynamic IR + event-loop optimization + performance regression suite.

## PHASE 3 — Security 🔴 CRITICAL
Goal: minimum security baseline for public network deployment.

- WebSocket Origin Validation — implemented for native WebSocket and ASGI runtime; disallowed browser origins are rejected with close code 1008.
- Message Size Limits — implemented for native WebSocket and ASGI connections; oversized payloads are rejected with close code 1009.
- WebSocket Rate Limiting via custom token bucket — implemented as a per-connection token bucket with configurable rate and burst; limit violations close with code 1013.
- WSS production support — Granian TLS certificate/key configuration implemented for HTTPS/WSS deployment; native WebSocketServer also supports an SSLContext.
- Input Sanitization Audit — Form, Text, Input, Textarea, user-controlled values, generated HTML, and media URL attributes audited; HTML escaping is preserved and unsafe media URL schemes are rejected.
- Session/Auth Tokens — stable opaque session tokens generated with secrets.token_urlsafe(32) are used; predictable connection IDs are not credentials; client connection logs redact session tokens.
- Database Safety Contract — audited current codebase; no database/SQL execution surface exists. Future database integration must use SQL plus bound parameters and never string interpolation.
- Dependency Security — pip-audit 2.10.1 completed with No known vulnerabilities found; audit tooling was kept out of project runtime dependencies.

Phase 3 Verification:
- Focused security regression: 86 passed in 1.30s.
- pip-audit: No known vulnerabilities found.
- All Phase 3 security requirements are implemented and covered by focused tests.

Exit: Origin + Limits + Rate limiting + WSS + Sanitization + Session security + Dependency audit — COMPLETE.

## PHASE 4 — Reactive Developer Experience 🟠
Goal: simple Python API for reactive power.

4.1 .bind(): state.bind(), two-way binding sugar.
4.2 ReactiveList: append, remove, insert, move, update + atomic deltas.
4.3 Cond: conditional reactive rendering.
4.4 For: reactive list rendering.
Dependency .bind() → ReactiveList → For.

Exit: .bind() + ReactiveList + Cond + For + reactive delta tests.

## PHASE 5 — File-Based Routing 🟠
Goal: real multi-page application framework.

Target:
pages/
├── dashboard.py
├── analytics.py
├── dashboard/
│   └── [user_id].py
└── settings/
    └── index.py

5.1 Router: startup scan → route table; no runtime filesystem scanning.
5.2 page() Contract: every page defines page(...); bare top-level component trees prohibited.
5.3 Dynamic Routes: /dashboard/42 → /dashboard/:user_id
5.4 Navigation: direct URL, back, forward, route transitions.
5.5 Session Safety: /user/1 in two users still independent state/component trees.
5.6 Backward Compatibility:
existing pl.run(app=...) continues;
new pl.run(pages_dir="pages").

Exit: Router + pages/ + dynamic routes + navigation + session isolation + legacy compatibility.

## PHASE 6 — Developer Experience 🟠
Goal: developer should not need runtime internals.

6.1 CLI: pylage run app.py, zero-config.
6.2 Hot Reload: save → detect → reload → browser update.
6.3 Error Handling: clean terminal traceback/useful context; readable browser error surface; no silent death.
6.4 Static Files: CSS, JS, images, assets; Content-Type, caching, compression.
6.5 Environment Configuration: PYLAGE_HOST, PYLAGE_PORT, PYLAGE_ENV, etc.
6.6 Structured Logging: session ID, component ID, event, error, lifecycle; scheduler error handling must preserve info.
6.7 /health.
6.8 CI: lint → pytest → build → security audit across supported Python versions.

Exit: CLI + Hot reload + Errors + Assets + Config + Logging + Health + CI.

## PHASE 7 — Deployment Readiness 🟠
Goal: deployable framework.

7.1 Docker: official Dockerfile.
7.2 Deployment Docs: Railway, Render, Fly.io, generic VPS.
7.3 Production command:
pylage run app.py --host 0.0.0.0 --port $PORT
7.4 Reverse proxy:
Browser → HTTPS → Reverse Proxy → WSS → PyLage
7.5 WebSocket Idle Timeout: docs explain heartbeat/idle timeout interaction.
7.6 Production Smoke Test:
open → connect → interact → reconnect → multi-user → health.

Exit: Docker + deployment guides + real deployment + WSS + health + production smoke test.

## PHASE 8 — Credibility, Benchmarks & Flagship Demos 🔴
Goal: technically complete and convincingly proven.

8.1 Benchmark Suite vs Streamlit, Reflex, NiceGUI:
startup, initial render, state update latency, payload size, update latency, memory, throughput where meaningful.
8.2 Reproducible methodology:
hardware, Python version, OS, framework versions, app code, commands, metrics, results.
8.3 Comparison table: PyLage vs Streamlit/Reflex/NiceGUI; real numbers only.
8.4 Flagship Demo ⭐⭐⭐: PyLage Operations Command Center
Dashboard, Analytics, Operations, Users, Data, Forms, System, Settings.
8.5 Additional Demos:
1 Operations dashboard
2 Todo/productivity app
3 Form-heavy application
4 Data/table application
8.6 Component coverage:
layout, navigation, forms, tables, metrics, overlays, themes, reactive state, routing, responsive behavior.

Exit: Benchmarks + reproducibility + comparison + flagship demo + 3–4 real apps.

## PHASE 8.5 — V2 Launch & Adoption Gate ⭐⭐⭐
Goal: code complete ≠ public launch ready.

8.5.1 5-Minute Quickstart: pip install → create app → pylage run → browser.
8.5.2 Documentation:
installation, quickstart, concepts, components, state, events, routing, deployment, security, performance, troubleshooting.
8.5.3 API Reference: every public API documented.
8.5.4 Migration Guide: V1 → V2, breaking changes, deprecated APIs, migration examples, compatibility notes.
8.5.5 Examples/Starters: dashboard, crud, forms, data-table, multi-page, authentication.
8.5.6 Troubleshooting: WebSocket disconnect, reverse proxy, WSS, session state, deployment, hot reload, assets, ports.
8.5.7 Compatibility Policy: Python versions, OS, browser, server configuration, V1 compatibility, V2 policy.
8.5.8 Security Policy: SECURITY.md + vulnerability reporting process.
8.5.9 CONTRIBUTING.md.
8.5.10 Issue templates: bug, feature, performance, security, documentation.
8.5.11 Changelog.
8.5.12 License clearly visible.

## PHASE 8.6 — Community + Sustainability Gate 💰
Engineering feature nahi; project sustainability.

GitHub Sponsors:
- –10 Supporter
- 5–50 Builder
- 00 Project Sponsor
- 00 Ecosystem Sponsor

00 examples: sponsor recognition, sponsor wall, roadmap discussions, early release access, priority consideration for reproducible issues.
00: prominent recognition, project/org logo, roadmap/community discussions, early access, priority consideration.
Important: sponsorship must NOT be feature-buying mechanism.

Buy Me a Coffee: casual one-time support.
Future revenue: free OSS + optional paid production support, migration, architecture consulting, training, enterprise assistance.

## PHASE 8.7 — Final Release Candidate Gate 🔴
Checklist:
- Full tests pass
- Performance regression pass
- Session isolation pass
- Reconnect pass
- Security audit pass
- CI green
- Docker works
- Real deployment works
- Benchmarks reproducible
- Flagship demo works
- Documentation complete
- Migration guide complete
- API docs complete
- Examples complete
- SECURITY.md
- CONTRIBUTING.md
- Changelog
- License
- Sponsor/support pages
- Release notes
- PyPI package verified

Flow: Phase 1 Runtime + Phase 2 Performance + Phase 3 Security + Phase 4 Reactive DX + Phase 5 Routing + Phase 6 DX + Phase 7 Deployment + Phase 8 Proof + Phase 8.5 Adoption + Phase 8.6 Sustainability → RC.

## PHASE 9 — V2.0 PUBLIC LAUNCH 🚀
Release v2.0.0:
- PyPI
- GitHub Release
- docs
- flagship demo
- benchmark report
- migration guide
- announcement

Positioning:
> PyLage — Simple, Ultrafast, Low-Latency Python UI

USP:
Python + server-driven + reactive + differential updates + low latency + no frontend build system.

Components are secondary.

## PHASE 10 — Post-Launch Stabilization 🟢
Monitor bugs, GitHub issues, performance regressions, deployment problems, browser compatibility, developer confusion, API pain points.

Releases 2.0.1, 2.0.2, 2.0.3...
Focus stability > new features.

## PHASE 11 — V2.x Differentiators 🟢
Original post-launch features moved here:
11.1 MCP
11.2 SSR / SEO
11.3 CDN JavaScript Component Bridge
11.4 Native DB Reactive Bindings
11.5 SDUI:
JSON Schema → PyLage Components → UI
11.6 WASM / Pyodide spike, experimental, not V2.0 blocker
11.7 Documentation expansion component-by-component.

## FINAL V2 ARCHITECTURE
Phase 0 Baseline
→ Phase 1 Runtime Foundation 🔴
→ Phase 2 Protocol/Performance 🔴
→ Phase 3 Security 🔴
→ Phase 4 Reactive DX
→ Phase 5 File Routing
→ Phase 6 Developer UX
→ Phase 7 Deployment
→ Phase 8 Proof & Demos
→ Phase 8.5 Adoption Gate ⭐
→ Phase 8.6 Sustainability Gate 💰
→ Phase 8.7 Release Candidate
→ Phase 9 V2.0 🚀
→ Phase 10 Stabilization
→ Phase 11 V2.x Differentiators

MCP, SSR, DB, SDUI, WASM remain V2.x branches.
