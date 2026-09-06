# PyLage UI Kit — Trend

`pl.trend()` is a semantic UI Kit component for displaying directional change, movement, or comparison values.

It is designed to complement `pl.metric()` and other dashboard components.

## Quick Start

```python
import pylage as pl

trend = pl.trend("+12%")
```

## Direction Detection

When `direction` is not provided, PyLage detects it from the value:

```python
pl.trend("+12%")   # Up
pl.trend("-8.5%")  # Down
pl.trend("0%")     # Neutral
```

## Explicit Direction

Use `direction` when the text itself does not contain a `+` or `-` sign:

```python
pl.trend("Improving", direction="up")
pl.trend("Declining", direction="down")
pl.trend("Stable", direction="neutral")
```

Available directions:

- `up`
- `down`
- `neutral`

## Indicators

By default, `pl.trend()` displays a directional indicator:

```python
pl.trend("+12%")
pl.trend("-8%")
pl.trend("0%")
```

Hide the indicator when only semantic styling is needed:

```python
pl.trend("+12%", show_indicator=False)
```

## Reactive Values

`pl.trend()` supports reactive `pylage.State` values:

```python

import pylage as pl

change = pl.State("+12%")
trend = pl.trend(change)
```

## Custom Styling

Custom styles override the default semantic styling:

```python

import pylage as pl

trend = pl.trend(
    "+12%",
    style=pl.style(padding="0.5rem 1rem"),
)
```

## Dashboard Usage

Use `pl.trend()` alongside `pl.metric()` to show directional context:

```python
pl.metric(
    label="Revenue",
    value="₹42,000",
)

pl.trend("+12%")
```

`pl.metric()` represents the primary KPI value, while `pl.trend()` communicates how that value is moving or changing.
