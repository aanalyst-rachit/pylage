# PyLage UI Kit — Heading

## Definition

`heading` is the public PyLage UI Kit wrapper around the existing PyLage `Heading` component.

It provides a semantic heading with a consistent UI Kit default style while preserving the existing engine rendering and properties.

## Use

Use `heading()` for page titles, section headings, dashboard headings, and other semantic heading content.

## Usage

### Basic Heading

```python
import pylage as pl

pl.heading("Dashboard")
```

### Custom Styling

Custom styles can override the UI Kit defaults.

```python
import pylage as pl

pl.heading(
    "Revenue Overview",
    style=pl.style(
        color="#123456",
        font_weight="600",
    ),
)
```

## API

```python
heading(value, style=None, **props)
```

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `Any` | — | Heading content. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying PyLage `Heading`. |

## Default Styling

The UI Kit heading applies these default styles:

- `margin: 0`
- `color: var(--color-text)`
- `font_weight: 700`
- `line_height: 1.25`

Custom values supplied through `style` take precedence over the corresponding defaults.

## Styling Behavior

The final heading style is created by merging the UI Kit base style with the optional user-provided `style`.

This keeps the standard heading foundation while allowing individual visual properties to be customized.

## Architecture

The public wrapper reuses the existing PyLage heading implementation:

```text
pl.heading()
    ↓
UI Kit heading wrapper
    ↓
PyLage Heading
    ↓
Existing renderer
```

No duplicate heading renderer is introduced by the UI Kit wrapper.

## API Boundary

The UI Kit owns the public `heading()` entry point and its default styling.

The underlying PyLage `Heading` component remains responsible for rendering and supported component properties.

## Verified Working Example

The project demo is `demo/demo_heading.py`.

It demonstrates a basic heading and a heading with custom styling.

## Verification

The implementation is covered by:

- `test/components/test_ui_kit_heading.py`

The component test verifies the public heading wrapper and its behavior against the existing PyLage heading implementation.

## Verified Sources

- `pylage/UI/components/heading.py`
- `demo/demo_heading.py`
- `test/components/test_ui_kit_heading.py`
- `documents/heading.md`

## Status

**Heading documentation refined and verified.**
