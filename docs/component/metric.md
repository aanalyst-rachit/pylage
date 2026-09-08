# PyLage UI Kit — Metric

## Definition

`metric` is a semantic PyLage UI Kit component for presenting a KPI or other important measurable value in a compact card.

It composes existing PyLage engine primitives: a `Card` containing a `Column` with optional label, value, delta, and description content.

## Use

Use `metric()` for dashboard and application values such as revenue, users, orders, conversion rates, latency, scores, or other measurable indicators.

A KPI is a use case of `metric()`; the UI Kit does not require a separate KPI component.

## Usage

### Basic Usage

```python
import pylage as pl

pl.metric(
    label="Revenue",
    value="₹42,000",
)
```

### Delta and Description

```python
import pylage as pl

pl.metric(
    label="Revenue",
    value="₹42,000",
    delta="+12%",
    description="vs last month",
)
```

`delta` and `description` are optional content displayed below the primary value.

The component does not interpret the meaning of the delta value; the supplied value is rendered as text using the component's delta text style.

### Reactive Values

```python
import pylage as pl

value = pl.state("42,000")
delta = pl.state("+12%")

pl.metric(
    label="Revenue",
    value=value,
    delta=delta,
)
```

`value` and `delta` can receive reactive `State` values. The existing PyLage rendering system handles those reactive values.

### Featured Variant

```python
import pylage as pl

pl.metric(
    label="Orders",
    value="1,284",
    delta="+5.2%",
    description="updated just now",
    featured=True,
)
```

`featured=True` changes the card border to the primary-colored featured treatment.

### Custom Styling

```python
import pylage as pl

pl.metric(
    label="Revenue",
    value="₹42,000",
    style=pl.style(
        padding="2rem",
        border="2px solid #111827",
    ),
)
```

Custom styles are merged over the component defaults.

### Metric Grid

For multiple metrics, compose `metric()` components with `metric_grid()`.

```python
import pylage as pl

pl.metric_grid(
    pl.metric(label="Total MRR", value="$248.5K", delta="+14.2%"),
    pl.metric(label="Net Retention", value="112%", delta="+3.1%"),
    pl.metric(label="Active Seats", value="18,400", delta="+850"),
    columns=3,
)
```

The project also provides a dedicated `metric_grid` component for responsive metric collections.

## API

```python
metric(label, value, delta=None, description=None, *, featured=False, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `label` | `Any` | required | Optional label displayed above the primary value. |
| `value` | `Any` | required | Primary metric value. |
| `delta` | `Any` | `None` | Optional change or comparison text. |
| `description` | `Any` | `None` | Optional supporting description. |
| `featured` | `bool` | `False` | Applies the featured primary-border treatment when enabled. |
| `style` | `Style \\| None` | `None` | Custom card style merged over the defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the root `Card`. |

## Content Behavior

Each content value is optional except for the function signature requirement of `label` and `value`.

- `label=None` omits the label text.
- `value=None` omits the primary value.
- `delta=None` omits the delta text.
- `description=None` omits the description text.

When present, content is added in this order: label, value, delta, description.

The label and delta use engine `Text` components. The primary value uses an engine `Heading` at level 2. The description uses an engine `Text` component.

## Default Styling

The root card defaults to:

- `display: flex`
- `flex_direction: column`
- `gap: var(--spacing-sm)`
- `padding: var(--spacing-lg)`
- `background_color: var(--color-background)`
- `border: 1px solid var(--color-border)`
- `border_radius: var(--radius-xl)`

The internal content column uses the same vertical flex direction and spacing token.

The label uses muted text at `0.875rem` with medium weight.

The primary value uses `1.75rem` text, bold weight, and the theme text color.

The delta uses `0.875rem` text, semibold weight, and the theme success color.

The description uses `0.75rem` muted text.

## Styling Behavior

The component first applies its default card style. When `featured=True`, the border is changed to `2px solid var(--color-primary)`. The optional `style` is then merged over the resulting card style, so explicitly supplied style values take precedence.

## State and Events

`metric()` does not define its own event API.

Standard engine properties and events can be forwarded through `**props`. The component has been verified to preserve `class_name`, `title`, and `on_click`.

## Architecture

`metric()` is a UI Kit composition built entirely from existing PyLage engine primitives.

The implementation creates the semantic content components, places them inside an engine `Column`, wraps that column in an engine `Card`, applies the semantic card styling, and forwards additional properties to the card.

It does not introduce a separate renderer or state system.

## API Boundary

The UI Kit owns the semantic metric composition, default visual treatment, featured border option, content ordering, and public `metric()` API.

The underlying engine remains responsible for rendering `Card`, `Column`, `Heading`, and `Text`, reactive value handling, styles, and forwarded events/properties.

## Verified Working Example

`demo/demo_metric_grid.py` demonstrates the public UI Kit API by composing three `metric()` components inside `metric_grid()` with three columns.

The standalone `demo/demo_metric.py` is a separate custom-styled metric-card demo built directly from PyLage primitives; its local `metric_card()` helper is not the implementation of `pl.metric()`.

## Verification

The implementation is covered by `test/components/test_ui_kit_metric.py`.

The tests verify:

- the component returns an engine `Card`
- default card styling
- semantic label, value, delta, and description rendering
- reactive `State` values and delta content
- custom style overrides
- forwarding `class_name` and `title` properties
- forwarding click events
- a non-`None` final style

`test/components/test_ui_kit_metric_grid.py` separately verifies composition of metrics inside `metric_grid()`, including rendered metric content and column configuration.

## Verified Sources

- `pylage/UI/components/metric.py`
- `demo/demo_metric.py`
- `demo/demo_metric_grid.py`
- `test/components/test_ui_kit_metric.py`
- `test/components/test_ui_kit_metric_grid.py`
- `documents/metric.md`

## Status

**Metric documentation refined and verified.**
