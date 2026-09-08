# PyLage UI Kit — Select

## Definition

`select` is a PyLage UI Kit component for creating a dropdown/select control from existing PyLage `Option` components.

It is a thin wrapper around the existing engine `Select`, adding the UI Kit default styling while preserving the engine select behavior.

## Use

Use `select()` when users need to choose one or more values from a defined set of options.

Options are supplied as existing PyLage `Option` components.

## Usage

### Basic Select

```python
import pylage as pl

group = pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    value="india",
)
```

The options are rendered in the order supplied to the select component.

### State Binding

```python
import pylage as pl

selected = pl.state("india")

country_select = pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    value=selected,
)
```

The existing engine `Select` supports a reactive `value`. Programmatic State changes update the selected option in the browser.

### Change Events

```python
import pylage as pl

def handle_change(payload):
    print(payload)

country_select = pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    on_change=handle_change,
)
```

`on_change` uses the existing PyLage browser event system.

### Multiple Selection

```python
import pylage as pl

country_select = pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    pl.option("Germany", value="germany"),
    multiple=True,
    size=3,
)
```

The existing engine supports native multiple selection through `multiple` and related select properties.

### Disabled Select

```python
import pylage as pl

country_select = pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    disabled=True,
)
```

Native disabled behavior is provided by the underlying engine select component.

### Native Select Properties

The normal engine `Select` properties can be forwarded through the UI Kit wrapper, including:

- `value`
- `multiple`
- `size`
- `name`
- `disabled`
- `required`
- `title`
- `on_change`

Options are created with the existing `Option` component, which provides each option label and value.

## API

```python
select(*children, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*children` | `Any` | — | Option components or other supported child components. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit default select style. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Select`. |

## Default Styling

The UI Kit wrapper applies the following default style:

- `width: 100%`
- `box_sizing: border-box`
- `padding: 0.625rem 0.75rem`
- `font_size: 1rem`
- `line_height: 1.5`
- `color: var(--color-text)`
- `background_color: var(--color-background)`
- `border: 1px solid var(--color-border)`
- `border_radius: var(--radius-md)`
- `cursor: pointer`
- `transition: border-color 150ms ease, box-shadow 150ms ease`

These defaults are applied to the underlying `Select` component.

## Styling Behavior

Custom styles are merged over the default select style.

For example:

```python
import pylage as pl

pl.select(
    pl.option("India", value="india"),
    pl.option("Japan", value="japan"),
    style=pl.style(
        width="100%",
        padding="0.75rem",
    ),
)
```

The supplied style overrides matching default properties while unrelated defaults remain available.

## State and Events

`select()` delegates reactive value handling and browser event integration to the existing engine `Select`.

A `State` can be supplied through `value`. Browser selection changes can be handled with `on_change`, while programmatic State changes can update the selected option.

## Component and Option Behavior

The UI Kit wrapper does not implement a separate select renderer.

The select container is provided by the existing engine `Select`, while each option is supplied through the existing `Option` component.

This keeps option rendering, selection behavior, native select properties, and browser integration within the existing engine contract.

## Architecture

```text
pl.select()
    ↓
UI Kit select wrapper
    ↓
PyLage ENGINE Select
    ↓
Existing renderer
    ↓
Native browser <select>
```

The UI Kit layer supplies the public wrapper and default styling. The existing engine remains responsible for select rendering, option handling, reactive values, and event integration.

## API Boundary

`select()` is the public UI Kit entry point.

It returns the existing engine `Select` component rather than introducing a separate renderer or select implementation.

Option configuration remains the responsibility of the existing `Option` component.

## Verified Working Example

`demo/demo_select.py` demonstrates:

- a language dropdown containing Python, JavaScript, Rust, Go, and C++
- reactive selection using `pl.state`
- a database dropdown using label/value option mappings
- custom `on_change` handlers that update State values
- custom select styling

The demo also displays the currently selected language and database values.

## Verification

Select behavior is covered by:

- `test/components/test_select.py`
- `test/components/test_select_option_api.py`
- `test/browser/test_active_selected_checked.py`

The verified coverage includes:

- select component rendering
- option rendering and ordering
- forwarded select properties
- initial value selection
- reactive State-backed selection
- change-event integration
- multiple-selection support
- native select behavior

## Verified Sources

- `pylage/UI/components/select.py`
- `demo/demo_select.py`
- `test/components/test_select.py`
- `test/components/test_select_option_api.py`
- `test/browser/test_active_selected_checked.py`
- `documents/select.md`

## Status

**Select documentation refined and verified.**
