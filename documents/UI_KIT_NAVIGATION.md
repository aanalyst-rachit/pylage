# PyLage UI Kit — Navigation

## Status

Phase 10 Navigation components are aligned with the current PyLage UI architecture. Existing navigation capabilities reuse the PyLage ENGINE and UI layers wherever possible. The genuinely missing Navigation Item capability was implemented as a semantic UI wrapper over the existing Button primitive.

## Public API

The canonical public API uses `import pylage as pl`. Navigation components are exposed through the semantic UI layer as lowercase APIs.

```python
import pylage as pl

pl.navbar(...)
pl.navigation(...)
pl.sidebar_layout(...)
pl.breadcrumb_trail(...)
pl.tabs(...)
pl.pagination(...)
pl.menu(...)
pl.navigation_item(...)
pl.mobile_sidebar(...)
```

Legacy CamelCase navigation aliases are not part of the root public API.

## Architecture

PyLage UI Kit does not duplicate the renderer, reactive engine, scheduler, WebSocket runtime, CSS engine, or layout engine. Existing PyLage primitives are reused through the public semantic UI layer.

```text
User Application
      ↓
import pylage as pl
      ↓
pylage.UI semantic layer
      ↓
pylage.ENGINE existing primitives
```

## Navigation Components

### Navbar

`pl.navbar()` is a semantic wrapper around the existing PyLage Navigation primitive. It provides the navigation-bar presentation defaults while preserving the underlying component implementation.

### Sidebar

`pl.sidebar_layout()` reuses the existing PyLage Row primitive to compose sidebar and content areas. It does not create a second layout engine.

### Breadcrumbs

`pl.breadcrumb_trail()` wraps the existing Breadcrumbs primitive and remains a semantic UI pattern.

### Tabs

`pl.tabs()` reuses the existing PyLage Tabs primitive.

### Pagination

`pl.pagination()` reuses the existing PyLage Pagination primitive.

### Menu

`pl.menu()` reuses the existing PyLage Menu primitive.

### Navigation Item

`pl.navigation_item()` was genuinely missing from the existing capability set. It is implemented as a semantic UI wrapper over the existing PyLage Button primitive rather than introducing a new ENGINE component.

It supports static and reactive active state:

```python
pl.navigation_item(
    "Home",
    active=True,
)
```

Reactive active state uses the existing PyLage `State` mechanism and reactive styling infrastructure. The `active` control value is not leaked into the rendered HTML as an unrelated engine property.

### Mobile Navigation

`pl.mobile_sidebar()` reuses the existing Drawer recipe. The Drawer provides actual off-canvas behavior and reactive open/close handling. No separate mobile navigation engine is introduced.

## Reactive Navigation Item

A `State` can control the active navigation item:

```python
active = pl.State(False)
item = pl.navigation_item("Products", active=active)

active.set(True)
active.set(False)
```

The active visual state is represented through reactive style values, allowing the existing dirty-node and WebSocket update architecture to detect and propagate style changes.

## Regression Coverage

Phase 10 regression coverage includes:

- Navbar API and layout behavior.
- Sidebar layout API.
- Breadcrumb trail API and rendering.
- Tabs API.
- Pagination API.
- Menu API.
- Navigation item construction and styling.
- Navigation item custom style overrides.
- Navigation item event forwarding.
- Navigation item reactive active state.
- Navigation item prevention of `active` prop leakage.
- Drawer component behavior used by mobile navigation.
- Reactive Drawer close behavior.
- Navigation responsiveness.
- Public API export checks.
- Layout export audit compatibility with the canonical lowercase navigation API.

## Verification

Focused Phase 10 navigation regression:

```text
35 passed in 2.02s
```

Full project regression after the Phase 10 architecture and audit updates:

```text
973 passed in 113.50s (0:01:53)
```

No test failures remain.

## Manual Verification

Navigation Item manual verification is provided by:

```text
demo/demo_navigation_item.py
```

The manual application verifies that the initially active item is visually selected and that clicking another navigation item updates both the active styling and status text.

## Architecture Decision

Phase 10 follows the project rule:

```text
inspect existing capability
        ↓
REUSE / WRAP / COMPOSE
        ↓
BUILD only when genuinely missing
```

All existing navigation capabilities were aligned using reuse, wrapping, or composition. Navigation Item was the only genuinely missing capability and was built without adding a new ENGINE primitive.

## Phase 10 Boundary

The implementation work for all Phase 10 navigation items is complete and regression-tested. Phase 10 can be marked complete after the tracker is updated and the final git checkpoint is created.
