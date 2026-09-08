# PyLage UI Kit — Input

## Definition

`input` is the public PyLage UI Kit wrapper around the existing PyLage `Input` component.

It provides a Python-first single-line input control with native input types, reactive state binding, event handling, and consistent UI Kit styling while reusing the existing engine implementation.

## Use

Use `input()` for single-line text entry and other native HTML input types such as email, password, and number.

The wrapper exposes the existing engine capabilities without introducing a separate renderer or client-side implementation.

## Usage

### Basic Input

```python
import pylage as pl

pl.input(
    placeholder="Enter your name...",
)
```

### Input Type

The `input_type` parameter selects the native HTML input type.

```python
pl.input(
    input_type="email",
    placeholder="Email address",
)

pl.input(
    input_type="password",
    placeholder="Password",
)
```

### Reactive State Binding

A `State` can be supplied as the input value.

```python
name = pl.state("")

pl.input(
    name,
    placeholder="Your name",
)
```

When no explicit `on_input` handler is supplied, the existing PyLage engine updates the supplied `State` from browser input events.

### Event Handling

Input supports the existing PyLage event system.

```python
def handle_input(payload):
    print(payload)

pl.input(
    "",
    on_input=handle_input,
)
```

Other supported event properties, such as `on_change`, can be passed through the normal component properties.

### Disabled Input

```python
pl.input(
    value="This field cannot be edited.",
    disabled=True,
)
```

The `disabled` property is passed through to the existing PyLage input implementation and native HTML rendering.

## API

```python
input(value="", input_type=None, style=None, **props)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `value` | Initial input value or a reactive `State`. |
| `input_type` | Native HTML input type such as `text`, `email`, `password`, or `number`. |
| `style` | Optional `Style` merged with the UI Kit default style. |
| `**props` | Additional supported PyLage and native input properties and event handlers. |

## Common Properties

Properties supported through the underlying input component can include:

- `value`
- `placeholder`
- `name`
- `disabled`
- `required`
- `readonly`
- `type`
- `title`
- `minlength`
- `maxlength`

The UI Kit `input_type` parameter provides the dedicated public argument for selecting the native input type.

## Default Styling

The UI Kit wrapper applies these default styles:

- `width: 100%`
- `box_sizing: border-box`
- `padding: 0.625rem 0.75rem`
- `font_size: 1rem`
- `line_height: 1.5`
- `color: var(--color-text)`
- `background_color: var(--color-background)`
- `border: 1px solid var(--color-border)`
- `border_radius: var(--radius-md)`
- `transition: border-color 150ms ease, box-shadow 150ms ease`

## Styling Behavior

The final style is created by merging the UI Kit base style with the optional user-provided `style`.

Custom values supplied through `style` therefore override the corresponding defaults.

```python
pl.input(
    placeholder="Search...",
    style=pl.style(
        width="100%",
        padding="0.75rem 1rem",
        border="1px solid #cbd5e1",
        border_radius="0.5rem",
        box_sizing="border-box",
    ),
)
```

## State and Events

Input preserves the existing engine behavior for reactive values and browser events.

When a reactive `State` is supplied as `value`, browser input events can update that state through the existing runtime. Explicit event handlers such as `on_input` and `on_change` remain available through normal component properties.

## Architecture

The public wrapper reuses the existing PyLage input implementation:

```text
PyLage UI Kit
    ↓
pylage.UI.components.input
    ↓
Existing PyLage Engine Input
    ↓
Existing Registry / Renderer
    ↓
Native <input>
```

No separate JavaScript renderer, HTML template system, or alternate reactive pipeline is introduced.

## API Boundary

The UI Kit owns the public `input()` entry point and its default styling.

The underlying engine remains responsible for native input rendering, state synchronization, event handling, registry integration, and client runtime behavior.

## Reuse Decision

Input is implemented as a reuse wrapper because the existing engine already provides the required input component, rendering, input type handling, state binding, browser events, registry integration, and client runtime support.

## Verified Working Example

The project provides two input demos:

- `demo/demo_input.py`
- `demo/demo_input_features.py`

The feature demo covers text input, reactive state binding, email and password inputs, disabled and required inputs, submit interaction, and the PyLage client runtime.

## Verification

The implementation is covered by:

- `test/browser/test_input_binding.py`
- `test/components/test_input_type_api.py`
- `test/integration/test_input_binding.py`

These tests cover input binding, input type behavior, and integration with the existing PyLage runtime.

## Verified Sources

- `pylage/UI/components/input.py`
- `demo/demo_input.py`
- `demo/demo_input_features.py`
- `test/browser/test_input_binding.py`
- `test/components/test_input_type_api.py`
- `test/integration/test_input_binding.py`
- `documents/input.md`

## Status

**Input documentation refined and verified.**
