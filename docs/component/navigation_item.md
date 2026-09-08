# PyLage UI Kit — Navigation Item

## Definition

`navigation_item` is a PyLage UI Kit component for creating navigation controls using the existing PyLage `Button` component.

It provides navigation-specific active-state styling while preserving the underlying Button rendering and event behavior.

## Use

Use `navigation_item()` for items in navigation bars, sidebars, menus, or other navigation surfaces where one item can be marked active.

The active state can be static with a boolean or controlled reactively with a PyLage `State`.

## Usage

### Basic Navigation Item

```python
import pylage as pl

pl.navigation_item("Dashboard")
```

### Static Active State

```python
import pylage as pl

pl.navigation_item("Dashboard", active=True)
```

An inactive item uses the base navigation styling. An active item uses the primary background and primary contrast text color.

### Reactive Active State

```python
import pylage as pl

active = pl.state(False)

pl.navigation_item("Dashboard", active=active)
```

When the supplied `State` changes, the active background and text color update reactively.

### Navigation Selection

```python
import pylage as pl

home_active = pl.state(True)
products_active = pl.state(False)

home = pl.navigation_item("Home", active=home_active)
products = pl.navigation_item("Products", active=products_active)
```

Application code can update these states from Button event handlers to implement navigation selection.

### Custom Styling

```python
import pylage as pl

pl.navigation_item(
    "Reports",
    active=True,
    style=pl.style(padding="0.75rem 1rem"),
)
```

Custom style values override corresponding component defaults. In reactive mode, explicitly supplied `background_color` and `color` values are preserved.

## API

```python
navigation_item(text, *, active=False, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `text` | `Any` | — | Navigation item content passed to the underlying Button. |
| `active` | `bool \\| State` | `False` | Controls the static or reactive active state. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the component defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying Button. |

## Active State Behavior

### Boolean Active State

When `active` is a boolean, the component resolves its final style immediately.

- `active=False` uses the base navigation styling.
- `active=True` applies the active background and contrast text color.

The `active` argument is handled by the UI Kit wrapper and is not forwarded to the underlying Button.

### Reactive Active State

When `active` is a `State`, the component creates reactive style values for the background and text color and subscribes to the supplied state.

State changes update:

- `background_color`: transparent when inactive and primary when active
- `color`: text color when inactive and primary contrast when active

If custom `background_color` or `color` values are supplied through `style`, those values are not replaced by reactive active-state updates.

## Default Styling

Navigation items use the following base styling:

- `display: flex`
- `align_items: center`
- `width: 100%`
- `text_align: left`
- `background_color: transparent`
- `color: var(--color-text)`
- `border: none`
- `border_radius: 0.375rem`
- `padding: 0.5rem 0.75rem`
- `cursor: pointer`

Active items use `var(--color-primary)` for the background and `var(--color-primary-contrast)` for the text color.

## Styling Behavior

The final style is created by merging the component defaults with the optional custom `style`.

For static active state, active defaults are applied before the custom style, so explicit custom values take precedence.

For reactive active state, background and text color remain reactive unless those values were explicitly supplied through custom styling.

## Events

Additional properties are forwarded to the underlying Button, so Button events such as `on_click` can be supplied directly.

```python
import pylage as pl

def select_dashboard():
    print("Dashboard selected")

pl.navigation_item("Dashboard", on_click=select_dashboard)
```

The wrapper does not introduce a separate navigation event system; it reuses the existing Button event contract.

## Validation

`active` must be either a boolean or a PyLage `State`.

Passing another value raises `TypeError` with the message `active must be a bool or State`.

## Architecture

```text
pl.navigation_item()
    ↓
UI Kit navigation wrapper
    ↓
PyLage Button
    ↓
Existing renderer
```

The UI Kit wrapper handles navigation-specific active-state styling and validation. The underlying Button remains responsible for component rendering and event behavior.

## API Boundary

`navigation_item()` is the public UI Kit entry point.

It does not create a new engine component type. The returned component is an existing engine `Button` with navigation styling applied.

## Verified Working Example

The project demo `demo/demo_navigation_item.py` demonstrates navigation items with reactive active states and event-driven selection.

## Verification

Navigation Item behavior is covered by:

- `test/components/test_ui_kit_navigation_item.py`

The tests cover:

- return type and Button composition
- default navigation styling
- active styling
- custom style overrides
- Button event forwarding
- active argument handling
- reactive active-state updates
- isolation of reactive state from engine props

## Verified Sources

- `pylage/UI/components/navigation_item.py`
- `demo/demo_navigation_item.py`
- `test/components/test_ui_kit_navigation_item.py`
- `documents/navigation_item.md`

## Status

**Navigation Item documentation refined and verified.**
