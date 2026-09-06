# UI Kit Alert

## Overview

`alert()` provides a semantic, high-level feedback component for informational, success, warning, and error messages.

The UI Kit Alert is a thin wrapper around the existing PyLage engine `Alert` component. It does not introduce a new renderer, runtime, or feedback engine.

## Basic Usage

```python
import pylage as pl

pl.alert("Your changes have been saved.")
```

## Variants

Supported semantic variants are:

| Variant | Purpose |
|---|---|
| `default` | Neutral informational feedback |
| `info` | Informational feedback |
| `success` | Successful operation feedback |
| `warning` | Caution or review feedback |
| `danger` | Failure or destructive-operation feedback |
| `error` | Error feedback |

Example:

```python
import pylage as pl

pl.alert("Profile updated.", variant="success")
pl.alert("Please review these values.", variant="warning")
pl.alert("The operation failed.", variant="danger")
pl.alert("Additional information.", variant="info")
```

## Composition

Alert accepts existing PyLage components as children and preserves component composition.

```python
import pylage as pl

pl.alert(
    pl.text("Component composition"),
    pl.text("Existing PyLage components remain valid children."),
    variant="info",
    title="Details",
)
```

Plain child values are normalized into existing PyLage `Text` components.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Alert content or existing PyLage components |
| `variant` | `str` | `"default"` | Semantic visual variant |
| `style` | `Style` | `None` | Custom style overrides |
| `**props` | `Any` | — | Forwarded to the underlying PyLage Alert |

## Styling

The wrapper applies UI Kit design tokens for spacing, radius, semantic colors, borders, and surface styling. A supplied `style` is merged last so developers can override the defaults.

## Architecture

```text
pl.alert()
    ↓
UI Kit alert wrapper
    ↓
PyLage ENGINE Alert
```

This implementation follows the UI Kit architecture by reusing the existing engine component instead of duplicating feedback infrastructure.

## Verification

- Automated UI Kit Alert tests: 8 passed.
- Full manual browser smoke: 63 manuals passed, 0 failed.
- Public API verified through `pylage.alert`.
- `pylage.UI.alert` and `pylage.UI.components.alert` verified.
- Alert is included in the public `__all__` export chain.
- Manual example: `demo/demo_alert.py`.

## Status

Alert is complete for Phase 09.
