# UI Kit Metric Grid

`pylage_ui.metric_grid()` arranges key performance indicator metrics and statistic cards into responsive grids.

## Basic Usage

```python
import pylage as pl

pl.metric_grid(
    pl.metric(label="MRR", value="$42,000", delta="+12%"),
    pl.metric(label="Subscribers", value="1,240", delta="+5%"),
    columns=2,
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*metrics` | `Any` | — | Positional metric cards or components |
| `items` | `list` | `None` | Optional list of mappings or tuples |
| `columns` | `int \| str` | `"repeat(auto-fit, minmax(240px, 1fr))"` | Number of columns or CSS grid template |
| `style` | `Style` | `None` | Custom style overrides merged with default grid style |
| `**props` | `Any` | — | Forwarded to root `Grid` |
