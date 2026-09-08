# PyLage UI Kit — Dashboard Grid

## Definition

`dashboard_grid()` is a high-level PyLage UI Kit layout component for arranging dashboard widgets in a CSS Grid.
It provides predefined grid layouts, custom column definitions, configurable spacing, and style overrides while reusing the existing Engine `Grid` component.

## Use

Use `dashboard_grid()` when multiple cards, metrics, charts, or other UI components need to be arranged as dashboard content.

- Arrange multiple dashboard widgets in a grid
- Use responsive auto-fit layout by default
- Select a predefined column arrangement
- Define a custom number or template of columns
- Override grid spacing
- Apply additional grid styling
- Forward standard Engine properties such as `class_name` and `id`

## Usage

### Basic grid

```python
import pylage as pl

grid = pl.dashboard_grid(
    pl.card(heading="Sales", body="1,200 units"),
    pl.card(heading="Traffic", body="45K visitors"),
    layout="2-col",
)
```

### Layout presets

The `layout` parameter selects one of the built-in grid presets.

| Layout | Grid columns |
|---|---|
| `"auto"` | `repeat(auto-fit, minmax(340px, 1fr))` |
| `"2-col"` | `repeat(2, minmax(0, 1fr))` |
| `"3-col"` | `repeat(3, minmax(0, 1fr))` |
| `"main-side"` | `2fr 1fr` |
| `"side-main"` | `1fr 2fr` |

### Custom column count

Pass an integer to `columns` to create that many equal-width columns.

```python
import pylage as pl

grid = pl.dashboard_grid(
    pl.card(body="Widget 1"),
    pl.card(body="Widget 2"),
    pl.card(body="Widget 3"),
    columns=3,
)
```

An integer such as `3` becomes `repeat(3, minmax(0, 1fr))`.

### Custom column template

Pass a string to `columns` when a custom CSS Grid template is required.

```python
import pylage as pl

grid = pl.dashboard_grid(
    pl.card(body="Main"),
    pl.card(body="Side"),
    columns="2fr 1fr",
)
```

When `columns` is provided, it takes precedence over `layout`.

### Custom gap

Use `gap` to override the default grid spacing.

```python
import pylage as pl

grid = pl.dashboard_grid(
    pl.card(body="Widget 1"),
    pl.card(body="Widget 2"),
    gap="2rem",
)
```

### Custom styling and properties

Use `style` for additional grid styling and `**props` for Engine properties.

```python
import pylage as pl

grid = pl.dashboard_grid(
    pl.card(body="Widget"),
    style=pl.style(
        padding="2rem",
        background_color="#f8fafc",
    ),
    class_name="primary-dashboard-grid",
    id="main-dash-grid",
)
```

## API

```python
dashboard_grid(
    *widgets,
    layout="auto",
    columns=None,
    gap=None,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `*widgets` | — | Positional dashboard widgets or components placed inside the grid. |
| `layout` | `"auto"` | Name of a predefined grid layout. Unknown names fall back to the `"auto"` preset. |
| `columns` | `None` | Custom grid column definition. An integer creates equal-width columns; a string is used as the column template. Overrides `layout` when supplied. |
| `gap` | `None` | Optional grid gap override. |
| `style` | `None` | Optional `Style` merged after the component defaults and generated grid settings. |
| `**props` | — | Additional properties forwarded to the Engine `Grid`. |

## Default Styling

The grid starts with these base styles:

```text
display: grid
width: 100%
gap: var(--spacing-xl)
```

The selected layout determines `grid_template_columns`.

## Styling Behavior

The final style is built in this order:

```text
default grid style
        ↓
layout / columns / gap settings
        ↓
user-provided style
```

Therefore, values supplied through `style` have the final precedence and can override generated grid properties.

## Layout Resolution

Column resolution follows this order:

1. If `columns` is an integer, it becomes `repeat(N, minmax(0, 1fr))`.
2. If `columns` is a string, that string becomes the grid column template.
3. Otherwise, the named `layout` preset is used.
4. If the layout name is not recognized, the `"auto"` preset is used.

## API Boundary

`dashboard_grid()` is a layout wrapper and does not create a separate rendering engine.

```text
pylage.UI.components.dashboard_grid.dashboard_grid
        ↓
PyLage Engine Grid
        ↓
PyLage renderer / runtime
        ↓
Browser DOM
```

## Verified Working Examples

- `demo/demo_dashboard_grid.py` — metric group plus dashboard cards arranged with the `"2-col"` layout.

## Verification

`test/components/test_ui_kit_dashboard_grid.py` verifies:

- The wrapper returns an Engine `Grid`.
- Dashboard widgets render inside the grid.
- Preset layouts such as `"main-side"` and `"2-col"` produce the expected column templates.
- Integer `columns` and custom `gap` are applied correctly.
- Custom styles override the generated grid style.
- Engine properties such as `class_name` and `id` are forwarded and rendered.

## Verified Sources

- Component: `pylage/UI/components/dashboard_grid.py`
- Demo: `demo/demo_dashboard_grid.py`
- Test: `test/components/test_ui_kit_dashboard_grid.py`
- Reference: `documents/dashboard_grid.md`

## Status

**FINAL / VERIFIED** — documentation reflects the current `dashboard_grid()` implementation, verified demo usage, and available automated coverage.
