# PyLage UI Kit — Development Tracker

## Project Goal

Build an opinionated, modern, Python-first UI kit on top of the existing PyLage engine and semantic `pylage.UI` layer.

Target API:

```python
import pylage as pl

pl.card("Revenue", value="₹42,000")
pl.button("Save")
pl.metric("Users", 12450)
````

The UI Kit must NOT duplicate the existing PyLage renderer, reactive engine,
WebSocket system, CSS engine, layout system, or existing components.

---

# Architecture

```text
User Application
       │
       ▼
pylage-ui-kit
       │
       ▼
pylage
       │
       ├── pylage.ENGINE  (internal engine)
       │
       └── pylage.UI      (public semantic UI layer)

---

# PHASE 00 — Scope Lock

* [x] Define `pylage-ui-kit`
* [x] Define Python import: `pylage`
* [x] Define `pl.*` API philosophy
* [x] Confirm UI Kit is a high-level recipe/wrapper layer
* [x] Confirm `pylage` remains the engine
* [x] Confirm layout capabilities are part of the `pylage.UI` architecture
* [x] No duplicate renderer
* [x] No duplicate reactive/state system
* [x] No duplicate CSS engine
* [x] No unnecessary component rewrites

### Exit Condition

PyLage = engine + public package
pylage.ENGINE = internal implementation
pylage.UI = public semantic UI layer

---

# PHASE 01 — Existing API Audit

## Component Audit

* [x] Audit existing `pylage` components
* [x] Audit existing PyLage UI/layout capabilities
* [x] Identify direct re-exports
* [x] Identify wrappers
* [x] Identify recipes
* [x] Identify genuinely missing capabilities

## Classification

```text
DIRECT
  ↓
reuse existing API

WRAPPER
  ↓
simplify existing API

RECIPE
  ↓
compose existing primitives

MISSING
  ↓
implement only when genuinely necessary
```

## Deliverable

* [x] Create `UI_KIT_API_AUDIT.md`

### Exit Condition

Every relevant existing capability is classified as:

`REUSE / WRAP / COMPOSE / BUILD`

---

# PHASE 02 — Package Foundation

* [x] Create `pylage-ui-kit`
* [x] Create `pylage_ui` package
* [x] Define public API
* [x] Define internal API
* [x] Define versioning
* [x] Define dependencies
* [x] Add basic tests
* [x] Verify:

```python
import pylage as pl
```

---

# PHASE 03 — UI Kit Design Contract

Reuse the existing PyLage design infrastructure.

* [x] Spacing behavior
* [x] Radius behavior
* [x] Typography
* [x] Surface behavior
* [x] Borders
* [x] Shadows
* [x] Semantic colors
* [x] Focus states
* [x] Hover states
* [x] Disabled states
* [x] Responsive defaults
* [x] Density
* [x] Component sizing

### Principle

Default API should already look modern:

```python
pl.card(...)
```

Advanced customization remains optional.

---

# PHASE 04 — API Conventions

* [x] `variant`
* [x] `size`
* [x] `disabled`
* [x] `visible`
* [x] `style`
* [x] Event/callback convention
* [x] State convention
* [x] Responsive convention
* [x] Naming convention
* [x] Return-value convention
* [x] Children handling
* [x] Props handling
* [x] Accessibility defaults

### Principle

Components should share predictable API vocabulary.

---

# PHASE 05 — First Component

## `pl.button()`

Target:

```python
pl.button("Save")
```

Variants:

* [x] primary
* [x] secondary
* [x] outline
* [x] ghost
* [x] danger

Sizes:

* [x] sm
* [x] md
* [x] lg

* [x] API
* [x] Implementation
* [x] Styling
* [x] Interaction
* [x] Disabled state
* [x] Tests
* [x] Manual demo
* [x] Documentation

### Exit Condition

`pl.button()` is production-quality.

---

# PHASE 06 — Surface Components

## Card

* [x] `pl.card()`
* [x] Card header
* [x] Card body
* [x] Card footer
* [x] Card variants
* [x] Interactive card

## Text

* [x] `ps.text()`
* [x] `ps.heading()`
* [x] Muted text
* [x] Label
* [x] Caption

## Other

* [x] `ps.badge()`
* [x] `ps.avatar()`
* [x] `ps.divider()`

---

# PHASE 07 — Data & Dashboard

## Metrics

* [x] `pl.metric()`
* [x] KPI
  - Skipped as a separate API/component: `pl.metric()` already represents the KPI presentation pattern.
  - `pl.metric()` should be used for KPIs such as Revenue, Users, Conversion, Orders, or Latency.
  - KPI is a use-case/concept, not a distinct component in the UI Kit.
  - No `ps.kpi()` API is added to avoid duplicate functionality and unnecessary API surface.
* [x] `ps.trend()`
* [x] Stat card
  - Skipped as a separate API/component: `pl.metric()` already provides the standard statistic/KPI presentation pattern.
  - Use `ps.trend()` for directional context and `pl.card()` when a richer or custom statistic layout is needed.
  - No `ps.stat_card()` API is added to avoid overlapping abstractions and unnecessary API surface.

## Data

* [x] Table
* [x] DataFrame
* [x] Data list
* [x] Empty state
* [x] Loading state
* [x] Error state

## Dashboard

* [x] Dashboard header
* [x] Metric grid
* [x] Dashboard section
* [x] Dashboard card
* [x] Responsive dashboard composition

### Exit Condition

A useful dashboard can be created with minimal Python.

---

# PHASE 08 — Forms

* [x] Input
* [x] Textarea
* [x] Select
* [x] Checkbox
* [x] Radio
* [x] Switch
* [x] Slider
* [x] Date picker
* [x] Form field
* [x] Form
* [x] Validation presentation
* [x] Error state
* [x] Help text
* [x] Disabled state

Reuse existing PyLage components wherever possible.

work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

---

# PHASE 09 — Feedback & Overlays

* [x] Alert
* [x] Toast — visibility bug resolved and verified
* [x] Dialog
* [x] Modal recipe
* [x] Drawer
* [x] Tooltip
* [x] Popover
* [x] Confirmation dialog
* [x] Loading overlay

---
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE


# PHASE 10 — Navigation

* [x] Navbar
* [x] Sidebar
* [x] Breadcrumbs
* [x] Tabs
* [x] Pagination
* [x] Menu
* [x] Navigation item
* [x] Mobile navigation

Phase 10 is complete. Existing navigation capabilities were aligned through reuse, wrapping, and composition. Navigation Item was created only because no equivalent existing capability was found.
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

---

# PHASE 11 — Layout API

Do NOT create a separate layout engine. Layout capabilities belong to the existing `pylage.UI` architecture.

* [x] Determine direct re-exports
  - Row wrapper added around the existing PyLage Row component.
  - Column wrapper added around the existing PyLage Column component.
  - Both use the existing UI Kit responsive style resolution.
  - Both are publicly exported through pylage.UI.layout and pylage.UI.
  - Neither duplicates the layout engine.
* [x] Responsive shorthand
* [x] Spacing shorthand
* [x] Dashboard layout helpers
* [x] Verify no duplicate layout engine

Potential API:

```python
pl.container(...)
pl.stack(...)
pl.row(...)
pl.grid(...)
pl.columns(...)
pl.sidebar(...)
```

work flow - reuse/create/------>manual create-------> manual verify---->documentation-----> tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

---

# PHASE 12 — High-Level Recipes

* [x] Login page
* [x] Signup page
* [x] Dashboard
* [x] Admin panel
* [x] Profile page
* [x] Settings page
* [x] Pricing section
* [x] Empty page
* [x] Error page
* [x] Data management page
Potential API:

```python
ps.dashboard(
    title="Sales Dashboard",
    metrics=[...],
    content=[...],
)
```

---
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE


# PHASE 13 — Responsive Intelligence

Reuse existing responsive infrastructure.

* [x] Responsive defaults
* [x] Mobile behavior
* [x] Tablet behavior
* [x] Desktop behavior
* [x] Responsive components
* [x] Responsive recipes
* [x] Developer overrides

### Goal

Components should adapt without requiring manual CSS/media queries.
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

---

# PHASE 14 — Customization

Default:

```python
pl.card(...)
```

Advanced:

```python
pl.card(
    ...,
    variant="dark",
)
```

More advanced:

```python
pl.card(
    ...,
    style=...
)
```

* [ ] Variant system
* [ ] Size system
* [ ] Theme integration
* [ ] Style overrides
* [ ] Semantic colors
* [ ] Custom tokens
* [ ] Component-level overrides
* [ ] set Global theme system
* [ ] Global overrides
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

### Principle

Customization must never destroy default simplicity.

---

# PHASE 15 — Accessibility & Interaction

* [ ] Keyboard behavior
* [ ] Focus behavior
* [ ] Disabled behavior
* [ ] Semantic labels
* [ ] Interactive states
* [ ] Modal behavior
* [ ] Navigation behavior
* [ ] Form accessibility

---
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

# PHASE 16 — Performance

PyLage UI Kit must preserve PyLage's low-latency architecture.

* [ ] Component creation overhead
* [ ] Render overhead
* [ ] State update overhead
* [ ] WebSocket update behavior
* [ ] Unnecessary tree changes
* [ ] Large dashboard behavior
* [ ] Large table behavior
* [ ] Repeated component creation
* [ ] Client/bundle impact

### Principle
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

High-level API → efficient existing PyLage primitives.

---

# PHASE 17 — Test Matrix

Every component should eventually pass:
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

```text
UNIT
  ↓
API
  ↓
RENDER
  ↓
REACTIVE
  ↓
INTERACTION
  ↓
RESPONSIVE
  ↓
MANUAL
```

* [ ] API tests
* [ ] Rendering tests
* [ ] State tests
* [ ] Interaction tests
* [ ] Regression tests
* [ ] Responsive tests
* [ ] Manual examples

---

# PHASE 18 — Example Application

Build one serious application entirely with UI Kit.

```text
PyLage UI Kit Demo
│
├── Dashboard
├── Analytics
├── Forms
├── Tables
├── Navigation
├── Overlays
├── Components
└── Themes
```
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

Goal:

```python
import pylage as pl
```

The majority of application code should use high-level `pl.*` APIs.

---

# PHASE 19 — Documentation
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

* [ ] Installation
* [ ] First app
* [ ] Components
* [ ] Layout
* [ ] Forms
* [ ] Dashboard
* [ ] Data
* [ ] Navigation
* [ ] Theming
* [ ] Customization
* [ ] Responsive behavior
* [ ] State/events
* [ ] Recipes
* [ ] Migration from low-level PyLage API

---

# PHASE 20 — API Stabilization
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

* [ ] Remove unnecessary APIs
* [ ] Fix inconsistent naming
* [ ] Reduce configuration surface
* [ ] Verify imports
* [ ] Verify documentation
* [ ] Verify examples
* [ ] Verify compatibility
* [ ] Verify performance
* [ ] Verify tests

### Principle

Small API surface + powerful composition.

---

# PHASE 21 — Release
work flow - reuse/create/------>manual create-------> manual verify---->documentation----->tracker update---git checkpoint
rules - PYTHON TERMINAL RULE + MD FILE RULE

Target:

```text
pylage-ui-kit 0.x
```

Release checklist:

* [ ] Package metadata
* [ ] Dependencies
* [ ] README
* [ ] Examples
* [ ] Tests
* [ ] Changelog
* [ ] Version
* [ ] Git tag
* [ ] Release notes
* [ ] Clean-environment installation test

---

# MASTER STATUS

```text
PHASE 00  Scope Lock                [x]
PHASE 01  Existing API Audit        [x]
PHASE 02  Package Foundation        [x]
PHASE 03  Design Contract           [x]
PHASE 04  API Conventions           [x]
PHASE 05  First Component           [x]
PHASE 06  Surface Components        [x]
PHASE 07  Data/Dashboard            [x]
PHASE 08  Forms                     [x]
PHASE 09  Feedback/Overlays         [x]
PHASE 10  Navigation                [x]
PHASE 11  Layout API                [ ]
PHASE 12  High-Level Recipes        [ ]
PHASE 13  Responsive Intelligence   [ ]
PHASE 14  Customization             [ ]
PHASE 15  Accessibility             [ ]
PHASE 16  Performance               [ ]
PHASE 17  Test Matrix               [ ]
PHASE 18  Example Application       [ ]
PHASE 19  Documentation             [ ]
PHASE 20  API Stabilization         [ ]
PHASE 21  Release                   [ ]
```

---

# Current State

```text
PyLage Core                [EXISTING]
Components                 [EXISTING]
Theme / Tokens             [EXISTING]
pylage.UI                  [EXISTING]
Reactive Engine            [EXISTING]

pylage-ui-kit              [PHASE 10 COMPLETE — Navigation aligned and Navigation Item added]

Latest Navigation checkpoint:
- Existing navigation capabilities reuse, wrap, or compose existing PyLage primitives.
- Navigation Item was implemented as a semantic wrapper over the existing Button primitive.
- Navigation Item reactive active state is verified.
- Navigation Item manual verification is complete.
- Phase 10 documentation is complete.
- Focused Phase 10 navigation regression: 35 passed.
- Full test suite: 973 passed.
```

# Development Rule

DO NOT rebuild functionality that already exists in `pylage` or its internal
`pylage.ENGINE`. Use the public semantic `pylage.UI` layer for user-facing APIs.

Before implementing anything new:

1. Inspect existing implementation.
2. Decide REUSE / WRAP / COMPOSE / BUILD.
3. Prefer reuse.
4. Add new implementation only when genuinely required.
5. Test.
6. Update this tracker.
7. Git checkpoint.

## file making rule
rules - PYTHON TERMINAL RULE + MD FILE RULE

PYTHON TERMINAL COMMAND RULE
Jab Python code/command terminal mein execute karne ke liye deni ho:
1. Command copy-paste safe honi chahiye.
2. Multiline heredoc (`python - <<'PY'`) avoid karo.
3. `>`, `|` jaise terminal prompt characters content ka part nahi banne chahiye.
4. Quotes, backticks, braces aur multiline strings safely preserve hone chahiye.
5. File generate/update karne ke liye terminal-safe method use karo.
6. Unnecessary `nano`/`vim` avoid karo jab direct command possible ho.
7. Command dene se pehle shell/Python syntax corruption check karo.

MARKDOWN FILE RULE — ESCAPED NEWLINE FORMAT
Jab `.md` file create/update karni ho:
1. `cat <<'EOF'` / heredoc use nahi karna.
2. `python - <<'PY'` ke andar multiline Markdown use nahi karna.
3. Markdown terminal-safe escaped-newline format mein dena.
4. Paragraph/section separation ke liye `\n\n` preserve karna.
5. Markdown code fences exactly preserve hone chahiye.
6. `>`, `$`, backticks, quotes aur special characters safely preserve hone chahiye.
7. Command directly copy-paste karke `.md` file create/update ho sake.
8. File create/update ke baad `git diff --check` se verify karna.

# FUTURE IDEAS

* CRUD page
* Analytics dashboard
