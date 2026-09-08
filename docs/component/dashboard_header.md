# PyLage UI Kit — Dashboard Header

## Definition

`dashboard_header()` is a high-level PyLage UI Kit component for creating a standardized dashboard or administrative header row.
It combines a title and optional description on the left with optional action controls on the right.

## Use

Use `dashboard_header()` when a dashboard or administrative view needs a consistent top-level heading area.

- Display a page or dashboard title
- Add supporting descriptive text
- Add one or more action controls
- Preserve existing components supplied as title or description content
- Apply consistent header spacing and border styling
- Customize the header through `style` and standard Engine properties

## Usage

### Basic header

```python
import pylage as pl

header = pl.dashboard_header("Analytics Overview")
```

### Header with description

```python
import pylage as pl

header = pl.dashboard_header(
    "Analytics Overview",
    "Real-time traffic and performance metrics.",
)
```

### Header with actions

Multiple actions can be supplied as a list or tuple. They are placed in a horizontal action row.

```python
import pylage as pl

header = pl.dashboard_header(
    title="Analytics Overview",
    description="Production environment metrics.",
    actions=[
        pl.button("Export CSV", variant="outline"),
        pl.button("Add Widget", variant="primary"),
    ],
)
```

### Single action

A single component can be passed directly through `actions`.

```python
import pylage as pl

header = pl.dashboard_header(
    "Financial Report",
    actions=pl.button("Download Report", variant="outline"),
)
```

### Component content

Existing components supplied as `title` or `description` are preserved instead of being wrapped in new text components.

```python
import pylage as pl

header = pl.dashboard_header(
    title=pl.heading("Operations"),
    description=pl.text("Current production status"),
)
```

### Custom styling

Use `style` to override the default header styling.

```python
import pylage as pl

header = pl.dashboard_header(
    "Custom Header",
    style=pl.style(
        padding="2rem",
        background_color="#ffffff",
    ),
)
```

## API

```python
dashboard_header(
    title,
    description=None,
    *,
    actions=None,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `title` | — | Required title content. Existing components are preserved; other values are wrapped in an Engine level-1 `Heading`. |
| `description` | `None` | Optional supporting content. Existing components are preserved; other values are wrapped in `Text`. |
| `actions` | `None` | Optional action component, or a list/tuple of components. Lists and tuples are wrapped in a horizontal action `Row`. |
| `style` | `None` | Optional `Style` merged after the default header style. |
| `**props` | — | Additional properties forwarded to the root Engine `Row`. |

## Composition Behavior

The header is composed as:

```text
┌──────────────────────────────────────────────────────┐
│  title + description              actions            │
│  (left column)                     (right side)       │
└──────────────────────────────────────────────────────┘
```

The left side is always an Engine `Column` containing the available title and description items.

When `actions` is a list or tuple, the items are placed inside an Engine `Row` with horizontal spacing and centered alignment. A single action component is used directly.

## Default Styling

The root header uses:

```text
display: flex
flex-direction: row
justify-content: space-between
align-items: center
width: 100%
padding-bottom: var(--spacing-md)
border-bottom: 1px solid var(--color-border-muted)
```

Generated title styling uses:

```text
font-size: 1.5rem
font-weight: 700
color: var(--color-text)
margin: 0
```

Generated description styling uses:

```text
font-size: 0.875rem
color: var(--color-text-muted)
margin: 0
```

## Styling Behavior

The final root style is built by merging the default header style with the user-provided `style`.
Therefore, explicit values supplied through `style` have final precedence over the defaults.

## API Boundary

`dashboard_header()` is a composition wrapper around existing PyLage Engine layout and content components.

```text
pylage.UI.components.dashboard_header.dashboard_header
        ↓
Engine Column / Heading / Text / Row
        ↓
PyLage renderer / runtime
        ↓
Browser DOM
```

## Verified Working Examples

- `demo/demo_dashboard_header.py` — title, description, multiple action buttons, metrics, and dashboard composition.

## Verification

`test/components/test_ui_kit_dashboard_header.py` verifies:

- The wrapper returns an Engine `Row`.
- Title and description render correctly.
- A single action renders correctly.
- Multiple actions render correctly.
- Custom style values override the defaults.
- Engine properties such as `class_name` and `id` are forwarded and rendered.

`test/browser/test_dashboard_header_spacing_probe.py` provides browser-level spacing coverage for the dashboard header.

## Verified Sources

- Component: `pylage/UI/components/dashboard_header.py`
- Demo: `demo/demo_dashboard_header.py`
- Tests: `test/components/test_ui_kit_dashboard_header.py` and `test/browser/test_dashboard_header_spacing_probe.py`
- Reference: `documents/dashboard_header.md`

## Status

**FINAL / VERIFIED** — documentation reflects the current `dashboard_header()` implementation, verified demo usage, and available automated coverage.
