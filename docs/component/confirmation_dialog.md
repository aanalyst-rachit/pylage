# PyLage UI Kit — Confirmation Dialog

## Definition

`confirmation_dialog` is a reusable PyLage UI Kit recipe for confirmation flows that require an explicit confirm or cancel action.

It composes the existing UI Kit `dialog`, `button`, and `row` components rather than introducing a separate dialog renderer or event system.

## Use

Use `confirmation_dialog()` when an action should be presented with a clear confirmation step, such as deleting an item, submitting a destructive action, or accepting a user decision.

## Usage

### Basic Confirmation

```python
import pylage as pl

pl.confirmation_dialog(
    "Delete this item?",
    title="Delete Item",
)
```

### Open State and Callbacks

The `open` property controls the underlying Dialog. Confirm and cancel callbacks are forwarded to their respective Button components when supplied.

```python
import pylage as pl

open_state = pl.state(False)

def confirm_delete(*args):
    print("confirmed")

def cancel_delete(*args):
    open_state.set(False)

pl.confirmation_dialog(
    "Delete this item?",
    title="Delete Item",
    open=open_state,
    on_confirm=confirm_delete,
    on_cancel=cancel_delete,
)
```

### Custom Button Text

Use `confirm_text` and `cancel_text` to customize the action labels.

```python
import pylage as pl

pl.confirmation_dialog(
    "Publish this article?",
    title="Publish",
    confirm_text="Publish",
    cancel_text="Not now",
)
```

### Confirm Button Variant

`confirm_variant` is passed to the confirm Button. This is useful for destructive confirmations.

```python
import pylage as pl

pl.confirmation_dialog(
    "This action cannot be undone.",
    title="Delete permanently?",
    confirm_text="Delete",
    confirm_variant="danger",
)
```

### Custom Dialog Styling

Custom styles are forwarded to the underlying UI Kit Dialog.

```python
import pylage as pl

pl.confirmation_dialog(
    "Continue with this action?",
    style=pl.style(max_width="32rem"),
)
```

## API

```python
confirmation_dialog(
    message,
    *,
    title=None,
    open=False,
    on_confirm=None,
    on_cancel=None,
    confirm_text="Confirm",
    cancel_text="Cancel",
    confirm_variant="primary",
    style=None,
    **props,
)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `message` | `Any` | — | Main confirmation message content. |
| `title` | `Any` | `None` | Optional dialog title. |
| `open` | `Any` | `False` | Initial or reactive open value passed to the Dialog. |
| `on_confirm` | `Any` | `None` | Callback assigned to the confirm Button when provided. |
| `on_cancel` | `Any` | `None` | Callback assigned to the cancel Button when provided. |
| `confirm_text` | `Any` | `"Confirm"` | Label for the confirm Button. |
| `cancel_text` | `Any` | `"Cancel"` | Label for the cancel Button. |
| `confirm_variant` | `str` | `"primary"` | Button variant used for the confirm action. |
| `style` | `Style \\| None` | `None` | Custom style passed to the Dialog. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying Dialog. |

## Content Composition

The recipe builds its content in this order:

1. The optional `title`, when provided.
2. The `message`, when it is not `None`.
3. A right-aligned action row containing Cancel and Confirm buttons.

The action row uses the UI Kit Row component with:

- `display: flex`
- `justify_content: flex-end`
- `gap: var(--spacing-sm)`
- `margin_top: var(--spacing-lg)`

## Callback Handling

Callbacks are only added to the Button properties when they are provided. A missing callback is therefore omitted instead of being passed as an event handler with a `None` value.

This preserves the existing PyLage Button event contract.

## Reactive Open State

The `open` value is passed directly to the underlying UI Kit Dialog. Reactive open behavior therefore remains owned by the existing Dialog implementation rather than being duplicated by the confirmation recipe.

## Architecture

```text
pl.confirmation_dialog()
    ↓
UI Kit confirmation recipe
    ├── UI Kit Dialog
    ├── UI Kit Row
    └── UI Kit Button × 2
```

The recipe owns the confirmation-flow composition and action configuration. Dialog rendering, Button events, Row layout, state handling, and the underlying renderer remain owned by the existing PyLage components.

## API Boundary

`confirmation_dialog()` is a composition recipe, not a new low-level component implementation.

It reuses the existing public UI Kit APIs and forwards Dialog properties through `**props`.

## Verified Working Example

The project provides an executable confirmation-dialog demo:

- `demo/demo_confirmation_dialog.py`

The demo exercises the confirmation flow through the normal PyLage application runtime.

## Verification

Focused coverage is provided by:

- `test/components/test_ui_kit_confirmation_dialog.py`

The test suite covers composition, content and actions, optional title, open-state behavior, callback forwarding, confirm variants, custom styling, and public recipe export.

## Verified Sources

- `pylage/UI/recipes/confirmation_dialog.py`
- `demo/demo_confirmation_dialog.py`
- `test/components/test_ui_kit_confirmation_dialog.py`
- `docs/helper/confirmation_dialog.md`

## Status

**Confirmation Dialog documentation refined and verified.**
