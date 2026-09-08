# PyLage UI Kit — Slider

## Definition

`slider` is a PyLage UI Kit component for creating a native range/slider control.

It is a thin wrapper around the existing engine `Slider`, adding the UI Kit default styling while preserving the engine slider behavior.

## Use

Use `slider()` when users need a numeric value selected from a defined range.

Range configuration and interaction behavior are provided by the underlying engine `Slider` component.

## Usage

### Basic Slider

```python
import pylage as pl

control = pl.slider(
    value=50,
    min=0,
    max=100,
    step=5,
)
```

### State Binding

```python
import pylage as pl

value = pl.state(25)

control = pl.slider(
    value=value,
    min=0,
    max=100,
    step=5,
)
```

A reactive `State` can be supplied through `value`. Browser slider changes and programmatic State updates use the existing PyLage reactive binding system.

### Range Configuration

The underlying slider API supports range properties such as:

- `min`
- `max`
- `step`
- `value`

These properties are forwarded to the existing engine `Slider`.

### Input Events

An `on_input` callback can be supplied through the existing slider API:

```python
import pylage as pl

def handle_input(payload):
    print(payload)

control = pl.slider(
    value=25,
    min=0,
    max=100,
    step=5,
    on_input=handle_input,
)
```

The event behavior is provided by the existing PyLage engine.

### Disabled Slider

The existing slider component also supports native control properties such as `disabled`.

```python
import pylage as pl

control = pl.slider(
    value=50,
    min=0,
    max=100,
    disabled=True,
)
```

## API

```python
slider(*, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit default slider style. |
| `**props` | `Any` | — | Slider properties, event handlers, and other supported properties forwarded to the underlying `Slider`. |

The wrapper itself does not define separate parameters for `value`, `min`, `max`, or `step`; these are forwarded through `**props` to the engine component.

## Default Styling

The UI Kit wrapper applies two default properties:

- `width: 100%`
- `cursor: pointer`

No other default slider styles are introduced by the UI Kit wrapper.

## Styling Behavior

Custom styles are merged over the default slider style.

For example:

```python
import pylage as pl

pl.slider(
    value=50,
    min=0,
    max=100,
    style=pl.style(
        width="80%",
    ),
)
```

The supplied style overrides matching default properties while unrelated defaults remain available.

## State and Events

`slider()` delegates state binding and event behavior to the existing engine `Slider`.

A `State` can be supplied through `value`. The existing engine also supports input-event callbacks such as `on_input` and preserves the established reactive behavior.

## Component and Attribute Behavior

The UI Kit wrapper does not implement a separate slider renderer.

It forwards slider properties directly to the existing engine `Slider`, including native range configuration and supported event properties.

## Architecture

```text
pl.slider()
    ↓
UI Kit slider wrapper
    ↓
PyLage ENGINE Slider
    ↓
Existing renderer/runtime
    ↓
Native browser range control
```

The UI Kit layer supplies the public wrapper and default styling. The existing engine remains responsible for rendering, value handling, state synchronization, and events.

## API Boundary

`slider()` is the public UI Kit entry point.

It returns the existing engine `Slider` component rather than introducing a separate renderer or slider implementation.

## Verified Working Example

The project slider demos cover the public slider behavior, including:

- basic slider usage
- configured range values
- State-backed values
- input event handling
- disabled behavior
- native slider properties

The related combined demo `demo/demo_slider_radio_checkbox.py` also exercises the slider alongside other form controls.

## Verification

Slider behavior is covered by:

- `test/components/test_slider.py`
- `test/browser/test_slider.py`

The verified coverage includes:

- slider component rendering
- value and range configuration
- reactive State binding
- browser input updates
- programmatic State updates
- input-event integration
- supported native slider properties

## Verified Sources

- `pylage/UI/components/slider.py`
- `demo/demo_slider.py`
- `demo/demo_slider_radio_checkbox.py`
- `test/components/test_slider.py`
- `test/browser/test_slider.py`
- `documents/slider.md`

## Status

**Slider documentation refined and verified.**
