# UI Kit Dialog

## Overview

`dialog()` provides a semantic, high-level dialog component for modal-style content and user interactions.

The UI Kit Dialog is a thin wrapper around the existing PyLage engine `Dialog` component. It does not introduce a new renderer, runtime, or dialog engine.

## Basic Usage

```python
import pylage as pl

pl.dialog(
    pl.text("Are you sure you want to continue?"),
    open=True,
)
```

## Composition

Dialog accepts existing PyLage components as children and preserves component composition.

```python
import pylage as pl

pl.dialog(
    pl.heading("Confirm Action", level=3),
    pl.text("This action cannot be undone."),
    pl.button("Confirm"),
    open=True,
)
```

Existing PyLage components remain valid children of the dialog.

## Open State

The `open` property can be controlled with a boolean or an existing PyLage reactive `State`.

```python
import pylage as pl

is_open = pl.State(False)

pl.dialog(
    pl.text("Reactive dialog"),
    open=is_open,
)

is_open.set(True)
```

When the state changes, the underlying PyLage Dialog uses the existing reactive rendering behavior.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Dialog content or existing PyLage components |
| `style` | `Style` | `None` | Custom style overrides |
| `**props` | `Any` | — | Forwarded to the underlying PyLage Dialog |

The `open` property is forwarded through `**props` to the existing PyLage Dialog.

## Styling

The wrapper applies UI Kit design tokens for spacing, surface color, text color, border, and radius. A supplied `style` is merged last so developers can override the default styling.

## Architecture

```text
pl.dialog()
    ↓
UI Kit dialog wrapper
    ↓
PyLage ENGINE Dialog
    ↓
Existing PyLage <dialog> renderer
```

This implementation follows the UI Kit architecture by reusing the existing engine component instead of duplicating dialog rendering or reactive infrastructure.

## Verification

- UI Kit Dialog tests: 8 passed.
- Direct dialog import verified through `pylage.UI.components.dialog`.
- Public UI API verified through `pylage.UI.dialog`.
- Basic `<dialog>` rendering verified.
- Boolean `open` behavior verified.
- Reactive `State`-controlled `open` behavior verified.
- Engine props forwarding verified.
- Custom style override verified.
- Component child preservation verified.
- Manual example: `demo/demo_dialog.py`.

## Status

Dialog is complete for Phase 09.
