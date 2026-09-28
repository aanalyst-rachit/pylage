# Styling & Themes API

Canonical URI: `/api/styling/`

PyLage styling APIs provide declarative styles, color definitions, and application theme control.

## `pl.style`

Creates or applies declarative styling.

```python
box = pl.container(
    pl.text("Hello"),
    style=pl.style(
        padding="1rem",
        border_radius="8px",
    ),
)
```

## `pl.colors`

Provides the public color definitions used by PyLage styling and themes.

## `pl.set_theme`

Sets the active application theme.

```python
pl.set_theme("dark")
```

## `pl.get_current_theme`

Returns the currently active theme.

```python
current = pl.get_current_theme()
```

## `pl.theme`

Provides the public theme facade.

## Related documentation

- [API Conventions](../helper/api_conventions.md)

## Implementation references

- `pylage/UI/style/`
- `pylage/UI/theme/`
- `pylage/__init__.py`
