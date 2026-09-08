# PyLage UI Kit — Dashboard Section

## Definition

`dashboard_section()` creates a structured dashboard section with an optional header and body content. It reuses the existing PyLage Engine `Column`, `Row`, `Heading`, and `Text` components rather than introducing a separate rendering system.

## Use

Use `dashboard_section()` to group related dashboard content under a consistent section header. It is useful for:

- Metrics and metric grids
- Tables and data lists
- Cards and charts
- Configuration or operational panels
- Sections with contextual actions such as Refresh, Edit, or View All

## Usage

### Basic section

```python
import pylage as pl

pl.dashboard_section(
    pl.card(heading="Node Alpha", body="Online"),
    title="Cluster Status",
    description="Live status of cluster nodes.",
)
```

### Section with an action

```python
import pylage as pl

pl.dashboard_section(
    pl.text("Current infrastructure configuration."),
    title="Infrastructure Config",
    action=pl.button("Edit Config", variant="ghost"),
)
```

### Dashboard metrics

```python
import pylage as pl
import pylage as pl

pl.dashboard_section(
    pl.metric_grid(
        pl.metric(label="Nodes Online", value="64/64", delta="100%"),
        pl.metric(label="Memory Pressure", value="42%", delta="-3%"),
        columns=2,
    ),
    title="Telemetry Overview",
    description="Aggregated cluster metrics.",
    action=pl.button("Refresh", variant="outline"),
)
```

### Component content

`title` and `description` may receive existing component instances. Component values are preserved instead of being wrapped in a new `Heading` or `Text` component.

Positional `*children` are appended as the section body and may contain any compatible PyLage components.

## API

```python
dashboard_section(
    *children,
    title=None,
    description=None,
    action=None,
    style=None,
    **props,
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Body content placed after the optional header. |
| `title` | `Any` | `None` | Section title. Non-component values become an Engine `Heading` at level 2. |
| `description` | `Any` | `None` | Optional description. Non-component values become an Engine `Text`. |
| `action` | `Any` | `None` | Optional contextual action rendered on the right side of the header. |
| `style` | `Style` or `None` | `None` | Custom root-section style merged after the defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the root Engine `Column`. |

## Composition Behavior

When `title`, `description`, or `action` is supplied, the component creates a header row.

```text
dashboard_section
├── header row (when header content exists)
│   ├── left column
│   │   ├── title
│   │   └── description
│   └── action (when supplied)
└── *children
```

Header details:

- Title strings and other non-component values become `Heading(level=2)`.
- Description values become `Text` when they are not already components.
- The title and description are grouped in a vertical Engine `Column`.
- The header uses an Engine `Row` with `justify_content="space-between"` and `align_items="center"`.
- The action is placed on the right side of the header row.
- The header is created only when at least one of `title`, `description`, or `action` is provided.
- Body children are appended after the header.

## Default Styling

The root section uses:

- `display="flex"`
- `flex_direction="column"`
- `width="100%"`
- `gap="var(--spacing-md)"`

Title text uses:

- `font_size="1.25rem"`
- `font_weight="600"`
- `color="var(--color-text)"`
- `margin="0"`

Description text uses:

- `font_size="0.875rem"`
- `color="var(--color-text-muted)"`
- `margin="0"`

The title/description column uses a `0.125rem` gap. The header row uses a horizontal flex layout with space-between alignment and full width.

## Styling Behavior

The final root style is built as:

```python
final_style = _DEFAULT_SECTION_STYLE.merge(style)
```

Therefore, values supplied through `style` override the default section styling.

For example:

```python
import pylage as pl

pl.dashboard_section(
    pl.text("Custom section"),
    title="Custom",
    style=pl.style(
        padding="1.5rem",
        background_color="#f8fafc",
    ),
)
```

## API Boundary

`dashboard_section()` is a composition helper. It does not implement its own renderer, state system, or DOM engine.

```text
dashboard_section()
        ↓
Engine Column / Row / Heading / Text
        ↓
PyLage renderer and runtime
        ↓
HTML / browser
```

Engine properties supplied through `**props`, such as `class_name` and `id`, are forwarded to the root `Column`.

## Verified Working Example

The project demo uses `dashboard_section()` with a metric grid and a data list:

```python
pl.dashboard_section(
    pl.metric_grid(
        pl.metric(label="Nodes Online", value="64/64", delta="100%"),
        pl.metric(label="Memory Pressure", value="42%", delta="-3%"),
        pl.metric(label="Network Inbound", value="1.2 Gbps", delta="+0.1"),
        columns=3,
    ),
    title="Telemetry Overview",
    description="Aggregated vitals from primary and secondary edge clusters.",
    action=pl.button("Refresh", variant="outline"),
)
```

## Verification

The component is covered by `test/components/test_ui_kit_dashboard_section.py`.

Verified behavior includes:

- Returns an Engine `Column`.
- Renders title and description.
- Renders positional child content.
- Renders contextual actions.
- Applies custom root styles.
- Forwards Engine properties such as `class_name` and `id`.

## Verified Sources

- Component source: `pylage/UI/components/dashboard_section.py`
- Demo: `demo/demo_dashboard_section.py`
- Tests: `test/components/test_ui_kit_dashboard_section.py`
- Reference documentation: `documents/dashboard_section.md`

## Status

**FINAL / VERIFIED**
