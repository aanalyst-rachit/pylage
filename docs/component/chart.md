# Chart

Interactive charts powered by Plotly, integrated with PyLage reactive state and differential updates.

## Install

    pip install "pylage[charts]"
    # or
    pip install plotly

## Basic usage

The high-level `pl.chart()` API accepts tabular data directly. This is the
recommended API when the chart only needs data columns and common chart
options.

    import pandas as pd
    import pylage as pl

    df = pd.DataFrame({
        "month": ["Jan", "Feb", "Mar"],
        "sales": [10, 20, 15],
    })

    app = pl.column(
        pl.chart(
            data=df,
            type="bar",
            x="month",
            y="sales",
            height=400,
        ),
    )

    pl.run(app)

## Native data API

The native API is designed to provide a simple chart interface without
requiring callers to construct a Plotly Figure.

    pl.chart(
        data=df,
        type="line",
        x="month",
        y="sales",
    )

Supported chart types are:

- `line`
- `bar`
- `scatter`
- `area`
- `pie`

### Multiple series

Pass multiple column names in `y` for Cartesian charts:

    pl.chart(
        data=df,
        type="line",
        x="month",
        y=["sales", "profit"],
    )

Each column becomes a separate chart trace.

### Color grouping

Use `color` to create separate traces for categories:

    pl.chart(
        data=df,
        type="line",
        x="month",
        y="sales",
        color="city",
    )

### Scatter marker size

For scatter charts, `size` can map marker size to a data column:

    pl.chart(
        data=df,
        type="scatter",
        x="age",
        y="income",
        size="company_size",
    )

### Labels and trace names

Use `x_label` and `y_label` to provide axis labels:

    pl.chart(
        data=df,
        type="line",
        x="month",
        y="sales",
        x_label="Month",
        y_label="Sales",
    )

Use `name` to provide a trace name when appropriate:

    pl.chart(
        data=df,
        type="bar",
        x="category",
        y="value",
        name="Revenue",
    )

### Accepted tabular data

The native data API accepts:

- pandas DataFrames
- Polars DataFrames
- Polars LazyFrames
- lists of record dictionaries
- column mappings where each key maps to a sequence

For example:

    pl.chart(
        data=[
            {"month": "Jan", "sales": 10},
            {"month": "Feb", "sales": 20},
            {"month": "Mar", "sales": 15},
        ],
        type="bar",
        x="month",
        y="sales",
    )

The native API converts supported tabular data into the internal chart
representation before it reaches the browser runtime.

## Advanced Plotly API

`pl.chart()` also accepts a Plotly `graph_objects.Figure` directly. This is
the advanced escape hatch when callers need Plotly-specific features that are
not represented by the native data API.

    import pylage as pl
    import plotly.graph_objects as go

    fig = go.Figure(
        data=[go.Bar(x=["A", "B"], y=[1, 3])]
    )

    app = pl.column(
        pl.chart(fig, height=400),
    )

    pl.run(app)

The two APIs are mutually exclusive. Pass either `figure` or `data`, not both.

## Supported Plotly figures

`pl.chart()` accepts Plotly `graph_objects.Figure` instances. Plotly Express
figures are also supported because Plotly Express produces Plotly Figure
objects.

The chart integration has been exercised with the following Plotly chart
families in the project showcase:

- Line and area charts
- Bar, multi-series bar, and stacked bar charts
- Scatter and bubble charts
- Pie and donut charts
- Histogram, box, and violin plots
- Heatmap and contour plots
- Candlestick and OHLC charts
- 3D scatter, surface, and mesh charts
- Polar / radar charts
- Funnel and waterfall charts
- Sunburst and treemap charts
- Parallel coordinates
- Multi-chart dashboards / subplots
- Plotly Express figures
- Figures containing animation frames

The PyLage `Chart` component transports the Plotly figure through the generic
chart payload/backend pipeline; chart-specific rendering remains handled by
Plotly.

## Plotly Express

Plotly Express figures can be passed directly to `pl.chart()`:

    import plotly.express as px
    import pylage as pl

    fig = px.scatter(
        x=[10, 20, 30, 40, 50],
        y=[15, 25, 35, 45, 60],
        size=[10, 20, 30, 40, 50],
        title="Plotly Express Chart",
    )

    app = pl.column(
        pl.chart(fig, height=500),
    )

The same `Chart` options and event handlers apply to Plotly Express figures.

## Reactive charts

    values = pl.state([1, 2, 3])
    figure = pl.derived(
        values,
        compute=lambda v: go.Figure(
            data=[go.Bar(x=["a", "b", "c"], y=list(v))]
        ),
    )
    pl.chart(figure, height=350)

When `values` changes, the chart updates in place via Plotly.react (no full page reload).

## Events

| Handler | Plotly event | Payload |
| --- | --- | --- |
| on_click | plotly_click | clicked point data |
| on_select | plotly_selected | selected points and selection range |
| on_hover | plotly_hover | hovered point data |
| on_relayout | plotly_relayout | zoom/pan relayout data |

    def on_click(payload):
        pts = (payload or {}).get("points") or []
        if pts:
            print(pts[0].get("x"), pts[0].get("y"))

    pl.chart(fig, on_click=on_click)

## Sizing

`height` and `width` control the PyLage chart container:

- Numeric values are interpreted as pixels.
- CSS-style strings can be used for responsive sizing, such as `"100%"` or
  `"40vh"`.
- The default height is `400px`.
- The default width is `100%`.

Examples:

    pl.chart(fig, height=480, width="100%")

    pl.chart(fig, height="40vh", width="80%")

Chart container sizing is separate from Plotly figure layout. Configure
Plotly-specific visual properties such as titles, axes, margins, templates,
and backgrounds on the Figure itself with `fig.update_layout()`.

## Themes and configuration

PyLage exposes Plotly browser configuration through the `config` argument:

    pl.chart(
        fig,
        height=420,
        config={
            "displayModeBar": False,
        },
    )

Figure appearance should normally be configured through Plotly:

    fig.update_layout(
        title="Monthly Revenue",
        margin=dict(l=40, r=20, t=50, b=40),
    )

These are separate layers:

- `fig.update_layout()` controls the Plotly figure and its visual layout.
- `Chart(..., config=...)` controls Plotly renderer/browser configuration.

PyLage enables responsive Plotly rendering by default. Application-specific
configuration can override supported Plotly config values.

For reusable chart themes, use Plotly's normal template and layout APIs rather
than treating PyLage component configuration as a theme system.

## Architecture

- Generic backend abstraction (ChartBackend) — Plotly is the first backend.
- Payload is JSON-safe and travels through the normal prop/diff pipeline.
- Plotly.js is served from /_pylage/assets/plotly.min.js as a packaged runtime asset.

## Security

Chart configuration and payloads are treated as data, not executable code.

### Safe configuration

- Use JSON-compatible values in chart figures and configuration: strings, numbers, booleans, lists, dictionaries, and `None`.
- Plotly configuration keys may be passed through the chart backend, including application-specific/custom keys when supported by the consuming layer.
- Strings containing HTML, JavaScript, or `javascript:` remain serialized data; they are not evaluated as Python or JavaScript by the chart component.
- Chart payloads cross the runtime boundary through JSON serialization. Python callables and arbitrary Python objects are therefore not valid chart payload values.

### Unsafe patterns

Do not use chart configuration as a mechanism for executing code.

- Do not place Python callables, executable objects, or other non-JSON Python values in chart payloads.
- Do not rely on JavaScript strings such as `<script>...</script>` or `javascript:...` as chart configuration handlers.
- Do not treat untrusted chart configuration as trusted browser code.
- URL/resource-valued chart options should only reference resources that the application intentionally permits.

### Browser and WebSocket boundaries

Chart browser events are validated by the server before dispatch. WebSocket connections enforce message-size and message-rate limits.

The runtime serves Plotly.js from the packaged `/_pylage/assets/` path and validates the requested asset path before reading the file.

### Content Security Policy

The current PyLage browser runtime embeds the client runtime as inline JavaScript and dynamically loads the packaged Plotly.js asset.

Deployments using a strict Content Security Policy must therefore account for the current inline-runtime architecture. A nonce/hash-based CSP is not currently exposed as a PyLage chart configuration option. Do not assume that a strict nonce-only policy will work without additional runtime integration.

### Dependency security

Chart dependencies are optional. The project CI includes `pip-audit` as a security-audit step.

The bundled browser asset should be kept aligned with the project's supported Plotly dependency policy and reviewed when Plotly versions are changed.

## Lifecycle behavior

A chart follows the normal PyLage component lifecycle:

1. Native tabular data is converted into the internal chart representation,
   or an advanced Plotly Figure is accepted directly.
2. The resulting chart is converted into a JSON-safe chart payload.
3. The payload travels through the normal component property/diff pipeline.
4. The browser creates or updates the Plotly chart.
5. Reactive Figure changes produce chart updates without a full page reload.
6. Browser chart events are sent back through the normal event dispatch path.

The advanced Figure API supports reactive `state`/`derived` Figure values.
The native `data=` API currently converts the supplied tabular value when the
chart is created.

If an initial Figure cannot be converted successfully, the Chart component
uses its chart-error rendering path rather than silently executing arbitrary
configuration.

## Errors and troubleshooting

### Plotly is not installed

Plotly is an optional dependency. Install the chart extra:

    pip install "pylage[charts]"

or install Plotly directly:

    pip install plotly

`dataframe_to_figure()` also requires Plotly and reports an installation error
when the dependency is unavailable.

### Chart does not render

For the native data API, check that:

- the supplied data is a supported pandas/Polars DataFrame, record list, or
  column mapping;
- `x` and `y` identify existing data columns;
- the requested chart `type` is supported;
- the chart dependency is installed.

For the advanced Figure API, check that:

- the application includes the `Chart` component;
- the Figure is a supported Plotly Figure object;
- the chart dependency is installed.

For both APIs, also check that:

- the application is serving the packaged PyLage runtime assets;
- the browser console does not report a Plotly runtime error.

### Reactive chart does not update

Ensure that the Figure is produced from the relevant PyLage `state` or
`derived` value and that the state is actually updated. A static Figure does
not become reactive merely because it is passed to `pl.chart()`.

### Event callback does not fire

Verify that the corresponding `on_*` handler is supplied to `pl.chart()` and
that the Plotly interaction can produce that event. Supported handlers are
`on_click`, `on_select`, `on_hover`, and `on_relayout`.

## Performance

Chart payloads contain the serialized Plotly figure, so large datasets can
increase serialization cost, WebSocket traffic, browser memory usage, and
rendering time.

For larger datasets:

- aggregate data before creating the Figure when the visualization allows it;
- explicitly sample data when appropriate;
- avoid sending unnecessary traces or fields;
- use a chart resolution appropriate to the information being displayed;
- prefer reactive updates that change the required data rather than rebuilding
  unrelated application state.

PyLage does not implicitly truncate or sample DataFrame input.

## Deployment requirements

Charts require both the Python Plotly dependency and the packaged browser
runtime asset.

Install the optional chart dependency in deployments:

    pip install "pylage[charts]"

PyLage packages `plotly.min.js` under the runtime asset path and serves it from:

    /_pylage/assets/plotly.min.js

Deployments should keep the Python Plotly version within PyLage's documented
supported range and keep the packaged Plotly.js asset aligned with the chart
dependency policy.

Applications using a strict Content Security Policy should also account for
PyLage's current inline browser runtime and dynamically loaded Plotly asset;
see the Security section.

## Compatibility and version policy

The chart extra currently supports:

    plotly>=5.18,<7

Plotly remains optional. Applications that do not install the `charts` extra
can continue to use unrelated PyLage functionality.

The supported Python version follows the main PyLage package requirement:

    Python >= 3.10

When changing the supported Plotly range or bundled Plotly.js asset, update
the package metadata, runtime asset, tests, and chart documentation together.

## DataFrame integration

For application code, use the public native API directly:

    import pandas as pd
    import pylage as pl

    df = pd.DataFrame({
        "category": ["A", "B", "C"],
        "value": [10, 20, 30],
    })

    pl.chart(
        data=df,
        type="bar",
        x="category",
        y="value",
    )

The lower-level `dataframe_to_figure()` adapter remains available internally
for code that specifically needs to convert tabular data into a Plotly Figure:

    from pylage.ENGINE.charts.dataframe import dataframe_to_figure

    fig = dataframe_to_figure(
        df,
        x="category",
        y="value",
        kind="bar",
    )

    pl.chart(fig)

Supported input forms are:

- pandas DataFrame
- Polars DataFrame / compatible tabular objects when Polars is installed
- list of record dictionaries
- column mappings such as `{"category": [...], "value": [...]}`

Normalization rules:

- `None` and `NaN` values become JSON-safe `None`.
- Positive and negative infinity become `None`.
- `datetime`, `date`, and `time` values are converted to ISO strings.
- pandas categorical values are preserved as ordinary chart category values.
- No implicit row truncation or sampling is performed.
- For large datasets, callers should explicitly aggregate or sample data before
  creating the chart when appropriate for the visualization.

The DataFrame adapter produces a normal Plotly figure. It does not bypass the
generic `ChartBackend` / `ChartPayload` abstraction.

### SQL boundary

Database access is intentionally outside the chart engine.

The planned data flow is:

    SQL / database layer
            |
            v
        DataFrame
            |
            v
    dataframe_to_figure()
            |
            v
       Plotly Figure
            |
            v
    generic ChartBackend
            |
            v
       ChartPayload

Future SQL/database integrations should therefore produce a supported
DataFrame or tabular representation first. Database connections, SQL query
execution, connection management, and database-specific logic should remain in
a separate DATA layer rather than being embedded in the chart subsystem.

## CLI

    pylage run demo/demo_chart.py
    pylage run demo/demo_charts_dashboard.py --port 3001

## Demos

- demo/demo_chart.py — reactive bar chart + click events
- demo/demo_charts_dashboard.py — line, donut, scatter
