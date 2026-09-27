# Framework Comparison — Drawer, Sidebar, and Navigation

This document records the deliberate architectural differences between PyLage and three Python web UI frameworks: Reflex, Streamlit, and NiceGUI.

The comparison is descriptive rather than a feature ranking. It focuses on the Drawer/sidebar/navigation model relevant to PyLage's current architecture.

## Scope

The comparison covers:

- generic Drawer behavior
- sidebar/navigation composition
- reactive open/close behavior
- routing/navigation
- responsive behavior
- accessibility-related interaction boundaries
- architectural separation between public API and renderer

Performance measurements belong in [Benchmark](../benchmark.md) and are intentionally not repeated here.

## Comparison

| Area | PyLage | Reflex | Streamlit | NiceGUI |
| --- | --- | --- | --- | --- |
| Generic drawer | `pl.drawer()` | `rx.drawer` | No direct Drawer primitive | `ui.drawer(side)` |
| Left/right sidebar | `pl.mobile_sidebar()` or `pl.drawer()` with styling | Drawer configured with direction | `st.sidebar` | `ui.left_drawer()` / `ui.right_drawer()` |
| Navigation entry point | `pl.navigation_drawer()` | Drawer composed with navigation links/state | `st.navigation` with sidebar/top positioning | Drawer composed with links/navigation |
| Open state | Boolean or reactive `State` passed through `open` | Controlled `open` state or `default_open` | Sidebar is framework-managed | Drawer element state/events |
| Open/close events | PyLage event/state system | `on_open_change` | Rerun/session model | Quasar model-value events |
| Responsive styling | `ResponsiveStyle` / `responsive_mode` | Drawer configuration and application layout | Framework-managed sidebar | Quasar drawer/layout behavior |
| Content composition | Normal PyLage components | Reflex components | Streamlit elements | NiceGUI elements/context managers |
| Renderer ownership | Central PyLage engine | Reflex component/runtime stack | Streamlit runtime | NiceGUI/Quasar layout stack |

## PyLage

PyLage exposes three public Drawer recipes:

```python
import pylage as pl

pl.drawer(...)
pl.navigation_drawer(...)
pl.mobile_sidebar(...)
```

These names are semantic entry points. They all reuse the existing Drawer implementation.

The public recipes accept:

- child components
- `Style` or `ResponsiveStyle`
- additional Drawer properties such as `open`, `title`, and CSS/class properties

The recipes therefore do not duplicate rendering, CSS, or state machinery.

### Deliberate PyLage separation

PyLage separates three concerns:

1. **Public semantic API**
   - `drawer()`
   - `navigation_drawer()`
   - `mobile_sidebar()`

2. **Shared Drawer implementation**
   - one underlying Drawer component
   - common rendering and behavior

3. **Engine responsibilities**
   - component construction
   - rendering
   - CSS
   - reactive property handling

This allows applications to communicate intent through the API without requiring three independent implementations.


## Reflex

Reflex provides a dedicated Drawer primitive.

Its documented Drawer API includes:

- controlled `open`
- `default_open`
- `modal`
- direction (`top`, `right`, `bottom`, `left`)
- dismissibility
- snap points
- open-change events
- outside-interaction and Escape-key events
- open/close focus events

Reflex also documents a sidebar-menu pattern built with the Drawer component and application state.

This is architecturally different from PyLage in emphasis: Reflex provides a highly configurable generic Drawer primitive, while PyLage additionally exposes semantic recipes for navigation and mobile-sidebar use cases.

Reference:

- https://reflex.dev/docs/library/overlay/drawer

## Streamlit

Streamlit's sidebar is primarily an application layout/navigation surface rather than a generic Drawer primitive.

For multipage applications, Streamlit documents `st.Page` and `st.navigation` as the preferred navigation mechanism.

`st.navigation`:

- defines the available pages
- acts as the application page router
- can display navigation in the sidebar or at the top
- can be customized with grouped navigation or custom page links

This creates a different boundary from PyLage.

PyLage's Drawer is a reusable UI component that can contain navigation, while Streamlit's navigation API is itself responsible for page selection and can place its navigation UI in the sidebar.

References:

- https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
- https://docs.streamlit.io/1.63.0/develop/api-reference/navigation/st.navigation

## NiceGUI

NiceGUI provides page-layout drawer elements:

```python
from nicegui import ui

with ui.left_drawer():
    ...

with ui.right_drawer():
    ...

with ui.drawer('left'):
    ...
```

The documented API treats drawers as layout elements. NiceGUI also exposes drawer state and events through its element/event model.

This is closer to PyLage's layout-oriented model than Streamlit's sidebar/navigation boundary.

The main architectural difference is that PyLage places semantic `navigation_drawer()` and `mobile_sidebar()` recipes above a shared Drawer component, whereas NiceGUI exposes drawer layout primitives and lets applications compose their own navigation semantics.

## Deliberate Differences

### 1. Semantic recipes are intentional

PyLage does not clone separate rendering implementations for navigation drawers and mobile sidebars.

Instead:

```text
navigation_drawer()
mobile_sidebar()
        |
        v
shared Drawer implementation
        |
        v
PyLage renderer
```

The additional names exist to make application intent explicit at the public API boundary.

### 2. Navigation is composition, not a second Drawer engine

A navigation drawer is still a Drawer.

Navigation links, routing, state, and content are composed using normal PyLage APIs rather than introducing a second renderer.

### 3. Mobile sidebar is a semantic layout choice

`mobile_sidebar()` communicates intended usage while retaining the same underlying Drawer implementation.

Responsive behavior is configured through the existing styling/property system rather than through a separate mobile renderer.

### 4. PyLage does not reproduce framework-specific APIs

PyLage intentionally does not attempt to reproduce:

- Reflex's Drawer prop/event surface
- Streamlit's sidebar/navigation runtime model
- NiceGUI's Quasar-specific drawer API

Similar user-facing capabilities are implemented through PyLage's own component, state, styling, event, and routing architecture.

## What PyLage Reuses

The comparison does not imply that every framework feature should be reproduced.

PyLage deliberately reuses its existing architecture for:

- component composition
- reactive state
- event handling
- responsive styling
- routing
- rendering
- accessibility behavior
- Drawer CSS and DOM behavior

The Drawer recipes are therefore thin public API adapters rather than independent feature implementations.

## Architectural Conclusion

The comparison establishes a deliberate PyLage boundary:

> **PyLage provides Drawer semantics at the public API layer while keeping rendering and behavior centralized in the existing engine.**

The framework comparison is useful for identifying capability differences and architectural trade-offs, not for determining a universal winner.

## Sources

- Reflex Drawer: https://reflex.dev/docs/library/overlay/drawer
- Streamlit multipage navigation: https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
- Streamlit `st.navigation`: https://docs.streamlit.io/1.63.0/develop/api-reference/navigation/st.navigation
- NiceGUI layout reference: https://github.com/zauberzeug/nicegui/blob/main/nicegui/llms.md
- PyLage Drawer documentation: `docs/component/drawer.md`
