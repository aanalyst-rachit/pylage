# UI Kit Dashboard Card

`pylage_ui.dashboard_card()` formats dashboard analytics widgets with structured title, action, content, and footer slots.

## Basic Usage

```python
import pylage as pl

pl.dashboard_card(
    title="Real-time Traffic",
    body="14,200 sessions actively streaming.",
    footer="Refreshed 10s ago",
)
```

## With Contextual Actions and Tags

```python
import pylage as pl

pl.dashboard_card(
    pl.metric(label="Active Containers", value="94/100", delta="+6"),
    title="Fleet Capacity",
    action=pl.badge("Healthy", variant="success"),
    footer="Cluster: us-west-prod",
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Embedded visualizers, tables, or metric components |
| `title` | `Any` | `None` | Card title text or component |
| `body` | `Any` | `None` | Primary text or descriptive body |
| `footer` | `Any` | `None` | Metadata or status text displayed at card base |
| `action` | `Any` | `None` | Contextual action button, badge, or menu |
| `variant` | `str` | `"elevated"` | Card surface visual style (`"elevated"`, `"outlined"`, `"default"`) |
| `style` | `Style` | `None` | Custom style overrides merged with base card style |
| `**props` | `Any` | — | Forwarded to base `card` |
