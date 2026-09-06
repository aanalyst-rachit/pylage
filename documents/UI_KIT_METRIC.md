# PyLage UI Kit — Metric

## Overview

`pl.metric()` provides a semantic KPI/metric card API while reusing the existing PyLage Layout `Metric` pattern.

```python
import pylage as pl

pl.metric(
    label="Revenue",
    value="₹42,000",
    delta="+12%",
    description="vs last month",
)
```

## KPI Usage

`pl.metric()` is the standard UI Kit component for presenting Key Performance Indicators (KPIs).

Use it for dashboard values such as Revenue, Active Users, Conversion Rate,
Orders, Latency, or other measurable business and system indicators.

For this reason, the UI Kit does not provide a separate `pl.kpi()` component.
A KPI is a use-case of `pl.metric()`, not a separate UI component.

## API

```python
pl.metric(label, value, delta=None, description=None, *, style=None, **props)
```

### Parameters

- `label` — metric label.
- `value` — primary metric value.
- `delta` — optional change indicator.
- `description` — optional supporting description.
- `style` — optional `pylage.Style` merged over semantic defaults.
- `**props` — forwarded to the existing PyLage metric pattern.

## Variants and Delta Semantics

The existing metric pattern automatically selects the delta badge variant:

- Values beginning with `+` use the success variant.
- Values beginning with `-` use the danger variant.
- Other delta values use the secondary variant.

## Reactive Values

Metric values and delta values can use PyLage reactive state because the UI Kit delegates rendering to the existing `pylage_layout.Metric` implementation.

## Styling

The UI Kit supplies semantic defaults using existing PyLage design tokens:

- Background uses the default surface/background token.
- Large spacing is used for padding.
- Extra-large radius is used for the card radius.
- The standard border token is used for the card border.

A custom `Style` is merged over these defaults.

## Architecture

`pl.metric()` is a WRAP/COMPOSE implementation. It does not introduce a new renderer, state engine, CSS engine, or layout engine. It delegates to the existing `pylage_layout.Metric` pattern.

The underlying metric pattern was also corrected so reactive/state-backed delta content is rendered through a primitive `Text` component.

## Manual Demo

See `demo/demo_metric.py` for the browser/manual smoke example.
