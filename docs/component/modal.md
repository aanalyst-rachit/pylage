# PyLage UI Kit — Modal

## Definition

`modal()` is a reusable UI Kit recipe that composes the existing `dialog()` and `card()` components into a focused modal content container.

It does not introduce a separate modal engine component, renderer, positioning system, or reactive runtime. Existing PyLage Dialog and Card behavior remain the source of truth.

## Use

Use `modal()` when content should be presented through the existing PyLage Dialog infrastructure with UI Kit Card-based content presentation.

```python
import pylage as pl

content = pl.modal(
    pl.text("Are you sure you want to continue?"),
    open=True,
 )
```

The modal content is placed inside the internal UI Kit Card, which is then supplied to the existing UI Kit Dialog.

## Usage

### Basic modal

```python
import pylage as pl

content = pl.modal(
    pl.text("Are you sure you want to continue?"),
    open=True,
 )
```

### Modal with title and actions

```python
import pylage as pl

content = pl.modal(
    pl.column(
        pl.text("This action cannot be undone."),
        pl.button("Confirm"),
    ),
    title=pl.heading("Confirm Action", level=3),
    open=True,
 )
```

The optional `title` is composed into the internal Card before the supplied `content`.
The supplied content remains a child of that Card.

## Open State

The `open` parameter accepts a value supported by the underlying Dialog, including a boolean or reactive `State`.

```python
import pylage as pl

is_open = pl.state(False)

modal = pl.modal(
    pl.text("Reactive modal"),
    open=is_open,
 )

is_open.set(True)
is_open.set(False)
```

The `open` value is passed to the existing UI Kit Dialog. Reactive updates therefore use the established PyLage reactive property infrastructure rather than a modal-specific implementation.

## Title Composition

The `title` parameter is handled by the modal recipe itself.
When supplied, it is added to the internal Card before the main `content`; it is not forwarded as a Dialog property.

```python
import pylage as pl

modal = pl.modal(
    pl.text("This action cannot be undone."),
    title=pl.heading("Confirm Action", level=3),
    open=True,
 )
```

## Styling

The recipe applies a default Card padding of `var(--spacing-lg)`.
A supplied `style` is merged with this base style and applied to the internal Card.

```python
import pylage as pl

modal = pl.modal(
    pl.text("Styled modal content"),
    style=pl.style(padding="2rem"),
    open=True,
 )
```

The style customizes the Card content presentation; it does not replace the underlying Dialog implementation.

## API

```python
modal(content, *, open=False, title=None, style=None, **props)
```

### Parameters

| Parameter | Description |
|---|---|
| `content` | Main modal content supplied to the internal Card. |
| `open` | Value passed to the underlying UI Kit Dialog to control its open state. |
| `title` | Optional content inserted into the internal Card before `content`. |
| `style` | Optional `Style` merged with the modal Card base style. |
| `**props` | Additional properties forwarded to the underlying UI Kit Dialog. |

## Behavior

- Creates an internal UI Kit Card for modal content.
- Applies `padding="var(--spacing-lg)"` as the Card base style.
- Merges a supplied `style` into the Card base style.
- Inserts `title` into the Card before the supplied `content` when `title` is not `None`.
- Passes the resulting Card to the existing UI Kit `dialog()`.
- Passes `open` to the existing Dialog implementation.
- Forwards additional `**props` to the existing UI Kit Dialog.
- Reuses the existing PyLage rendering and reactive infrastructure.

## Architecture

```text
pl.modal()
      ↓
UI Kit modal recipe
      ↓
UI Kit dialog() + UI Kit card()
      ↓
Existing Engine Dialog + Card
      ↓
Existing PyLage renderer / reactive runtime
      ↓
Browser DOM
```

The recipe is intentionally composition-based. No duplicate modal renderer, overlay engine, scheduler, WebSocket runtime, or client-side modal implementation is introduced.

## Verified Working Example

- `demo/demo_modal.py` — manual modal usage through the normal PyLage application runtime.

## Verification

### Automated tests

Focused Modal coverage is provided by:

- `test/components/test_ui_kit_modal.py` — modal composition, rendering, open state, reactive open state, title composition, style handling, property forwarding, and content preservation.
- `test/components/test_ui_kit_dialog.py` — underlying UI Kit Dialog behavior used by the recipe.
- `test/components/test_dialog.py` — underlying Engine Dialog behavior.

### Manual verification

- `demo/demo_modal.py` — modal behavior through the normal application runtime.

The canonical documentation intentionally does not record a historical full-suite test count. Verification results are recorded from the focused regression run used for this documentation update.

## Verified Sources

- Recipe: `pylage/UI/recipes/modal.py`
- UI Kit Dialog: `pylage/UI/components/dialog.py`
- UI Kit Card: `pylage/UI/components/card.py`
- Recipe exports: `pylage/UI/recipes/__init__.py`, `pylage/__init__.py`
- Recipe tests: `test/components/test_ui_kit_modal.py`
- Dialog tests: `test/components/test_ui_kit_dialog.py`, `test/components/test_dialog.py`
- Manual example: `demo/demo_modal.py`

## Status

**FINAL / VERIFIED** — documentation reflects the current `modal()` recipe implementation, its Dialog/Card composition boundary, styling behavior, open-state forwarding, and available verification coverage.