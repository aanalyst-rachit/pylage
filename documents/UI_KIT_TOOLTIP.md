# PyLage UI Kit — Tooltip

## Purpose

The UI Kit Tooltip recipe provides a thin, reusable wrapper around the existing PyLage Tooltip component.

The UI Kit does not duplicate tooltip rendering, browser behavior, or client-side interaction logic.

## Architecture

- Public API: `pylage.UI.recipes.tooltip`
- Underlying component: existing `pylage.ENGINE.Tooltip`
- Rendering: existing PyLage renderer
- Interaction behavior: native HTML `title` behavior provided by the existing Tooltip implementation
- `client.py`: untouched

## API

```python
import pylage as pl

component = pl.tooltip(
    pl.text("Info"),
    title="Helpful information",
)
```

The recipe accepts arbitrary children and forwards props to the existing Tooltip component.

## Behavior

- Renders through the existing Tooltip component.
- Supports existing Tooltip props such as `title` and `class_name`.
- Preserves child components.
- Does not introduce a second tooltip implementation.

## Regression Coverage

Existing Tooltip tests:

- `test/test_tooltip_component.py` — 3 tests

UI Kit wrapper tests:

- `test/test_ui_kit_tooltip.py` — 2 tests

Focused verification result:

```text
5 passed
```

## Manual Verification

Manual application:

- `demo/demo_tooltip.py`

Verified:

- UI Kit Tooltip heading renders.
- Button tooltip target renders.
- Text tooltip target renders.
- Native title tooltip behavior works on hover.
- Layout renders correctly.

## Design Boundary

Tooltip is implemented as a WRAP recipe because the underlying PyLage Tooltip component already exists and provides the required behavior.

No new renderer, reactive engine, WebSocket behavior, or client-side tooltip system was introduced.

## Phase 09 Status

Tooltip is complete.

Phase 09 Feedback & Overlays is now complete; Toast is resolved and verified.
