# PyLage

**PyLage** is a reactive, server-driven, differential UI framework written entirely in Python. You build a component tree in Python, bind it to reactive `State` objects, and PyLage renders it to HTML — either as a static file or as a live, WebSocket-powered application where state changes on the server are diffed and patched straight into the browser DOM, with no client-side framework code to write.

```
Python State  →  DependencyGraph  →  DirtyNodes  →  Scheduler
     │                                                   │
     ▼                                                   ▼
Component Tree  ──── snapshot/diff/patch ────►  WebSocket  ──►  Browser DOM
```

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quickstart](#quickstart)
  - [1. Static HTML rendering](#1-static-html-rendering)
  - [2. Live, reactive app](#2-live-reactive-app)
- [Architecture Overview](#architecture-overview)
- [Component Reference](#component-reference)
- [Styling & Theming](#styling--theming)
- [Reactivity Model](#reactivity-model)
- [Client ↔ Server Protocol](#client--server-protocol)
- [Testing](#testing)
- [Project Layout](#project-layout)
- [Known Limitations](#known-limitations)
- [License](#license)

---

## Features

- **Pure Python component model** — no JSX, no templates. Components are plain trees built with functions like `Column`, `Row`, `Text`, `Button`.
- **Fine-grained reactivity** — `State` objects, a `DependencyGraph` mapping state → (component, prop), `DirtyNodes` tracking, and a `Scheduler` that batches multiple synchronous state changes into a single flush.
- **Two render modes**:
  - `serve=False` (default): renders one static `index.html` file.
  - `serve=True`: starts an HTTP server (initial HTML) + a WebSocket server (live diff/patch updates) and opens a browser.
- **Snapshot → Diff → Patch pipeline** for tree-level changes (`insert`, `remove`, `replace`, `update`, `events`) and a **generic reactive prop pipeline** for value-level changes, both delivered over the same WebSocket connection.
- **Central component registry** — every component's HTML tag, prop contract (`kind`: `attribute` / `boolean` / `text`, `reactive`, `html_name`) and optional custom renderer are declared once and used consistently by the renderer, the state binder, and the IR/compiler layer.
- **Two-way input binding** — `Input(value=state)` auto-wires an `on_input` handler that calls `state.set(...)`, and the browser round-trips edits back to Python.
- **Structured `Style` / `ResponsiveStyle` / `Theme` system** with CSS custom-property support and breakpoint-based media queries.
- **463 passing tests** covering components, registry contracts, reactivity, diffing, protocol messages, the browser client runtime, and live browser integration (Playwright).

---

## Installation

PyLage is a local Python package (no PyPI release referenced in this codebase). Clone/copy the `pylage/` package into your project and install its runtime dependency:

```bash
pip install websockets
```

> The WebSocket server (`pylage/runtime/websocket.py`) imports `websockets.asyncio.server`. Browser-integration tests additionally require `playwright` (`pip install playwright && playwright install chromium`), and `pytest-asyncio` is used by several async tests — these are **test-only** dependencies, not required to use PyLage itself.

Project layout expected on `PYTHONPATH`:

```
your_project/
├── pylage/            # the framework package
│   ├── app.py
│   ├── components/
│   ├── core/
│   ├── renderers/
│   ├── runtime/
│   └── styling/
└── your_app.py
```

---

## Quickstart

### 1. Static HTML rendering

The simplest usage — build a tree, call `pylage.run()`, get a self-contained HTML file back.

```python
import pylage as ps

app = ps.Column(
    ps.Heading("Hello PyLage"),
    ps.Text("This file was rendered statically."),
    ps.Button("Click me", variant="primary"),
)

output_path = ps.run(
    app,
    title="My PyLage App",
    output="dist/index.html",   # defaults to "index.html"
)

print("Rendered to:", output_path)
```

`ps.run(app, serve=False, ...)` (the default) never starts a server; it writes one HTML document (including the embedded client runtime `<script>` — inert since no WebSocket URL is configured) to `output` and returns a `pathlib.Path`.

### 2. Live, reactive app

Set `serve=True` to start a local HTTP + WebSocket server, wire up `State`, and get live DOM updates whenever Python-side state changes — including from Python-side timers/threads, not just click handlers.

```python
import pylage as ps

count = ps.State(0)

def increment():
    count.set(count.value + 1)
    return count.value

app = ps.Column(
    ps.Heading(count),                 # State passed directly as a prop
    ps.Button("Increment", on_click=increment),
)

ps.run(
    app,
    title="Reactive Counter",
    serve=True,          # starts HTTP + WebSocket servers, opens a browser
    output="live/index.html",
)
```

Two-way input binding works the same way — pass a `State` as `value=` to `Input` and PyLage wires the browser `input` event back to `state.set(...)` automatically:

```python
name = ps.State("Dollar")

app = ps.Column(
    ps.Heading(name),
    ps.Input(value=name),   # typing in the browser updates `name` in Python
)
```

For production/embedded use without the blocking `run()` loop, drive the `Runtime` object directly:

```python
from pylage.runtime import Runtime

runtime = Runtime(app, title="My App", output="dist/index.html")
url = runtime.start()      # returns "http://127.0.0.1:<port>/"
...
runtime.stop()
```

---

## Architecture Overview

PyLage is organized into five layers. Data flows one way on state change, and the browser only ever receives small JSON patch messages, never a full re-render.

```
┌───────────────────────────────────────────────────────────────────────┐
│ 1. COMPONENT LAYER (pylage/core/component.py, pylage/components/)     │
│    Component: type, props, children, events, id (uuid4 hex[:10])      │
│    component() factory splits on_* kwargs into `events`,              │
│    consults ComponentRegistry for the prop contract                   │
└───────────────────────────────────────────────────────────────────────┘
                                   │
┌───────────────────────────────────────────────────────────────────────┐
│ 2. REGISTRY LAYER (pylage/core/registry.py)                           │
│    ComponentRegistry: type -> ComponentDefinition(tag, void, renderer,│
│    props: {name: PropDefinition(kind, reactive, html_name)})          │
│    Single source of truth used by HTMLRenderer, StateBinding, IR      │
└───────────────────────────────────────────────────────────────────────┘
                                   │
┌───────────────────────────────────────────────────────────────────────┐
│ 3. REACTIVITY LAYER (pylage/core/state.py, graph.py, dirty.py,        │
│    scheduler.py, binding.py)                                          │
│    State.set() -> notifies subscribers                                │
│    StateBinding walks the tree at construction time, subscribes to    │
│    every State-valued *reactive* prop, and on change either:          │
│      a) calls the callback immediately (no scheduler), or             │
│      b) marks the owning Component dirty in DirtyNodes and calls      │
│         Scheduler.request() (coalesces N sync changes -> 1 flush)     │
└───────────────────────────────────────────────────────────────────────┘
                                   │
┌───────────────────────────────────────────────────────────────────────┐
│ 4. RENDER / DIFF / PATCH LAYER                                        │
│    HTMLRenderer (core/renderer.py): Component tree -> HTML string,    │
│      registry-driven tag/attribute/boolean/text resolution            │
│    component_to_snapshot (core/snapshot.py): Component -> JSON dict   │
│    diff() (core/diff.py): previous snapshot, current snapshot ->      │
│      [update | insert | remove | replace | events] operations         │
│    operation_to_message() (core/patch.py): operation -> protocol      │
│      message (UpdateMessage / TreeAddMessage / TreeRemoveMessage /    │
│      TreeReplaceMessage)                                              │
│    Tree mutations (add/remove/replace/clear/set_children/move_to)     │
│      are additionally observed live via TreeMutationObserver and      │
│      broadcast directly as Tree*Message, independent of diff/patch    │
└───────────────────────────────────────────────────────────────────────┘
                                   │
┌───────────────────────────────────────────────────────────────────────┐
│ 5. RUNTIME / TRANSPORT LAYER (pylage/runtime/)                        │
│    LocalServer: threaded http.server serving the rendered index.html  │
│    WebSocketServer: websockets.asyncio.server; binds StateBinding +   │
│      TreeMutationObserver to the root, dispatches inbound `event`     │
│      messages via EventDispatcher, broadcasts outbound update/tree_*  │
│      messages to all connected clients                                │
│    client.py (CLIENT_RUNTIME): vanilla-JS runtime embedded in the     │
│      HTML document; listens for click/input/change, sends `event`     │
│      messages, and applies update/tree_add/tree_remove/tree_replace/  │
│      tree_clear/tree_set_children/tree_move patches to the real DOM   │
└───────────────────────────────────────────────────────────────────────┘
```

**Round trip for a browser click:**
`click` (DOM) → `data-pylage-events` lookup → `sendEvent()` → WebSocket `event` message → `EventDispatcher.dispatch()` → your Python handler → `State.set()` → `StateBinding._changed()` → `DirtyNodes.mark()` + `Scheduler.request()` → (next loop tick) `Scheduler.flush()` → `UpdateMessage` broadcast → client `onResponse` → DOM attribute/text/property patch.

**Round trip for structural changes** (`component.add()`, `.remove()`, `.replace()`, `.clear()`, `.set_children()`, `.move_to()`): each mutation method emits a single mutation event synchronously to `TreeMutationObserver`, which is translated straight into a `Tree*Message` and broadcast — this path does **not** go through the scheduler/batching layer.

---

## Component Reference

All components are exported from the top-level `pylage` package (`import pylage as ps`). Every component maps 1:1 to an entry in `pylage.core.registry.registry`.

| Component | HTML tag | Void element | Notable props |
|---|---|---|---|
| `Column(*children, **props)` | `div` | no | `class_name`, `title`; default `style=Style(display="flex", flex_direction="column")`, overridable via `style=` |
| `Row(*children, **props)` | `div` | no | same as `Column`, default `flex_direction="row"` |
| `Grid(*children, **props)` | `div` | no | `class_name`, `title`; layout via `style=Style(display="grid", ...)` |
| `Text(text, **props)` | `div` | no | `text` (kind=`text`, HTML-escaped), supports `State` |
| `Heading(text, **props)` | `h1` | no | `text` (kind=`text`) |
| `Button(text, **props)` | `button` | no | `text`, `value`, `disabled` (boolean), `title`; use `on_click=...` |
| `Input(value="", **props)` | `input` | yes | `value`, `disabled`, `title`; passing `value=State(...)` auto-wires `on_input` |
| `Form(*children, **props)` | `form` | no | arbitrary attrs (e.g. `method`, `action`) pass through generically |
| `Table(*children, **props)` | `table` | no | `class_name`, `title` |
| `Dialog(*children, **props)` | `dialog` | no | `class_name`, `title` |
| `Navigation(*children, **props)` | `nav` | no | `class_name`, `title` |
| `Tabs(*children, **props)` | `div` | no | `class_name`, `title` |
| `Card(*children, **props)` | `div` | no | `class_name`, `title`; default block layout style |
| `Divider(*children, **props)` | `hr` | yes | `class_name`, `title` |
| `Badge` / `Avatar` / `Accordion` / `Carousel` | `span` / `span` / `div` / `div` | no | `class_name`, `title` |
| `Image(**props)` | `img` | yes | `src`, `alt`, `class_name`, `title` |
| `Video` / `Audio` | `video` / `audio` | no | `src`, `controls` (boolean), `class_name`, `title` |
| `Icon(**props)` | `span` | no | `name` (kind=`text`), `class_name`, `title` |
| `Canvas(*children, **props)` | `svg` | no | `width`, `height`, `class_name`, `title` |
| `Checkbox(**props)` | `input type="checkbox"` | no | `checked` (boolean), `class_name`, `title` |
| `Switch(**props)` | `input type="checkbox"` | no | same as `Checkbox` |
| `RadioGroup(*children, **props)` | `div` | no | `class_name`, `title` |
| `Select(*children, **props)` | `select` | no | `value`, `class_name`, `title` |
| `Slider(**props)` | `input type="range"` | yes | `value`, `min`, `max`, `step` |
| `DatePicker(**props)` | `input type="date"` | yes | `value`, `min`, `max` |
| `Alert` / `Toast` / `Spinner` / `Skeleton` | `div` | no | `text` (kind=`text`), `class_name`, `title` |
| `ProgressBar(**props)` | `progress` | no | `value`, `max`, `text` |
| `Breadcrumbs(*children, **props)` | `nav` | no | renders children inside `<ol><li>...</li></ol>` |
| `Pagination(*children, **props)` | `nav` | no | `class_name`, `title` |
| `Menu(*children, **props)` | `menu` | no | `class_name`, `title` |
| `Drawer(*children, **props)` | `aside` | no | `class_name`, `title` |
| `Tooltip(*children, **props)` | `span` | no | `class_name`, `title` |
| `Popover(*children, **props)` | `div` | no | `class_name`, `title` |

Every rendered element also carries `data-pylage-id="<component.id>"` and, if the component has any `on_*` handlers, `data-pylage-events="click,input,..."` — these two attributes are what the client runtime uses to route DOM events back to Python and apply patches.

Unknown/custom component types still render (falling back to a `<div>` tag with generic attribute/text handling) so you can register your own components without modifying the framework:

```python
from pylage.core.registry import registry, PropDefinition

registry.register(
    "RatingStars",
    "div",
    props={
        "value": PropDefinition("value", kind="attribute", html_name="data-value"),
        "class_name": PropDefinition("class_name", kind="attribute", html_name="class"),
    },
)
```

---

## Styling & Theming

```python
import pylage as ps

card = ps.Card(
    ps.Text("Styled content"),
    style=ps.Style(
        padding="16px",
        border_radius="8px",
        box_shadow="0 1px 3px rgba(0,0,0,.15)",
    ),
)
```

- `Style` is an immutable dataclass covering box model, flex, grid, border, and typography properties, plus a `custom={"--my-var": "..."}` escape hatch for arbitrary CSS custom properties.
- `Style.merge(override)` combines a component's default layout style (e.g. `Column`'s `display:flex;flex-direction:column`) with user-supplied overrides — user values always win.
- `ResponsiveStyle(base=..., sm=..., md=..., lg=..., xl=...)` emits `@media (min-width: ...)` blocks (`640px` / `768px` / `1024px` / `1280px`).
- `Theme(colors=..., spacing=..., radius=..., fonts=...)` renders `--color-*`, `--spacing-*`, `--radius-*`, `--font-*` CSS custom properties; pass `theme=` to `HTMLRenderer(theme=theme)` to inject a `<style>:root{...}</style>` block once per document.
- `Style` values may themselves be `State` objects — `to_css()` unwraps them automatically, so layout can be reactive too.

---

## Reactivity Model

- `State(value)` — holds a value, notifies subscribers on `set()` **only if the new value compares unequal to the old one**.
- Any component prop can be a `State` instance. `StateBinding` walks the tree once at construction and subscribes to every `State`-valued prop whose `PropDefinition.reactive` is `True` (the default for unknown props/components, preserving backward compatibility).
- `DependencyGraph` records `State -> {(Component, prop_name)}` edges — used for introspection/tooling and by `DirtyNodes.mark_from_state`.
- `DirtyNodes` is a `set` + insertion-ordered `list`, so multiple state changes to the same component in one batch collapse into a single scheduled update, and processing order is deterministic (first-marked-first-flushed).
- `Scheduler.request()` calls `schedule_flush()` **at most once** per batch (`WebSocketServer` schedules a flush ~1ms later on its own event loop via `call_later`), then `Scheduler.flush()` drains `DirtyNodes` and re-reads each dirty component's **current** prop values — so three synchronous `state.set()` calls in a row produce exactly one WebSocket message reflecting the final value, not three.

---

## Client ↔ Server Protocol

All messages are newline-free compact JSON (`json.dumps(..., separators=(",", ":"))`) sent over a single WebSocket per client.

| Direction | Type | Purpose |
|---|---|---|
| client → server | `event` | `{id, event, payload?}` — DOM event dispatched to `EventDispatcher` |
| server → client | `update` | `{id, props, remove_props?, prop_meta?}` — reactive prop change |
| server → client | `tree_add` | `{parent_id, components[], index?}` — component(s) inserted |
| server → client | `tree_remove` | `{parent_id, component_ids[]}` — component(s) removed |
| server → client | `tree_replace` | `{parent_id, old_component_id, new_component, index}` |
| server → client | `tree_clear` | `{parent_id, component_ids[]}` — all children removed |
| server → client | `tree_set_children` | `{parent_id, children[]}` — full children replacement |
| server → client | `tree_move` | `{component_id, old_parent_id, new_parent_id}` |
| server → client | `response` | `{ok, result?, error?}` — reply to an `event` message |

`prop_meta` (on `update`) carries each prop's registry `kind` (`attribute`/`boolean`/`text`) and `html_name`, so the client can apply the correct DOM operation (attribute set/remove, boolean toggle, or `textContent` assignment) without any component-specific JavaScript.

---

## Testing

The project ships an extensive `test/` suite (unit, integration, protocol, benchmark, and Playwright browser tests). Run everything with:

```bash
pip install pytest websockets playwright pytest-asyncio
playwright install chromium   # only needed for browser tests

pytest -q
```

Latest recorded run: **463 passed** (see `pylage_code_and_test_log.txt`, Section 3).

Notable test categories:
- `test_*_component.py` — one file per component, verifying tag, props, and children rendering.
- `test_registry_*.py` — registry contract enforcement (`PropDefinition` kind/reactive/html_name validation, custom renderer preservation, void-element rendering).
- `test_diff.py`, `test_tree_patch_protocol.py` — diff/patch algorithm correctness.
- `test_batching.py`, `test_scheduler.py`, `test_dirty_nodes.py` — reactive pipeline batching semantics.
- `test_browser_*.py` — full round-trip tests using Playwright against a real running `Runtime`.
- `test_phase6_*.py` — latency/throughput benchmarks for diff, patch, scheduler, and WebSocket broadcast.

---

## Project Layout

```
pylage/
├── app.py                 # pylage.run() — the top-level entry point
├── components/
│   ├── basic.py            # Text, Column, Row, Card, Button, Input, ... factories
│   └── __init__.py
├── core/
│   ├── component.py        # Component dataclass, component() factory, mutation API
│   ├── registry.py         # ComponentRegistry, PropDefinition, ComponentDefinition
│   ├── renderer.py         # HTMLRenderer — Component -> HTML
│   ├── state.py             # State (reactive value + subscribers)
│   ├── graph.py             # DependencyGraph (State -> (Component, prop))
│   ├── dirty.py             # DirtyNodes (batched-update tracking)
│   ├── scheduler.py         # Scheduler (coalesced flush)
│   ├── binding.py           # StateBinding (wires State subscriptions into the tree)
│   ├── events.py            # EventDispatcher (component_id/event -> handler)
│   ├── snapshot.py          # component_to_snapshot (Component -> JSON dict)
│   ├── diff.py               # diff() — snapshot A/B -> patch operations
│   ├── patch.py              # operation_to_message() — ops -> protocol messages
│   ├── protocol.py           # EventMessage, UpdateMessage, Tree*Message dataclasses
│   ├── ir.py                 # Compiler-layer IR (IRNode, normalize/analyze/optimize)
│   └── tree.py                # print_tree, collect_ids, TreeMutationObserver
├── renderers/
│   └── html.py              # HTMLDocumentRenderer — full standalone <html> document
├── runtime/
│   ├── runtime.py            # Runtime — coordinates HTTP + WebSocket servers
│   ├── server.py             # LocalServer — threaded static-file HTTP server
│   ├── websocket.py          # WebSocketServer — live transport + broadcast
│   └── client.py             # CLIENT_RUNTIME — embedded browser JS
└── styling/
    ├── style.py               # Style dataclass + to_css()
    ├── responsive.py          # ResponsiveStyle + media-query generation
    └── theme.py                # Theme — CSS custom-property tokens
```

---

## Known Limitations

See `Developer_Manual.md` → **Known Limitations & Edge Cases** for the full, test-verified list (registry mutation is process-global, `events` diff operations have no dedicated protocol message, `State.__eq__` gates change notification, single-file HTTP server, no SSR hydration diffing, etc.).

## License

No `LICENSE` file is present in the provided codebase — add one appropriate to your organization before distributing PyLage externally.
