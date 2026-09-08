# PyLage UI Kit — Datepicker

## Definition

`datepicker()` is the PyLage UI Kit wrapper for the existing PyLage `DatePicker` engine component. It provides a styled native HTML5 date input while preserving the engine's value binding, event handling, date constraints, disabled state, and native input properties.

## Use

Use `datepicker()` when an application needs a date input with PyLage styling and optional reactive state synchronization.

- Native HTML5 `input[type="date"]` rendering
- Static date values
- Reactive `pl.state` value binding
- Browser `input` events synchronized to bound state
- Custom `on_input` callbacks preserved with state binding
- Custom `on_change` callbacks
- `min` and `max` date constraints
- Disabled state through the underlying engine API
- Native input properties such as `name`, `id`, `title`, and `class_name`
- Programmatic state updates reflected by the component

## Usage

### Basic date input

```python
import pylage as pl

pl.datepicker(
    value="2026-09-03",
)
```

### Reactive date binding

```python
import pylage as pl

selected_date = pl.state("2026-09-03")

pl.datepicker(
    value=selected_date,
    min="2026-01-01",
    max="2026-12-31",
)
```

When `value` is a `pl.state`, browser `input` events update the bound state. Programmatic state changes are also reflected in the rendered date input.

### Change callback

```python
import pylage as pl

selected_date = pl.state("2026-09-03")

def handle_date_change(payload):
    selected_date.set(payload["value"])

pl.datepicker(
    value=selected_date,
    on_change=handle_date_change,
)
```

### Input callback with reactive state

```python
import pylage as pl

selected_date = pl.state("2026-09-03")

def handle_input(payload):
    print(payload["value"])

pl.datepicker(
    value=selected_date,
    on_input=handle_input,
)
```

The existing state-binding behavior is preserved while the custom `on_input` callback receives the input event payload.

## API

```python
datepicker(*, style=None, **props)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `style` | Optional PyLage `Style` merged with the component's default visual style. |
| `value` | Static date value or a reactive `State`. |
| `min` | Optional minimum permitted date. |
| `max` | Optional maximum permitted date. |
| `on_input` | Optional callback for browser input events. |
| `on_change` | Optional callback for change events. |
| `disabled` | Optional disabled state forwarded to the engine component. |
| `class_name` | Optional CSS class forwarded to the underlying date input. |
| `name` | Optional native input name. |
| `id` | Optional native input identifier. |
| `title` | Optional native input title. |
| `**props` | Other supported engine/native input properties. |

## Reactive Behavior

With a `State` supplied as `value`, the underlying `DatePicker` synchronizes browser `input` events back to that state.

The browser verification covers the complete binding path: an initial state value is rendered into `input[type="date"]`, a browser input event changes the state, and the updated state is reflected back in the input.

Custom `on_input` callbacks are preserved during this binding and receive the event payload.

## Date Constraints

`min` and `max` are forwarded to the native date input and rendered as HTML date constraints.

```python
pl.datepicker(
    min="2026-01-01",
    max="2026-12-31",
)
```

## Styling

The UI Kit wrapper applies a default form-control style:

- `width: 100%`
- `box-sizing: border-box`
- `padding: 0.625rem 0.75rem`
- `font-size: 1rem`
- `line-height: 1.5`
- text and background colors from the active theme variables
- themed border and medium radius
- pointer cursor
- border-color and box-shadow transition

An explicitly supplied `style` is merged over the default style.

```python
pl.datepicker(
    style=pl.style(
        padding="0.5rem 0.75rem",
        border="1px solid #cbd5e1",
        border_radius="6px",
    )
)
```

The form-control visual foundation test also verifies that the UI Kit Datepicker receives a style and renders with the standard PyLage component identity attribute.

## Architecture

The UI Kit does not introduce a separate Datepicker renderer. The public wrapper delegates to the existing engine implementation:

`Application → pl.datepicker() → ENGINE DatePicker → existing renderer/runtime`

This keeps date rendering and event behavior in the existing engine while the UI Kit wrapper supplies the public API and default styling.

## API Boundary

`datepicker()` accepts the public `style` argument explicitly and forwards the remaining properties to the underlying engine `DatePicker`. The wrapper does not implement a separate date-selection system or custom browser renderer.

The documented behavior is limited to functionality verified by the current source, demo, and tests. Features such as sorting, calendar customization, localization, or additional date-picker behavior are not documented here because they are not established by the verified implementation.

## Verified Working Example

The project demo `demo/demo_datepicker.py` demonstrates a live state-bound Datepicker with an `on_change` handler, displayed selected-date state, custom styling, and quick actions that update the selected date programmatically.

```python
import pylage as pl

selected_date = pl.state("2026-09-01")

def handle_date_change(val=None):
    if isinstance(val, dict):
        val = val.get("value", selected_date.value)
    selected_date.set(str(val))

picker = pl.datepicker(
    value=selected_date,
    on_change=handle_date_change,
)
```

## Verification

Verified coverage includes:

- Native `input[type="date"]` rendering
- Native properties including `class_name`, `title`, and `value`
- `min` and `max` date constraints
- Initial rendering from `State`
- State updates from browser `input` events
- State updates through `on_change` handling
- Browser-level reactive binding
- Preservation of custom `on_input` callbacks
- Public wrapper delegation to the engine `DatePicker`
- Standard form-control visual foundation

## Verified Sources

- `pylage/UI/components/datepicker.py`
- `demo/demo_datepicker.py`
- `test/components/test_datepicker.py`
- `test/browser/test_datepicker.py`
- `test/regression/test_public_wrappers.py`
- `test/browser/test_form_control_visual_foundation.py`
- `documents/datepicker.md` (reference/archive)

## Status

Datepicker documentation is refined against the current implementation and verified test coverage.
