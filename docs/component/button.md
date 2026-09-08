# PyLage UI Kit — Button

## Definition

`pl.button()` provides a semantic button API for the PyLage UI Kit. It reuses the existing PyLage `Button` component and renderer while adding UI Kit variants, sizes, and semantic styling.

## Use

Use `pl.button()` for primary actions, secondary actions, navigation actions, destructive actions, form submission, and other interactive controls that require a clickable button.

## Usage

### Basic Button

```python
import pylage as pl

button = pl.button("Save")
```

### Variants

```python
import pylage as pl

pl.button("Primary")
pl.button("Secondary", variant="secondary")
pl.button("Outline", variant="outline")
pl.button("Ghost", variant="ghost")
pl.button("Danger", variant="danger")
```

Supported variants:

- `primary`
- `secondary`
- `outline`
- `ghost`
- `danger`

The default variant is `primary`.

### Sizes

```python
import pylage as pl

pl.button("Small", size="sm")
pl.button("Medium", size="md")
pl.button("Large", size="lg")
```

Supported sizes:

- `sm`
- `md`
- `lg`

The default size is `md`.

### Click Events

```python
import pylage as pl

def save():
    print("saved")

pl.button("Save", on_click=save)
```

The `on_click` callback is forwarded to the existing PyLage event system.

### Disabled State

```python
import pylage as pl

pl.button("Save", disabled=True)
```

The `disabled` property is forwarded to the underlying PyLage Button.

### Custom Styling

```python
import pylage as pl

pl.button(
    "Custom",
    style=pl.style(
        background_color="#123456",
        border_radius="999px",
    ),
)
```

Explicit custom styles take precedence over the UI Kit defaults.

### Style Preset with `bg`

The `bg` parameter accepts a PyLage `Style` and provides an intermediate style layer before the explicit `style` parameter.

```python
import pylage as pl

pl.button(
    "Save",
    bg=pl.style(background_color="#334155"),
)
```

## API

```python
button(
    text,
    *,
    variant="primary",
    size="md",
    bg=None,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Description | Default |
|---|---|---|
| `text` | Button content. | required |
| `variant` | Semantic visual variant. | `"primary"` |
| `size` | Semantic button size. | `"md"` |
| `bg` | Optional PyLage `Style` merged before explicit `style`. | `None` |
| `style` | Explicit PyLage `Style` overrides. | `None` |
| `**props` | Other supported PyLage Button properties, including events and state properties. | — |

## Validation

`variant` must be one of the supported variants. Invalid values raise `ValueError`.

`size` must be one of the supported sizes. Invalid values raise `ValueError`.

`bg` must be a PyLage `Style` or `None`. Invalid values raise `TypeError`.

## Styling Behavior

The component builds its default style from the base, variant, and size styles.

The final style is merged in this order:

1. UI Kit base style
2. Selected variant style
3. Selected size style
4. `bg` style, when supplied
5. Explicit `style`, when supplied

This means explicit custom styles have the highest precedence.

## API Boundary

`variant` and `size` are UI Kit semantic properties. They are consumed by the UI Kit and are not forwarded as renderer/component properties.

The implementation reuses the existing:

- `pl.button()`
- `PyLage Style`
- `pylage_layout.tokens.COLORS`
- PyLage event system
- PyLage renderer

The UI Kit therefore provides a higher-level developer API without introducing a second rendering system.

## Verified Working Example

The primary executable example is maintained in `demo/demo_button.py`. It demonstrates basic, primary, large, outline, danger, and custom-styled buttons together with click handling.

## Verification

The implementation and tests verify:

- Existing PyLage `Component` and `Button` types are returned.
- Default `primary` variant and `md` size are applied.
- All five variants are supported.
- All three sizes are supported.
- Custom styles override variant and size styles.
- `disabled` is forwarded and rendered.
- `on_click` is forwarded.
- Invalid variants raise `ValueError`.
- Invalid sizes raise `ValueError`.
- `variant` and `size` do not leak into engine properties.
- Primary and secondary hover behavior is rendered correctly.

## Verified Sources

- Component source: `pylage/UI/components/button.py`
- Demo: `demo/demo_button.py`
- Tests: `test/components/test_ui_kit_button.py`
- Browser test: `test/browser/test_button_hover.py`
- Reference documentation: `documents/button.md`

## Status

**Verified against the current Button implementation and test coverage.**
