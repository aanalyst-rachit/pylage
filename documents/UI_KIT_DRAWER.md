# PyLage UI Kit — Drawer

## Status

Drawer is complete as a Phase 09 Feedback & Overlays component.

- Drawer recipe: `pylage.UI.recipes.drawer.drawer`
- Navigation Drawer recipe: `pylage.UI.recipes.drawer.navigation_drawer`
- Mobile Sidebar recipe: `pylage.UI.recipes.drawer.mobile_sidebar`
- Full test suite: **918 passed**
- Stable checkpoint: `e044905` — `ui_kit_drawer_bug resolved`

## Architecture

The UI Kit reuses the existing PyLage Drawer implementation instead of creating a second Drawer system.

The recipes wrap:

```python
import pylage as pl

drawer = pl.drawer
navigation_drawer = pl.navigation_drawer
mobile_sidebar = pl.mobile_sidebar
```

Architecture:

```text
pylage-ui-kit
      ↓
pylage_layout
      ↓
pylage
```

The UI Kit does not duplicate the renderer, reactive engine, scheduler, WebSocket runtime, or layout system.

## Drawer Behavior

The Drawer is an actual off-canvas Drawer.

### Closed

- Hidden from the visible viewport.
- Translated outside the viewport.
- `visibility: hidden`.
- `pointer-events: none`.

### Open

- Slides into view.
- Visible to the user.
- Accepts pointer interaction.

The Drawer uses fixed positioning and viewport height rather than behaving as a normal left-side layout column.

## Reactive Open/Close

The `open` property is a normal reactive boolean property.

A transition:

```python
open_state.set(False)
```

is serialized as:

```python
props={"open": False}
remove_props=[]
```

A boolean changing from `True` to `False` is a changed property. It has not been removed from the component snapshot.

`remove_props` is reserved for properties that actually disappear from the snapshot.

## Reactive Update Architecture

Changed properties are tracked by the dirty-node system:

```text
State change
    ↓
DirtyNodes.mark(component, prop_name)
    ↓
Scheduler batches component
    ↓
Changed property names are preserved
    ↓
Scheduled update
    ↓
Only changed props are serialized
```

Multiple changed properties for the same component remain available during the same scheduler batch.

## Renderer

The Drawer renderer provides the off-canvas presentation through the registered Drawer renderer and CSS.

The implementation keeps Drawer behavior in the renderer/layout architecture and does not add a Drawer-specific workaround to the client runtime.

## Recipes

### Drawer

```python
import pylage as pl

pl.drawer(...)
```

### Navigation Drawer

```python
import pylage as pl

pl.navigation_drawer(...)
```

### Mobile Sidebar

```python
import pylage as pl

pl.mobile_sidebar(...)
```

## Regression Coverage

Drawer work includes coverage for:

- Drawer component construction.
- Drawer renderer registration.
- Drawer CSS/off-canvas behavior.
- Drawer recipe exports.
- Navigation Drawer.
- Mobile Sidebar.
- Reactive open/close behavior.
- WebSocket update serialization.
- Dirty-node changed-property tracking.
- Existing checkbox boolean reactive updates.
- Existing switch boolean reactive updates.

## Verification

The final full regression suite passed:

```text
918 passed in 157.97s (0:02:37)
```

Focused checkbox and switch boolean regression tests also passed.

## Git Checkpoint

```text
e044905 ui_kit_drawer_bug resolved
```

The checkpoint was pushed to `origin/main`.

## Phase 09 Boundary

Drawer is complete, but Phase 09 remains incomplete.

Remaining Phase 09 items:

- Toast — complete.
- Tooltip
- Popover
- Confirmation dialog
- Loading overlay

Phase 09 must not be marked complete until its remaining required components are implemented and verified.
