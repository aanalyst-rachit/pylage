# PyLage UI Kit — Row

## Purpose

The UI Kit Row wrapper provides a stable layout-level API around the existing PyLage `Row` component.

## Architecture

Row is implemented as a thin WRAP layer. The UI Kit does not introduce a new layout engine, renderer, reactive system, CSS engine, or component implementation.

The wrapper delegates to the existing PyLage `Row` component and uses the established UI Kit responsive style resolution.

## API

```python
import pylage as pl

pl.row(
    pl.text("First"),
    pl.text("Second"),
    class_name="content-row",
)
```

The wrapper accepts arbitrary children, filters `None` children, forwards supported properties, and accepts `Style` or `ResponsiveStyle` values.

## Existing Core Contract

The underlying PyLage `Row` renders as a `<div>` and supports the existing `class_name` and `title` properties.

No core Row implementation was duplicated or modified.

## Responsive Style

When no custom style is supplied, the wrapper uses the existing `resolve_style()` convention from the UI Kit layout layer.

Custom styles are forwarded without replacing the underlying PyLage style system.

## Regression Coverage

Coverage includes:

- core Row wrapping
- Row rendering
- property forwarding
- custom style support
- default responsive style resolution
- reactive style values
- component child preservation
- `None` child filtering
- public layout export
- existing Phase 09 layout contract compatibility

Focused verification completed with **14 tests passed**.

## Design Boundary

The UI Kit intentionally does not create a second Row implementation. Existing PyLage Row behavior remains the source of truth.

## Workflow

reuse/create/------>manual create-------> manual verify----> documentation----->tracker update---git checkpoint

rules - PYTHON TERMINAL RULE + MD FILE RULE
