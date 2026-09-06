# UI Kit Stat Group

`pylage_ui.stat_group()` arranges multiple metric cards into responsive KPI grids for dashboards and analytics views.

## Basic Usage

```python
import pylage as pl

pl.stat_group(
    pl.metric(label="Revenue", value="₹1,20,000", delta="+12%"),
    pl.metric(label="Subscribers", value="3,450", delta="+4%"),
    columns=2,
)
```

## Mapping and Tuple Syntax

```python
import pylage as pl

pl.stat_group(
    items=[
        {"label": "Direct Visits", "value": "12.4K", "delta": "+8%"},
        {"label": "Organic Visits", "value": "45.1K", "delta": "+15%"},
    ],
    columns="repeat(auto-fit, minmax(220px, 1fr))",
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*stats` | `Any` | — | Positional metric cards or tuples |
| `items` | `list` | `None` | Optional list of dicts, metrics, or tuples |
| `columns` | `int \| str` | `"repeat(auto-fit, minmax(240px, 1fr))"` | Column count or CSS grid template columns |
| `style` | `Style` | `None` | Custom style overrides merged with default grid style |
| `**props` | `Any` | — | Forwarded to root `Grid` |
