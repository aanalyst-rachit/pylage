# PyLage UI Kit — Radio

## Definition

`radio_group` is a PyLage UI Kit component for grouping native radio input components into a single radio-selection control.

It is a thin wrapper around the existing engine `RadioGroup`, adding the UI Kit default group styling while preserving the engine radio-group behavior.

## Use

Use `radio_group()` when multiple native radio inputs represent mutually exclusive choices.

The radio options are supplied as existing PyLage `input()` components configured with `input_type="radio"`.

## Usage

### Basic Radio Group

```python
import pylage as pl

group = pl.radio_group(
    pl.input(
        input_type="radio",
        name="language",
        value="python",
    ),
    pl.input(
        input_type="radio",
        name="language",
        value="javascript",
    ),
)
```

Radio options preserve the order in which they are supplied to the group.

### Initial Selection

```python
import pylage as pl

group = pl.radio_group(
    pl.input(input_type="radio", name="access", value="available"),
    pl.input(input_type="radio", name="access", value="locked"),
    value="available",
)
```

The `value` property selects the radio option whose value matches the supplied value.

### State Binding

```python
import pylage as pl

selected = pl.state("python")

group = pl.radio_group(
    pl.input(input_type="radio", name="language", value="python"),
    pl.input(input_type="radio", name="language", value="javascript"),
    value=selected,
)
```

The selected radio follows the current `State` value. Programmatic State changes update the selected browser radio.

### Change Events

```python
import pylage as pl

def handle_change(payload):
    print(payload)

group = pl.radio_group(
    pl.input(input_type="radio", name="language", value="python"),
    pl.input(input_type="radio", name="language", value="javascript"),
    on_change=handle_change,
)
```

The existing PyLage change-event contract is used. Browser radio changes can provide the selected value and checked state in the event payload.

### Disabled Options

```python
import pylage as pl

pl.radio_group(
    pl.input(input_type="radio", name="access", value="available"),
    pl.input(
        input_type="radio",
        name="access",
        value="locked",
        disabled=True,
    ),
)
```

Disabled behavior is provided by the underlying native input component.

### Native Radio Attributes

Radio options can use the normal `input()` API, including properties such as `name`, `value`, `checked`, `disabled`, and `id`.

## API

```python
radio_group(*children, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*children` | `Any` | — | Radio input components or other supported child components. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the default group style. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `RadioGroup`. |

## Default Styling

The UI Kit wrapper applies the following default group style:

- `display: flex`
- `flex_direction: column`
- `gap: 0.5rem`

The style is applied to the `RadioGroup` container rather than individual radio inputs.

## Styling Behavior

Custom styles are merged over the default group style.

For example:

```python
import pylage as pl

pl.radio_group(
    pl.input(input_type="radio", name="plan", value="basic"),
    pl.input(input_type="radio", name="plan", value="pro"),
    style=pl.style(gap="1rem"),
)
```

The custom `gap` overrides the default `0.5rem` value while the other default group properties remain available.

## State and Events

`radio_group()` itself delegates state and event behavior to the existing engine `RadioGroup`.

The engine supports a reactive `value` property. With a `State`, browser selection can update the state through the existing change-event mechanism, and programmatic state changes can update the browser selection.

`on_change` is registered through the existing PyLage event system.

## Component and Attribute Behavior

The UI Kit wrapper does not create a separate radio-input implementation.

Each option remains an existing input component, while the group provides the shared container and selection behavior.

Useful native radio properties include:

- `input_type="radio"`
- `name`
- `value`
- `checked`
- `disabled`
- `id`

## Architecture

```text
pl.radio_group()
    ↓
UI Kit radio wrapper
    ↓
PyLage ENGINE RadioGroup
    ↓
Existing renderer
    ↓
Native radio inputs
```

The UI Kit layer supplies the public wrapper and default styling. The existing engine remains responsible for radio-group rendering, reactive value handling, and event integration.

## API Boundary

`radio_group()` is the public UI Kit entry point.

It returns the existing engine `RadioGroup` component rather than introducing a separate renderer or component type.

Radio option configuration remains the responsibility of the existing `input()` API.

## Verified Working Example

`demo/demo_radio.py` demonstrates four scenarios:

- a basic group with three radio options and an initial checked option
- a State-bound language group with Python, JavaScript, and Rust options
- a group containing a disabled option
- native radio attributes using explicit option IDs

The State-bound example also displays the selected value and the latest change event.

## Verification

Radio-group behavior is covered by:

- `test/components/test_radio_group.py`
- `test/components/test_radio_group_api.py`
- `test/browser/test_radio.py`

The tests verify:

- container rendering
- child rendering and option ordering
- forwarded group properties
- initial value selection
- reactive State-backed selection
- change-event registration
- reactive registry metadata for `value`
- browser-to-State synchronization
- programmatic State-to-browser synchronization
- preservation of the existing engine `RadioGroup` contract

## Verified Sources

- `pylage/UI/components/radio.py`
- `pylage/UI/components/stat_group.py`
- `demo/demo_radio.py`
- `test/components/test_radio_group.py`
- `test/components/test_radio_group_api.py`
- `test/browser/test_radio.py`
- `documents/radio.md`

## Status

**Radio documentation refined and verified.**
