# PyLage UI Kit — Metric Grid

## Definition

`metric_grid` is a PyLage UI Kit component for arranging multiple metric cards in a grid layout.

It is a thin UI Kit wrapper around the existing `stat_group()` composition and ultimately returns an engine `Grid` containing the supplied metric cards.

## Use

Use `metric_grid()` when several KPI or metric cards need to be presented together in a consistent grid.

It supports both already-created `metric()` components and convenient item definitions that are converted into metric cards by the underlying `stat_group()` implementation.

## Usage

### Basic Usage

```python
import pylage as pl

pl.metric_grid(
    pl.metric(label="MRR", value="$42,000", delta="+12%"),
    pl.metric(label="Subscribers", value="1,240", delta="+5%"),
    columns=2,
)
```

### Item Mappings

```python
import pylage as pl

pl.metric_grid(
    items=[
        {"label": "NPS Score", "value": "72"},
        {"label": "CSAT", "value": "98%"},
    ],
    columns=2,
)
```

Mapping items are passed to `metric()` as keyword arguments.

### Tuple Items

`items` can also contain tuples using the positional metric structure:

```python
import pylage as pl

pl.metric_grid(
    items=[
        ("Revenue", "$42,000", "+12%", "vs last month"),
        ("Users", "12,450", "+8.4%", "active users"),
    ],
    columns=2,
)
```

For tuple items, the first four positions represent label, value, delta, and description.

### Custom Grid Template

```python
import pylage as pl

pl.metric_grid(
    pl.metric(label="Revenue", value="$42K"),
    pl.metric(label="Users", value="12K"),
    columns="repeat(auto-fit, minmax(240px, 1fr))",
)
```

An integer `columns` value is converted into an equal-width CSS grid template. A string is used as the grid template directly.

### Custom Styling

```python
import pylage as pl

pl.metric_grid(
    pl.metric(label="Revenue", value="$42K"),
    style=pl.style(gap="2rem"),
)
```

Custom styles are merged over the default grid styling.

## API

```python
metric_grid(*metrics, items=None, columns="repeat(auto-fit, minmax(240px, 1fr))", style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*metrics` | `Any` | — | Positional metric components or other supported stat items. |
| `items` | `list[Any] \\| None` | `None` | Optional list of mappings, tuples, existing components, or other supported items. |
| `columns` | `int \\| str` | `"repeat(auto-fit, minmax(240px, 1fr))"` | Number of equal columns or a CSS grid-template-columns value. |
| `style` | `Style \\| None` | `None` | Custom grid style merged over the defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the root `Grid`. |

## Item Behavior

The underlying `stat_group()` implementation combines positional `metrics` and `items` into one collection.

- Existing PyLage components are preserved as supplied.
- Mapping items are converted to `metric(**item)`.
- List or tuple items use up to four positions: label, value, delta, and description.
- Other item types are passed through as supplied.

This makes `metric_grid()` suitable for both explicit component composition and data-oriented metric definitions.

## Column Behavior

The default value is:

`repeat(auto-fit, minmax(240px, 1fr))`

When `columns` is an integer, the implementation converts it to:

`repeat(N, minmax(0, 1fr))`

For example, `columns=3` produces `repeat(3, minmax(0, 1fr))`.

When `columns` is a string, that value is used directly as the grid template.

## Default Styling

The underlying grid defaults to:

- `display: grid`
- `width: 100%`
- `gap: var(--spacing-lg)`

The calculated `grid_template_columns` is added to these defaults before the optional custom `style` is merged.

## Styling Behavior

The final style preserves the default grid presentation while allowing explicitly supplied style values to override corresponding defaults.

For example, `style=pl.style(gap="2rem")` changes the grid gap while retaining the default width and grid display.

## Architecture

`metric_grid()` is a thin composition wrapper around `stat_group()`.

The UI Kit implementation forwards positional metrics, `items`, `columns`, `style`, and additional properties directly to `stat_group()`.

`stat_group()` performs item normalization, creates metric cards where required, calculates the grid template, merges styles, and returns the engine `Grid`.

## API Boundary

The `metric_grid()` API provides the public metric-grid entry point and delegates its behavior to the shared `stat_group()` implementation.

The underlying engine remains responsible for rendering the final `Grid` and its child components.

## Verified Working Example

`demo/demo_metric_grid.py` demonstrates three `metric()` components arranged with `columns=3` inside a page-level layout.

The example uses:

- Total MRR: `$248.5K` with `+14.2%`
- Net Retention: `112%` with `+3.1%`
- Active Seats: `18,400` with `+850`

## Verification

The implementation is covered by `test/components/test_ui_kit_metric_grid.py`.

The tests verify:

- the component returns an engine `Grid`
- supplied metric components render correctly
- mapping items are converted into rendered metrics
- integer column configuration produces the expected grid template

## Verified Sources

- `pylage/UI/components/metric_grid.py`
- `pylage/UI/components/stat_group.py`
- `demo/demo_metric_grid.py`
- `test/components/test_ui_kit_metric_grid.py`
- `documents/metric_grid.md`

## Status

**Metric Grid documentation refined and verified.**
