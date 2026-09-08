# PyLage UI Kit — Divider

## Definition

`divider()` is the PyLage UI Kit wrapper around the existing PyLage `Divider` engine component. It provides a semantic horizontal separator with UI Kit styling defaults.

## Use

Use `divider()` to visually separate sections of content while keeping the separator consistent with the PyLage design system.

- Horizontal content separation
- Full-width layout separation
- Custom border and spacing through `Style`
- Additional engine properties through `**props`

## Usage

### Basic divider

```python
import pylage as pl

pl.divider()
```

### Custom styling

```python
import pylage as pl

pl.divider(
    style=pl.style(
        border_top="2px solid #111827",
        margin="2rem 0",
    )
)
```

The supplied `Style` overrides the corresponding UI Kit defaults.

### Inside a layout

```python
import pylage as pl

pl.column(
    pl.heading("Profile", level=2),
    pl.text("Account information"),
    pl.divider(),
    pl.text("Additional settings"),
)
```

## API

```python
divider(*, style=None, **props)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `style` | Optional PyLage `Style` merged over the default divider style. |
| `**props` | Additional properties forwarded to the underlying PyLage `Divider`. |

## Default Styling

The UI Kit applies these defaults:

- `width: 100%`
- `border: 0`
- `border-top: 1px solid var(--color-border)`
- `margin: 1rem 0`

The default `border` removes the browser default border styling, while `border-top` provides the visible separator.

## Styling Behavior

The final style is created by merging the UI Kit defaults with the optional `style` argument:

```python
final_style = _DEFAULT_STYLE.merge(style)
```

Explicit style values therefore override matching defaults while unspecified defaults remain active.

## Architecture

`divider()` does not implement a separate renderer or primitive. It delegates rendering to the existing engine `Divider` component.

`Application → pl.divider() → ENGINE Divider → existing renderer/runtime`

The wrapper is responsible for the public UI Kit API and default styling; engine behavior remains in the underlying `Divider` implementation.

## API Boundary

The UI Kit wrapper explicitly handles the public `style` argument, merges it with the default style, and forwards the resulting style and remaining properties to the engine `Divider`.

## Verified Working Example

The project demo `demo/demo_divider.py` demonstrates the divider as part of composed PyLage layouts and styling examples.

```python
import pylage as pl

pl.divider()
```

## Verification

Verified coverage includes:

- UI Kit divider creation
- Wrapping of the existing engine `Divider`
- Default width, border, border-top, and margin styling
- Custom `Style` merging
- Property forwarding
- Public UI Kit API exposure
- Divider rendering behavior

## Verified Sources

- `pylage/UI/components/divider.py`
- `demo/demo_divider.py`
- `demo/demo_avatar_badge_divider.py`
- `test/components/test_divider.py`
- `test/components/test_ui_kit_divider.py`
- `documents/divider.md` (reference/archive)

## Status

Divider documentation is refined against the current implementation, demo coverage, and verified tests.
