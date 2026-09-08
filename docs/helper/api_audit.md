# PyLage UI Kit — Existing API Audit

## Purpose

The new pylage-ui-kit is a high-level developer experience layer on top of the existing PyLage engine and pylage_layout.

It must NOT duplicate the existing renderer, runtime, state, reactivity, styling, theme, layout, or primitive component system.

Architecture:

User Application
        ↓
pylage-ui-kit
        ↓
pylage_layout
        ↓
pylage

## Classification

### REUSE
Use an existing PyLage capability directly.

### WRAP
Provide a simpler or more opinionated API around an existing capability.

### COMPOSE
Combine existing components, layouts, styles, themes, tokens, or patterns into a higher-level recipe.

### BUILD
Create new implementation only when the capability genuinely does not exist.

## 1. Core Runtime

| Capability | Decision |
|---|---|
| Renderer | REUSE |
| WebSocket transport | REUSE |
| DOM patching | REUSE |
| Client runtime | REUSE |
| Reactive State | REUSE |
| Dependency graph | REUSE |
| Scheduler | REUSE |
| Component registry | REUSE |
| Event handling | REUSE |

The UI Kit is NOT a rendering engine.


## 2. Existing Components

Existing `pylage.components.basic` already provides a large component
library.

| Component | Decision |
|---|---|
| Text | REUSE / WRAP |
| Heading | REUSE / WRAP |
| Button | WRAP |
| Card | WRAP / COMPOSE |
| Divider | REUSE |
| Badge | WRAP |
| Avatar | WRAP |
| Image | REUSE / WRAP |
| Video | REUSE |
| Audio | REUSE |
| Icon | WRAP |
| Canvas | REUSE |
| Column | REUSE |
| Row | REUSE |
| Grid | REUSE |
| Accordion | WRAP |
| Carousel | WRAP |
| Table | WRAP |
| Form | WRAP / COMPOSE |
| Dialog | WRAP |
| Drawer | WRAP |
| Navigation | WRAP |
| Tabs | WRAP |
| Checkbox | WRAP |
| RadioGroup | WRAP |
| Switch | WRAP |
| Select | WRAP |
| Slider | WRAP |
| DatePicker | WRAP |
| Input | WRAP |
| Menu | WRAP |
| Tooltip | WRAP |
| Popover | WRAP |
| Alert | WRAP |
| Toast | WRAP |
| Spinner | REUSE / WRAP |
| ProgressBar | WRAP |
| Skeleton | REUSE / WRAP |
| Breadcrumbs | WRAP |
| Pagination | WRAP |

No duplicate primitive implementation should be created.

## 3. Styling

Existing `Style` already provides broad CSS/style coverage.

It includes:

- colors
- backgrounds
- typography
- margin and padding
- dimensions
- display and position
- flex and grid
- gap
- borders
- border radius
- box shadow
- opacity
- overflow
- cursor
- object fitting
- aspect ratio
- z-index
- transform
- transition
- custom properties
- style merging

Decision: REUSE.

The UI Kit must consume the existing `Style` system.


## 4. Theme and Tokens

Existing theme infrastructure provides:

- colors
- spacing
- radius
- fonts
- immutable theme configuration
- CSS custom properties

Existing token groups include:

- COLORS
- FONTS
- RADIUS
- SPACING

Decision: REUSE.

The UI Kit may provide opinionated defaults through this system but
must not create a second theme engine.


## 5. Layout

Existing `pylage_layout` provides:

- AppShell
- Center
- Container
- Footer
- Header
- Navigation
- Pagination
- Menu
- Section
- SidebarLayout
- Split
- Stack
- TwoColumn
- ThreeColumn
- Navbar
- Topbar
- Drawer
- NavigationDrawer
- MobileSidebar
- NavigationControls

Decision: REUSE.

UI Kit layout APIs should wrap or compose these existing layouts.


## 6. Existing Patterns

Existing patterns include:

- LoginForm
- SignupForm
- BreadcrumbTrail
- ContactSection
- ContentSection
- CTA
- FAQ
- FeatureSection
- Hero
- List
- NewsletterSection
- PricingSection
- SearchBar
- EmptyState
- ErrorState
- Loading
- Metric
- MetricCard
- StatsSection
- Testimonial

Decision: WRAP / COMPOSE.

These are strong candidates for high-level UI Kit APIs.


## 7. Existing Templates

Existing templates include:

- LandingPage
- Dashboard
- AdminPanel
- Authentication
- ProfilePage
- Settings
- Documentation

Decision: WRAP / COMPOSE.

The UI Kit should expose easier high-level APIs rather than recreate
these templates.

## 8. Proposed Public API

| API | Decision | Existing Base |
|---|---|---|
| pl.button() | WRAP | Button |
| pl.card() | COMPOSE | Card + primitives |
| pl.metric() | COMPOSE | Metric / MetricCard |
| pl.input() | WRAP | Input |
| pl.form() | COMPOSE | Form + input controls |
| pl.alert() | WRAP | Alert |
| pl.toast() | WRAP | Toast |
| pl.dialog() | WRAP | Dialog |
| pl.drawer() | WRAP | Drawer / NavigationDrawer |
| pl.tabs() | WRAP | Tabs |
| pl.table() | WRAP | Table |
| pl.dashboard() | COMPOSE | Dashboard + layouts |


## 9. Responsive Behavior

Existing ResponsiveStyle already provides responsive styling with sm, md, lg, and xl breakpoints.

Decision: REUSE.

The UI Kit should provide sensible responsive defaults and compose existing ResponsiveStyle behavior. It must not create a second responsive engine.


## 10. Public Export Surface

The existing layout, pattern, and template packages contain public objects that are imported but not always fully represented in __all__.

Decision: CLEANUP.

The UI Kit should expose a stable, intentional public API while preserving the existing package exports. Missing __all__ entries should be normalized where appropriate.

This is API/export cleanup, not a new rendering or component implementation.


## 11. UI Kit Responsibilities

The UI Kit is responsible for developer experience rather than rendering infrastructure.

Responsibilities include:

- simple Python-first component APIs
- modern visual defaults
- component variants
- consistent spacing and sizing
- typography hierarchy
- visual composition
- responsive defaults
- accessibility defaults
- high-level dashboard primitives
- reusable UI recipes
- page-level composition
- clear documentation and examples

## 12. Explicitly Out of Scope

The UI Kit must not implement or duplicate:

- renderer
- WebSocket transport engine
- DOM patching runtime
- reactive State engine
- dependency graph
- scheduler
- component registry
- CSS engine
- Style implementation
- Theme implementation
- token engine
- layout engine
- existing primitive components
- existing patterns
- existing page templates

Any missing capability must first be verified against the existing PyLage architecture before considering BUILD.


## 13. Initial Build Priority

The first implementation wave should focus on the highest-value developer-facing APIs:

1. pl.button()
2. pl.card()
3. pl.metric()
4. pl.badge()
5. pl.input()
6. pl.select()
7. pl.form()
8. pl.alert()
9. pl.toast()
10. pl.dialog()
11. pl.table()
12. pl.tabs()
13. pl.dashboard()
14. layout recipes
15. page recipes

The implementation order may change after each component is validated, but every component must follow the existing architecture boundary.

## 14. Development Rule

For every new UI Kit capability:

1. Inspect the existing implementation.
2. Classify it as REUSE, WRAP, COMPOSE, or BUILD.
3. Prefer REUSE over new implementation.
4. Implement only the UI Kit developer-experience layer.
5. Add tests for the public API and behavior.
6. Update tracker.md.
7. Create a Git checkpoint.

BUILD is the last option, not the default.


## 15. Audit Status

Phase 01 — Existing API Audit: COMPLETE.

The existing PyLage runtime, components, styling, theme, tokens, layouts, patterns, templates, responsive system, and public export surface have been classified for UI Kit reuse.

Conclusion: the UI Kit should be implemented primarily as a WRAP / COMPOSE developer-experience layer. BUILD should only be used when a required capability is proven absent from the existing architecture.

Next phase: PHASE 02 — Package Foundation.

