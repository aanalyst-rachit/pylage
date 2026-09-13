# Changelog


## 1.0.3 — 2026-09-13

PyLage 1.0.3 is the public release following completion of the Phase 0–7 V2 implementation scope. This release establishes the production-oriented PyLage runtime, reactive developer experience, file-based routing, deployment tooling, security baseline, and public documentation.

### Added

- Added the ASGI runtime adapter with Granian integration for HTTP and WebSocket applications.
- Added per-session state isolation and session resumption across WebSocket reconnects.
- Added the pluggable in-memory SessionStore with TTL-based session expiration and lifecycle cleanup.
- Added configurable WebSocket heartbeat and dead-connection detection.
- Added MessagePack binary transport with differential updates and reduced protocol overhead.
- Added CSS deduplication and compiler-layer static/dynamic template IR support.
- Added reactive state.bind() two-way binding support.
- Added ReactiveList with reactive append, remove, insert, move, update, and atomic delta operations.
- Added cond for conditional reactive rendering and for_each for reactive list rendering.
- Added file-based routing with page contracts, dynamic routes, navigation, and session-safe route state.
- Added the zero-configuration pylage run app.py developer workflow, hot reload, environment configuration, structured logging, and /health.
- Added static asset serving with appropriate content types, caching, and compression support.
- Added production deployment support including Docker, HTTPS/WSS configuration, reverse-proxy guidance, and production smoke verification.
- Added the public PyLage playground and release documentation covering the Phase 0–7 capabilities.

### Security

- Added WebSocket Origin validation for native and ASGI runtimes.
- Added WebSocket message-size limits and per-connection token-bucket rate limiting.
- Added WSS/TLS support for production deployment.
- Hardened HTML/input handling and rejected unsafe media URL schemes.
- Replaced predictable connection identifiers as credentials with secure opaque session tokens.
- Completed the dependency security audit with no known vulnerabilities reported by pip-audit.

### Performance & Reliability

- Added explicit event-loop selection with optional uvloop support while preserving asyncio compatibility.
- Removed redundant renderer-side static/dynamic template compilation from the render hot path.
- Preserved the compiler IR implementation while reducing renderer workload substantially in profiling.
- Added focused regression coverage for runtime migration, protocol behavior, reactive updates, routing, security, and deployment paths.

### Public API

- Stabilized the public API around lowercase component and helper names.
- Added public reactive helpers including state, reactive_list, derived, cond, and for_each.
- Added public layout, component, pattern, recipe, theme, styling, and navigation helpers covered by the release API surface.
- Preserved public custom theme injection through set_theme.

### Breaking Changes

- The public API is standardized around lowercase component and helper names. Projects using legacy uppercase public aliases should migrate to the lowercase API.
- Internal implementation packages such as pylage.ENGINE and pylage.UI are not part of the public root namespace and should be imported through their canonical internal paths only when working on PyLage internals.
- No additional Phase 0–7 breaking changes are introduced beyond the public API stabilization described above.

### Upgrade & Migration Notes

- Update application imports to the current lowercase public API before upgrading.
- Existing applications using pl.run(app=...) remain supported.
- Applications using the file-based router may adopt pl.run(pages_dir="pages") without changing the legacy application entry point.
- Review deployment configuration when moving to the production ASGI/Granian runtime, particularly host, port, HTTPS/WSS, reverse-proxy, and environment settings.

### Phase 0–7 Release Summary

- Phase 0 established the frozen V1 baseline, V2 architecture direction, regression baseline, and browser playground foundation.
- Phase 1 completed the production-oriented ASGI/session runtime migration.
- Phase 2 completed the protocol, rendering, CSS, event-loop, and performance optimizations.
- Phase 3 established the minimum public-network security baseline.
- Phase 4 delivered the reactive Python developer experience.
- Phase 5 delivered file-based routing and navigation.
- Phase 6 delivered the zero-config developer workflow and operational tooling.
- Phase 7 completed deployment readiness and production smoke verification.

### Verification

- Phase 0–7 implementation work and release-preparation verification completed.
- Security regression suite and dependency audit completed.
- Runtime, reactive, routing, deployment, and browser verification completed during the Phase 0–7 release preparation.



## 1.0.2 — 2026-09-08

- Corrected the published package metadata so the PyPI project description is generated from the current README.md.


## 1.0.1 — 2026-09-08

### Added

- Consolidated the development history of the PyLage, pylage-ui, pylage_layout, and pylage-ui-speed repositories into the canonical pylage repository.
- Restored the PyPI packaging configuration required for the canonical pylage package.

### Changed

- Stabilized the public PyLage API around lowercase component and helper names.
- Updated the package and public UI version to 1.0.1.
- Updated release-facing demo version labels to 1.0.1.
- Removed legacy test files from the former pylage-ui repository that were no longer compatible with the stabilized public API.

### Verification

- Full test suite: 1090 passed.
- Release verification suite: passed.
- Current release test tree matches the final pylage-ui-speed test tree: 251 Python test files.
- Working tree and release diff checks passed before release preparation.

## 1.0.0

Initial packaged PyLage release.
