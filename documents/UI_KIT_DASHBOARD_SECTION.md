# UI Kit Dashboard Section

`pylage_ui.dashboard_section()` groups related dashboard widgets and visualizers beneath a standardized title bar with optional contextual actions.

## Basic Usage

```python
import pylage as pl

pl.dashboard_section(
    pl.card(heading="Node Alpha", body="Online"),
    title="Cluster Status",
    description="Live status of cluster nodes.",
    action=pl.button("View Logs", variant="ghost"),
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Widgets, cards, tables, or charts |
| `title` | `Any` | `None` | Section title heading |
| `description` | `Any` | `None` | Section subtitle or explanatory text |
| `action` | `Any` | `None` | Contextual action button or link |
| `style` | `Style` | `None` | Custom style overrides merged with default section style |
| `**props` | `Any` | — | Forwarded to root `Column` |
