# PyLage Drawer — Progress Tracker

> Goal: PyLage Drawer system ko production-grade, accessible, responsive aur reusable banana.

## Current Baseline

- [x] `pl.drawer()` public API
- [x] `pl.navigation_drawer()` public API
- [x] `pl.mobile_sidebar()` public API
- [x] Arbitrary child composition
- [x] Boolean `open` support
- [x] Reactive `open` state support
- [x] Custom style/class/title support
- [x] Fixed off-canvas Drawer rendering
- [x] CSS open/close transition
- [x] Route-aware `navigation_item()` integration
- [x] Responsive styling infrastructure
- [x] Existing Drawer/navigation/browser/WebSocket/regression tests
- [x] Live public-API Drawer application

## Phase 1 — Contract Freeze & Baseline

- [x] Freeze current Drawer API contract
- [x] Audit existing Drawer implementation
- [x] Audit existing Drawer tests
- [x] Identify reusable runtime, event, responsive and accessibility infrastructure
- [x] Establish focused regression baseline

## Phase 2 — Interaction Foundation [P0]

- [x] Overlay/backdrop
- [x] Outside-click dismissal
- [x] Escape-key dismissal
- [ ] Canonical close/state pipeline
- [x] Drawer-specific interaction tests

## Phase 3 — Direction & Positioning [P0]

- [x] Generalize Drawer side/position model
- [x] Left Drawer
- [x] Right Drawer
- [x] Top Drawer
- [x] Bottom Drawer
- [x] Direction-specific CSS transitions
- [x] Viewport sizing/constraints
- [x] Direction regression tests

## Phase 4 — Accessibility [P0]

- [x] Correct Drawer semantics
- [x] ARIA attributes
- [x] Keyboard navigation
- [x] Focus entry behavior
- [x] Focus containment for modal Drawer
- [x] Focus restoration on close
- [x] Accessibility browser tests

## Phase 5 — Modal vs Persistent [P0]

- [x] Define modal Drawer contract
- [x] Define persistent Drawer contract
- [ ] Optional overlay behavior
- [x] Background interaction rules
- [x] Scroll-lock behavior for modal Drawer
- [x] Restore scrolling after close
- [x] Tests for both modes

## Phase 6 — Scroll & Content Behavior [P0]

- [x] Drawer content scrolling
- [x] Long-content browser test
- [x] Small-viewport test
- [x] Body scroll-lock test

## Phase 7 — Responsive Drawer System [P1]

- [x] Reuse existing ResponsiveStyle infrastructure
- [x] Define responsive Drawer behavior
- [x] Desktop persistent mode
- [x] Mobile overlay mode
- [ ] Breakpoint-aware navigation behavior
- [x] Responsive browser/integration tests

## Phase 8 — Navigation Drawer [P1]

- [x] Define NavigationDrawer specialization
- [x] Current-route integration
- [x] Active navigation item integration
- [x] Navigation click behavior
- [x] Mobile navigation auto-close
- [x] Navigation Drawer browser tests

## Phase 9 — Mobile Sidebar [P1]

- [x] Define MobileSidebar specialization
- [x] Mobile overlay behavior
- [x] Backdrop behavior
- [x] Escape/outside-click behavior
- [x] Route-change close behavior
- [x] Mobile browser tests

## Phase 10 — Drawer Lifecycle Events [P1]

- [x] Evaluate canonical `on_open_change` API
- [x] Wire lifecycle events through existing event system
- [x] Reactive state/event consistency tests
- [x] WebSocket verification

## Phase 11 — Advanced Interaction [P2]

- [x] Evaluate drag-to-close — evaluated; no existing gesture infrastructure, so not justified for core Drawer
- [x] Evaluate snap points — evaluated; would introduce a new intermediate-position model not required by current Drawer architecture
- [x] Evaluate close threshold — evaluated; only becomes meaningful with drag interaction, which is not justified currently
- [x] Implement only if architecture and UX justify them — evaluation concluded that implementation is not justified at this stage

## Phase 12 — Persistent / Mini Sidebar [P2]

- [x] Audit existing sidebar primitives — existing SidebarLayout, State/DerivedState, Style, ResponsiveStyle, and cond() already cover the required composition
- [x] Define expanded/collapsed model if needed — no new model required; expanded/collapsed state can use existing State/DerivedState with reactive Style values
- [x] Avoid forcing persistent-sidebar concerns into core Drawer — persistent/mini sidebar behavior is presentation/layout state and remains outside core Drawer
- [x] Add dedicated sidebar behavior only where justified — no dedicated primitive justified; existing public primitives provide the required behavior

## Phase 13 — Portal & Layering [P2]

- [x] Audit current renderer layering — existing `position`, `z_index`, fixed overlay, Drawer backdrop, and loading-overlay primitives already provide the required layering model
- [x] Determine whether portal is architecturally necessary — no current component requires DOM reparenting; existing fixed overlays render correctly through normal component composition
- [x] Handle overlay/z-index/clipping if required — existing z-index contracts remain intact; browser verification confirms a fixed loading overlay remains viewport-sized inside an `overflow: hidden` ancestor
- [x] Add portal only when justified — no portal introduced because the current architecture has no demonstrated portal requirement

## Phase 14 — Nested Drawer Coordination [P2]

- [x] Define nested Drawer behavior — nested modal Drawers remain independently open, with DOM order defining the topmost modal
- [x] Define modal Drawer stacking rules — existing modal z-index contract is preserved; the last open modal Drawer is treated as topmost
- [x] ESC closes topmost applicable Drawer — existing Escape handling targets the last open dismissible Drawer
- [x] Focus restoration rules — each modal stores its return-focus target; nested close restores the parent Drawer action, then the original trigger
- [x] Multi-Drawer tests — browser coverage verifies two simultaneously open modal Drawers, topmost Escape dismissal, and nested focus restoration

## Phase 15 — Public API Cleanup

- [x] Review final Drawer API — top-level `pylage` exposes the canonical `drawer`, `navigation_drawer`, and `mobile_sidebar` APIs
- [x] Remove unnecessary internal leakage — package-level `pylage.UI.layout` does not expose the uppercase Drawer constructors; dedicated `pylage.UI.layout.drawer` remains available for existing consumers
- [x] Preserve public API consistency — top-level Drawer recipes and the dedicated layout module retain their established API boundaries
- [x] Add public API regression tests — public exports, package-level leakage boundaries, and dedicated layout compatibility are covered

## Phase 16 — Comprehensive Testing

- [x] Component tests
- [x] Reactive state tests
- [x] Interaction tests
- [x] Accessibility tests
- [x] Responsive tests
- [x] Navigation tests
- [x] WebSocket tests
- [x] Browser tests
- [x] Full regression suite

## Phase 17 — Live Drawer Showcase

- [x] Keep `live/drawer/` public-API-only
- [x] Basic Drawer demonstration
- [x] Navigation Drawer demonstration
- [x] Mobile Sidebar demonstration
- [x] Reactive open/close
- [x] Image/content composition
- [x] Routing
- [x] Responsive behavior
- [x] Accessibility behavior
- [x] Overlay/outside-click behavior
- [x] Multiple Drawer configurations

## Phase 18 — Framework Comparison

- [x] Compare final PyLage behavior with Reflex Drawer
- [x] Compare final PyLage sidebar/navigation model with Streamlit
- [x] Compare final PyLage Drawer/sidebar model with NiceGUI
- [x] Document deliberate differences
- [x] Avoid feature cloning without architectural justification

## Phase 19 — Performance Audit

- [ ] Initial render measurement
- [ ] Open latency measurement
- [ ] Close latency measurement
- [ ] Reactive update measurement
- [ ] DOM mutation measurement
- [ ] WebSocket payload measurement
- [ ] Multiple-Drawer stress test
- [ ] Large navigation list test

## Phase 20 — Documentation

- [x] Basic Drawer documentation
- [x] Modal Drawer documentation
- [x] Navigation Drawer documentation
- [x] Mobile Sidebar documentation
- [x] Responsive usage documentation
- [x] Accessibility documentation
- [x] Final API reference

## Phase 21 — Final Verification & Release Readiness

- [x] Focused Drawer tests pass
- [x] Live browser verification passes
- [x] Routing verification passes
- [x] Responsive browser verification passes
- [x] Accessibility verification passes
- [x] Full pytest regression passes
- [x] `git diff --check` passes
- [x] `git status` reviewed
- [x] Final implementation diff reviewed
- [ ] Release notes/documentation updated when requested
- [x] Git checkpoint created

## Phase 22 — Navigation & Routing Integration

> Merged from the root v1.0.7 Navigation & Routing tracker.
>
> This phase records the completed integration of the existing Router and
> RoutingRuntime with PyLage's public navigation primitives and UI containers.
> The archived Drawer phases above remain unchanged.

### Scope

- Reuse the existing Router and RoutingRuntime.
- Expose semantic public navigation through `pl.link()`.
- Make NavigationItem route-aware and reactive.
- Integrate route state with Navbar, Sidebar, Drawer, and MobileSidebar.
- Connect BreadcrumbTrail to routing state.
- Preserve normal browser behavior for external URLs.
- Preserve existing Button, Drawer, and routing semantics.

### Phase A - Public Link Primitive

#### Objective

Create a semantic public navigation primitive:

```python
pl.link("Dashboard", href="/dashboard")
```

Expected semantic HTML:

```html
<a href="/dashboard">Dashboard</a>
```

#### Tasks

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

#### Acceptance Criteria

```python
pl.link("Dashboard", href="/dashboard")
```

The link must navigate through the existing PyLage routing system without a full page reload.

### Phase B - Route-Aware NavigationItem

#### Objective

Connect the existing NavigationItem component to the Link primitive.

#### Tasks

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

### Phase C - Reactive Current Route

#### Objective

Expose current routing state to the public UI layer.

#### Tasks

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

### Phase D - Automatic Active Navigation

#### Objective

NavigationItem should derive its active state from the current route.

#### Tasks

- [x] Add automatic active-state detection.
- [x] Define exact-match behavior.
- [x] Define parent-route matching.
- [x] Support nested routes.
- [x] Define optional exact matching.
- [x] Preserve manually controlled active state where required.
- [x] Add unit tests.
- [x] Add browser tests.

### Phase E - Navbar / Sidebar / Drawer Integration

#### Objective

Keep Navbar, Sidebar, Drawer, and MobileSidebar as layout/container components while their navigation children become route-aware.

#### Navbar

- [x] Route-aware NavigationItem works inside Navbar.
- [x] Active state works inside Navbar.
- [x] Navigation does not perform a full page reload.
- [x] Browser Back/Forward works.

#### Sidebar

- [x] Route-aware NavigationItem works inside Sidebar.
- [x] Nested routes work.
- [x] Parent-route active state works.
- [x] Responsive behavior remains unaffected.

#### Drawer

- [x] NavigationItem works inside NavigationDrawer.
- [x] NavigationItem works inside MobileSidebar.
- [x] Route transition works while Drawer is open.
- [x] Evaluate automatic Drawer close after navigation.

#### Design Rule

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

### Phase F - Breadcrumb Integration

#### Objective

Connect BreadcrumbTrail to routing information.

#### Tasks

- [x] Define automatic breadcrumb mode.
- [x] Generate breadcrumb segments from current route.
- [x] Support nested routes.
- [x] Connect breadcrumb items to Link.
- [x] Support current breadcrumb semantics.
- [x] Define labels for dynamic route parameters.
- [x] Add unit tests.
- [x] Add browser tests.

### Phase G - Route Metadata

#### Objective

Introduce optional route metadata only where it provides real value.

Potential metadata:

```text
path
name
label
title
```

#### Tasks

- [x] Evaluate route metadata requirements.
- [x] Add optional route labels.
- [x] Use metadata for breadcrumbs where available.
- [x] Evaluate document-title integration — deferred; keep the existing application-level Runtime title until route-level document-head updates have a concrete requirement.
- [x] Evaluate automatic navigation generation only after lower-level primitives are stable — deferred; keep navigation explicit so the Router remains responsible for route resolution rather than UI generation.
- [x] Keep route metadata optional.

### Phase H - Navigation Error Handling

#### Objective

Make navigation failures predictable and user-facing.

#### Tasks

- [x] Define 404 behavior — HTTP/ASGI requests return the existing 404 response; SPA routing raises `LookupError` for an unresolved route.
- [x] Define missing-route behavior — `RoutingRuntime.navigate()` raises `LookupError` before mutating routed content or current-route/path state.
- [x] Evaluate public `not_found` page support — deferred; the Router currently has no special `not_found` page convention, so no new routing convention is introduced without a concrete requirement.
- [x] Ensure failed navigation does not leave the UI in an inconsistent state — failed SPA navigation rolls the browser URL back to the last successful path while preserving the current UI.
- [x] Add regression tests — browser rollback/UI regression and binary navigation-response context tests pass.

### Phase I - Full Integration Tests

#### Tasks

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

### Phase J - Documentation

#### Tasks

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
