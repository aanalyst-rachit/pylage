# PyLage UI Kit — Stat Group

## Definition

`stat_group` creates a responsive grid of metric cards.

It accepts existing metric components as well as mapping and tuple data, converts supported data items into metric cards, and renders them through the existing engine `Grid`.

## Use

Use `stat_group()` for dashboard and analytics layouts where several related statistics should be presented as a cohesive responsive group.

The component supports both direct metric components and compact data-driven definitions.

## Usage

### Existing Metric Components

Pass `metric()` components directly as positional arguments:

```python
import pylage as pl

pl.stat_group(
    pl.metric(label="Revenue", value="₹1,20,000", delta="+12%"),
    pl.metric(label="Subscribers", value="3,450", delta="+4%"),
    columns=2,
)
```

Existing components are preserved rather than converted into new metric cards.

### Mapping Items

Use `items` with mappings containing metric arguments:

```python
import pylage as pl

pl.stat_group(
    items=[
        {"label": "Direct Visits", "value": "12.4K", "delta": "+8%"},
        {"label": "Organic Visits", "value": "45.1K", "delta": "+15%"},
    ],
    columns=2,
)
```

Each mapping is passed to the UI Kit `metric()` component.

### Tuple Items

Tuple or list entries can provide metric data in this order:

```text
(label, value, delta, description)
```

Only the available positions are used; missing positions receive empty or `None` values as defined by the component implementation.

### Mixed Inputs

Positional `stats` and the optional `items` list are combined into one grid.

The component can therefore combine existing components with mapping- or tuple-based metric definitions.

### Column Configuration

An integer `columns` value creates an equal-width CSS grid with that many columns:

```python
import pylage as pl

pl.stat_group(
    pl.metric(label="Users", value="12K"),
    pl.metric(label="Orders", value="840"),
    columns=2,
)
```

A string can instead provide the complete CSS `grid-template-columns` value:

```python
import pylage as pl

pl.stat_group(
    items=[
        {"label": "Users", "value": "12K"},
        {"label": "Orders", "value": "840"},
    ],
    columns="repeat(auto-fit, minmax(220px, 1fr))",
)
```

## API

```python
stat_group(*stats, items=None, columns="repeat(auto-fit, minmax(240px, 1fr))", style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*stats` | `Any` | — | Positional statistics, including existing components, mappings, tuples, lists, or other values accepted by the implementation. |
| `items` | `list[Any] \\| None` | `None` | Additional statistics using the same supported item forms. |
| `columns` | `int \\| str` | `"repeat(auto-fit, minmax(240px, 1fr))"` | Integer column count or a CSS grid-template-columns value. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the default grid style. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Grid`. |

## Input Handling

`stat_group()` processes each supplied item as follows:

1. Existing components with a `type` attribute are preserved.
2. Mappings are passed to `metric()` as keyword arguments.
3. Lists and tuples are interpreted as `(label, value, delta, description)`.
4. Other values are passed through unchanged.

Positional `stats` are processed first, followed by entries from `items` when `items` is supplied.

## Default Styling

The component applies the following base grid styling:

- `display: grid`
- `width: 100%`
- `gap: var(--spacing-lg)`

The component also sets `grid-template-columns` from the `columns` argument.

The default column template is:

```text
repeat(auto-fit, minmax(240px, 1fr))
```

## Styling Behavior

The default grid style is merged with the generated `grid-template-columns` style, and the optional `style` argument is merged last.

This allows custom styles to override matching defaults while preserving unrelated grid styles.

## Architecture

```text
pl.stat_group()
    ↓
UI Kit stat_group wrapper
    ↓
Normalize stats and data items
    ↓
UI Kit metric() for supported data items
    ↓
PyLage ENGINE Grid
```

The component composes the existing `metric()` and `Grid` implementations rather than introducing a separate rendering system.

## API Boundary

`stat_group()` is the public UI Kit entry point for grouped metric layouts.

It owns input normalization and grid configuration, while metric rendering is delegated to the existing `metric()` component and final layout rendering is delegated to the engine `Grid`.

## Verified Working Example

The project demo `demo/demo_stat_group.py` provides the primary working example for grouped statistics and demonstrates the public `stat_group()` API in a dashboard-oriented layout.

## Verification

Stat Group behavior is covered by:

- `test/components/test_ui_kit_stat_group.py`

The implementation and public API are also represented by the project demo:

- `demo/demo_stat_group.py`

## Verified Sources

- `pylage/UI/components/stat_group.py`
- `demo/demo_stat_group.py`
- `test/components/test_ui_kit_stat_group.py`
- `documents/stat_group.md`

## Status

**Stat Group documentation refined and verified.**
