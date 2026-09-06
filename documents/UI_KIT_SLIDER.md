# UI Kit Slider

## Overview

PyLage UI Kit `slider()` is the public Python-first slider control. It reuses the existing PyLage Engine `Slider` implementation and exposes it through the public `pylage` namespace.

## Public API

```python
import pylage as pl

slider = pl.slider(
    value=50,
    min=0,
    max=100,
    step=5,
)
```

## Supported Behavior

- Initial slider value rendering
- Minimum, maximum, and step configuration
- State-backed slider values
- Browser input events updating bound `State`
- Custom `on_input` callbacks preserved together with State binding
- Reactive State updates
- Standard slider attributes supported by the existing engine registry

## State Binding

```python
value = pl.State(25)

slider = pl.slider(
    value=value,
    min=0,
    max=100,
    step=5,
)
```

When the browser slider changes, the bound `State` is updated. Programmatic State changes remain reactive through the existing PyLage binding system.

When a custom `on_input` callback is supplied, PyLage updates the bound State and then preserves the user callback.

## Manual Verification

Manual application:
`demo/demo_slider.py`

Verified manually in the browser:

- Basic slider
- Custom range slider
- State-bound slider
- Custom input event handling
- Disabled slider
- Native slider properties

## Automated Verification

- Slider unit/public tests: 16 passed
- Slider browser regression tests: 2 passed
- Manual browser verification: PASS

## Architecture Decision

Slider is **REUSE**: the existing Engine `Slider` implementation and public UI wrapper are reused. No duplicate slider engine implementation was created.

Phase 08 — Forms: Slider COMPLETE.
