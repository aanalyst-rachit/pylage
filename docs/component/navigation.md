# PyLage UI Kit — Navigation

## Definition

The PyLage UI Kit navigation API provides semantic navigation and navigation-related layout helpers while reusing existing PyLage Engine primitives.

The navigation layer does not introduce a second renderer, reactive runtime, scheduler, WebSocket runtime, CSS engine, or layout engine. Most navigation APIs are thin semantic wrappers around existing Engine components. `sidebar_layout()` and `navigation_controls()` compose existing layout primitives.

## Public API

The canonical public API uses lowercase names through `import pylage as pl`.

| API | Role |
|---|---|
| `pl.navbar()` | Navigation bar with navigation-specific default presentation styling. |
| `pl.navigation()` | Direct semantic wrapper around the Engine Navigation primitive. |
| `pl.sidebar_layout()` | Composes sidebar and content using the Engine Row primitive. |
| `pl.tabs()` | Semantic wrapper around the Engine Tabs primitive. |
| `pl.pagination()` | Semantic wrapper around the Engine Pagination primitive. |
| `pl.menu()` | Semantic wrapper around the Engine Menu primitive. |
| `pl.navigation_controls()` | Composes Previous and Next buttons inside an Engine Row. |
| `pl.breadcrumb_trail()` | Semantic wrapper around the Engine Breadcrumbs primitive. |

`pl.navigation_item()` is documented separately in `docs/navigation_item.md`.

`pl.drawer()`, `pl.navigation_drawer()`, and `pl.mobile_sidebar()` are documented separately in `docs/drawer.md`.

## Architecture

```text
Application
    |
    v
import pylage as pl
    |
    v
PyLage UI semantic navigation layer
    |
    +--> Engine Navigation
    +--> Engine Tabs
    +--> Engine Pagination
    +--> Engine Menu
    +--> Engine Breadcrumbs
    +--> Engine Row + Button composition
    |
    v
Existing PyLage renderer / reactive runtime
```

The navigation layer therefore follows the reuse and composition boundary rather than introducing duplicate Engine primitives.

## Navbar

`pl.navbar()` wraps the existing Engine `Navigation` primitive and applies navigation-bar presentation defaults.

| Property | Default |
|---|---|
| `display` | `flex` |
| `align_items` | `center` |
| `justify_content` | `space-between` |
| `width` | `100%` |
| `padding` | `1rem 1.5rem` |

```python
import pylage as pl

navbar = pl.navbar(
    pl.text("PyLage"),
    pl.button("Login"),
)
```

A supplied `Style` is merged with the navbar base style.

## Navigation

`pl.navigation()` is a semantic wrapper around the existing Engine `Navigation` primitive.

```python
import pylage as pl

navigation = pl.navigation(
    pl.text("Home"),
    pl.button("Login"),
    class_name="main-nav",
    title="Main Navigation",
)
```

The wrapper does not add a separate navigation implementation or renderer.

## Sidebar Layout

`pl.sidebar_layout()` composes the supplied sidebar and content into the existing Engine `Row` primitive.

```python
import pylage as pl

layout = pl.sidebar_layout(
    sidebar=pl.column(
        pl.text("Home"),
        pl.text("Settings"),
    ),
    content=pl.column(
        pl.heading("Dashboard", level=1),
        pl.text("Main content"),
    ),
)
```

The function appends `sidebar` first when it is not `None`, followed by `content` when it is not `None`.

A supplied `Style` or `ResponsiveStyle` is resolved through the existing UI style resolution infrastructure.

`sidebar_layout()` is a layout composition helper; it does not introduce a second layout engine.

## Tabs

`pl.tabs()` wraps the existing Engine `Tabs` primitive.

```python
import pylage as pl

tabs = pl.tabs(
    pl.text("Home"),
    pl.button("Profile"),
    title="Sections",
)
```

The underlying Engine Tabs implementation remains responsible for rendering, property handling, and reactive values.

## Pagination

`pl.pagination()` wraps the existing Engine `Pagination` primitive.

```python
import pylage as pl

pagination = pl.pagination(
    pl.button("Previous"),
    pl.text("2"),
    pl.button("Next"),
    title="Page navigation",
)
```

The underlying Engine Pagination implementation remains responsible for rendering and property handling.

## Menu

`pl.menu()` wraps the existing Engine `Menu` primitive.

```python
import pylage as pl

menu = pl.menu(
    pl.button("Home"),
    pl.button("Settings"),
)
```

The wrapper preserves the existing Engine Menu behavior and property boundary.

## Navigation Controls

`pl.navigation_controls()` composes two Engine Buttons inside an Engine Row.

The controls are:

- `Previous`
- `Next`

Default style:

| Property | Default |
|---|---|
| `display` | `flex` |
| `gap` | `0.5rem` |
| `align_items` | `center` |

```python
import pylage as pl

controls = pl.navigation_controls()
```

Callbacks can be supplied independently.

```python
import pylage as pl

def previous_page():
    print("previous")

def next_page():
    print("next")

controls = pl.navigation_controls(
    on_prev=previous_page,
    on_next=next_page,
)
```

The callbacks are forwarded to the corresponding Button `on_click` event.

A supplied `Style` is merged with the navigation-controls base style.

## Breadcrumb Trail

`pl.breadcrumb_trail()` wraps the existing Engine `Breadcrumbs` primitive.

```python
import pylage as pl

breadcrumbs = pl.breadcrumb_trail(
    pl.text("Home"),
    pl.text("Products"),
    pl.text("Details"),
)
```

The optional `class_name` argument is explicitly placed into the forwarded properties.

## Related Navigation APIs

### Navigation Item

`pl.navigation_item()` is a separate UI Kit component implemented by composing the existing Button primitive with navigation-specific active-state styling.

See `docs/navigation_item.md` for its API, active state, reactive behavior, styling, and verification coverage.

### Drawer-Based Navigation

`pl.navigation_drawer()` and `pl.mobile_sidebar()` use the existing Drawer infrastructure for off-canvas navigation behavior.

See `docs/drawer.md` for their open/close behavior, reactive state, and responsive usage.

## API Boundary

| UI Kit API | Underlying implementation |
|---|---|
| `navbar()` | Engine `Navigation` |
| `navigation()` | Engine `Navigation` |
| `sidebar_layout()` | Engine `Row` |
| `tabs()` | Engine `Tabs` |
| `pagination()` | Engine `Pagination` |
| `menu()` | Engine `Menu` |
| `navigation_controls()` | Engine `Row` + Engine `Button` |
| `breadcrumb_trail()` | Engine `Breadcrumbs` |

This boundary keeps rendering and reactive behavior in the existing PyLage Engine instead of duplicating it in the UI Kit.

## Responsive Styling

Navigation layout components that accept styling use the existing PyLage style infrastructure.

`navbar()` accepts `Style` and `ResponsiveStyle`.

`sidebar_layout()` accepts `Style` and `ResponsiveStyle`.

`navigation_controls()` accepts `Style`.

Responsive behavior therefore remains part of the existing style system rather than introducing navigation-specific responsive logic.

## Verified Working Examples

- `demo/demo_menu_breadcrumbs_pagination.py` — breadcrumb trail, navigation, and pagination usage.
- `demo/demo_pagination.py` — breadcrumb and pagination usage.
- `demo/demo_tabs.py` — tabs usage.
- `demo/demo_navigation_item.py` — navigation item behavior; documented separately.
- `demo/demo_drawer_navigation.py` — drawer-based navigation; documented separately in `docs/drawer.md`.

## Verification

### Automated tests

Navigation-related regression coverage includes:

- `test/components/test_ui_kit_navigation.py` — Engine Navigation rendering, properties, and export.
- `test/components/test_ui_kit_tabs.py` — Tabs rendering, properties, value handling, and reactivity.
- `test/components/test_ui_kit_pagination.py` — Pagination rendering, properties, and children.
- `test/components/test_ui_kit_navigation_item.py` — Navigation Item behavior documented separately.
- `test/integration/test_ui_kit_navigation_responsiveness.py` — responsive style propagation across navigation-related layout components.

The canonical documentation does not record historical full-suite test counts.

## Verified Sources

- `pylage/UI/layout/navbar.py`
- `pylage/UI/layout/navigation.py`
- `pylage/UI/layout/sidebar.py`
- `pylage/UI/layout/tabs.py`
- `pylage/UI/layout/pagination.py`
- `pylage/UI/layout/menu.py`
- `pylage/UI/layout/navigation_controls.py`
- `pylage/UI/patterns/breadcrumbs.py`
- `pylage/ENGINE/components/basic.py`
- `pylage/UI/__init__.py`
- `pylage/UI/layout/__init__.py`
- `pylage/UI/components/__init__.py`
- `pylage/UI/patterns/__init__.py`
- `pylage/__init__.py`
- `test/components/test_ui_kit_navigation.py`
- `test/components/test_ui_kit_tabs.py`
- `test/components/test_ui_kit_pagination.py`
- `test/integration/test_ui_kit_navigation_responsiveness.py`
- `demo/demo_menu_breadcrumbs_pagination.py`
- `demo/demo_pagination.py`
- `demo/demo_tabs.py`

## Status

**FINAL / VERIFIED** — documentation reflects the current navigation-related UI Kit APIs, their Engine reuse/composition boundaries, default styling where applicable, responsive styling support, and verified regression coverage.
