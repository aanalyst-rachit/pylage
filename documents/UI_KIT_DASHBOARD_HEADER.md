# UI Kit Dashboard Header

`pylage_ui.dashboard_header()` provides a standardized, responsive top header bar for dashboards, settings, and analytical consoles.

## Basic Usage

```python
import pylage as pl

pl.dashboard_header("Overview")
```

## With Subtitle and Action Controls

```python
import pylage as pl

pl.dashboard_header(
    title="Sales Pipeline",
    description="Track quarterly deal stages and team velocity.",
    actions=[
        pl.button("Export CSV", variant="outline"),
        pl.button("Add Deal", variant="primary"),
    ],
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `Any` | — | Title text or component |
| `description` | `Any` | `None` | Subtitle description or guidance |
| `actions` | `Any` | `None` | Action buttons, date pickers, or interactive components |
| `style` | `Style` | `None` | Custom style overrides merged with default header style |
| `**props` | `Any` | — | Forwarded to root `Row` |
