# PyLage UI Kit — Textarea

## Definition

`textarea` is a PyLage UI Kit component for multi-line text input.

It creates the registered `Textarea` component through the existing PyLage renderer and adds semantic UI Kit styling.

## Use

Use `textarea()` for notes, messages, descriptions, comments, and other multi-line text input.

It supports normal text values, reactive `State` values, native textarea attributes, custom input handlers, and `Style` customization.

## Usage

### Basic Textarea

```python
import pylage as pl

pl.textarea(
    placeholder="Enter your message...",
    rows=5,
)
```

### Initial Value

```python
import pylage as pl

pl.textarea(
    value="Existing text",
    rows=5,
)
```

### Reactive State Binding

Pass a `State` as `value` to keep the textarea value synchronized with that state.

```python
import pylage as pl

message = pl.state("")

pl.textarea(
    message,
    placeholder="Write something...",
)
```

When `value` is a `State` and no explicit `on_input` handler is supplied, the UI Kit automatically registers an input handler that updates the state from the browser input payload.

### Custom Input Handler

An explicit `on_input` handler is preserved instead of being replaced by the automatic State handler.

```python
import pylage as pl

def handle_input(payload):
    print(payload)

pl.textarea(
    "",
    on_input=handle_input,
)
```

### Disabled Textarea

```python
import pylage as pl

pl.textarea(
    "This field cannot be edited.",
    disabled=True,
)
```

## API

```python
textarea(value="", *, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `value` | `Any` | `""` | Initial or reactive textarea value. A `State` enables automatic input synchronization when no explicit `on_input` is supplied. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit defaults. |
| `**props` | `Any` | — | Additional registered or engine-supported component properties. |

## Supported Properties

The registered textarea properties include:

- `value`
- `placeholder`
- `name`
- `rows`
- `cols`
- `disabled`
- `required`
- `readonly`
- `title`
- `minlength`
- `maxlength`

These map to the corresponding textarea behavior or native HTML attributes through the existing component registry and renderer.

## Default Styling

The UI Kit applies these default styles:

- `width: 100%`
- `box_sizing: border-box`
- `min_height: 120px`
- `padding: 0.625rem 0.75rem`
- `font_size: 1rem`
- `line_height: 1.5`
- `color: var(--color-text)`
- `background_color: var(--color-background)`
- `border: 1px solid var(--color-border)`
- `border_radius: var(--radius-md)`
- `transition: border-color 150ms ease, box-shadow 150ms ease`

## Styling Behavior

Custom styles are merged over the UI Kit defaults.

```python
import pylage as pl

pl.textarea(
    placeholder="Notes",
    rows=6,
    style=pl.style(
        padding="0.75rem",
        border_radius="0.5rem",
    ),
)
```

Only supplied custom values override matching defaults; other defaults remain available.

## State and Events

When `value` is a `State` and `on_input` is not supplied, `textarea()` creates an input callback that reads the `value` field from the browser event payload and updates the state.

If an explicit `on_input` is supplied, that handler is passed through unchanged.

The UI Kit does not introduce a separate state or event system; it uses the existing PyLage `State` and component runtime.

## Native Attributes

Properties such as `placeholder`, `name`, `rows`, `cols`, `disabled`, `required`, `readonly`, `title`, `minlength`, and `maxlength` are registered as textarea properties and rendered through the existing PyLage component system.

## Architecture

```text
pl.textarea()
    ↓
UI Kit textarea wrapper
    ↓
Registered Textarea component
    ↓
Existing PyLage registry / renderer
    ↓
Native <textarea>
```

The UI Kit component does not introduce a separate HTML template system, renderer, or reactive pipeline.

## API Boundary

`textarea()` is the public UI Kit entry point.

The wrapper owns the UI Kit defaults and the automatic State-to-input synchronization behavior. Component registration, property handling, and rendering remain part of the existing PyLage engine.

## Verified Working Example

The project provides the executable textarea demo:

- `demo/demo_textarea.py`

The demo exercises the public textarea API and its supported interactive behavior.

## Verification

Textarea behavior is covered by:

- `test/components/test_textarea.py`

The component test covers the textarea API and behavior provided by the current implementation.

## Verified Sources

- `pylage/UI/components/textarea.py`
- `demo/demo_textarea.py`
- `test/components/test_textarea.py`
- `documents/textarea.md`

## Status

**Textarea documentation refined and verified.**
