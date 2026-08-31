# PySkin — Developer Manual

Version basis: source + test suite as captured in `pyskin_source_code.txt` and
`pyskin_code_and_test_log.txt` (463 tests passing). This manual documents the
framework as implemented — every code reference below points at a real
module, class, or function in the codebase, not a proposed API.

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Layer-by-Layer Architecture](#2-layer-by-layer-architecture)
3. [Core Module Reference](#3-core-module-reference)
4. [Component Model](#4-component-model)
5. [Registry Contract](#5-registry-contract)
6. [Rendering Pipeline](#6-rendering-pipeline)
7. [Reactivity Pipeline](#7-reactivity-pipeline)
8. [Snapshot / Diff / Patch Pipeline](#8-snapshot--diff--patch-pipeline)
9. [Runtime & Transport](#9-runtime--transport)
10. [Client Runtime (Browser JS)](#10-client-runtime-browser-js)
11. [Styling System](#11-styling-system)
12. [Compiler-Layer IR (Experimental)](#12-compiler-layer-ir-experimental)
13. [Full Component Catalog](#13-full-component-catalog)
14. [Extending PySkin](#14-extending-pyskin)
15. [Testing & Benchmarking](#15-testing--benchmarking)
16. [Known Limitations & Edge Cases](#16-known-limitations--edge-cases)
17. [Troubleshooting](#17-troubleshooting)

---

## 1. Design Philosophy

PySkin follows a **server-authoritative, differential-update** model, similar
in spirit to Phoenix LiveView or Laravel Livewire, but implemented in pure
Python with no external templating engine:

- The **source of truth lives in Python** (`State` objects). The browser is a
  thin renderer that applies patches; it never independently computes UI
  state.
- **Structural changes** (adding/removing/replacing/reordering components)
  and **value changes** (a prop's reactive value changing) are handled by
  *two separate pipelines* — tree mutation events vs. state-change batching —
  because they have different consistency requirements: structural changes
  must be applied in mutation order and are not coalesced, while value
  changes are safe to batch and only the latest value matters.
- A **central registry** (`ComponentRegistry`) is the single source of truth
  for how a component type maps to an HTML tag and which props are
  attributes/booleans/text/reactive. The renderer, the reactivity binder,
  and the compiler-layer IR analyzer all consult the *same* registry object,
  so there is exactly one place to add or change a component's contract.

---

## 2. Layer-by-Layer Architecture

```
 Python developer code
        │
        ▼
 pyskin.components.basic  (Text, Column, Button, ...)  ──► pyskin.core.component.component()
        │                                                        │
        │                                                        ▼
        │                                          pyskin.core.registry.registry
        │                                          (ComponentDefinition / PropDefinition)
        ▼
   Component tree (dataclass graph, parent-linked, mutation-observable)
        │
        ├──────────────► pyskin.core.renderer.HTMLRenderer.render()  ──► static HTML
        │                  (used by pyskin.renderers.html.render_document
        │                   for pyskin.run(serve=False))
        │
        └──────────────► pyskin.core.binding.StateBinding(root, callback, graph, dirty, scheduler)
                            walks tree, subscribes State props
                                   │
                State.set() ──────┤
                                   ▼
                          DirtyNodes.mark() + Scheduler.request()
                                   │
                          (coalesced) Scheduler.flush()
                                   │
                                   ▼
                      pyskin.runtime.websocket.WebSocketServer._scheduled_update()
                                   │
                                   ▼
                      protocol.UpdateMessage.to_json() ──► broadcast to all clients
                                   │
                                   ▼
                      pyskin.runtime.client.CLIENT_RUNTIME (browser)
                      window.PySkin.onResponse(message) → DOM patch
```

Parallel to the state pipeline, `pyskin.core.tree.TreeMutationObserver`
listens to every `Component.subscribe_mutation()` callback and, inside
`WebSocketServer._on_tree_mutation()`, converts `add` / `remove` / `replace`
/ `clear` / `set_children` / `move` events directly into
`TreeAddMessage` / `TreeRemoveMessage` / `TreeReplaceMessage` /
`TreeClearMessage` / `TreeSetChildrenMessage` / `TreeMoveMessage` and
broadcasts them — this bypasses `DirtyNodes`/`Scheduler` entirely, so
structural changes are never batched or delayed.

---

## 3. Core Module Reference

| Module | Responsibility |
|---|---|
| `pyskin/app.py` | `run()` — top-level entry point; static-file mode vs. `Runtime`-backed serve mode |
| `pyskin/core/component.py` | `Component` dataclass + mutation API (`add`, `remove`, `insert`, `replace`, `clear`, `set_children`, `move_to`, `on`, `subscribe_mutation`); `component()` factory |
| `pyskin/core/registry.py` | `ComponentRegistry`, `ComponentDefinition`, `PropDefinition`; the global `registry` singleton pre-populated with all built-in components |
| `pyskin/core/renderer.py` | `HTMLRenderer` — Component tree → HTML string, registry-driven |
| `pyskin/core/state.py` | `State` — minimal observable value container |
| `pyskin/core/graph.py` | `DependencyGraph` — `State → {(Component, prop_name)}` |
| `pyskin/core/dirty.py` | `DirtyNodes` — ordered dirty-component set |
| `pyskin/core/scheduler.py` | `Scheduler` — coalesced flush scheduling |
| `pyskin/core/binding.py` | `StateBinding` — wires `State` subscriptions into a Component tree |
| `pyskin/core/events.py` | `EventDispatcher` — routes `(component_id, event, payload)` to a handler |
| `pyskin/core/snapshot.py` | `component_to_snapshot()` — Component → JSON-safe dict |
| `pyskin/core/diff.py` | `diff(previous, current)` — snapshot diffing |
| `pyskin/core/patch.py` | `operation_to_message()` / `operations_to_messages()` / `operations_to_json()` |
| `pyskin/core/protocol.py` | Wire-format dataclasses: `EventMessage`, `UpdateMessage`, `TreeAddMessage`, `TreeRemoveMessage`, `TreeMoveMessage`, `TreeReplaceMessage`, `TreeSetChildrenMessage`, `TreeClearMessage` |
| `pyskin/core/ir.py` | Experimental compiler-layer intermediate representation (`IRNode`, `normalize_ir`, `analyze_ir`, `validate_ir`, `optimize_ir`, `constant_fold`, `analyze_ir_dependencies`, `plan_patches`) |
| `pyskin/core/tree.py` | `print_tree`, `collect_ids`, `count_components`, `TreeMutationObserver` |
| `pyskin/components/basic.py` | Public component factory functions |
| `pyskin/renderers/html.py` | `HTMLDocumentRenderer` — wraps rendered body in a full `<html>` doc + embeds client runtime |
| `pyskin/runtime/runtime.py` | `Runtime` — coordinates `LocalServer` + `WebSocketServer` lifecycle |
| `pyskin/runtime/server.py` | `LocalServer` — threaded `http.server.ThreadingHTTPServer` serving one static file |
| `pyskin/runtime/websocket.py` | `WebSocketServer` — live transport, JSON-safety conversion, broadcast |
| `pyskin/runtime/client.py` | `CLIENT_RUNTIME` — embedded vanilla-JS client, `get_client_runtime()` |
| `pyskin/styling/style.py` | `Style` — immutable structured CSS declaration |
| `pyskin/styling/responsive.py` | `ResponsiveStyle` — breakpoint-based `Style` composition |
| `pyskin/styling/theme.py` | `Theme` — CSS custom-property token system |

---

## 4. Component Model

### 4.1 `Component` dataclass (`pyskin/core/component.py`)

```python
@dataclass
class Component:
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Child] = field(default_factory=list)
    events: dict[str, EventHandler] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    # _parent and _mutation_subscribers are internal (init=False)
```

- `id` is a 10-character hex UUID fragment, used as the DOM anchor
  (`data-pyskin-id`) and as the key for `EventDispatcher`/patch targeting.
- **`__hash__`** is defined by `id` alone — components are hashable and safe
  to use as `dict`/`set` keys (used by `DirtyNodes`, `DependencyGraph`).
- **Parent tracking**: every mutation method (`add`, `insert`, `replace`,
  `set_children`, `move_to`) maintains a private `_parent` back-reference and
  actively **detaches a child from its previous parent** before attaching it
  elsewhere — a component can only ever have one parent at a time.
- **Cycle protection**: `add`, `insert`, `replace`, and `set_children` all
  walk the ancestor chain and raise `ValueError` (`"A component cannot
  contain itself."` / `"...an ancestor."`) before mutating the tree if the
  incoming child is the node itself or one of its own ancestors.
- **Mutation events**: every structural method emits exactly **one**
  synchronous event dict (even for multi-child calls) to
  `_mutation_subscribers`, e.g.:
  `{"type": "add", "parent": self, "children": [...], "index": ...?}`,
  `{"type": "move", "component": self, "old_parent": ..., "new_parent": ...}`,
  `{"type": "replace", "parent": self, "old_child": ..., "new_child": ..., "index": ...}`,
  `{"type": "clear", "parent": self, "children": [...]}`,
  `{"type": "set_children", "parent": self, "old_children": [...], "children": [...]}`.
- `subscribe_mutation(callback) -> unsubscribe` — idempotent removal.
- `on(event, handler)` registers directly into `self.events` (bypasses the
  `on_*` kwarg convention — useful for dynamic wiring after construction).

### 4.2 `component(type, *children, **props)` factory

- Filters out `None` children (`Column(a, None, b)` is valid and drops the
  `None`).
- Any kwarg starting with `on_` is popped out of `props` and installed into
  `events` under the suffix name (`on_click` → `events["click"]`); a
  non-callable value raises `TypeError`.
- Consults `registry.get(type)` for informational purposes only — **props
  are never filtered or rejected** based on the registry; unknown props on a
  known component, and any props on an unknown component type, are kept for
  backward compatibility.

### 4.3 Component-specific factory behavior (`pyskin/components/basic.py`)

Most factories are one-line wrappers around `component(...)`. Two are
notable:

- **`Input(value="", **props)`** — if `value` is a `State` instance and
  `on_input` was not explicitly supplied, PySkin auto-installs an
  `on_input` handler that calls `value.set(payload["value"])` whenever the
  browser sends an `input` event with a `value` payload. This is the
  mechanism behind two-way binding; it only fires for dict payloads
  containing a `"value"` key.
- **Dynamically-registered components** (`Card`, `Badge`, `Avatar`,
  `Accordion`, `Carousel`, `Image`, `Video`, `Audio`, `Icon`, `Canvas`) each
  call `registry.has(name)` and, if absent, `registry.register(...)` with an
  identical contract to the one pre-registered in `registry.py` at import
  time — this is a defensive **idempotent self-registration** in case the
  registry was reset or the component module was reloaded independently of
  `core/registry.py`. In the default import path both registrations exist
  and agree, so this is invisible in practice.

---

## 5. Registry Contract

### 5.1 `PropDefinition` (frozen dataclass)

```python
@dataclass(frozen=True)
class PropDefinition:
    name: str
    kind: str = "attribute"      # "attribute" | "boolean" | "text"
    reactive: bool = True
    html_name: str | None = None  # None => renderer falls back to `name`
```

`ComponentRegistry.register()` validates, at registration time:
- `name` matches the dict key it's stored under.
- `html_name` is either `None` or a non-empty `str`.
- `reactive` is strictly `bool` (rejects `1`/`0`/`"true"`/`None`/`[]`).
- `kind` is one of `{"attribute", "boolean", "text"}`.

### 5.2 `ComponentDefinition` (frozen dataclass)

```python
@dataclass(frozen=True)
class ComponentDefinition:
    type: str
    tag: str
    void: bool = False
    renderer: Callable[..., str] | None = None
    props: dict[str, PropDefinition] | None = None
```

### 5.3 `ComponentRegistry` API

| Method | Behavior |
|---|---|
| `register(type, tag, *, void=False, renderer=None, props=None)` | Validates and stores/overwrites a `ComponentDefinition`. Re-registering a type **replaces** its definition entirely. |
| `get(type)` | Returns `ComponentDefinition \| None` |
| `require(type)` | Returns the definition or raises `KeyError` |
| `set_renderer(type, renderer)` | Attaches a renderer to an **already-registered** type without touching tag/void/props |
| `has(type)` | Membership check |
| `unregister(type)` | Removes a type (no-op if absent) |
| `types()` | Tuple of all registered type names |

The registry is a **process-global singleton** (`pyskin.core.registry.registry`).
Tests that mutate it for isolated scenarios generally construct a fresh
`ComponentRegistry()` and pass it explicitly (`HTMLRenderer(registry_instance=...)`)
rather than mutating the shared instance — this is the recommended pattern
for custom/isolated component sets (see [§14](#14-extending-pyskin)).

---

## 6. Rendering Pipeline

### 6.1 `HTMLRenderer` (`pyskin/core/renderer.py`)

Constructed as `HTMLRenderer(registry_instance=None, theme=None)`. On
construction, `_register_builtin_renderers()` attaches Python callback
renderers for `Column`, `Row`, `Dialog`, `Table`, `Form`, `Card`, `Text`,
`Heading`, `Breadcrumbs`, `Button`, `Input` **only if** the registry
definition doesn't already have a `renderer` set — this makes builtin
renderer attachment **idempotent** and safe to call multiple times (verified
by `test_registry_renderer_idempotent.py`) and **non-destructive** toward
custom renderers registered before `HTMLRenderer()` is constructed
(`test_registry_custom_renderer_protection.py`).

Rendering algorithm (`_render_component`):
1. Look up `registry.get(component.type)`; unknown types fall back to `tag = "div"`.
2. If the definition has a custom `renderer` callback, delegate entirely to
   it: `definition.renderer(self, component)`.
3. Otherwise, generically render:
   - `data-pyskin-id="<id>"` always.
   - `data-pyskin-events="a,b,c"` if `component.events` is non-empty.
   - `style` attribute resolved via `_render_common_attributes` (supports a
     component-type `default_style` merged with a user `Style`/`ResponsiveStyle`
     value, which may itself be a `State`).
   - Every other prop resolved via registry `PropDefinition`: `boolean` kind
     emits the bare attribute name only if truthy; `text` kind is excluded
     from attributes and instead concatenated (HTML-escaped) as element
     content, **before** children; `attribute` kind emits `name="value"`
     (values `None` are skipped entirely; values `True` with no matching
     `PropDefinition` render as a bare attribute for backward compatibility).
   - Void elements (`definition.void`) render as `<tag ...>` with **no**
     closing tag and no children.
4. Special-cased components (`Column`/`Row` inject a default flex `Style`;
   `Card` also injects a default block-layout `Style`; `Breadcrumbs` wraps
   children in `<ol><li>...</li></ol>`; `Input`/`Slider` force
   `data-pyskin-events="input,change"` when no explicit handler is present,
   and `Slider` forces `type="range"`; `Checkbox`/`Switch` default
   `_html_type="checkbox"`, `DatePicker` defaults `_html_type="date"`).

`render(component)` at module scope is a convenience wrapper:
`HTMLRenderer().render(component)`.

### 6.2 `HTMLDocumentRenderer` (`pyskin/renderers/html.py`)

Wraps `render(component)` in a full `<!DOCTYPE html>` document, escapes
`title`, and splits `get_client_runtime(websocket_url)`'s bootstrap
`<script>` (which sets `window.PySkin.websocketUrl`) from the raw client
JS so both end up correctly wrapped in real `<script>` tags in the final
document body.

---

## 7. Reactivity Pipeline

### 7.1 `State` (`pyskin/core/state.py`)

```python
state = State(initial_value)
state.value            # read
state.set(new_value)   # write; no-ops (no notification) if new_value == old_value
unsubscribe = state.subscribe(lambda old, new: ...)
unsubscribe()
```

- Equality-gated: `if old_value == value: return` — **objects that compare
  equal but are semantically different will not trigger a notification.**
  This is a documented, test-verified behavior (`test_same_value_does_not_notify`).
- Subscriber iteration snapshots `tuple(self._subscribers)` before
  notifying, so a subscriber may safely unsubscribe itself or subscribe new
  listeners mid-notification without breaking iteration — new subscribers
  added during a notification do **not** receive that same notification
  (verified by `test_subscriber_iteration_is_stable`).

### 7.2 `DependencyGraph` (`pyskin/core/graph.py`)

Maps `State -> set[(Component, prop_name)]`. `add_dependency`,
`remove_dependency` (auto-deletes the key once its set is empty),
`get_dependents`, `clear`.

### 7.3 `DirtyNodes` (`pyskin/core/dirty.py`)

A `set[Component]` for O(1) membership plus a parallel ordered `list` for
deterministic flush order. `mark()` is idempotent (a component marked twice
appears once, in its *first* mark position). `mark_from_state(state, graph)`
marks every component dependent on a given state via the graph.

### 7.4 `StateBinding` (`pyskin/core/binding.py`)

```python
StateBinding(root, callback, graph=None, dirty=None, scheduler=None)
```

- On construction, `_bind_tree(root)` recursively walks every component and
  every prop; for each `State`-valued prop, it consults
  `_is_reactive(component, prop_name)` — which defers to the registry's
  `PropDefinition.reactive` flag, **defaulting to `True`** for unknown
  components or unknown props (backward-compatible opt-out design: you must
  explicitly register `reactive=False` to suppress binding).
- If reactive, it `state.subscribe(...)`s a closure bound to that specific
  `(component, prop_name)` pair, tracks the `unsubscribe` callable for
  `stop()`, and — if a `graph` was supplied — records the dependency edge.
- **Two operating modes** on change (`_changed`):
  - **Scheduler mode** (`scheduler` provided): marks the component dirty and
    calls `scheduler.request()`; the actual callback fires later, in
    `flush()`, with the component's *current* resolved values (not
    necessarily the value that triggered this particular change — see
    `_scheduled_update` in `WebSocketServer`).
  - **Immediate mode** (`scheduler=None`): invokes `callback(component,
    {prop_name: value})` synchronously with the *value from this specific
    change event*, then still marks `dirty` if supplied (for external
    inspection, without requiring a flush).
- `stop()` unsubscribes everything; idempotent.

### 7.5 `Scheduler` (`pyskin/core/scheduler.py`)

```python
Scheduler(dirty, callback, schedule_flush=None)
```

- `request()` is a no-op if `schedule_flush is None` (some tests construct a
  scheduler with no `schedule_flush` purely to batch dirty marks without
  ever auto-flushing — flush must then be called manually).
- Otherwise, thread-safe (`threading.Lock`) **debouncing**: the first
  `request()` in a batch calls `schedule_flush()` once and sets an internal
  flag; subsequent `request()` calls in the same batch are no-ops until
  `flush()` runs and clears the flag.
- `flush()` snapshots `dirty.nodes()` (in insertion order), calls
  `dirty.clear()` **before** invoking any callbacks (so a callback that
  triggers a new `state.set()` mid-flush correctly creates fresh work for
  the *next* flush cycle, not the current one — verified by
  `test_re_entrant_state_change`), then invokes `callback(node)` for each
  dirty node in order.

### 7.6 WebSocket-side scheduling (`WebSocketServer._schedule_scheduler_flush`)

Uses `loop.call_soon_threadsafe(lambda: loop.call_later(0.001, scheduler.flush))`
— a ~1ms debounce window on the server's own asyncio event loop, so that
several `state.set()` calls issued synchronously (even from another thread)
collapse into exactly one `UpdateMessage` per affected component
(`test_websocket_batches_multiple_state_changes_into_one_final_update`).

---

## 8. Snapshot / Diff / Patch Pipeline

This pipeline exists primarily to support **compiler-layer** and
**batch-reconciliation** use cases (see `pyskin/core/ir.py`'s
`plan_patches`) — the live `WebSocketServer` uses the reactive pipeline
(§7) for prop-level updates and `TreeMutationObserver` (§9.3) directly for
structural updates, rather than diffing full snapshots on every change.

### 8.1 `component_to_snapshot(component)` (`pyskin/core/snapshot.py`)

Recursively converts a `Component` into a JSON-safe dict:
`{id, type, tag, events (comma-joined string), props (State-unwrapped,
deep-copied), children: [...]}`. Guarantees `json.dumps(snapshot)` succeeds,
raising `TypeError` with a clear message if any prop value is not JSON
serializable (e.g. a raw callable). Non-`Component` children (plain strings,
numbers, `None`) are silently skipped.

### 8.2 `diff(previous, current)` (`pyskin/core/diff.py`)

Pure function over two snapshot dicts. Produces a deterministic, ordered
list of operations:

- If `id` or `type` differ at a node → single `{"type": "replace", ...}"`
  operation (subtree is *not* recursed into further).
- Else, prop-level diff → `{"type": "update", "id", "props": {changed},
  "remove_props": [dropped]}` (only emitted if there's an actual change).
- `events` string difference → `{"type": "events", "id", "events": "..."}`
  (see [§16](#16-known-limitations--edge-cases) — no dedicated protocol
  message consumes this).
- Children are diffed by `id`: `previous`-only ids → `remove` ops (emitted
  in previous-tree order); `current`-only ids → `insert` ops (index =
  current-tree position); ids present in both → recursive `_diff_node`.

### 8.3 `operation_to_message` / `operations_to_messages` / `operations_to_json`
(`pyskin/core/patch.py`)

Maps each diff operation dict to its protocol dataclass counterpart:
`update → UpdateMessage`, `insert → TreeAddMessage`, `remove →
TreeRemoveMessage`, `replace → TreeReplaceMessage`. **`events` operations
raise `ValueError`** ("...do not have a dedicated protocol message") — this
is an intentional, tested gap (see §16). Helper functions validate required
fields (`_require_id`, `_require_index`) and raise `ValueError` on missing
or malformed data.

---

## 9. Runtime & Transport

### 9.1 `pyskin.run()` (`pyskin/app.py`)

```python
def run(app, *, title="PySkin App", output="index.html", serve=False,
        host="127.0.0.1", port=0, open_browser=True) -> Path
```

- Requires `isinstance(app, Component)` or raises `TypeError`.
- `serve=False` (default): renders via `render_document()` and writes the
  file directly — no server involved, returns the `Path`.
- `serve=True`: constructs a `Runtime`, calls `runtime.render()` then
  `runtime.start()`, prints the URL, optionally opens the system browser,
  then **blocks** in a `time.sleep(0.25)` loop until `KeyboardInterrupt`,
  finally calling `runtime.stop()`. This makes `run(serve=True)` unsuitable
  for embedding inside an existing event loop or web framework — use
  `Runtime` directly for that (see Quickstart in `README.md`).

### 9.2 `Runtime` (`pyskin/runtime/runtime.py`)

Owns an optional `LocalServer` and `WebSocketServer`. `start()`:
1. Creates and starts a `WebSocketServer` (port `0` = OS-assigned).
2. Renders the document **with** the now-known `websocket_url` embedded.
3. Writes the file and starts a `LocalServer` bound to the file's parent
   directory and `self.output.name`.
4. On any exception, tears down the WebSocket server and re-raises, leaving
   `Runtime` in a clean not-running state.

`stop()` is idempotent (no-op if `_server is None`) and stops both
sub-servers. Supports `with Runtime(app) as runtime:` context-manager usage.

### 9.3 `WebSocketServer` (`pyskin/runtime/websocket.py`)

- Runs its own `asyncio` event loop on a dedicated daemon thread
  (`_thread_main`); `start()` blocks the caller until the server thread
  signals `self._ready` (an `threading.Event`), re-raising any startup
  error synchronously.
- Constructs, in order: `EventDispatcher(root)`, `DependencyGraph`,
  `DirtyNodes`, `Scheduler(..., schedule_flush=self._schedule_scheduler_flush)`,
  `StateBinding(root, self._on_state_change, graph=..., dirty=..., scheduler=...)`,
  and a `TreeMutationObserver(root, self._on_tree_mutation)`.
- `_json_safe(value)` recursively converts `State` (unwraps), `Style` /
  `ResponsiveStyle` (field-by-field dict), `dict`/`list`/`tuple` (recursed),
  primitives (passed through), and **anything else falls back to `str(value)`**
  — a broad safety net that also means non-primitive custom prop values
  serialize as their `repr`/`str`, which may not be what a consumer expects
  (documented in §16).
- `_on_state_change` builds `prop_meta` for each changed prop **only if**
  the registry has a matching `PropDefinition` (props with no registry
  entry are sent without metadata, and the client falls back to raw
  `setAttribute`).
- `_on_tree_mutation` handles all six mutation event types
  (`move`/`replace`/`set_children`/`clear`/`remove`/`add`), each building the
  appropriate `Tree*Message` and broadcasting; `move`/`clear`/`remove`
  reference existing DOM nodes by id only (no re-serialization needed since
  the DOM subtree already exists client-side), while `replace`/
  `set_children`/`add` recursively serialize the new subtree(s) via a local
  `serialize_component()` closure.
- `_handle(connection)` is the per-client coroutine: adds the connection to
  `self._connections`, then loops receiving `event` messages, dispatching
  via `EventDispatcher.dispatch()`, and replying with an
  `EventMessageResponse.success(result)` or `.error(str(exc))` JSON envelope
  — **any exception raised by a handler is caught and reported back over
  the wire as `{"ok": false, "error": "<message>"}`**, never crashes the
  server or the connection.
- `_broadcast(raw_message)` sends to all connections concurrently via
  `asyncio.gather(..., return_exceptions=True)` and prunes any connection
  whose `send()` raised (dead-connection cleanup) — a broadcast to zero
  connections is a no-op.
- `flush()` exposes `Scheduler.flush()` directly for tests/manual control.
- `stop()` stops the `StateBinding` subscriptions, closes the server on its
  own loop via `call_soon_threadsafe`, joins the thread (2s timeout), and
  clears all state — safe to call when never started (`_thread is None`
  short-circuits).

### 9.4 `LocalServer` (`pyskin/runtime/server.py`)

A minimal `ThreadingHTTPServer` serving **exactly one file** (`filename`,
default `index.html`) at `/` or `/<filename>` — any other path returns `404`.
Runs on a daemon thread; `stop()` calls `shutdown()` + `server_close()` and
joins with a 2s timeout.

---

## 10. Client Runtime (Browser JS)

`pyskin/runtime/client.py` embeds a self-contained IIFE
(`CLIENT_RUNTIME`) with no external dependencies. Key behaviors:

- `connectWebSocket(url)` — no-ops if `url` is falsy (static-file mode has
  no live updates); logs connect/disconnect/error to `console`.
- Delegated event listeners on `document` for `click`/`input`/`change`:
  `handleEvent` walks up via `event.target.closest("[data-pyskin-id]")`,
  checks the element's `data-pyskin-events` allow-list, builds a `payload`
  (`{value: target.value}` for `input`/`change` events on elements with a
  DOM `value` property), and calls `sendEvent(componentId, eventType, payload)`.
- `sendEvent` sends immediately over an open socket; if the socket isn't
  ready, it logs a warning and calls `window.PySkin.onEvent(message)` as a
  fallback hook (overridable by consumers embedding PySkin in a larger app).
- `window.PySkin.onResponse` is the single message dispatcher, handling
  `tree_move` (via `appendChild`, preserving the existing subtree — **not**
  a destroy/recreate), `tree_add` (recursive `createTreeNode`, with
  index-aware `insertBefore` vs. `appendChild`), `tree_remove`
  (`querySelector` + `.remove()`, relying on the browser to cascade-remove
  descendants), `tree_clear` (removes only the listed direct-child ids from
  a parent), `tree_set_children` (full child-list replacement, rebuilding
  from scratch), `tree_replace` (`Node.replaceWith`), and `update` (generic,
  registry-metadata-driven attribute/property patching — see below).
- **Generic `update` handling** (no hard-coded prop names, verified by
  `test_browser_generic_reactive_props.py`): for each `remove_props` entry
  and each `props` entry, resolves `kind`/`html_name` from `prop_meta`
  (defaulting to `kind="attribute"`, `html_name=propName` if metadata is
  absent), then:
  - `kind === "text"` → sets `element.textContent`.
  - `kind === "boolean"` → sets/removes the bare attribute.
  - otherwise → tries the JS DOM property first (`component[htmlName] =
    value`), falling back to `setAttribute` if the property assignment
    throws (some props, like custom attributes, only exist as HTML
    attributes, not JS properties).

---

## 11. Styling System

### 11.1 `Style` (`pyskin/styling/style.py`)

An immutable dataclass with ~50 explicit CSS-adjacent fields (box model,
typography, flex, grid, border, misc) plus `custom: dict[str, Any] | None`
for arbitrary `--custom-property: value` declarations.

- `to_css()` iterates `self.__dict__` (excluding `custom`), skips `None`
  values, resolves any `State`-valued field to its current `.value`, and
  emits `kebab-case:value` pairs joined by `;`. Custom properties are
  appended after standard fields and **must** start with `--` or
  `to_css()` raises `ValueError`.
- `merge(override)` returns a new `Style` where non-`None` fields of
  `override` take precedence over `self`, and `custom` dicts are shallow-merged
  (`override` wins on key collision). This is how component default layout
  styles (e.g. `Column`'s flex defaults) combine with user-supplied `style=`.

### 11.2 `ResponsiveStyle` (`pyskin/styling/responsive.py`)

`base`/`sm`/`md`/`lg`/`xl` each an optional `Style`. `to_css()` emits the
base style unwrapped, then each breakpoint wrapped in
`@media (min-width:<px>){...}` using the fixed breakpoint table
(`sm=640px, md=768px, lg=1024px, xl=1280px`). `to_base_css()` /
`to_responsive_css(selector)` provide partial extraction for advanced
integration (e.g. writing responsive rules into a separate stylesheet
instead of inline `style=`).

### 11.3 `Theme` (`pyskin/styling/theme.py`)

Immutable; wraps `colors`/`spacing`/`radius`/`fonts` dicts in
`MappingProxyType` at `__post_init__` (mutation attempts raise `TypeError`).
`color(name)` / `spacing_value(name)` / `radius_value(name)` / `font(name)`
raise `KeyError` with a descriptive message for unknown tokens (fail-fast,
no silent `None`). `to_css()` emits `--<prefix>-<kebab-name>:value` for every
non-`None` token, in the fixed order `color → spacing → radius → font`.
`HTMLRenderer(theme=theme).render(...)` prepends a single
`<style>:root{...}</style>` block containing this CSS once per document.

---

## 12. Compiler-Layer IR (Experimental)

`pyskin/core/ir.py` implements an intermediate representation **explicitly
decoupled from the runtime** — it does not evaluate `State`, does not touch
styles, and does not run diff/patch/event logic on its own initiative
(each function's docstring states this constraint, and it's enforced by
tests like `test_no_runtime_evaluation`).

- `IRNode(node_id, node_type="component", component_id=None, props=None,
  children=None, style_ref=None)` — validated on construction; `props` are
  deep-copied except `State` values, which are preserved by *identity*
  (`_copy_ir_value`), so subsequent `.set()` calls on that `State` continue
  to notify the original subscribers even after IR normalization/optimization.
- `snapshot_to_ir(snapshot)` — converts a `component_to_snapshot()` output
  into an `IRNode` tree, using `snapshot["type"]` (the PySkin component
  type) as `component_id`, **not** `snapshot["tag"]` (the HTML tag).
- `normalize_ir(node)` — deep, non-mutating canonical copy.
- `analyze_ir(node)` — returns `{total_nodes, node_ids, component_ids,
  duplicate_node_ids, is_valid}`; duplicate ids are *detected*, not raised.
- `validate_ir(node)` — same duplicate-id check but *raises* `ValueError`
  on the first duplicate found (fail-fast variant of `analyze_ir`).
- `constant_fold(value)` — folds 3-tuples shaped `(operator, left, right)`
  with `operator ∈ {add, sub, mul, div}` when both operands are already
  numeric constants (never touches `State`-typed operands, and leaves
  division-by-zero and unrecognized operators untouched rather than
  raising).
- `optimize_ir(node)` — recursively applies `constant_fold` to every prop.
- `analyze_ir_dependencies(node)` — walks the tree consulting the registry's
  `PropDefinition.reactive` flag (defaulting `True` for unregistered
  components/props) to build a `{node_id, prop_name}` dependency list —
  this is a **static** analysis; it reports a prop as a dependency purely
  based on registry reactivity metadata, independent of whether the prop's
  *current value* is actually a `State` instance (verify with
  `test_analyze_ir_dependencies_detects_state` vs.
  `test_analyze_ir_dependencies` for the distinction in behavior across the
  two related-but-different helper functions in the test suite).
- `plan_patches(previous, current)` — thin wrapper around `diff()`,
  provided as the IR-layer's entry point into the diff engine.

This layer has no consumer in the shipped runtime (`WebSocketServer` does
not call into `ir.py`); it exists as a foundation for a future
ahead-of-time compilation or static-analysis tool.

---

## 13. Full Component Catalog

Below is the exhaustive registry contract for every built-in component
(`pyskin/core/registry.py`). `html_name` defaults to the prop name itself
when omitted.

| Type | Tag | Void | Props (`name: kind[, html_name]`) |
|---|---|---|---|
| `Text` | `div` | — | `text: text` |
| `Heading` | `h1` | — | `text: text` |
| `Card` | `div` | — | `class_name: attribute→class`, `title: attribute` |
| `Tabs` | `div` | — | `class_name: attribute→class`, `title: attribute` |
| `DatePicker` | `input` | ✔ | `class_name→class`, `title`, `value`, `min`, `max` (all attribute) |
| `Alert` | `div` | — | `class_name→class`, `title`, `text: text` |
| `Toast` | `div` | — | `class_name→class`, `title`, `text: text` |
| `Spinner` | `div` | — | `class_name→class`, `title`, `text: text` |
| `ProgressBar` | `progress` | — | `class_name→class`, `title`, `value`, `max`, `text: text` |
| `Skeleton` | `div` | — | `class_name→class`, `title`, `text: text` |
| `Breadcrumbs` | `nav` | — | `class_name→class`, `title` |
| `Pagination` | `nav` | — | `class_name→class`, `title` |
| `Menu` | `menu` | — | `class_name→class`, `title` |
| `Drawer` | `aside` | — | `class_name→class`, `title` |
| `Tooltip` | `span` | — | `class_name→class`, `title` |
| `Popover` | `div` | — | `class_name→class`, `title` |
| `RadioGroup` | `div` | — | `class_name→class`, `title` |
| `Switch` | `input` | — | `class_name→class`, `title`, `checked: boolean` |
| `Select` | `select` | — | `class_name→class`, `title`, `value` |
| `Slider` | `input` | ✔ | `class_name→class`, `title`, `value`, `min`, `max`, `step` |
| `Form` | `form` | — | *(no declared props — arbitrary attrs pass through generically)* |
| `Table` | `table` | — | `class_name→class`, `title` |
| `Dialog` | `dialog` | — | `class_name→class`, `title` |
| `Navigation` | `nav` | — | `class_name→class`, `title` |
| `Checkbox` | `input` | — | `class_name→class`, `title`, `checked: boolean` |
| `Divider` | `hr` | ✔ | `class_name→class`, `title` |
| `Row` | `div` | — | `class_name→class`, `title` |
| `Grid` | `div` | — | `class_name→class`, `title` |
| `Column` | `div` | — | `class_name→class`, `title` |
| `Badge` | `span` | — | `class_name→class`, `title` |
| `Avatar` | `span` | — | `class_name→class`, `title` |
| `Accordion` | `div` | — | `class_name→class`, `title` |
| `Carousel` | `div` | — | `class_name→class`, `title` |
| `Image` | `img` | ✔ | `src`, `alt`, `class_name→class`, `title` |
| `Video` | `video` | — | `src`, `controls: boolean`, `class_name→class`, `title` |
| `Audio` | `audio` | — | `src`, `controls: boolean`, `class_name→class`, `title` |
| `Icon` | `span` | — | `name: text`, `class_name→class`, `title` |
| `Canvas` | `svg` | — | `width`, `height`, `class_name→class`, `title` |
| `Heading` *(dup. above)* | `h1` | — | `text: text` |
| `Button` | `button` | — | `text: text`, `class_name→class`, `value`, `disabled: boolean`, `title` |
| `Input` | `input` | ✔ | `value`, `disabled: boolean`, `title` |

> Registration order in `registry.py` re-registers `Text`, `Card`, and
> `Heading` more than once across the file (each with an identical
> contract) — this is harmless since `register()` overwrites by `type` key,
> but is worth knowing if you're auditing registration call sites.

---

## 14. Extending PySkin

### 14.1 Register a fully custom component

```python
from pyskin.core.registry import registry, PropDefinition
from pyskin.core.component import component

registry.register(
    "RatingStars",
    "div",
    props={
        "value": PropDefinition("value", kind="attribute", html_name="data-value"),
        "class_name": PropDefinition("class_name", kind="attribute", html_name="class"),
        "label": PropDefinition("label", kind="text"),
    },
)

def RatingStars(**props):
    return component("RatingStars", **props)

widget = RatingStars(value=4, class_name="stars", label="4 / 5")
```

### 14.2 Attach a fully custom renderer

```python
def render_rating(renderer, component):
    value = renderer._value(component.props.get("value", 0))
    stars = "★" * int(value) + "☆" * (5 - int(value))
    return f'<div data-pyskin-id="{component.id}">{stars}</div>'

registry.set_renderer("RatingStars", render_rating)
```

`set_renderer` requires the type to already be registered (`require()`
raises `KeyError` otherwise) and preserves the existing `tag`/`void`/`props`
contract while swapping only the render callback.

### 14.3 Suppress reactivity for a specific prop

```python
registry.register(
    "StaticLabel",
    "span",
    props={"text": PropDefinition("text", kind="text", reactive=False)},
)
```

A `State` passed as `text` on a `StaticLabel` will render its **initial**
value only — `StateBinding` will not subscribe to it, so later `.set()`
calls will not push updates to this component (verified by
`test_analyze_ir_dependencies_excludes_non_reactive_props` and
`test_registry_state_binding_contract.py`).

### 14.4 Isolated registries for testing/tooling

For any tool that needs to render or analyze components without touching
the shared global registry, construct a fresh instance and pass it through
explicitly rather than mutating `pyskin.core.registry.registry`:

```python
from pyskin.core.registry import ComponentRegistry
from pyskin.core.renderer import HTMLRenderer

local_registry = ComponentRegistry()
local_registry.register("Widget", "div")
renderer = HTMLRenderer(registry_instance=local_registry)
```

---

## 15. Testing & Benchmarking

```bash
pip install pytest websockets playwright pytest-asyncio
playwright install chromium
pytest -q
```

Recorded result: **463 passed in 16.45s** (see `pyskin_code_and_test_log.txt`,
Section 3).

Test suite structure highlights:

- **Component tests** (`test_*_component.py`) — one file per public
  component; each checks type identity, HTML tag, prop rendering, and
  children rendering.
- **Core mechanics** — `test_component.py`, `test_component_mutation.py`,
  `test_component_mutation_events.py` (cycle rejection, parent tracking,
  single-event-per-mutation-call guarantees).
- **Registry contract tests** — `test_registry_*.py` (11+ files): prop
  kind/reactive/html_name validation, void rendering, custom renderer
  idempotency/preservation, generic (non-hard-coded) dispatch enforcement
  (`test_registry_no_builtin_dispatch.py`, `test_registry_renderer_ownership.py`
  literally grep the renderer source to assert no component-name string
  literals remain in the dispatch path).
- **Reactivity tests** — `test_state.py`, `test_state_semantics.py`,
  `test_dirty_nodes.py`, `test_scheduler.py`, `test_batching.py`,
  `test_dependency_graph.py`, `test_state_binding_graph.py`,
  `test_state_binding_semantics.py`.
- **Diff/patch/protocol tests** — `test_diff.py`, `test_tree_patch_protocol.py`,
  `test_tree_*_protocol.py` (one per message type), `test_snapshot.py`.
- **Runtime/WebSocket integration** — `test_websocket.py`,
  `test_websocket_reactive_pipeline.py`, `test_tree_*_runtime.py`,
  `test_input_binding.py`, `test_reactive_counter.py`, `test_reactive_props.py`,
  `test_registry_prop_mapping.py`.
- **Browser integration (Playwright)** — `test_browser_event.py`,
  `test_browser_input_binding.py`, `test_browser_reactive_counter.py` — spin
  up a real `Runtime`, load it in headless Chromium, interact with the DOM,
  and assert Python-side state changed in response.
- **Performance benchmarks** — `test_phase6_*.py`, `test_batching_benchmark.py`,
  `test_phase6_dependency_scaling.py` (dependency graph lookup/registration
  at 10/100/1,000/10,000 scale), `test_phase6_websocket_benchmarks.py`
  (per-update latency, tree-patch latency, multi-client broadcast scaling
  at 10/50/100 clients). These print timing to stdout and assert
  correctness, not specific latency thresholds — treat them as
  regression/characterization tests, not hard SLAs.
- **Manual/interactive scripts** — several `test_browser_state.py`,
  `test_live_state_debug.py`-style files are designed to be run manually
  (they `print()` instructions and loop on `time.sleep`) rather than
  asserted by `pytest`; they exist for live debugging against a real
  browser tab.

---

## 16. Known Limitations & Edge Cases

These are real, code-verified characteristics of the current implementation
— documented here so they are not mistaken for bugs when integrating
PySkin into a larger system.

1. **Global, mutable registry.** `pyskin.core.registry.registry` is a
   process-wide singleton. `register()` on an existing type name silently
   **replaces** the definition (last write wins). Tests that need isolation
   construct a fresh `ComponentRegistry()` — application code doing dynamic
   plugin-style registration should follow the same pattern to avoid
   cross-module collisions.

2. **`events` diff operations have no protocol message.**
   `pyskin/core/patch.py::operation_to_message` explicitly raises
   `ValueError` for `operation_type == "events"`. If you drive the
   diff/patch pipeline directly (rather than the live `WebSocketServer`,
   which handles event wiring separately via `EventDispatcher`), a
   component whose *only* change is its registered event set will produce
   a diff operation that cannot be converted to a wire message.

3. **`State` equality gating.** `State.set(value)` only notifies if
   `value != old_value`. For mutable objects (lists, dicts) mutated in
   place and re-`.set()` with the *same* object reference, no notification
   fires — always construct a new value (or a shallow copy) when updating
   collection-typed state.

4. **Single-file `LocalServer`.** `pyskin/runtime/server.py`'s
   `_RequestHandler` only serves the exact `filename` it was configured
   with, at `/` or `/<filename>` — any other path (e.g. relative asset
   references, favicon requests) returns `404`. There is no static-asset
   directory serving; images/fonts/etc. referenced by URL must be hosted
   externally or inlined.

5. **`_json_safe` fallback to `str(value)`.** In
   `WebSocketServer._json_safe`, any prop value that isn't `State`, `Style`,
   `ResponsiveStyle`, `dict`, `list`/`tuple`, or a JSON primitive is
   serialized as `str(value)` before being sent to the browser — custom
   objects will arrive client-side as their Python `repr`/`str`, not a
   structured representation, unless you pre-serialize them yourself.

6. **No SSR/hydration diffing.** The static-file render path
   (`serve=False`) and the live-serve path (`serve=True`) both produce a
   full document from scratch; there is no mechanism to hydrate a
   server-rendered static page into a subsequently-connected live
   WebSocket session — `serve=True` always renders its own initial HTML
   with the WebSocket URL pre-embedded.

7. **`run(serve=True)` is blocking.** It runs an infinite `time.sleep(0.25)`
   loop until `KeyboardInterrupt`; it is designed for standalone script
   usage, not for embedding inside another async application or web
   framework request handler. Use `Runtime` (or `WebSocketServer` /
   `LocalServer` directly) for non-blocking integration.

8. **Tree mutations bypass batching entirely.** Unlike prop-value changes,
   structural mutations (`add`/`remove`/`replace`/`clear`/`set_children`/
   `move_to`) are broadcast **immediately and individually** — calling
   `column.add(a)` followed by `column.add(b)` in the same synchronous
   block produces two separate `tree_add` WebSocket messages, not one
   batched message. If you need to add many children atomically, prefer a
   single `add(a, b, c, ...)` / `insert(index, a, b, c)` / `set_children(...)`
   call, all of which are single-mutation-event operations.

9. **`Registry.register()` prop validation happens once, at registration
   time**, not at component-construction or render time. Constructing a
   `Component` with a prop name that has **no** matching `PropDefinition`
   on an otherwise-registered type is always accepted (renders as a
   generic `attribute`) — there is no "unknown prop" error path for known
   component types, by design, for forward/backward compatibility.

10. **`Style.to_css()` custom-property validation.** Any `custom` key not
    starting with `--` raises `ValueError` **at `to_css()` call time**, not
    at `Style(...)` construction time — errors here surface only during
    rendering, which can be surprising if `Style` objects are constructed
    far from where they are eventually rendered.

11. **Playwright/`websockets` are runtime-optional but test-required.**
    Core PySkin usage (`Component`, `render()`, static `run()`) has zero
    third-party dependencies. Live serving requires `websockets`;
    Playwright-based browser tests require `playwright` and a Chromium
    install (`playwright install chromium`) — omitting these only breaks
    the relevant test files/serve mode, not static rendering.

---

## 17. Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: websockets` | `serve=True` / `Runtime` used without the dependency installed | `pip install websockets` |
| Browser shows initial state but never updates | No WebSocket connection reached the client (e.g. `run(serve=False)` was used, or a firewall blocks the local port) | Use `serve=True` / `Runtime.start()`; check `runtime._websocket.url` |
| Two-way `Input` binding doesn't update Python state | `on_input` was explicitly overridden, disabling the auto-wire | Don't pass `on_input` explicitly if you want `value=state` auto-binding, or replicate `value.set(payload["value"])` in your custom handler |
| A prop change never reaches the browser | The prop's registry `PropDefinition.reactive` is `False`, or the prop was set on the raw dict (`component.props["x"] = state`) *after* `StateBinding` already walked the tree | Register `reactive=True` (or omit — it's the default), and ensure `State` props exist before constructing the `StateBinding`/starting the `Runtime` |
| `ValueError: A component cannot contain an ancestor.` | Attempting to `add`/`insert`/`replace`/`set_children` a component into one of its own descendants | Restructure the tree — cycles are actively rejected, not silently allowed |
| Custom component renders as a bare `<div>` with no styling | Component type was never `registry.register()`-ed | Register the type (see [§14.1](#141-register-a-fully-custom-component)) or accept the generic-`div` fallback |
| `KeyError: Unknown component type` from `registry.require(...)` | Called `require()` (not `get()`) on an unregistered type | Register first, or use `registry.get()` / `registry.has()` for a non-raising check |
