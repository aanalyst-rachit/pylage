# UI Kit Empty State

`pylage_ui.empty_state()` provides a semantic, high-level placeholder component for empty views, zero-data tables, and pending lists while reusing existing PyLage layout tokens and primitives.

## Basic Usage

```python
import pylage as pl

pl.empty_state(
    title="No projects found",
    description="You have not created any projects yet.",
)
```

## With Icon and Action Button

```python
import pylage as pl

pl.empty_state(
    title="No items in cart",
    description="Explore our catalog and add items to your cart.",
    icon="🛒",
    action=pl.button("Browse Products", variant="primary"),
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `title` | `Any` | `"No data found"` | Heading text or component |
| `description` | `Any` | `"There are no items..."` | Descriptive guidance text |
| `icon` | `Any` | `None` | Emoji string or custom icon component |
| `action` | `Any` | `None` | Primary or secondary action button |
| `style` | `Style` | `None` | Style overrides merged with default card style |
| `**props` | `Any` | — | Forwarded to root component |

## Custom Styling

```python

import pylage as pl

pl.empty_state(
    title="No records",
    style=pl.style(padding="4rem", background_color="#fafafa"),
)
```
