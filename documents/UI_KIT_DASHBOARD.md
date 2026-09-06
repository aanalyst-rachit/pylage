# UI Kit Dashboard

`pylage_ui.dashboard()` composes a complete, production-grade responsive dashboard layout in minimal lines of Python code.

## Basic Usage

```python
import pylage as pl

app = pl.dashboard(
    title="Operations Overview",
    metrics=[
        pl.metric(label="Revenue", value="$52,000", delta="+14%"),
        pl.metric(label="Active Users", value="4,850", delta="+6%"),
    ],
    content=pl.dashboard_card(
        title="Weekly Summary",
        body="All cluster nodes operational with zero reported incidents.",
    ),
    table=pl.table(
        [["Cluster A", "Healthy"], ["Cluster B", "Healthy"]],
        headers=["Cluster", "Status"],
    ),
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `Any` | `None` | Primary dashboard page title |
| `header` | `Any` | `None` | Top page header or `dashboard_header` |
| `sidebar` | `Any` | `None` | Navigation sidebar or side panel |
| `metrics` / `stats` | `Any` | `None` | List of metrics or `stat_group` / `metric_grid` |
| `filters` | `Any` | `None` | Controls or filter bar |
| `content` | `Any` | `None` | Main content widgets or `dashboard_grid` |
| `table` | `Any` | `None` | Primary data table or visualizer |
| `footer` | `Any` | `None` | Dashboard page footer |
| `**props` | `Any` | — | Forwarded to underlying layout container |
