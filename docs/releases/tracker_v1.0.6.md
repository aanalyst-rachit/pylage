# PyLage v1.0.6 Release Tracker

## Purpose

v1.0.6 records the completion of the PyLage chart integration phase following
the v1.0.5 runtime baseline, including the native high-level `pl.chart()` data
API, chart integration documentation, and release verification.

## Chart Integration

### Phase 17 — Documentation and Native Chart API

**Status: 🟢 COMPLETE**

The public PyLage Chart API and chart integration behavior are documented in
`docs/component/chart.md`.

The release includes both the existing advanced Plotly Figure API and the
native high-level tabular-data API:

    pl.chart(
        data=df,
        type="bar",
        x="month",
        y="sales",
    )

The native data API supports:

- `line`
- `bar`
- `scatter`
- `area`
- `pie`
- Multiple `y` columns for supported Cartesian charts.
- `color` grouping for supported Cartesian charts.
- `size` for scatter charts.
- `name`, `x_label`, and `y_label`.

The advanced Plotly Figure API remains supported through:

    pl.chart(fig)

The documentation covers:

- Public `Chart` / `pl.chart()` usage.
- Chart installation and optional dependency handling.
- Supported Plotly figure types and chart families.
- Plotly Express usage.
- Plotly `graph_objects` usage.
- Chart sizing and layout behavior.
- Themes and Plotly configuration.
- Reactive charts and derived state.
- Chart events and callbacks:
  - `on_click`
  - `on_select`
  - `on_hover`
  - `on_relayout`
- DataFrame and tabular-data integration.
- Native chart data conversion and validation.
- Advanced Plotly Figure integration.
- Chart lifecycle behavior.
- Errors and troubleshooting.
- Security considerations and browser/runtime boundaries.
- Performance considerations and large-data guidance.
- Deployment requirements.
- Plotly and Python compatibility/version policy.

### Packaging and Dependency Documentation

Chart installation is documented using the optional `charts` dependency:

    pip install "pylage[charts]"

Direct Plotly installation is also documented:

    pip install plotly

The supported Plotly dependency range is:

    plotly>=5.18,<7

Plotly remains optional for applications that do not use charts.

### Runtime Asset Documentation

The documentation records the packaged Plotly browser runtime asset:

    /_pylage/assets/plotly.min.js

The deployment documentation explains that chart deployments require both the
Python Plotly dependency and the packaged browser runtime asset.

### Verification

- `python -m mkdocs build --strict` completed successfully.
- Chart documentation is included in the MkDocs documentation build.
- Required Phase 17 documentation topics were verified in
  `docs/component/chart.md`.
- Native Chart API tests passed.
- Existing DataFrame, backend, and chart-event tests passed.
- Combined chart verification result: **59 passed**.
- Documentation and tests were checked against the implemented public Chart
  API, Plotly backend behavior, native DataFrame integration, events,
  lifecycle, security, performance, deployment, and compatibility behavior.

## Current Native API Boundary

The native `data=` API converts the supplied tabular data when the chart is
created. Reactive updates through a native `data=State(...)` value are not yet
implemented.

The advanced Plotly Figure API continues to support the existing reactive
Figure/state lifecycle.

## Release Boundary

v1.0.6 records completion of the native chart API integration, chart
documentation, and verification.

Production examples, broader analytics workloads, cross-browser production QA,
native data reactivity, and the final production release gate remain tracked
by subsequent chart integration phases.
