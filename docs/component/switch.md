# PyLage UI Kit — Switch

## Definition

`switch` is a PyLage UI Kit component for creating a boolean toggle control.

It is a thin wrapper around the existing engine `Switch`, adding the UI Kit default styling while preserving the engine switch behavior.

## Use

Use `switch()` when an interface needs a compact on/off control.

The underlying engine provides the switch value handling, State synchronization, events, disabled behavior, and supported native properties.

## Usage

### Basic Switch

```python
import pylage as pl

control = pl.switch(
    checked=False,
)
```

### Checked State

```python
import pylage as pl

control = pl.switch(
    checked=True,
)
```

The `checked` property controls the initial boolean state through the underlying engine `Switch`.

### Reactive State Binding

```python
import pylage as pl

enabled = pl.state(False)

control = pl.switch(
    checked=enabled,
)
```

A reactive `State` can be supplied through `checked`. The existing engine handles synchronization between the Python State and the browser control.

### Change Events

An `on_change` callback can be supplied through the existing switch API:

```python
import pylage as pl

def handle_change(payload):
    print(payload)

control = pl.switch(
    checked=False,
    on_change=handle_change,
)
```

Event behavior is provided by the underlying engine `Switch`.

### Disabled Switch

Native switch properties such as `disabled` can be forwarded directly:

```python
import pylage as pl

control = pl.switch(
    checked=True,
    disabled=True,
)
```

## API

```python
switch(*, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit default switch style. |
| `**props` | `Any` | — | Switch properties, event handlers, and other supported properties forwarded to the underlying `Switch`. |

The wrapper itself does not define separate parameters for `checked`, `on_change`, or `disabled`; these are forwarded through `**props` to the engine component.

## Default Styling

The UI Kit wrapper applies three default properties:

- `width: 2.75rem`
- `height: 1.5rem`
- `cursor: pointer`

No other default switch styles are introduced by the UI Kit wrapper.

## Styling Behavior

Custom styles are merged over the UI Kit defaults.

For example:

```python
import pylage as pl

pl.switch(
    checked=True,
    style=pl.style(
        width="3rem",
    ),
)
```

The supplied style overrides matching default properties while unrelated defaults remain available.

## State and Events

`switch()` delegates reactive state and event behavior to the existing engine `Switch`.

When `checked` receives a `State`, the established PyLage reactive system handles synchronization between application state and the browser control. Event callbacks such as `on_change` continue to use the existing engine event contract.

## Component and Attribute Behavior

The UI Kit wrapper does not implement a separate switch renderer.

It forwards switch properties directly to the existing engine `Switch`, including checked state, event handlers, disabled state, and other supported properties.

## Architecture

```text
pl.switch()
    ↓
UI Kit switch wrapper
    ↓
PyLage ENGINE Switch
    ↓
Existing renderer/runtime
    ↓
Native browser switch control
```

The UI Kit layer supplies the public wrapper and default styling. The existing engine remains responsible for rendering, state synchronization, value handling, and events.

## API Boundary

`switch()` is the public UI Kit entry point.

It returns the existing engine `Switch` component rather than introducing a separate renderer or runtime implementation.

## Verified Working Example

The project demos provide working examples of the public switch API:

- `demo/demo_switch.py`
- `demo/demo_switch_reactive.py`

These demos exercise switch usage within PyLage interfaces, including reactive switch behavior.

## Verification

Switch behavior is covered by:

- `test/components/test_switch.py`
- `test/browser/test_switch_api.py`
- `test/browser/test_theme_switching.py`

The verification sources cover the switch component, its public API, browser behavior, and related theme-switching integration.

## Verified Sources

- `pylage/UI/components/switch.py`
- `demo/demo_switch.py`
- `demo/demo_switch_reactive.py`
- `test/components/test_switch.py`
- `test/browser/test_switch_api.py`
- `test/browser/test_theme_switching.py`
- `documents/switch.md`

## Status

**Switch documentation refined and verified.**
