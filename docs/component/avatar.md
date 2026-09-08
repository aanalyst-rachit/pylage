# PyLage UI Kit — Avatar

## Definition

`pl.avatar()` provides a semantic avatar component for the PyLage UI Kit. It reuses the existing PyLage `Avatar` component while adding consistent UI Kit sizing and styling.

## Use

Use `pl.avatar()` to display user initials, names, images, or other compact identity content.

## Usage

### Basic Avatar

```python
import pylage as pl

pl.avatar("RK")
```

### Sizes

```python
import pylage as pl

pl.avatar("RK", size="sm")
pl.avatar("RK", size="md")
pl.avatar("RK", size="lg")
```

Supported sizes:

| Size | Width | Height |
|---|---:|---:|
| `sm` | `32px` | `32px` |
| `md` | `40px` | `40px` |
| `lg` | `48px` | `48px` |

The default size is `md`.

### Component Content

`pl.avatar()` accepts one or more children.

Plain values are normalized into existing PyLage `Text` components, while existing PyLage components are preserved.

```python
import pylage as pl

pl.avatar("Rachit Kumar", size="lg")
```

Existing components such as `Image` can also be supplied as children.

```python
import pylage as pl

pl.avatar(
    pl.image(
        src="https://example.com/avatar.png",
        alt="User",
    )
)
```

`None` children are ignored during child normalization.

### Custom Styling

Explicit `style` values override the UI Kit defaults.

```python
import pylage as pl

pl.avatar(
    "RK",
    style=pl.style(
        border_radius="8px",
    ),
)
```

## API

```python
avatar(*children, size="md", style=None, **props)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Avatar content or existing PyLage components. |
| `size` | `str` | `"md"` | Semantic avatar size. |
| `style` | `Style` | `None` | Custom style overrides. |
| `**props` | `Any` | — | Properties forwarded to the underlying PyLage Avatar. |

## Validation

`size` must be one of `sm`, `md`, or `lg`. An unknown value raises `ValueError`.

## Styling Behavior

The UI Kit builds the final Avatar style from a common base style and the selected size.

The base style provides:

- Inline-flex layout
- Centered content
- Circular border radius
- Hidden overflow
- Semibold content

The final style is merged in this order:

1. UI Kit base style
2. Selected size style
3. Explicit `style`, when supplied

Therefore, explicit custom styles take precedence over the UI Kit defaults.

## API Boundary

`size` is a UI Kit semantic property consumed by the wrapper and is not forwarded as an engine property.

The implementation reuses the existing:

- `pylage.ENGINE.Avatar`
- `PyLage Style`
- `pylage.ENGINE.Text`
- PyLage `Component`
- PyLage renderer

The UI Kit therefore provides a higher-level Avatar API without introducing a second rendering or styling system.

## Verified Working Example

The executable examples are maintained in:

- `demo/demo_avatar.py`
- `demo/demo_avatar_badge_divider.py`

These demos provide running Avatar usage and composition examples.

## Verification

The implementation and tests verify:

- The UI Kit returns the existing PyLage `Avatar` component.
- `sm`, `md`, and `lg` sizes are supported.
- The default size is `md`.
- Invalid sizes raise `ValueError`.
- Existing `Component` children are preserved.
- Plain child values are normalized to `Text` components.
- `None` children are ignored.
- Custom styles override UI Kit defaults.
- Additional engine properties can be forwarded through `**props`.

## Verified Sources

- Component source: `pylage/UI/components/avatar.py`
- Demos: `demo/demo_avatar.py`, `demo/demo_avatar_badge_divider.py`
- UI Kit tests: `test/components/test_ui_kit_avatar.py`
- Engine tests: `test/components/test_avatar.py`
- Reference documentation: `documents/avatar.md`

## Status

**Verified against the current Avatar implementation, demos, and test coverage.**
