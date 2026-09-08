# PyLage UI Kit — Dashboard

## Definition

`dashboard()` is a public PyLage UI Kit composition helper for building a complete dashboard page from existing PyLage UI and Engine components.
It assembles optional header, sidebar, title, metrics, filters, main content, table, and footer sections into the existing PyLage layout system.

## Use

Use `dashboard()` when an application needs a structured dashboard page without manually composing the surrounding layout containers.

- Compose a dashboard header and footer
- Add an optional sidebar
- Display a page title
- Display metrics or statistics
- Add filters or filter controls
- Add arbitrary main content
- Add a primary data table
- Reuse existing PyLage components inside each section
- Build large dashboard component trees using the same underlying rendering system

## Usage

### Basic dashboard

```python
import pylage as pl

app = pl.dashboard(
    title="Operations Overview",
    metrics=[
        pl.metric(label="Revenue", value="$52,000", delta="+14%"),
        pl.metric(label="Active Users", value="4,850", delta="+6%"),
    ],
    content=pl.dashboard_card(
        title="Weekly Summary",
        body="All cluster nodes operational.",
    ),
    table=pl.table(
        [["Cluster A", "Healthy"], ["Cluster B", "Healthy"]],
        headers=["Cluster", "Status"],
    ),
)
```

### Header and sidebar

`header` and `sidebar` can contain existing components such as `dashboard_header()` or `card()`.

```python
import pylage as pl

app = pl.dashboard(
    header=pl.dashboard_header("Operations"),
    sidebar=pl.card(body="Navigation"),
    content=pl.card(body="Dashboard content"),
)
```

The header is placed above the dashboard body. The sidebar is placed alongside the main dashboard content.

### Metrics

`metrics` can receive a list or tuple of components. When a list or tuple is supplied, `dashboard()` wraps those items with `stat_group()`.

```python
import pylage as pl

app = pl.dashboard(
    metrics=[
        pl.metric(label="Revenue", value="$50,000", delta="+12%"),
        pl.metric(label="Customers", value="1,200", delta="+5%"),
    ],
)
```

`metrics` takes precedence over `stats` when both are supplied.

### Statistics with `stats`

`stats` provides the fallback statistics input when `metrics` is not supplied.

```python
import pylage as pl

app = pl.dashboard(
    stats=[
        pl.metric(label="Orders", value="850"),
        pl.metric(label="Conversion", value="8.4%"),
    ],
)
```

### Filters

`filters` can be a single component or a list/tuple of components. Lists and tuples are wrapped in an Engine `Row` with the class `dashboard-filters-row`.

```python
import pylage as pl

app = pl.dashboard(
    filters=[
        pl.select(["All Regions", "North", "South"]),
        pl.button("Apply", variant="primary"),
    ],
    content=pl.card(body="Filtered dashboard content"),
)
```

### Custom title content

String titles and reactive title-like values are wrapped in an Engine `Heading` with the class `dashboard-title`.
A non-string component value can instead be supplied directly as `title`.

### Footer

`footer` is added after the dashboard body and can contain any compatible PyLage component.

```python
import pylage as pl

app = pl.dashboard(
    content=pl.card(body="Main content"),
    footer=pl.card(
        body="PyLage Operations Console",
        variant="outlined",
    ),
)
```

## API

```python
dashboard(
    *, 
    title=None,
    header=None,
    sidebar=None,
    metrics=None,
    stats=None,
    filters=None,
    content=None,
    table=None,
    footer=None,
    **props,
)
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `title` | `None` | Dashboard title. Strings and reactive title-like values are wrapped in an Engine `Heading`; other component values are inserted directly. |
| `header` | `None` | Optional header component placed above the dashboard body. |
| `sidebar` | `None` | Optional sidebar or navigation component placed beside the main content. |
| `metrics` | `None` | Primary metrics/statistics content. Lists and tuples are wrapped with `stat_group()`. Takes precedence over `stats`. |
| `stats` | `None` | Fallback statistics content used when `metrics` is not supplied. Lists and tuples are wrapped with `stat_group()`. |
| `filters` | `None` | Filter content. Lists and tuples are wrapped in an Engine `Row`. |
| `content` | `None` | Main dashboard content inserted into the main column. |
| `table` | `None` | Optional table or other data-display component inserted after `content`. |
| `footer` | `None` | Optional footer component placed after the dashboard body. |
| `**props` | — | Additional properties forwarded to the outer `Stack` used by the dashboard composition. |

## Composition Behavior

The dashboard is assembled in this order:

```text
header
   ↓
dashboard body
   ├── sidebar
   └── main column
       ├── title
       ├── metrics / stats
       ├── filters
       ├── content
       └── table
   ↓
footer
```

Internally, the body uses an Engine `Row`, while the main dashboard content uses an Engine `Column`.
The complete result is wrapped in the existing UI Kit `Container` and `Stack` layout primitives.

The generated main and body containers use these internal classes:

- `dashboard-title`
- `dashboard-filters-row`
- `dashboard-main`
- `dashboard-body`

These classes are implementation details useful when inspecting rendered dashboard markup or related styling.

## API Boundary

`dashboard()` is a composition layer. It does not introduce a separate rendering, state, or layout engine.

```text
pylage.UI.components.dashboard.dashboard
        ↓
PyLage UI / Engine components
        ↓
Container + Stack + Row + Column
        ↓
PyLage renderer / runtime
        ↓
Browser DOM
```

Supporting components such as `dashboard_header()`, `dashboard_card()`, `dashboard_grid()`, `dashboard_section()`, `metric()`, and `table()` remain independent APIs.

## Verified Working Examples

- `demo/demo_dashboard.py` — dashboard header, action buttons, metrics, dashboard grid/cards, table, and footer composition.

The demo exercises the intended high-level dashboard composition pattern using existing PyLage UI components.

## Verification

### Automated tests

Verified dashboard coverage includes:

- `test/integration/test_ui_kit_dashboard.py` — title, metrics, content, table, header, sidebar, and rendered composition.
- `test/performance/test_large_dashboard.py` — large dashboard-like component trees, rendering, tree size, and repeated render behavior.
- `test/browser/test_dashboard_header_spacing_probe.py` — dashboard-related browser styling verification.
- `test/components/test_ui_kit_dashboard_card.py` — supporting dashboard card component.
- `test/components/test_ui_kit_dashboard_grid.py` — supporting dashboard grid component.
- `test/components/test_ui_kit_dashboard_header.py` — supporting dashboard header component.
- `test/components/test_ui_kit_dashboard_section.py` — supporting dashboard section component.

The supporting-component tests are listed separately because those components have their own public APIs and are not parameters of `dashboard()`.

## Verified Sources

- Component: `pylage/UI/components/dashboard.py`
- Demo: `demo/demo_dashboard.py`
- Integration tests: `test/integration/test_ui_kit_dashboard.py`
- Performance test: `test/performance/test_large_dashboard.py`
- Browser test: `test/browser/test_dashboard_header_spacing_probe.py`
- Supporting dashboard tests listed above
- Reference: `documents/dashboard.md`

## Status

**FINAL / VERIFIED** — documentation reflects the current `dashboard()` implementation, verified demo usage, composition behavior, and available automated coverage.
