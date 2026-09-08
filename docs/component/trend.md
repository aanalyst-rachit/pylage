# PyLage UI Kit — Trend

## Definition

`trend` is a PyLage UI Kit component for displaying directional change, movement, or comparison values.

It is implemented as a semantic wrapper around the existing PyLage `Badge` component, with directional indicators and semantic styling.

## Use

Use `trend()` alongside metrics, dashboard cards, or other summary components to communicate whether a value is moving up, down, or remaining neutral.

## Usage

### Automatic Direction Detection

When `direction` is omitted, the component determines the direction from the leading character of `value`:

- A leading `+` selects `up`.
- A leading `-` selects `down`.
- Any other leading value selects `neutral`.

```python
import pylage as pl

pl.trend("+12%")
pl.trend("-8.5%")
pl.trend("0%")
```

### Explicit Direction

Use `direction` when the displayed value does not itself provide a leading `+` or `-` sign.

```python
import pylage as pl

pl.trend("Improving", direction="up")
pl.trend("Declining", direction="down")
pl.trend("Stable", direction="neutral")
```

Supported directions are `up`, `down`, and `neutral`.

### Hide the Indicator

The directional indicator is displayed by default. Set `show_indicator=False` when the semantic styling is desired without the arrow.

```python
import pylage as pl

pl.trend("+12%", show_indicator=False)
```

### Component Values

An existing PyLage `Component` can be supplied as the value. Other values are normalized into an existing PyLage `Text` component.

```python
import pylage as pl

pl.trend(pl.text("+12%"))
```

## API

```python
trend(value, *, direction=None, show_indicator=True, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `Any` | — | Value or component displayed by the trend indicator. |
| `direction` | `str \\| None` | `None` | Direction: `up`, `down`, or `neutral`. When omitted, direction is detected from the value. |
| `show_indicator` | `bool` | `True` | Whether to display the directional arrow. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the base and semantic variant styles. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Badge`. |

## Direction Behavior

The automatic detection rules are based on the resolved string representation of `value`.

```text
"+12%"  → up      → ↑
"-8%"   → down    → ↓
"0%"    → neutral → →
```

If an explicit `direction` is supplied, it takes precedence over automatic detection.

An unsupported direction raises `ValueError` and reports the valid direction names.

## Semantic Styling

Each direction maps to a semantic visual variant:

| Direction | Indicator | Variant | Background | Text |
| --- | --- | --- | --- | --- |
| `up` | `↑` | `success` | `var(--color-success)` | `var(--color-primary-contrast)` |
| `down` | `↓` | `danger` | `var(--color-danger)` | `var(--color-primary-contrast)` |
| `neutral` | `→` | `secondary` | `var(--color-secondary)` | `var(--color-secondary-contrast)` |

Each semantic variant also receives a 1px border using its corresponding semantic color.

## Default Styling

The base UI Kit styling is:

- `padding: 0.25rem 0.625rem`
- `border_radius: var(--radius-full)`
- `font_size: 0.75rem`
- `font_weight: 600`

The selected direction then adds its semantic background, text, and border styles.

## Styling Behavior

Styles are merged in this order:

1. Base Trend styles.
2. Direction-specific semantic styles.
3. User-supplied `style`.

Therefore, a supplied `Style` value takes precedence over the default and semantic styles.

```python
import pylage as pl

pl.trend(
    "+12%",
    style=pl.style(padding="0.5rem 1rem"),
)
```

## State and Reactivity

The implementation can resolve a value exposing a `.value` attribute when detecting direction, which allows a `State` value to be read at component creation time.

The current `trend()` implementation does not subscribe to that state or install an update callback. Therefore, this component should not be documented as providing automatic live direction updates when the underlying state changes.

## Dashboard Usage

Trend indicators can complement KPI components such as `metric()`:

```python
import pylage as pl

pl.metric(
    label="Revenue",
    value="₹42,000",
)

pl.trend("+12%")
```

The metric communicates the primary value, while the trend communicates its directional context.

## Architecture

```text
pl.trend()
    ↓
UI Kit trend wrapper
    ↓
PyLage ENGINE Badge
    ↓
Text children + existing renderer
```

The wrapper owns direction detection, semantic variant selection, indicator composition, and UI Kit styling. Rendering remains owned by the existing PyLage engine.

## API Boundary

`trend()` is the public UI Kit entry point.

It returns the existing engine `Badge` component rather than introducing a separate trend renderer or state system.

## Verified Working Example

The project provides the executable Trend demo:

- `demo/demo_trend.py`

The demo exercises directional values, explicit direction, styling, and dashboard-oriented usage.

## Verification

Trend behavior is covered by:

- `test/components/test_ui_kit_trend.py`

The component test verifies the current UI Kit Trend behavior and public API.

## Verified Sources

- `pylage/UI/components/trend.py`
- `demo/demo_trend.py`
- `test/components/test_ui_kit_trend.py`
- `documents/trend.md`

## Status

**Trend documentation refined and verified.**
