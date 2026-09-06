# PyLage UI Kit — Divider

## Overview

`pl.divider()` provides a semantic horizontal separator using the existing PyLage `Divider` primitive.

## API

```python
import pylage as pl

pl.divider()
```

## Default behavior

The UI Kit applies sensible defaults:

- Full available width
- No default browser border
- Semantic muted top border
- Vertical margin for visual separation

## Customization

A PyLage `Style` can override the defaults:

```python


pl.divider(
    style=pl.style(
        border_top="2px solid #111827",
        margin="2rem 0",
    )
)
```

## Architecture

The UI Kit does not introduce a new renderer or primitive. `pl.divider()` wraps the existing `pylage.Divider` and adds the semantic UI Kit styling contract.

Engine props and events are forwarded to the underlying component.
