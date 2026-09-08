# PyLage UI Kit — Popover

## Definition

`popover()` is a reusable UI Kit recipe that exposes the existing PyLage `Popover` component through the UI Kit recipe API.

The recipe does not introduce a separate popover renderer, overlay engine, positioning system, reactive mechanism, or client-side implementation. Existing PyLage Popover behavior remains the source of truth.

## Use

Use `popover()` when contextual content should be represented through the existing PyLage Popover component while using the public UI Kit recipe API.

```python
import pylage as pl

content = pl.popover(
    pl.text("Additional information"),
    title="More information",
    class_name="ui-kit-popover",
)
```

The recipe forwards the supplied children and properties directly to the existing Engine Popover implementation.

## Usage

### Basic popover

```python
import pylage as pl

popover = pl.popover(
    pl.text("Popover content"),
)
```

### Popover with properties

```python
import pylage as pl

popover = pl.popover(
    pl.text("Details"),
    title="Additional information",
    class_name="ui-kit-popover",
)
```

### Popover with multiple children

```python
import pylage as pl

popover = pl.popover(
    pl.text("Details"),
    pl.button("Close"),
)
```

Multiple children are passed through unchanged to the underlying Popover component.

## API

```python
popover(*children, **props)
```

### Parameters

| Parameter | Description |
|---|---|
| `*children` | Content children supplied directly to the underlying PyLage Popover. |
| `**props` | Properties forwarded directly to the underlying PyLage Popover. |

The UI Kit recipe does not define a separate Popover-specific property contract beyond the existing component API.

## Behavior

- Returns the existing PyLage Engine `Popover` component.
- Preserves all supplied children.
- Forwards supplied properties unchanged.
- The underlying Engine Popover renders as a `<div>`.
- Existing PyLage rendering and component infrastructure remain responsible for final DOM output.

The current verified contract includes `class_name` and `title` property forwarding, child preservation, and normal component rendering.

## Architecture

```text
pl.popover()
      ↓
UI Kit popover recipe
      ↓
Existing Engine Popover
      ↓
Existing PyLage renderer
      ↓
Browser DOM
```

The recipe is intentionally composition-free at the UI Kit level: it delegates directly to the existing Engine component instead of duplicating Popover behavior.

No separate overlay engine, positioning implementation, scheduler, WebSocket runtime, or client-side Popover implementation is introduced by the UI Kit recipe.

## API Boundary

The UI Kit recipe is a public convenience boundary around the existing Engine component.

```python
from pylage.UI.recipes import popover
```

The recipe is also exported through the public PyLage UI Kit API as `pl.popover`.

Core Popover behavior must be changed in the Engine implementation when required; the recipe should remain a thin delegation layer unless a deliberate UI Kit-specific composition requirement is introduced.

## Verified Working Example

- `demo/demo_popover.py` — manual Popover usage through the normal PyLage application runtime.
- `demo/demo_popover_tooltip.py` — combined Popover and Tooltip manual usage.

## Verification

### Automated tests

Focused Popover coverage is provided by:

- `test/components/test_popover.py` — core Popover rendering, property forwarding, and child rendering.
- `test/components/test_ui_kit_popover.py` — UI Kit recipe delegation, property preservation, and child preservation.
- `test/regression/test_templates_audit.py` — public recipe export, callability, and component-return contract.

The canonical documentation intentionally does not record a historical full-suite test count. Verification results are recorded from the focused regression run used for this documentation update.

### Manual verification

- `demo/demo_popover.py` — Popover behavior through the normal application runtime.

## Verified Sources

- Recipe: `pylage/UI/recipes/popover.py`
- Engine Popover: `pylage/ENGINE/components/basic.py`
- Engine exports: `pylage/ENGINE/components/__init__.py`, `pylage/ENGINE/__init__.py`
- UI Kit recipe exports: `pylage/UI/recipes/__init__.py`, `pylage/UI/__init__.py`
- Recipe tests: `test/components/test_ui_kit_popover.py`
- Core tests: `test/components/test_popover.py`
- Recipe audit: `test/regression/test_templates_audit.py`
- Manual example: `demo/demo_popover.py`

## Status

**FINAL / VERIFIED** — documentation reflects the current `popover()` recipe implementation, its direct delegation boundary, child and property forwarding behavior, public export, and available verification coverage.
