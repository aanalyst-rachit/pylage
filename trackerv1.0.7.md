# PyLage Navigation & Routing Integration Tracker

## Goal

Integrate the existing PyLage routing system with Navbar, Sidebar, Drawer, NavigationItem, and Breadcrumb components through a clean public navigation API.

The existing Router and RoutingRuntime should be reused. The goal is to connect the existing routing infrastructure with the public navigation UI without unnecessarily redesigning the routing engine.

## Current State

- [x] Router exists.
- [x] Static routes supported.
- [x] Nested routes supported.
- [x] Dynamic routes supported.
- [x] Dynamic route parameters passed to page functions.
- [x] Static route precedence implemented.
- [x] RoutingRuntime exists.
- [x] `RoutingRuntime.navigate()` replaces the stable root page.
- [x] `pl.run(pages_dir=...)` enables public file-based routing.
- [x] Browser-side `window.PyLage.navigate()` exists.
- [x] Browser history `pushState` exists.
- [x] Browser Back/Forward `popstate` handling exists.
- [x] WebSocket `NavigateMessage` exists.
- [x] Navbar exists.
- [x] Sidebar layout exists.
- [x] Drawer / NavigationDrawer / MobileSidebar exist.
- [x] NavigationItem exists.
- [x] BreadcrumbTrail exists.
- [x] Navigation UI is automatically route-aware.
- [x] Public `pl.link()` navigation primitive exists.
- [x] NavigationItem has a route/href contract.
- [x] Active navigation is automatically derived from the current route.
- [x] BreadcrumbTrail is automatically generated from routing state.

## Phase A - Public Link Primitive

### Objective

Create a semantic public navigation primitive:

```python
pl.link("Dashboard", href="/dashboard")
```

Expected semantic HTML:

```html
<a href="/dashboard">Dashboard</a>
```

### Tasks

- [x] Add public `Link` / `link` component.
- [x] Render semantic `<a>` element.
- [x] Support `href`.
- [x] Support standard link attributes.
- [x] Support `class_name` and `style`.
- [x] Distinguish internal routes from external URLs.
- [x] Internal routes use existing PyLage client navigation.
- [x] External URLs retain normal browser navigation.
- [x] Preserve accessibility semantics.
- [x] Add unit tests.
- [x] Add renderer tests.
- [x] Add browser navigation tests.

### Acceptance Criteria

```python
pl.link("Dashboard", href="/dashboard")
```

The link must navigate through the existing PyLage routing system without a full page reload.

## Phase B - Route-Aware NavigationItem

### Objective

Connect the existing NavigationItem component to the Link primitive.

### Tasks

- [x] Add `href` support to NavigationItem.
- [x] Use Link semantics for route navigation.
- [x] Preserve existing action/button behavior.
- [x] Define behavior for conflicting `href` and `on_click`.
- [x] Add validation for invalid combinations.
- [x] Preserve existing styling API.
- [x] Add unit tests.
- [x] Add browser tests.
- [x] Verify NavigationItem inside Navbar.
- [x] Verify NavigationItem inside Sidebar.
- [x] Verify NavigationItem inside Drawer.
- [x] Verify NavigationItem inside MobileSidebar.

## Phase C - Reactive Current Route

### Objective

Expose current routing state to the public UI layer.

### Tasks

- [x] Define public current-route API.
- [x] Make route changes observable/reactive.
- [x] Update route state after successful navigation.
- [x] Update route state after browser Back/Forward.
- [x] Normalize paths consistently.
- [x] Keep route state synchronized with browser URL.
- [x] Add static-route tests.
- [x] Add nested-route tests.
- [x] Add dynamic-route tests.
- [x] Add Back/Forward browser tests.

## Phase D - Automatic Active Navigation

### Objective

NavigationItem should derive its active state from the current route.

### Tasks

- [x] Add automatic active-state detection.
- [x] Define exact-match behavior.
- [x] Define parent-route matching.
- [x] Support nested routes.
- [x] Define optional exact matching.
- [x] Preserve manually controlled active state where required.
- [x] Add unit tests.
- [x] Add browser tests.

## Phase E - Navbar / Sidebar / Drawer Integration

### Objective

Keep Navbar, Sidebar, Drawer, and MobileSidebar as layout/container components while their navigation children become route-aware.

### Navbar

- [x] Route-aware NavigationItem works inside Navbar.
- [x] Active state works inside Navbar.
- [x] Navigation does not perform a full page reload.
- [x] Browser Back/Forward works.

### Sidebar

- [x] Route-aware NavigationItem works inside Sidebar.
- [x] Nested routes work.
- [x] Parent-route active state works.
- [x] Responsive behavior remains unaffected.

### Drawer

- [x] NavigationItem works inside NavigationDrawer.
- [x] NavigationItem works inside MobileSidebar.
- [x] Route transition works while Drawer is open.
- [x] Evaluate automatic Drawer close after navigation.

### Design Rule

Navbar, Sidebar, and Drawer must remain layout/composition components. They should not own the Router.

```text
Router
  ↓
RoutingRuntime
  ↓
Navigation primitive
  ↓
Navbar / Sidebar / Drawer composition
```

## Phase F - Breadcrumb Integration

### Objective

Connect BreadcrumbTrail to routing information.

### Tasks

- [x] Define automatic breadcrumb mode.
- [x] Generate breadcrumb segments from current route.
- [x] Support nested routes.
- [x] Connect breadcrumb items to Link.
- [x] Support current breadcrumb semantics.
- [x] Define labels for dynamic route parameters.
- [x] Add unit tests.
- [x] Add browser tests.

## Phase G - Route Metadata

### Objective

Introduce optional route metadata only where it provides real value.

Potential metadata:

```text
path
name
label
title
```

### Tasks

- [x] Evaluate route metadata requirements.
- [x] Add optional route labels.
- [x] Use metadata for breadcrumbs where available.
- [x] Evaluate document-title integration — deferred; keep the existing application-level Runtime title until route-level document-head updates have a concrete requirement.
- [x] Evaluate automatic navigation generation only after lower-level primitives are stable — deferred; keep navigation explicit so the Router remains responsible for route resolution rather than UI generation.
- [x] Keep route metadata optional.

## Phase H - Navigation Error Handling

### Objective

Make navigation failures predictable and user-facing.

### Tasks

- [x] Define 404 behavior — HTTP/ASGI requests return the existing 404 response; SPA routing raises `LookupError` for an unresolved route.
- [x] Define missing-route behavior — `RoutingRuntime.navigate()` raises `LookupError` before mutating routed content or current-route/path state.
- [x] Evaluate public `not_found` page support — deferred; the Router currently has no special `not_found` page convention, so no new routing convention is introduced without a concrete requirement.
- [x] Ensure failed navigation does not leave the UI in an inconsistent state — failed SPA navigation rolls the browser URL back to the last successful path while preserving the current UI.
- [x] Add regression tests — browser rollback/UI regression and binary navigation-response context tests pass.

## Phase I - Full Integration Tests

### Tasks

- [x] Link to static route.
- [x] Link to nested route.
- [x] Link to dynamic route.
- [x] NavigationItem to static route.
- [x] NavigationItem to dynamic route.
- [x] Navbar navigation.
- [x] Sidebar navigation.
- [x] Drawer navigation.
- [x] MobileSidebar navigation.
- [x] Active navigation state.
- [x] Browser Back.
- [x] Browser Forward.
- [x] `replace=True` behavior.
- [x] External URL handling.
- [x] Invalid route handling.
- [x] Breadcrumb navigation.
- [x] Dynamic route parameters.
- [x] Existing Button behavior regression.
- [x] Existing Drawer behavior regression.
- [x] Existing routing regression tests.
- [x] Full PyLage test suite.

## Phase J - Documentation

### Tasks

- [x] Add routing guide.
- [x] Add Link documentation.
- [x] Add NavigationItem documentation.
- [x] Add Navbar example.
- [x] Add Sidebar example.
- [x] Add NavigationDrawer example.
- [x] Add MobileSidebar example.
- [x] Add active navigation example.
- [x] Add BreadcrumbTrail example.
- [x] Add dynamic route example.
- [x] Document browser Back/Forward behavior.
- [x] Update API reference.
- [ ] Add complete navigation example application.

## Final Target Architecture

```text
                         Router
                           ↓
                    RoutingRuntime
                           ↓
                  Current Route State
                           ↓
                Link / Navigation Primitive
                           ↓
                     NavigationItem
                           ↓
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
          Navbar        Sidebar        Drawer
                                         ↓
                                   MobileSidebar
```

## Core Principles

1. Router remains the single source of route resolution.
2. RoutingRuntime remains the single source of server-side route transitions.
3. Browser navigation continues through the existing PyLage navigation mechanism.
4. Link becomes the semantic navigation primitive.
5. NavigationItem builds on Link.
6. Navbar, Sidebar, Drawer, and MobileSidebar remain layout/container components.
7. Current route becomes reactive framework state.
8. Active navigation derives from current route.
9. Breadcrumbs consume routing information.
10. External URLs remain normal browser links.
11. Existing Button semantics remain unchanged.
12. Each phase requires focused tests before moving to the next phase.
13. Do not redesign Router without a concrete requirement.
14. Do not introduce automatic menu generation before the lower-level navigation primitives are stable.

## Recommended Implementation Order

```text
Phase A → Public Link Primitive
Phase B → Route-Aware NavigationItem
Phase C → Reactive Current Route
Phase D → Automatic Active Navigation
Phase E → Navbar / Sidebar / Drawer Integration
Phase F → Breadcrumb Integration
Phase G → Route Metadata
Phase H → Navigation Error Handling
Phase I → Full Integration Tests
Phase J → Documentation
```

## Status

**Roadmap created — implementation not started.**

Current target: **Phase A — Public Link Primitive**
