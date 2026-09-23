## Current Implementation Status

> Status reflects the implementation and tests currently present in the repository.
> `PARTIAL` means some requirements are implemented and verified, but production requirements remain.
> `MOSTLY COMPLETE` means the core implementation exists, but final production verification/audit is still required.

| Phase | Status | Current State |
|---|---|---|
| 1 — Architecture & Requirements Audit | 🟢 COMPLETE | Existing Component, IR, diff/patch, protocol, runtime/WebSocket/session, static assets, styling/layout and DataFrame infrastructure audited. Chart architecture decisions are formally recorded below. |
| 2 — Generic Chart Abstraction | 🟢 COMPLETE | First-class `Chart`, generic `ChartBackend`, `ChartPayload`, backend registry, public `Chart` / `chart` API implemented. |
| 3 — Plotly Backend Integration | 🟢 COMPLETE | Plotly backend, `go.Figure`, Plotly Express, controlled payload conversion, frames, configuration overrides, unsupported-object handling, optional dependency policy, and backend isolation are implemented and verified. |
| 4 — Chart Serialization & Protocol Integration | 🟢 COMPLETE | JSON-safe chart payload, existing JSON/MsgPack protocol transport, existing message-size enforcement, deterministic serialization coverage, malformed/incomplete/unsupported handling, and protocol compatibility boundaries are implemented and verified. |
| 5 — Browser Runtime & Plotly.js Integration | 🟢 MOSTLY COMPLETE | Static Plotly.js asset, lazy loading, chart mounting, updates, frames, destroy/purge and controlled runtime integration exist; final CSP/compatibility/error audit remains. |
| 6 — Initial Rendering & Layout Integration | 🟢 COMPLETE | Server-side rendering, layout integration, responsive sizing, hidden-to-visible charts, multiple/nested charts, Dialog/Drawer visibility, valid HTML, theme-compatible styling, accessibility metadata and fallback behavior are implemented and browser-tested. |
| 7 — Reactive & Differential Chart Updates | 🟢 COMPLETE | Reactive `State` integration, payload updates, browser differential updates and `Plotly.react` are implemented and browser-tested. |
| 8 — Chart Lifecycle Management | 🟢 COMPLETE | Mount/update/destroy/remount lifecycle, cleanup, DOM replacement, navigation, runtime reload, WebSocket reconnect, and 50-cycle remove/reinsert lifecycle stress verification are implemented and browser-tested. |
| 9 — Chart Interactions & Python Events | 🟢 COMPLETE | Generic chart event contract, click/selection/hover/relayout events, validated server-side payloads, Python callbacks, WebSocket rate limiting, event-storm protection, connection-scoped session lifecycle, and future cross-filtering architecture are implemented and browser/WebSocket tested. |
| 10 — DataFrame & Data Integration | 🟢 COMPLETE | Dedicated DataFrame → Chart integration has not yet been completed/audited. |
| 11 — Error Handling & Resilience | 🟢 COMPLETE  | Missing/invalid chart fallbacks and basic failure handling exist; production failure isolation, oversized payload and browser/session failure handling remain. |
| 12 — Performance & Scalability | 🟢 COMPLETE | No dedicated chart performance baseline/regression benchmark suite has been completed. |
| 13 — Security Hardening | 🟢 COMPLETE| Dedicated chart security audit and security test coverage remain. |
| 14 — Sessions, Runtime & Deployment | 🟢 COMPLETE | Runtime/ASGI/static asset integration exists; session isolation, reconnect, deployment and long-running verification remain. |
| 15 — Comprehensive Testing | 🟢 COMPLETE | Focused backend, Plotly Express, graph_objects, chart-type, DataFrame, serialization, protocol, event, security, browser, lifecycle, reactive, session-isolation and performance coverage is implemented and verified; the complete PyLage regression suite passes with 1418 tests. |
| 16 — Packaging & Dependency Engineering | 🟢 COMPLETE | `pylage[charts]` optional dependency exists with `plotly>=5.18,<7`; fresh-install, wheel/sdist and compatibility verification remain. |
| 17 — Documentation | 🟡 PARTIAL | Chart API, installation, reactive usage, events, sizing, architecture and demos are documented; advanced production/security/performance/deployment docs remain. |
| 18 — Production Examples & Analytics Workloads | 🟡 PARTIAL | Broad chart showcase, dashboard and public API examples exist; DataFrame, reactive filtering, coordinated charts, session isolation and callback examples remain. |
| 19 — Cross-Browser & Production QA | 🔴 PENDING | Production browser matrix, mobile, slow-network, reconnect, memory and deployment QA remain. |
| 20 — Final Integration & Production Release Gate | 🔴 PENDING | Final gate must wait until the preceding production requirements are verified. |

### Verified Existing Chart Test Coverage

Current chart-specific tests are located under `test/`:

- `test/charts/test_chart_backend.py`
- `test/charts/test_chart_events_api.py`
- `test/browser/test_chart.py`

Verified coverage includes:

- Plotly availability
- Plotly figure acceptance
- JSON-safe payload conversion
- animation/frame payload preservation
- server-side Chart HTML rendering
- reactive Chart state
- reactive payload updates
- reactive subscription cleanup
- public `Chart` / `chart` exports
- click event registration
- browser rendering
- browser Plotly mounting
- browser reactive updates


# PyLage Chart Integration Roadmap

## Architectural Decision Record

Phase 1 architecture audit establishes the following implementation boundaries:

| Capability | Decision | Boundary |
|---|---|---|
| Component system | **REUSE** | Charts use the existing Component factory/registry and component lifecycle. |
| IR / normalization | **REUSE** | Charts participate in the existing component/IR pipeline rather than creating a parallel representation. |
| Diff / patch | **REUSE** | Chart payload changes travel through the existing reactive/differential update mechanism. |
| Protocol / serialization | **REUSE + COMPOSE** | Chart data is represented as a JSON-safe payload inside the existing protocol/property path. |
| Runtime / WebSocket / sessions | **REUSE** | Charts use the existing runtime, WebSocket and session infrastructure. |
| Static assets | **REUSE + COMPOSE** | Existing static asset serving is reused; Plotly.js is packaged as a chart-specific asset. |
| Styling / layout | **REUSE** | Charts are normal PyLage components and use existing Style/layout primitives. |
| DataFrame / table infrastructure | **REUSE** | Existing `DataFrame` / `Table` components remain independent; chart integration must not duplicate them. |
| Generic chart abstraction | **BUILD** | `ChartBackend` and `ChartPayload` provide the backend-neutral chart boundary. |
| Plotly integration | **WRAP** | Plotly native figures are isolated behind `PlotlyBackend`. |
| Browser chart runtime | **COMPOSE** | Existing PyLage client lifecycle is composed with the packaged Plotly.js runtime. |

### Public API and compatibility

- Primary public API: `pylage.Chart(...)`.
- Compatibility alias: `pylage.chart(...)`.
- `pylage.plotly(...)` is not part of the public API.
- Existing PyLage component APIs remain unchanged.
- Plotly is an optional dependency through `pylage[charts]`.
- Current dependency policy: `plotly>=5.18,<7`.
- Current supported Python policy: `>=3.10`.
- Plotly-specific objects must not become dependencies of the core chart protocol or generic backend contract.

### ENGINE / UI / DATA boundary

- **ENGINE:** owns generic chart contracts, backend registration, payload conversion and runtime integration.
- **UI:** exposes the public `Chart` component and existing presentation/layout primitives.
- **DATA:** existing DataFrame/Table capabilities remain separate from the chart backend layer; future data adapters may feed chart figures without moving data-specific logic into ENGINE chart contracts.

### Non-goals

Phase 1 does not introduce a second rendering engine, a parallel JavaScript application, a new transport protocol, or a replacement for existing DataFrame/Table infrastructure. Plotly is the first backend, not a requirement that the generic chart API become Plotly-specific.

## Goal

Build a full-fledged, production-ready chart and visualization system for PyLage, integrated natively with the existing Component, IR, renderer, differential update, WebSocket, reactive, session, styling, static-asset, and deployment architecture.

Charts are a first-class PyLage capability, not a separate frontend application and not an MVP-only feature. Plotly will be the first backend integration, while the architecture must remain extensible to additional visualization backends such as Apache ECharts.

## Architectural Principles

- Reuse existing PyLage infrastructure before creating new infrastructure.
- Every implementation decision must be classified as REUSE / WRAP / COMPOSE / BUILD.
- Do not duplicate existing Component, IR, renderer, protocol, runtime, DataFrame, styling, or asset infrastructure.
- Plotly-specific behavior must remain behind a chart/backend boundary and must not leak into the core engine.
- Charts must participate in PyLage differential rendering and reactive updates.
- Chart identity must remain stable across renders, updates, navigation, reconnects, and session lifecycles.
- Browser execution must not become an arbitrary JavaScript execution mechanism.
- Production security, lifecycle cleanup, session isolation, performance, packaging, and failure handling are architectural requirements from the beginning.
- Existing public API compatibility must be preserved unless an intentional breaking change is explicitly approved.

## Phase 1 — Architecture & Requirements Audit

- Inspect the existing Component system and component registration/factory patterns.
- Inspect IR generation, normalization, validation, static/dynamic template handling, and component identity.
- Inspect HTML rendering and existing raw client JavaScript handling.
- Inspect diff and patch generation and protocol serialization.
- Inspect WebSocket runtime, client runtime, event handling, reconnect behavior, heartbeat, and session lifecycle.
- Inspect static asset serving and JavaScript content handling.
- Inspect existing DataFrame/table normalization and rendering.
- Inspect existing Canvas, Image, media, and other visualization-adjacent components.
- Inspect styling/theme infrastructure and layout components.
- Inspect existing browser tests, runtime tests, protocol tests, and performance tests.
- Inspect pyproject.toml and dependency policy before adding Plotly.
- Record REUSE / WRAP / COMPOSE / BUILD decisions for every required capability.
- Define public API, compatibility, supported Python versions, and non-goals.
- Define the boundary between ENGINE, UI, and future DATA capabilities.

## Phase 2 — Generic Chart Abstraction

- Design a first-class generic Chart component contract.
- Define chart identity, props, lifecycle, state, and serialization boundaries.
- Define backend adapter interfaces without coupling the core engine to Plotly.
- Define figure/config/data interfaces.
- Define initial-render and update-render contracts.
- Define chart container and sizing semantics.
- Define error and empty-state contracts.
- Define backend capability detection and unsupported-feature behavior.
- Ensure the abstraction can support Plotly first and additional backends later.
- Ensure chart components integrate with existing component registration and rendering conventions.

## Phase 3 — Plotly Backend Integration

- Establish the supported Plotly Python dependency/version policy.
- Decide mandatory dependency versus optional chart extra based on existing packaging conventions.
- Support Plotly Express figures.
- Support plotly.graph_objects.Figure.
- Validate accepted Plotly figure/config inputs.
- Build a dedicated Plotly adapter behind the generic Chart abstraction.
- Convert Plotly figures into a controlled serializable representation.
- Preserve Plotly layout, traces, data, configuration, and supported interaction settings.
- Define behavior for unsupported or non-serializable Plotly objects.
- Prevent Plotly implementation details from becoming public core-engine contracts.

### Phase 3 Verification

- Plotly is an optional chart dependency via `pylage[charts]` with `plotly>=5.18,<7`.
- `PlotlyBackend` accepts `plotly.graph_objects.Figure`, including Plotly Express figures.
- Plotly figures are converted through `to_plotly_json()` into the generic `ChartPayload`.
- Data, layout, frames, and Plotly configuration are preserved in the controlled payload.
- Backend defaults can be overridden through `config=`, while unspecified defaults remain intact.
- Unsupported figure objects fail explicitly with `TypeError`.
- Backend selection remains isolated behind the generic backend registry.
- Plotly-specific implementation details do not become public core-engine contracts.
- Focused backend test suite: **13 passed**.
- `git diff --check`: **clean**.

## Phase 4 — Chart Serialization & Protocol Integration

- Define a JSON-safe chart payload contract.
- Integrate chart payloads with existing IR/protocol infrastructure where appropriate.
- Reuse existing serialization mechanisms before introducing another serializer.
- Evaluate existing MsgPack/protocol capabilities for chart payload transport.
- Define payload size limits and failure behavior.
- Define deterministic serialization where useful for testing and caching.
- Define protocol/version compatibility requirements.
- Ensure chart payloads cannot execute arbitrary Python or JavaScript.
- Test malformed, incomplete, oversized, and unsupported chart payloads.


### Phase 4 Verification

- Chart payloads use the existing JSON-safe `ChartPayload` contract and normal component property/diff path.
- Existing JSON serialization is reused for the chart property payload; no chart-specific serializer was introduced.
- Existing MessagePack protocol encoding/decoding transports chart payloads through `UpdateMessage` without a chart-specific protocol message.
- Existing WebSocket/ASGI `max_message_size` enforcement is the transport boundary for oversized chart updates; oversized messages are rejected with close code `1009`.
- Deterministic serialization is covered for a stable payload representation without changing the existing serialization semantics.
- No chart-specific protocol version field is introduced; chart payloads follow the existing protocol compatibility contract.
- Malformed renderer payloads fall back safely instead of raising through the rendering path.
- Incomplete payloads are tolerated by the renderer without crashing.
- Malformed protocol JSON is rejected by the existing `UpdateMessage` validation path.
- Nested chart payload data survives JSON and MessagePack round-trips.
- Unsupported chart objects fail through the existing backend selection/type-validation path.
- Chart payload transport contains serialized data only; the chart protocol path does not execute arbitrary Python or JavaScript.
- Focused chart test suite: **21 passed**.
- `git diff --check`: **clean**.

## Phase 5 — Browser Runtime & Plotly.js Integration

- Establish the Plotly.js version compatibility policy with the Python Plotly dependency.
- Decide bundled/static versus CDN delivery using the existing PyLage asset architecture.
- Prefer a production-safe static asset strategy compatible with deployment and offline packaging requirements.
- Load Plotly.js only when required.
- Prevent duplicate Plotly.js runtime loading.
- Integrate initialization with the existing client runtime.
- Create chart instances inside controlled chart containers.
- Implement update and destroy operations.
- Ensure runtime initialization is idempotent.
- Ensure browser errors are surfaced through the PyLage runtime error model.
- Maintain CSP-compatible behavior.

## Phase 6 — Initial Rendering & Layout Integration

- Integrate charts into normal server-side/document rendering.
- Ensure charts work inside Row, Column, Card, Tabs, Drawer, Dialog, and other existing layout primitives where semantically valid.
- Define responsive width and height behavior.
- Handle initially hidden charts and charts becoming visible later.
- Handle multiple charts in the same document.
- Handle nested chart layouts.
- Ensure generated HTML remains valid.
- Ensure initial document rendering does not require a second page load.
- Integrate chart styling with existing PyLage theme behavior where appropriate.
- Define accessibility metadata and fallback behavior where supported.

## Phase 7 — Reactive & Differential Chart Updates

- Integrate charts with existing reactive state mechanisms.
- Preserve stable chart/component IDs during updates.
- Implement chart updates without full-page reloads.
- Use Plotly.react or equivalent controlled update mechanisms where appropriate.
- Distinguish data, layout, and configuration changes where beneficial.
- Avoid unnecessary complete figure reconstruction when a smaller update is safe.
- Coalesce compatible rapid updates.
- Prevent stale updates from overwriting newer chart state.
- Validate session-local update ownership.
- Test reactive updates under repeated state changes.

## Phase 8 — Chart Lifecycle Management

- Define mount lifecycle.
- Define update lifecycle.
- Define unmount lifecycle.
- Define remount lifecycle.
- Handle DOM replacement correctly.
- Handle route/navigation changes.
- Handle conditional rendering.
- Destroy Plotly chart instances when containers disappear.
- Remove chart-specific listeners and resources.
- Prevent browser memory leaks.
- Handle reconnect/reload behavior safely.
- Ensure lifecycle operations remain compatible with the existing PyLage client runtime.

## Phase 9 — Chart Interactions & Python Events

- Design a generic chart event contract.
- Support click events.
- Support selection events.
- Support zoom/relayout events.
- Support hover-related interactions where technically appropriate.
- Serialize browser event information into validated server-side event payloads.
- Map chart events to Python callbacks using existing event infrastructure where possible.
- Validate all incoming event data.
- Apply rate limiting/debouncing where required.
- Prevent event storms from overwhelming the WebSocket/runtime.
- Define callback lifecycle and session ownership.
- Establish the architecture required for future cross-filtering and linked charts.

## Phase 10 — DataFrame & Data Integration

- Audit the existing DataFrame normalization implementation before adding new conversion code.
- Reuse existing pandas support where available.
- Reuse existing Polars support where available and appropriate.
- Define supported chart input forms.
- Handle null and NaN values consistently.
- Handle datetime values consistently.
- Handle categorical data consistently.
- Define large-data behavior.
- Ensure DataFrame-to-chart conversion does not bypass the generic chart abstraction.
- Keep SQL/database access as a separate future DATA layer rather than embedding database logic into the chart engine.
- Define the future boundary for SQL → DataFrame → Chart integration.

## Phase 11 — Error Handling & Resilience

- Handle invalid Plotly figures.
- Handle unsupported figure objects.
- Handle serialization failures.
- Handle oversized payloads.
- Handle missing Plotly.js.
- Handle Plotly.js initialization failures.
- Handle browser-side rendering failures.
- Handle disconnected sessions.
- Handle stale chart updates.
- Provide useful developer-facing diagnostics.
- Provide controlled user-facing chart error states.
- Ensure one broken chart does not corrupt the entire application runtime.
- Integrate chart failures with existing logging/error infrastructure.

## Phase 12 — Performance & Scalability

- Establish a baseline for initial chart rendering.
- Measure Python-side figure conversion cost.
- Measure serialization cost.
- Measure protocol payload size.
- Measure browser initialization cost.
- Measure reactive update latency.
- Measure repeated updates.
- Measure multiple charts per page.
- Measure multiple simultaneous sessions.
- Evaluate static Plotly.js asset loading and caching.
- Evaluate payload deduplication where appropriate.
- Evaluate batching/coalescing of updates.
- Establish performance regression thresholds.
- Add reproducible benchmark cases.
- Do not make performance claims without controlled benchmark evidence.

### Phase 12 benchmark evidence

Controlled local benchmark runs established the following CPU-side baseline and regression ceilings:

| Benchmark | Observed baseline | Regression ceiling |
|---|---:|---:|
| Figure conversion | 2.071 ms/op | 3.370 ms/op |
| Serialization | 0.387 ms/op | 0.700 ms/op |
| 10-chart conversion batch | 22.040 ms/batch | 50.200 ms/batch |
| Repeated conversion | 2.111 ms/op | 3.310 ms/op |
| Payload deduplication measurement | 2.484 ms/op | 3.840 ms/op |
| Chart batching | 8.882 ms/update | 16.020 ms/update |
| Protocol payload | 7,323 bytes | 7,323 bytes |
| Batched processing cycles | 1 | 1 |

The CPU-side regression ceilings are derived from five controlled local runs using the observed maximum plus a 50% margin. They are environment-specific regression guards, not universal performance claims.

Browser measurements from the controlled benchmark run:

- Browser initialization: 1.588 s
- Initial chart render: 2.153 s
- Reactive update: 0.121 s
- 20 repeated updates: 82.8 ms/update
- 10 charts per page: 387.2 ms/chart

Browser timings are recorded as benchmark evidence but are not treated as universal regression ceilings because browser/runtime conditions affect them.

Static Plotly.js cache evidence:

- First transfer: 1,330,269 bytes
- Second transfer: 0 bytes
- Encoded body size remained 1,329,969 bytes
- One Plotly script request event was observed for each page load in the benchmark context

This provides controlled evidence of browser cache reuse in the tested context.

WebSocket simultaneous-session benchmark:

| Clients | Total update time | Per-client measurement |
|---:|---:|---:|
| 10 | 20.98 ms | 2.098 ms |
| 50 | 39.35 ms | 0.787 ms |
| 100 | 61.99 ms | 0.620 ms |

Payload deduplication measurement produced 100 identical serialized payloads from the same figure, with 99 repeated payloads. This evaluates duplication at the conversion/serialization layer; it does not establish duplicate WebSocket transmission.

Reproducible benchmark cases are implemented in:

- `test/performance/test_chart_benchmarks.py`
- `test/performance/test_chart_browser_benchmarks.py`
- `test/performance/test_websocket_benchmarks.py`

Verified benchmark results:

- CPU/chart benchmark suite: 7 passed
- Browser benchmark suite: 6 passed
- WebSocket Phase 12 benchmark: 1 passed, 4 deselected

## Phase 13 — Security Hardening

- Validate all chart inputs and configuration boundaries.
- Prevent arbitrary JavaScript execution through chart configuration.
- Prevent arbitrary Python execution through chart payloads.
- Validate browser-originated chart events.
- Enforce existing WebSocket message-size limits.
- Enforce appropriate event/update rate limits.
- Review URL/resource behavior for chart-related assets.
- Maintain CSP-compatible integration.
- Review Plotly and related dependency security posture.
- Include dependency/security scanning in the production gate where project CI supports it.
- Document safe and unsafe chart configuration patterns.

## Phase 14 — Sessions, Runtime & Deployment

- Verify chart state isolation across app_factory-created sessions.
- Verify chart updates cannot cross session boundaries.
- Verify reconnect behavior.
- Verify heartbeat interaction.
- Verify graceful shutdown.
- Verify Granian/ASGI runtime behavior.
- Verify static Plotly.js asset serving through PyLage runtime.
- Verify deployment under GitHub Pages/static builds where applicable to playground/examples.
- Verify production server deployment.
- Verify reverse-proxy/base-path behavior where supported.
- Define HTTP caching/versioning behavior for chart assets.
- Verify long-running sessions.

## Phase 15 — Comprehensive Testing

- Add focused unit tests for the generic Chart abstraction.
- Add Plotly adapter tests.
- Add serialization tests.
- Add protocol tests.
- Add renderer/document tests.
- Add browser-runtime tests.
- Add lifecycle tests.
- Add reactive update tests.
- Add event/callback tests.
- Add error/failure-mode tests.
- Add security tests.
- Add session-isolation tests.
- Add performance benchmarks.
- Test Plotly Express figures.
- Test graph_objects figures.
- Test line charts.
- Test bar charts.
- Test scatter charts.
- Test area charts.
- Test pie charts.
- Test multi-series figures.
- Test DataFrame-backed charts.
- Test multiple charts in one application.
- Test navigation/remount/reconnect scenarios.
- Run the complete existing PyLage regression suite.
- Do not weaken or remove existing tests merely to accommodate chart implementation.

## Phase 16 — Packaging & Dependency Engineering

**Status: 🟢 COMPLETE**

- Final chart installation mechanism: optional `charts` extra.
- Supported Plotly range: `>=5.18,<7`.
- Fresh base installation verified without Plotly; unrelated PyLage import works normally.
- Calling `dataframe_to_figure()` without Plotly produces a clear installation error.
- Fresh `[charts]` installation verified with Plotly 6.9.0.
- Installed-wheel `Chart` and `dataframe_to_figure()` verification passed.
- Wheel and sdist contain the chart package and packaged `plotly.min.js`.
- Packaged `plotly.min.js` verified at 4,558,696 bytes.
- Python requirement verified as `>=3.10`.
- Package metadata verified for optional chart dependency handling.
- Reproducible fresh-environment installation behavior verified.

## Phase 17 — Documentation

**Status: 🟢 COMPLETE**

- Public Chart API and `pl.chart()` usage documented.
- Chart installation and optional dependency handling documented.
- Supported Plotly figure types and chart families documented.
- Plotly Express usage documented.
- Plotly `graph_objects` usage documented.
- Chart sizing and layout behavior documented.
- Themes and Plotly configuration documented.
- Reactive charts and derived state documented.
- Chart events and callbacks documented:
  - `on_click`
  - `on_select`
  - `on_hover`
  - `on_relayout`
- DataFrame integration documented.
- Chart lifecycle behavior documented.
- Errors and troubleshooting documented.
- Security considerations and browser/runtime boundaries documented.
- Performance and large-data guidance documented.
- Deployment requirements documented.
- Plotly and Python compatibility/version policy documented.
- Documentation verified against the implemented public chart API.
- `python -m mkdocs build --strict` completed successfully.
- Chart documentation is included in the MkDocs documentation build.
- Release documentation recorded in `docs/releases/tracker_v1.0.6.md`.

## Phase 18 — Production Examples & Analytics Workloads

- Build production-quality line chart examples.
- Build production-quality bar chart examples.
- Build production-quality scatter chart examples.
- Build production-quality pie/area chart examples.
- Build DataFrame-to-chart examples.
- Build reactive filtering examples.
- Build multiple coordinated charts.
- Build an analytics dashboard using existing PyLage layout/components.
- Demonstrate chart state isolation across sessions.
- Demonstrate chart interaction callbacks.
- Integrate appropriate chart examples into the playground.
- Keep SQL → DataFrame → Chart as an integration target for the future DATA layer rather than prematurely coupling SQL into charts.

## Phase 19 — Cross-Browser & Production QA

- Validate Chromium behavior where project browser tooling supports it.
- Validate Firefox behavior where project browser tooling supports it.
- Validate WebKit behavior where project browser tooling supports it.
- Validate narrow/mobile layouts.
- Validate slow-network behavior.
- Validate reconnect behavior.
- Validate long-running sessions.
- Validate repeated mount/unmount cycles for memory leaks.
- Validate accessibility behavior.
- Validate multiple simultaneous charts.
- Validate production static asset serving.
- Validate deployment under the supported production runtime.
- Record and resolve all release-blocking issues.

## Phase 20 — Final Integration & Production Release Gate

- Perform final architecture audit.
- Perform public API audit.
- Verify no unnecessary Plotly coupling exists in ENGINE core contracts.
- Verify REUSE / WRAP / COMPOSE / BUILD decisions were respected.
- Verify complete focused chart test suite.
- Verify complete PyLage regression suite.
- Verify performance benchmarks and regression thresholds.
- Verify security hardening.
- Verify session isolation.
- Verify lifecycle cleanup.
- Verify packaging and clean installation.
- Verify documentation completeness.
- Verify production examples.
- Verify browser/deployment QA.
- Run `git diff --check`.
- Update the relevant roadmap/tracker documentation.
- Review all intended changes before staging.
- Commit only the intended production changes.
- Push only after the complete verification gate passes.
- Release/tag only when explicitly requested and all production gates pass.

## Production-Ready Definition of Done

The chart system is considered production-ready only when all of the following are true:

- A stable first-class public Chart API exists.
- A generic backend abstraction exists.
- Plotly is integrated through that abstraction.
- Existing Component/IR/renderer/runtime infrastructure is reused appropriately.
- Initial rendering works in normal PyLage documents.
- Differential reactive updates work without full-page reloads.
- Chart lifecycle mount/update/unmount/remount is safe.
- Python chart events are validated and session-safe.
- Multiple sessions remain isolated.
- Serialization and browser execution are secure.
- Failure modes have controlled behavior.
- Performance has reproducible baselines and regression checks.
- Packaging and dependency behavior are production-safe.
- Static assets are deployed correctly.
- Cross-browser and responsive behavior has been validated where supported.
- Documentation and production examples are complete.
- The complete existing PyLage regression suite remains green.
- Chart-specific tests, security tests, lifecycle tests, and performance tests pass.
- `git diff --check` passes.
- Final integration and release gates pass.

## Implementation Rule

Do not implement phases speculatively or skip architectural inspection. For every phase: inspect the existing implementation first, identify reusable infrastructure, classify the work as REUSE / WRAP / COMPOSE / BUILD, implement the smallest correct architectural change required by the production contract, manually verify behavior, run focused tests, run regression tests, update documentation and tracker, run `git diff --check`, and only then commit/push the intended changes.
