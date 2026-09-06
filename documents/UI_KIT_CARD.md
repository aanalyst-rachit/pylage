# UI Kit Card

`pylage.card()` provides a semantic, high-level Card API while reusing the existing PyLage Card and primitive components.

## Basic usage

```python
import pylage as pl

pl.card(heading="Revenue", body="₹42,000", footer="Monthly revenue")
```

## Optional sections

```python
pl.card(heading="Revenue", body="₹42,000")
pl.card(body="Nothing to show")
```

## Variants

Supported variants:

- `default`
- `elevated`
- `outlined`
- `interactive`

```python
pl.card(heading="Active Users", body="12,450", variant="elevated")
```

## Interactive card

Cards support the existing PyLage event system:

```python
pl.card(
    heading="Click me",
    body="Interactive content",
    variant="interactive",
    on_click=handle_click,
)
```

Event handling uses the existing PyLage runtime event delegation.

## Advanced composition

Existing PyLage children remain supported:

```python
import pylage as pl

pl.card(
    pl.column(
        pl.heading("Custom Header"),
        pl.text("Custom body"),
    ),
    variant="elevated",
)
```

The UI Kit does not introduce separate CardHeader, CardBody, or CardFooter engine components. Semantic sections are composed from existing PyLage primitives.

## Custom styling

Use `style=` for customization:

```python
import pylage as pl

pl.card(
    heading="Revenue",
    body="₹42,000",
    style=pl.style(background_color="#f8fafc"),
)
```
