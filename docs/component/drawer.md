# PyLage UI Kit — Drawer

## Definition

`drawer` is a PyLage UI Kit component recipe for displaying content in an off-canvas side panel.

The UI Kit exposes three public drawer recipes: `drawer()`, `navigation_drawer()`, and `mobile_sidebar()`. All three reuse the existing PyLage Drawer implementation.

## Use

Use a drawer when secondary content should appear beside the main application without occupying normal document layout space.

Typical uses include navigation panels, settings, contextual controls, and mobile sidebars.

## Usage

### Generic Drawer

```python
import pylage as pl

open_state = pl.state(False)

pl.drawer(
    pl.column(
        pl.heading("Navigation", level=2),
        pl.button("Dashboard"),
        pl.button("Settings"),
    ),
    open=open_state,
    title="Side Navigation",
)
```

### Navigation Drawer

`navigation_drawer()` provides a semantic UI Kit entry point for navigation-oriented drawer content. It uses the same underlying Drawer component.

```python
import pylage as pl

pl.navigation_drawer(
    pl.column(
        pl.heading("Navigation", level=2),
        pl.button("Dashboard"),
        pl.button("Users"),
        pl.button("Settings"),
    ),
    open=True,
    title="Navigation",
)
```

### Mobile Sidebar

`mobile_sidebar()` provides a semantic UI Kit entry point for sidebar content intended for mobile-oriented layouts. It also reuses the existing Drawer implementation.

```python
import pylage as pl

pl.mobile_sidebar(
    pl.column(
        pl.heading("Menu", level=2),
        pl.button("Dashboard"),
        pl.button("Profile"),
    ),
    open=True,
    title="Mobile Menu",
)
```

### Reactive Open and Close

The `open` property accepts a reactive `State`. Changing the state updates the Drawer visibility.

```python
import pylage as pl

drawer_open = pl.state(False)

pl.drawer(
    pl.text("Drawer content"),
    open=drawer_open,
)

drawer_open.set(True)
drawer_open.set(False)
```

### Custom Content

Drawer content is composed from normal PyLage components.

```python
import pylage as pl

pl.drawer(
    pl.column(
        pl.heading("Tools", level=2),
        pl.text("Choose an action."),
        pl.button("Export"),
        pl.button("Close", variant="secondary"),
    )
)
```

### Custom Styling

The drawer recipes accept `Style` or `ResponsiveStyle` values and forward them to the underlying Drawer.

```python
import pylage as pl

pl.drawer(
    pl.text("Drawer content"),
    style=pl.style(width="320px"),
)
```

### Additional Properties

Additional properties are forwarded to the underlying Drawer component.

```python
import pylage as pl

pl.drawer(
    pl.text("Navigation"),
    open=True,
    title="Navigation drawer",
    class_name="custom-drawer",
)
```

## API

### `drawer()`

```python
drawer(*children, style=None, **props)
```

### `navigation_drawer()`

```python
navigation_drawer(*children, style=None, **props)
```

### `mobile_sidebar()`

```python
mobile_sidebar(*children, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*children` | `Any` | — | Content rendered inside the Drawer. |
| `style` | `Style \\| ResponsiveStyle \\| None` | `None` | Custom or responsive styling forwarded to the Drawer. |
| `**props` | `Any` | — | Additional Drawer properties, including properties such as `open`, `title`, and `class_name`. |

## Open State

The underlying Drawer supports both boolean and reactive `open` values.

- `open=False` renders the Drawer closed.
- `open=True` renders the Drawer open.
- A `State` value can be used for reactive open/close behavior.

The UI Kit recipe does not implement a separate visibility state system; it forwards `open` to the existing Drawer component.

## Rendering Behavior

The underlying Drawer renders as an HTML `aside` element.

When closed, the built-in Drawer presentation moves the panel outside the viewport, hides it from visibility, and disables pointer interaction.

When open, the panel is translated into view and pointer interaction is enabled.

The Drawer uses fixed positioning with viewport-height sizing and a high stacking order so it behaves as an off-canvas overlay rather than a normal layout column.

The built-in renderer provides the Drawer CSS and rendering behavior.

## Styling Boundary

The UI Kit drawer recipes do not duplicate the Drawer renderer or its CSS. They accept `Style` or `ResponsiveStyle` and pass the supplied styling to the existing Drawer implementation.

This keeps rendering behavior centralized in the PyLage engine.

## Architecture

```text
pl.drawer()
pl.navigation_drawer()
pl.mobile_sidebar()
        ↓
UI Kit drawer recipes
        ↓
UI layout Drawer wrappers
        ↓
PyLage ENGINE Drawer
        ↓
Existing renderer + Drawer CSS
```

`navigation_drawer()` and `mobile_sidebar()` are semantic entry points over the same underlying Drawer component; they do not create separate renderer implementations.

## API Boundary

The UI Kit owns the public recipe names and accepts `Style` or `ResponsiveStyle` before forwarding the configuration.

The underlying PyLage Drawer remains responsible for component construction, rendering, HTML structure, CSS presentation, and reactive `open` behavior.

## Verified Working Examples

The project provides two executable Drawer demos:

- `demo/demo_drawer.py`
- `demo/demo_drawer_navigation.py`

The demos exercise generic drawers, navigation drawers, mobile sidebars, reactive open/close behavior, custom content, and action handlers.

## Verification

Focused coverage is provided by:

- `test/components/test_ui_kit_drawer_component.py`
- `test/components/test_ui_kit_drawer.py`
- `test/websocket/test_ui_kit_drawer_reactive_close.py`

The tests cover component construction, HTML rendering, children, boolean and reactive open state, off-canvas presentation, custom properties, styling, public exports, and reactive updates.

## Verified Sources

- `pylage/UI/recipes/drawer.py`
- `pylage/UI/layout/drawer.py`
- `pylage/ENGINE/components/basic.py`
- `pylage/ENGINE/core/renderer.py`
- `demo/demo_drawer.py`
- `demo/demo_drawer_navigation.py`
- `test/components/test_ui_kit_drawer_component.py`
- `test/components/test_ui_kit_drawer.py`
- `test/websocket/test_ui_kit_drawer_reactive_close.py`
- `docs/helper/drawer.md`

## Status

**Drawer documentation refined and verified.**
