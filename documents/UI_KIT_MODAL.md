# UI Kit Modal

## Overview

`modal()` provides a reusable, high-level modal recipe for focused content, confirmation flows, and modal-style interactions.

The UI Kit Modal is a composition of the existing UI Kit `dialog()` and `card()` components. It does not introduce a new engine component, renderer, or reactive runtime.

## Basic Usage

```python
import pylage as pl

pl.modal(
    pl.text("Are you sure you want to continue?"),
    open=True,
)
```

## Composition

Modal composes a UI Kit Dialog with a UI Kit Card. Existing PyLage components remain valid as modal content.

```python
import pylage as pl

pl.modal(
    pl.heading("Confirm Action", level=3),
    pl.text("This action cannot be undone."),
    pl.button("Confirm"),
    open=True,
)
```

The supplied content is preserved as a child of the internal Card.

## Title

The optional `title` parameter provides semantic modal title content. It is composed into the internal Card rather than forwarded as a native Dialog property.

```python
import pylage as pl

pl.modal(
    pl.text("This action cannot be undone."),
    title=pl.heading("Confirm Action", level=3),
    open=True,
)
```

## Open State

The `open` parameter accepts a boolean or an existing PyLage reactive `State`.

```python
import pylage as pl

is_open = pl.State(False)

pl.modal(
    pl.text("Reactive modal"),
    open=is_open,
)

is_open.set(True)
```

The existing reactive behavior of the underlying Dialog controls the rendered `open` state.

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `content` | `Any` | — | Main modal content |
| `open` | `Any` | `False` | Boolean or reactive state controlling visibility |
| `title` | `Any` | `None` | Optional title content composed into the Card |
| `style` | `Style` | `None` | Custom style applied to the internal Card |
| `**props` | `Any` | — | Props forwarded to the underlying UI Kit Dialog |

## Styling

The recipe applies UI Kit spacing to the internal Card. A supplied `style` is merged into that Card styling so developers can customize modal content presentation.

Dialog-level properties such as `class_name` can be supplied through `**props` and are forwarded to the underlying UI Kit Dialog.

## Architecture

```text
pl.modal()
    ↓
UI Kit modal recipe
    ↓
UI Kit dialog() + UI Kit card()
    ↓
Existing PyLage ENGINE Dialog + Card
    ↓
Existing PyLage rendering and reactive infrastructure
```

This implementation follows the UI Kit architecture by composing existing primitives instead of duplicating modal, dialog, card, rendering, or reactive infrastructure.

## Verification

- Manual UI verification completed successfully.
- Modal composition tests verified Dialog and Card structure.
- Boolean `open` behavior verified.
- Reactive `State`-controlled `open` behavior verified.
- Title composition verified.
- Dialog prop forwarding verified.
- Custom Card style override verified.
- Existing component content preservation verified.
- Public `pylage.UI.recipes.modal` import verified.
- Full test suite: 897 passed.
- Manual example: `demo/demo_modal.py`.

## Status

Modal recipe is complete for Phase 09.
