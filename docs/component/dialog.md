# PyLage UI Kit — Dialog

## Definition

`dialog()` is the PyLage UI Kit wrapper around the existing PyLage `Dialog` engine component. It provides a high-level dialog container for modal-style content while reusing the existing rendering and reactive infrastructure.

## Use

Use `dialog()` when an application needs modal-style content that can be opened or closed with a boolean or reactive state.

- Modal-style content rendered as a native HTML `<dialog>` element
- Existing PyLage components as dialog children
- Boolean `open` control
- Reactive `State` control for `open`
- Engine property forwarding such as `title` and `class_name`
- Custom `Style` overrides
- Component composition without replacing child components

## Usage

### Basic dialog

```python
import pylage as pl

pl.dialog(
    pl.text("Are you sure you want to continue?"),
    open=True,
)
```

### Composed dialog

```python
import pylage as pl

pl.dialog(
    pl.heading("Confirm Action", level=3),
    pl.text("This action cannot be undone."),
    pl.button("Confirm"),
    open=True,
)
```

Existing PyLage components are preserved as dialog children.

### Reactive open state

```python
import pylage as pl

is_open = pl.state(False)

pl.dialog(
    pl.text("Reactive dialog"),
    open=is_open,
)

is_open.set(True)
```

Changing the bound state updates the rendered `open` state of the underlying dialog.

## API

```python
dialog(*children, style=None, **props)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `*children` | Dialog content and existing PyLage components. `None` children are ignored. |
| `style` | Optional PyLage `Style` merged over the UI Kit default style. |
| `open` | Boolean or reactive `State` controlling whether the dialog is open. Forwarded to the engine. |
| `title` | Optional dialog title forwarded to the engine. |
| `class_name` | Optional CSS class forwarded to the engine. |
| `**props` | Other properties supported by the underlying PyLage `Dialog`. |

## Open State

The `open` property is forwarded to the underlying engine `Dialog` and supports both static booleans and reactive `State` values.

With `open=False`, the rendered dialog does not contain the HTML `open` attribute. With `open=True`, the attribute is present.

When a `State` is supplied, changing the state from `False` to `True` updates the rendered dialog accordingly.

## Composition

`dialog()` accepts existing PyLage components as positional children. The UI Kit wrapper removes `None` children but otherwise preserves supplied components.

```python
import pylage as pl

content = pl.card(
    pl.heading("Deployment", level=3),
    pl.text("Review the deployment before continuing."),
)

pl.dialog(
    content,
    open=True,
)
```

## Styling

The UI Kit wrapper applies the following default dialog style:

- `padding: var(--spacing-lg)`
- `background-color: var(--color-background)`
- `color: var(--color-text)`
- `border: 1px solid var(--color-border)`
- `border-radius: var(--radius-xl)`

An explicitly supplied `style` is merged over these defaults.

```python
import pylage as pl

pl.dialog(
    pl.text("Custom dialog"),
    style=pl.style(padding="32px"),
    open=True,
)
```

## Architecture

The UI Kit Dialog does not implement a separate renderer or runtime. It delegates to the existing engine component:

`Application → pl.dialog() → ENGINE Dialog → existing renderer/runtime`

This keeps dialog rendering and reactive behavior in the existing engine while the UI Kit wrapper provides the public API and default styling.

## API Boundary

`dialog()` explicitly handles the public `style` argument, removes `None` children, merges the UI Kit default style, and forwards the remaining properties to the engine `Dialog`.

The wrapper does not introduce a separate modal state system, renderer, or browser implementation.

## Verified Working Example

The project demo `demo/demo_dialog.py` demonstrates a state-controlled dialog containing a card, heading, text, and action buttons. The buttons update the same `State` to close the dialog and update an action log.

```python
import pylage as pl

dialog_open = pl.state(False)

dialog_modal = pl.dialog(
    pl.card(
        pl.heading("Confirm System Deployment", level=3),
        pl.text("Are you sure you want to deploy the updated PyLage components to production?"),
    ),
    open=dialog_open,
    title="Deployment Modal",
    class_name="pylage-dialog-overlay",
)
```

## Related Recipe

`confirmation_dialog()` is a separate higher-level recipe built on the same dialog infrastructure. Its verified behavior includes confirmation/cancellation actions, configurable button text, reactive open state, callbacks, and a confirm-button variant.

It is documented separately from the base `dialog()` component.

## Verification

Verified coverage includes:

- UI Kit wrapper returns the existing engine `Dialog` component
- Native `<dialog>` rendering
- Text and component child rendering
- Boolean `open` behavior
- Reactive `State`-controlled `open` behavior
- Engine property forwarding
- Custom style override
- Component child preservation
- Public UI Kit export
- Engine-level dialog rendering and reactive behavior

## Verified Sources

- `pylage/UI/components/dialog.py`
- `demo/demo_dialog.py`
- `test/components/test_ui_kit_dialog.py`
- `test/components/test_dialog.py`
- `test/components/test_ui_kit_confirmation_dialog.py`
- `documents/dialog.md` (reference/archive)

## Status

Dialog documentation is refined against the current implementation, demo, and verified test coverage.
