# UI Kit Badge

`pl.badge()` provides a semantic UI Kit wrapper around the existing PyLage `Badge` primitive.

## Basic usage

```python
import pylage as pl

pl.badge("Active")
```

## Variants

```python
pl.badge("Default")
pl.badge("Primary", variant="primary")
pl.badge("Secondary", variant="secondary")
pl.badge("Success", variant="success")
pl.badge("Warning", variant="warning")
pl.badge("Danger", variant="danger")
pl.badge("Info", variant="info")
```

Supported variants:

- `default`
- `primary`
- `secondary`
- `success`
- `warning`
- `danger`
- `info`

## Styling

Badges receive UI Kit defaults for compact padding, full radius, small typography, semibold text, and semantic background, text, and border colors.

Custom styling can override the defaults:

```python


pl.badge(
    "Custom",
    style=pl.style(
        font_size="0.875rem",
        padding="0.5rem 0.75rem",
    ),
)
```

## Composition

Component children remain supported:

```python
import pylage as pl

pl.badge(pl.text("Active"))
```

Primitive children are composed through the existing PyLage `Text` primitive rather than introducing a new renderer or Badge content engine.

Reactive values are also supported through the existing PyLage state system.

## Props and events

Existing PyLage props and event callbacks can be forwarded.

## Architecture

```text
Developer
    ↓
pylage_ui.badge()
    ↓
semantic UI Kit defaults
    ↓
pylage.Badge + pylage.Text
    ↓
existing PyLage renderer
```

The UI Kit does not introduce a new Badge renderer, styling engine, or state system.
