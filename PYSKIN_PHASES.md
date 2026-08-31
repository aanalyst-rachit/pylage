# 🐍 PyLage / PU — PHASE ROADMAP

> Purpose: This file is the compact phase tracker and architectural
> checkpoint for the PyLage project.
>
> Long-term vision:
> Build a Python-first, low-latency, fine-grained reactive UI framework
> where developers use Python only and browser/native rendering complexity
> remains hidden inside PyLage.

---

# 🔒 PROJECT IDENTITY

Project: PyLage
Long-term vision: PU — Python Universal UI Framework
Repository: https://github.com/aanalyst-rachit/pylage
Branch: main

Current architectural phase:

    Phase 10 — Multi-Backend Architecture

Latest validated regression:

    463 passed

Latest focused IR validation:

    73 passed

Master blueprint:

    project pylage blueprint.txt

Phase tracker:

    PYLAGE_PHASES.md

---

# 🧭 NORTH STAR

Python application
        ↓
PyLage API
        ↓
Component Tree
        ↓
Registry
        ↓
Reactive State Graph
        ↓
Dependency Graph
        ↓
Dirty Nodes
        ↓
Scheduler
        ↓
Diff
        ↓
Patch
        ↓
WebSocket
        ↓
Tiny Client Runtime
        ↓
Browser / Future Native Backend

Core principle:

> PyLage is not just a Python-to-HTML generator.
> PyLage is a Python-first reactive UI programming model.

---

# 📊 PHASE STATUS

Legend:

- ✅ COMPLETE
- 🟢 ACTIVE
- 🟡 PARTIAL
- 🔴 NOT STARTED
- ⏸️ DEFERRED

---

# PHASE 0 — FOUNDATION

Status: ✅ COMPLETE

Goals:

- Component system
- Component tree
- Props
- Children
- Events
- Stable component IDs
- State foundation
- Basic HTML rendering

Completed:

- Components can be constructed.
- Components form a tree.
- Props and children are represented.
- Events can be attached.
- State can hold reactive values.
- Basic HTML can be rendered.

Definition of done:

- Foundation APIs are functional.
- Component tree semantics are stable.
- State foundation is available to the reactive runtime.

---

# PHASE 1 — REGISTRY

Status: 🟢 ~95% COMPLETE

Goals:

- ComponentDefinition
- PropDefinition
- Prop kinds
- HTML metadata
- Reactive metadata
- Renderer ownership
- Custom renderer support
- Generic prop mapping

Completed:

- Component registry
- Prop registry
- `attribute` kind
- `boolean` kind
- `text` kind
- `reactive` boolean contract
- `html_name`
- Renderer callback ownership
- Custom renderer protection
- Generic text prop handling
- Registry-driven rendering
- Generic browser prop metadata

Remaining:

- Final runtime edge-case audit for reactive metadata
- Further renderer genericization where architecturally justified

Important rule:

> Do not expand registry features without an architectural need.

---

# PHASE 2 — FINE-GRAINED REACTIVE RUNTIME

Status: ✅ COMPLETE

Objective:

Turn:

    State → Update → Browser

into:

    State
      ↓
    Dependency Graph
      ↓
    Affected Components
      ↓
    Dirty Nodes
      ↓
    Scheduler
      ↓
    Minimal Update
      ↓
    Browser

Phase 2 established the fine-grained reactive runtime foundation.

---

## PHASE 2A — REACTIVE SEMANTICS

Status: 🟢 VALIDATED

Completed:

- `reactive=True` registry contract
- `reactive=False` registry contract
- State-to-component reactive binding
- Generic reactive prop updates
- Registry-driven reactive behavior
- WebSocket update propagation
- State value resolution before serialization
- Reactive browser DOM update path

Defined semantics:

### `reactive=True`

A prop participates in the reactive update pipeline when its
value is backed by reactive state.

### `reactive=False`

A prop does not participate in automatic reactive dependency updates,
even when a State-like value is supplied.

### Dependency creation

Reactive State values are connected to their consuming component props
during StateBinding.

### Update emission

A state change produces an update only when the corresponding dependency
is reactive and the value actually changes.

### Update suppression

No update is emitted for unchanged state values or non-reactive props.

---

## PHASE 2B — DEPENDENCY GRAPH

Status: ✅ COMPLETE

Completed:

- Dependency registration
- State → Component → Prop dependency mapping
- Multiple dependents
- Dependency lookup
- Integration with StateBinding
- Lifecycle-safe binding foundation
- Duplicate subscription protection

Target model:

    State A
       ├──→ Component X
       └──→ Component Y

    State B
       └──→ Component Z

When State A changes:

    X + Y → affected
    Z     → untouched

Definition of done:

- State changes identify only affected components.
- Unrelated components are not marked dirty.

---

## PHASE 2C — DIRTY NODE TRACKING

Status: ✅ COMPLETE

Completed:

- Dirty node marking
- Duplicate dirty-node suppression
- Dirty node collection
- Scheduler integration
- Deterministic processing foundation

Target:

    State change
        ↓
    dependency lookup
        ↓
    dirty set

Definition of done:

- Only affected nodes enter the update pipeline.

---

## PHASE 2D — UPDATE SCHEDULER

Status: ✅ COMPLETE

Completed:

- Scheduler abstraction
- Dirty node processing
- Component update scheduling
- Integration with StateBinding
- State value resolution during scheduled update
- Reactive update dispatch
- Deterministic scheduling behavior

Architectural note:

> The scheduler provides the processing boundary required by batching.

---

## PHASE 2E — BATCHING

Status: ✅ COMPLETE

Completed:

- Coalesced scheduler flush
- Duplicate scheduler request suppression
- Multiple State changes coalesced into one processing cycle
- Multiple States affecting one component processed once
- Final State value observed during scheduled processing
- Re-entrant State changes deferred to the next scheduler cycle
- Deterministic dirty-node processing
- WebSocket runtime integration
- Batching benchmark

Validated benchmark:

    1000 state changes
        ↓
    1 processing cycle

Processing reduction:

    1000x

Definition of done:

- Multiple related changes can be safely coalesced.
- Final state is observed.
- Duplicate processing is suppressed.
- Re-entrant updates remain deterministic.
- WebSocket/browser reactivity remains intact.

---

# PHASE 3 — UI REPRESENTATION / SNAPSHOT

Status: ✅ COMPLETE

Objective:

Create a stable representation of rendered UI that can be compared.

Target:

    Component Tree
         ↓
    UI Representation
         ↓
    Previous + Current

Completed:

- Stable UI snapshot representation
- Stable node identity
- Stable component identity
- Props representation
- Text representation
- Children representation
- Deterministic snapshot structure
- Previous/current snapshot comparison foundation
- Focused snapshot test coverage

Implementation:

- `pylage/core/snapshot.py`
- `test/test_snapshot.py`

Definition of done:

- Current UI state can be represented deterministically.
- Previous and current representations can be compared.

---

# PHASE 4 — DIFF ENGINE

Status: ✅ COMPLETE

Objective:

Calculate the smallest meaningful UI change.

Example:

    Before:
        <span>10</span>

    After:
        <span>11</span>

Target:

    text update only

Not:

    full application rerender

Completed:

- Prop diff
- Text diff
- Child diff
- Node identity matching
- Insert
- Remove
- Replace
- Update
- Event change handling
- Nested diff handling
- Deterministic diff ordering
- No-op detection

Definition of done:

- Correct minimal diffs are produced.
- Unchanged nodes generate no operations.
- Nested changes are represented correctly.

---

# PHASE 5 — PATCH ENGINE

Status: 🟢 COMPLETE

Objective:

Convert diff results into browser patch operations.

Pipeline:

    UI Diff
       ↓
    Patch Operations
       ↓
    Update Protocol
       ↓
    WebSocket
       ↓
    Browser

Supported operation categories:

- set attribute
- remove attribute
- set boolean
- set DOM property
- set text
- insert node
- remove node
- replace node
- tree add
- tree remove
- tree move
- tree replace
- tree clear
- tree set-children
- events update

Completed:

- Patch operation generation
- Patch application foundation
- Tree mutation protocol
- Recursive subtree serialization
- Recursive client DOM replacement
- Client tree insertion
- Client tree removal
- Client tree movement
- Client tree clearing
- Client set-children replacement
- WebSocket mutation broadcasting
- Reactive WebSocket patch path

Architectural rule:

> Patch semantics must remain smaller than the UI representation they
> transform.

Definition of done:

- Patch operations can transform old UI state into new UI state.
- Browser/client state remains synchronized with server state.

---

# PHASE 6 — PERFORMANCE / BENCHMARKS

Status: 🟢 COMPLETE / BASELINE ESTABLISHED

Objective:

Measure real runtime performance instead of relying on assumptions.

Benchmark areas:

- State update latency
- Event latency
- WebSocket latency
- Update throughput
- Patch size
- CPU usage
- Memory usage
- Component count scaling
- Dependency graph scaling
- Scheduler/batching behavior

Validated:

- Dependency graph lookup scaling
- Dependency registration scaling
- WebSocket state update latency
- WebSocket tree patch latency
- WebSocket client scaling
- Batching processing reduction

Validated dependency graph scale:

    10,000 dependencies

Validated WebSocket client scale:

    10 clients
    50 clients
    100 clients

Batching benchmark:

    1000 state changes
        ↓
    1 processing cycle

Important:

> Performance claims must come from benchmarks, not assumptions.

Future performance work:

- More realistic application workloads
- Memory profiling
- Larger component trees
- Browser-side measurements
- End-to-end latency
- Optimization regression benchmarks

---

# PHASE 7 — UI COMPONENT SYSTEM

Status: ✅ COMPLETE

Objective:

Provide the target foundational UI component library.

Completed:

- Public component exports
- Registry definitions
- HTML rendering contracts
- Component-specific regression tests
- Target component APIs

Final target:

    38 / 38 components implemented

Core primitives:

- Text
- Heading
- Button
- Input
- Form
- Table
- Card
- Dialog
- Navigation
- Tabs

Data input and selection:

- Checkbox
- Radio Group
- Switch / Toggle
- Select / Dropdown
- Slider
- DatePicker

Feedback and status:

- Alert
- Toast / Notification
- Spinner / Loader
- Progress Bar
- Skeleton

Navigation and overlay:

- Breadcrumbs
- Pagination
- Menu / ContextMenu
- Drawer / Sidebar
- Tooltip
- Popover

Data display and layout:

- Badge / Tag
- Avatar
- Accordion
- Carousel
- Divider
- Grid / Flex Container

Media and canvas:

- Image
- Video
- Audio
- Icon
- Canvas / SVG Container

Architectural rule:

> Component expansion must follow actual framework requirements rather
> than becoming a substitute for core runtime work.

---

# PHASE 8 — STYLING SYSTEM

Status: 🟡 PARTIAL / FOUNDATION EXISTS

Objective:

Provide a Python-first styling layer independent from the core reactive
engine.

Goals:

- Python style API
- Themes
- Responsive design
- Layout
- CSS generation
- Layout constraints

Potential API:

    ps.Text(
        "Hello",
        style=ps.Style(...)
    )

Architectural rule:

> Styling must remain independent from the core reactive engine.

Future work:

- Complete public styling API
- Theme system
- Responsive primitives
- CSS generation guarantees
- Layout constraints
- Style normalization
- Browser style patch integration

---

# PHASE 9 — COMPILER / UI IR

Status: ✅ COMPLETE

Objective:

Introduce a small compiler-layer intermediate representation capable
of normalizing UI structures, performing safe static analysis, applying
safe constant folding, analyzing dependencies, planning patches, and
optimizing IR without taking ownership of runtime behavior.

Core principle:

> The compiler layer must remain separate from the runtime layer.

Target:

    Snapshot / Component Representation
             ↓
           UI IR
             ↓
       Normalization
             ↓
       Static Analysis
             ↓
      Safe Optimization
             ↓
       Patch Planning
             ↓
          Runtime

---

## PHASE 9A — IR FOUNDATION

Status: ✅ COMPLETE

Completed:

- `IRNode`
- Node validation
- Component identity
- Node identity
- Props representation
- Children representation
- Style reference representation
- Snapshot-to-IR conversion

Implementation:

    pylage/core/ir.py

---

## PHASE 9B — IR NORMALIZATION

Status: ✅ COMPLETE

Completed:

- `normalize_ir`
- Canonical compiler-layer copies
- Stable node identity
- Stable component identity
- Stable child ordering
- Props preservation
- Opaque style reference preservation
- Source immutability

Architectural rule:

> Normalization must not evaluate runtime State, resolve styles, execute
> events, or invoke runtime dependency/diff/patch systems.

---

## PHASE 9C — STATIC IR ANALYSIS

Status: ✅ COMPLETE

Completed:

- `analyze_ir`
- Node counting
- Ordered node identity collection
- Component identity analysis
- Duplicate node ID detection
- Structural validation

Definition of done:

- IR can be inspected without mutating runtime state.

---

## PHASE 9D — CONSTANT FOLDING

Status: ✅ COMPLETE

Completed:

- `constant_fold`
- Addition folding
- Subtraction folding
- Multiplication folding
- Division folding
- Recursive constant folding
- Unsafe division protection
- Unknown operation preservation
- Literal preservation

Example:

    ("add", 10, 20)
            ↓
           30

Nested example:

    ("mul", ("add", 2, 3), 4)
            ↓
           20

Safety rule:

> Only compiler-safe constant expressions may be evaluated.

Runtime State must never be evaluated as a compile-time constant.

---

## PHASE 9E — IR DEPENDENCY ANALYSIS

Status: ✅ COMPLETE

Completed:

- `analyze_ir_dependencies`
- Node traversal
- Reactive prop detection
- Registry-aware reactive metadata
- State dependency representation
- Nested dependency analysis
- Non-reactive prop exclusion

Target:

    State
      ↓
    IR prop
      ↓
    Component
      ↓
    Dependency information

Architectural rule:

> IR dependency analysis describes dependencies; it does not replace the
> runtime dependency graph.

---

## PHASE 9F — PATCH PLANNING

Status: ✅ COMPLETE

Completed:

- `plan_patches`
- Integration with existing diff semantics
- Minimal update planning
- Insert planning
- Remove planning
- Replace planning
- Event update planning
- Nested patch planning
- Deterministic operation ordering

Architectural rule:

> Patch planning reuses stable diff semantics instead of creating a
> second incompatible diff engine.

---

## PHASE 9G — IR OPTIMIZATION

Status: ✅ COMPLETE

Completed:

- `optimize_ir`
- Recursive child optimization
- Constant prop folding
- Nested constant expression folding
- Unsafe expression preservation
- Source immutability
- Node identity preservation
- Child ordering preservation
- Style reference preservation
- State identity preservation
- Runtime State safety
- Dynamic expression preservation

State safety validation:

    State("Hello")
        ↓
    optimize_ir()
        ↓
    same State object

Dynamic expression validation:

    ("add", State(10), 5)
        ↓
    optimize_ir()
        ↓
    ("add", same State object, 5)

Validated guarantees:

- State objects are not cloned.
- State subscribers are not copied.
- State objects are not evaluated.
- Runtime State remains attached to the runtime.
- Dynamic State expressions remain dynamic.
- Constant values can still be folded safely.

Important rule:

> Optimization may transform compile-time constants, but must never
> clone, evaluate, or detach runtime State objects.

---

# PHASE 9 VALIDATION

Latest focused IR validation:

    test/test_ir.py
    73 passed

Latest full regression:

    463 passed

Current Phase 9 milestone:

    IR Foundation              ✅
    IR Normalization            ✅
    Static Analysis             ✅
    Constant Folding            ✅
    Dependency Analysis         ✅
    Patch Planning              ✅
    IR Optimization             ✅

Optimization status:

    COMPLETE

Optimization validation:

- Constant folding
- Recursive folding
- Unsafe expression preservation
- IR tree optimization
- Child optimization
- Source immutability
- State identity preservation
- State subscriber preservation
- State preservation inside dynamic expressions

Definition of done for completed optimization milestone:

- Safe constants are folded.
- Runtime values remain runtime values.
- State identity is preserved.
- State subscribers remain attached.
- Source IR is not mutated.
- Existing runtime behavior remains green.

---

# 🧩 PHASE 9 ARCHITECTURAL BOUNDARY

Compiler layer:

    IR
    Normalization
    Static Analysis
    Constant Folding
    Dependency Analysis
    Patch Planning
    Optimization

Runtime layer:

    State
    Dependency Graph
    Dirty Nodes
    Scheduler
    Batching
    Component Tree
    WebSocket
    Client Runtime

These layers must remain separate.

Do not allow compiler optimization to:

- mutate live State
- subscribe to State
- execute events
- render DOM
- own WebSocket connections
- replace runtime dependency tracking
- replace runtime scheduling

Phase 9 compiler/runtime boundaries have been validated through focused IR
coverage and the full regression suite. Phase 9 is complete.

---

# PHASE 10 — MULTI-BACKEND ARCHITECTURE

Status: 🔴 FUTURE

Target:

    PyLage API
        ↓
    Shared UI Representation / IR
        ↓
    ┌───────────────┬───────────────┐
    ↓               ↓               ↓
   Web           Desktop          Future
                                  Native

Potential backends:

- Web
- Desktop
- Mobile
- Future native rendering

Potential technologies:

- Skia
- WebGPU
- OpenGL
- Vulkan
- Native platform APIs

Do not begin serious multi-backend work until the shared UI IR and
compiler boundaries are sufficiently stable.

---

# PHASE 11 — GPU / HARDWARE RENDERING

Status: 🔴 FUTURE RESEARCH

Long-term:

    Component Tree
          ↓
        UI IR
          ↓
      Render Graph
          ↓
     GPU Backend
          ↓
    Hardware Rendering

Possible technologies:

- WebGPU
- Skia
- OpenGL
- Vulkan
- Native GPU APIs

Do not begin this before software architecture and benchmarks justify it.

---

# 🔥 CURRENT ARCHITECTURAL PROGRESSION

    Phase 2A — Reactive Semantics
            ↓
        🟢 VALIDATED
            ↓
    Phase 2B — Dependency Graph
            ↓
        ✅ COMPLETE
            ↓
    Phase 2C — Dirty Tracking
            ↓
        ✅ COMPLETE
            ↓
    Phase 2D — Scheduler
            ↓
        ✅ COMPLETE
            ↓
    Phase 2E — Batching
            ↓
        ✅ COMPLETE
            ↓
    Phase 3 — UI Snapshot
            ↓
        ✅ COMPLETE
            ↓
    Phase 4 — Diff Engine
            ↓
        ✅ COMPLETE
            ↓
    Phase 5 — Patch Engine
            ↓
        🟢 COMPLETE
            ↓
    Phase 6 — Performance Baseline
            ↓
        🟢 COMPLETE
            ↓
    Phase 7 — UI Components
            ↓
        ✅ COMPLETE
            ↓
    Phase 8 — Styling System
            ↓
        🟡 PARTIAL
            ↓
    Phase 9 — Compiler / UI IR
            ↓
        ✅ COMPLETE
            ↓
    Phase 10 — Multi-Backend Architecture
            ↓
        🟢 ACTIVE
            ↓

# 🎯 CURRENT ACTIVE TASK

Phase 10 — Multi-Backend Architecture

Current Phase 9 completion record:

    Phase 9 — Compiler / UI IR
        ↓
    ✅ COMPLETE

    IR Foundation
        ↓
    Normalization
        ↓
    Static Analysis
        ↓
    Constant Folding
        ↓
    Dependency Analysis
        ↓
    Patch Planning
        ↓
    IR Optimization
        ↓
    State Identity Safety
        ↓
    463-Test Regression

Validated Phase 9 results:

    Focused IR suite: 73 passed
    Full regression: 463 passed
    Git commit: accba10
    Git tag: phase-9-complete

Phase 9 optimization:

    COMPLETE

Validated optimization guarantees:

- Safe constants are folded.
- Runtime values remain runtime values.
- State identity is preserved.
- State subscribers remain attached.
- State objects are not evaluated during optimization.
- Dynamic State expressions remain dynamic.
- Source IR remains immutable.

Current Phase 10 direction:

    Shared UI Representation / IR
              ↓
       Backend abstraction
              ↓
        Web backend
              ↓
      Future Desktop backend
              ↓
       Future Native backend

Immediate practical milestone:

    Build and validate a real sample web page
            ↓
    Exercise PyLage components
            ↓
    Exercise styling
            ↓
    Exercise reactive State
            ↓
    Exercise diff / patch pipeline
            ↓
    Validate the framework end-to-end

Architectural rule:

> Phase 10 should validate the existing architecture through real
> applications before introducing additional backend complexity.

# 🧪 TESTING POLICY

Every architectural change follows:

    Audit
      ↓
    Small change
      ↓
    Focused test
      ↓
    Relevant full suite
      ↓
    git diff --check
      ↓
    git diff review
      ↓
    Commit
      ↓
    Push

Never:

    Large rewrite
        ↓
    Hope it works

Tests must prove architecture, not only implementation details.

Required validation:

    pytest -q

Before commit:

    git diff --check
    git status
    git diff

---

# 🔐 CHECKPOINT POLICY

Create a Git checkpoint before every major phase or risky architectural
change.

Checkpoint format:

    phase-X-precheck

Recommended flow:

    pytest -q
    git diff --check
    git status
    git add -A
    git commit -m "checkpoint: ..."
    git push origin main
    git tag -a phase-X-precheck -m "..."
    git push origin phase-X-precheck

Before risky changes:

    git status
    git log -3 --oneline
    git tag --list

---

# 🚫 DO NOT DO YET

Until the compiler/runtime architecture is stable:

- Do not build a huge compiler
- Do not build desktop backend
- Do not build mobile backend
- Do not build GPU backend
- Do not build cloud platform
- Do not build authentication
- Do not build AI layer
- Do not build a huge CSS framework
- Do not add components without architectural need
- Do not move runtime responsibilities into compiler code

Priority:

    Reactive Runtime
          ↓
    Snapshot
          ↓
    Diff
          ↓
    Patch
          ↓
    Performance
          ↓
    UI IR
          ↓
    Compiler Optimization
          ↓
    Multi-Backend

---

# 📌 CURRENT CHECKPOINT

Latest validated state:

    Phase 9 — Compiler / UI IR
    ✅ COMPLETE

Phase 9 validation:

    Focused IR suite: 73 passed
    Full regression: 463 passed

Phase 9 Git checkpoint:

    Commit: accba10
    Message: feat: complete phase 9 compiler and UI IR
    Tag: phase-9-complete

Phase 9 capabilities:

    IRNode
    snapshot_to_ir
    normalize_ir
    analyze_ir
    constant_fold
    analyze_ir_dependencies
    plan_patches
    optimize_ir

Runtime safety:

    State identity preserved
    State subscribers preserved
    Source IR remains immutable
    Dynamic State expressions remain dynamic

Current architectural phase:

    Phase 10 — Multi-Backend Architecture
    🟢 ACTIVE

Current practical objective:

    Build a sample web page and use it as the first real-world
    end-to-end validation of the PyLage architecture.
