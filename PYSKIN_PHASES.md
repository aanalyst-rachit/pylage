# 🐍 PySkin / PU — PHASE ROADMAP

> Purpose: This file is the compact phase tracker for the PySkin project.
> Update phase status here instead of rewriting the full master blueprint.
>
> Long-term vision:
> Build a Python-first, low-latency, fine-grained reactive UI framework
> where developers use Python only and browser/native rendering complexity
> remains hidden inside PySkin.

---

# 🔒 PROJECT IDENTITY

Project: PySkin
Long-term vision: PU — Python Universal UI Framework
Repository: https://github.com/aanalyst-rachit/pyskin
Branch: main

Current stable checkpoint:
- Commit: 38efd85 — test: add phase 2e batching benchmark
- Tag: phase-2e-batching
- Tests: 117 passed
- Status: Tree mutation + dependency graph + dirty tracking + scheduler foundation stable; batching remains

Master blueprint:
- `project pyskin blueprint.txt`

This file:
- `PYSKIN_PHASES.md`

---

# 🧭 NORTH STAR

Python application
        ↓
PySkin API
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

> PySkin is not just a Python-to-HTML generator.
> PySkin is a Python-first reactive UI programming model.

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

Definition of done:

- Components can be constructed.
- Components form a tree.
- Props and children are represented.
- Events can be attached.
- State can hold reactive values.
- Basic HTML can be rendered.

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

- Complete runtime semantics of reactive metadata
- Further renderer genericization

Important rule:

> Do not expand registry features without an architectural need.

---

# PHASE 2 — FINE-GRAINED REACTIVE RUNTIME

Status: 🟢 ACTIVE

Current phase.

## Phase 2 — Completed Tree Mutation Runtime Foundation

The following tree-mutation infrastructure is now implemented and covered
by focused runtime/protocol/client tests:

- `Component.add()`
- `Component.insert()`
- `Component.remove()`
- `Component.move_to()`
- `Component.replace()`
- `Component.clear()`
- `Component.set_children()`

Mutation event system:

- Atomic mutation events
- Mutation subscribers
- Replace mutation events
- Clear mutation events
- Set-children mutation events
- Correct parent ownership updates

Tree protocol:

- `tree_add`
- `tree_remove`
- `tree_move`
- `tree_replace`
- `tree_clear`
- `tree_set_children`

Runtime:

- WebSocket mutation broadcasting
- Recursive subtree serialization
- Nested replacement support
- Nested set-children support
- Empty-clear no-op behavior

Client runtime:

- Indexed tree insertion
- Tree move DOM patch
- Recursive tree replacement
- Tree clear DOM patch
- Recursive tree set-children DOM replacement

Validation:

    Full test suite: 106 passed

Architectural significance:

> This establishes the mutation-to-DOM transport foundation required by
> the later fine-grained reactive runtime.

Important:

> This does NOT mean Phase 2 reactive semantics are complete.
> Dependency tracking, dirty-node tracking, scheduling, and batching
> remain separate tasks.


Main objective:

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

## Phase 2A — Reactive Semantics

Status: 🟢 VALIDATED

Completed:
- `reactive=True` / `reactive=False` registry contracts
- State-to-component reactive binding
- Generic reactive prop updates
- Registry-driven reactive behavior
- WebSocket update propagation
- State value resolution before serialization
- Reactive browser DOM update path

Validation:
- Reactive registry/state contract tests passing
- WebSocket reactive pipeline passing
- Browser reactive counter passing

Remaining:
- Final semantic edge-case audit
- Confirm batching interaction with reactive semantics

Define precisely:

- What `reactive=True` means
- What `reactive=False` means
- Which State values create dependencies
- When dependencies are registered
- When updates are emitted
- When updates are suppressed

Definition of done:

- Runtime behavior matches registry metadata.
- Semantics are covered by focused tests.

---

## Phase 2B — Dependency Graph

Status: ✅ COMPLETE

Completed:
- Dependency registration
- State → Component → Prop dependency mapping
- Multiple dependents
- Dependency lookup
- Integration with StateBinding
- Lifecycle-safe binding foundation

Validation:
- `test_dependency_graph.py`
- `test_state_binding_graph.py`
- Full relevant suite passing

Target model:

    State A
       ├──→ Component X
       └──→ Component Y

    State B
       └──→ Component Z

When State A changes:

    X + Y → affected
    Z     → untouched

Required capabilities:

- Register dependency
- Remove dependency
- Find dependents
- Handle multiple dependents
- Avoid duplicate subscriptions
- Handle component lifecycle safely

Definition of done:

- State changes identify only affected components.
- Unrelated components are not marked dirty.

---

## Phase 2C — Dirty Node Tracking

Status: ✅ COMPLETE

Completed:
- Dirty node marking
- Duplicate dirty-node suppression
- Dirty node collection
- Scheduler integration
- Deterministic processing foundation

Validation:
- `test_dirty_nodes.py`
- Reactive pipeline tests passing

Target:

    State change
        ↓
    dependency lookup
        ↓
    dirty set

Example:

    dirty_nodes = {
        component_123,
        component_456
    }

Requirements:

- Mark node dirty
- Avoid duplicate dirty entries
- Clear dirty state after processing
- Preserve deterministic processing order where required

Definition of done:

- Only affected nodes enter the update pipeline.

---

## Phase 2D — Update Scheduler

Status: ✅ COMPLETE — PRE-BATCH SCHEDULER

Completed:
- Scheduler abstraction
- Dirty node processing
- Component update scheduling
- Integration with StateBinding
- State value resolution during scheduled update
- Reactive update dispatch

Important:
- Current scheduler is immediate/pre-batch.
- It does NOT yet provide multi-update coalescing.

Validation:
- `test_scheduler.py`
- `test_reactive_pipeline.py`
- `test_websocket_reactive_pipeline.py`
- Full suite: 117 passed

Target:

    State changes
        ↓
    mark dirty
        ↓
    schedule update
        ↓
    process dirty nodes

Questions to solve:

- Immediate vs deferred updates
- Synchronous batching
- Event-loop integration
- Re-entrant State changes
- Multiple State changes in one event

Do not assume batching improves performance.
Benchmark it.

Definition of done:

- Updates are scheduled deterministically.
- No unnecessary duplicate processing occurs.

---

## Phase 2E — Batching

Status: ✅ COMPLETE

Completed:
- Coalesced scheduler flush
- Duplicate scheduler request suppression
- Multiple State changes coalesced into one processing cycle
- Multiple States affecting one component processed once
- Final State value observed during scheduled processing
- Re-entrant State changes deferred to the next scheduler cycle
- Deterministic dirty-node processing preserved
- WebSocket runtime integration validated
- Batching benchmark added

Validation:
- Focused batching tests passing
- Focused WebSocket batching tests passing
- Full test suite: 126 passed
- Benchmark: 1000 state changes → 1 processing cycle
- Benchmark processing reduction: 1000x


First target:

    count.set(1)
    count.set(2)
    count.set(3)

should be experimentally evaluated for:

    one scheduled processing cycle
    final value = 3

Requirements:
- Define batching boundary
- Define flush semantics
- Prevent duplicate component processing
- Handle multiple States affecting one component
- Handle re-entrant State changes
- Preserve deterministic behavior
- Measure update count before/after batching

Do not assume batching is faster.
Benchmark actual latency and update counts.

Definition of done:
- Batching semantics explicitly defined.
- Focused batching tests pass.
- Existing 117-test suite remains green.
- No regression in WebSocket/browser reactivity.

Example:

    count.set(1)
    count.set(2)
    count.set(3)

Potential target:

    one update
    final value = 3

But this must be validated against actual runtime semantics.

Definition of done:

- Multiple related changes can be coalesced safely.
- Tests verify final state and update count.

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

Requirements:

- Stable node identity
- Stable component identity
- Props representation
- Text representation
- Children representation
- Deterministic structure

Important:

> Do not build a huge compiler/IR system here.
> Build only the representation required by the reactive runtime.

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

- `pyskin/core/snapshot.py`
- `test/test_snapshot.py`

Validation:

- Snapshot tests: 5 passed
- Tree replacement/set-children runtime tests: 5 passed
- Full test suite: 165 passed

Checkpoint:

- Commit: `f9c9001` — Complete Phase 3 runtime tree and snapshot work

Definition of done:

- Current UI state can be represented deterministically. ✅
- Previous and current representations can be compared. ✅

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

Responsibilities:

- Prop diff
- Text diff
- Child diff
- Node identity matching
- Insert
- Remove
- Replace
- Update

Definition of done:

- Correct minimal diffs for supported UI structures.
- Unchanged nodes generate no operations.

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

Possible operations:

- set attribute
- remove attribute
- set boolean
- set DOM property
- set text
- insert node
- remove node
- replace node

Exact protocol must be designed after diff semantics are stable.

Definition of done:

- Patch operations correctly transform old DOM state into new DOM state.

---

# PHASE 6 — PERFORMANCE / BENCHMARKS

Status: 🟢 ACTIVE

Measure real performance.

Required benchmarks:

- State update latency
- Event latency
- WebSocket latency
- Update throughput
- Patch size
- CPU usage
- Memory usage
- Component count scaling
- Dependency graph scaling

Test sizes:

- 10 nodes
- 100 nodes
- 1,000 nodes
- 10,000 nodes

Important:

> Performance claims must come from benchmarks, not assumptions.

---

# PHASE 7 — UI COMPONENT SYSTEM

Status: 🔴 NOT STARTED

Only after reactive runtime is stable.

Potential components:

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
- Data components

Rule:

> Do not build a huge component library before the runtime is proven.

---

# PHASE 8 — STYLING SYSTEM

Status: 🔴 NOT STARTED

Goals:

- Python style API
- Themes
- Responsive design
- Layout
- CSS generation
- Layout constraints

Potential future API:

    ps.Text(
        "Hello",
        style=ps.Style(...)
    )

Keep styling independent from the core reactive engine.

---

# PHASE 9 — COMPILER / UI IR

Status: 🟡 EARLY / ~10%

Potential systems:

- UI IR
- Normalization
- Static analysis
- Constant folding
- Dependency analysis
- Patch planning
- Optimization

Rule:

> Do not build a large compiler before reactive semantics,
> dependency tracking, diffing, and patching are stable.

---

# PHASE 10 — MULTI-BACKEND ARCHITECTURE

Status: 🔴 FUTURE

Target:

    PySkin API
        ↓
    Shared UI Representation / IR
        ↓
    ┌───────────────┬───────────────┐
    ↓               ↓               ↓
   Web           Desktop          Future

Potential native technologies:

- Skia
- WebGPU
- OpenGL
- Vulkan
- Native platform APIs

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

Do not begin this before the software architecture and benchmarks justify it.

---

# 🔥 CURRENT PHASE — PHASE 6

Current priority:

    Tree Mutation Foundation
            ↓
       ✅ COMPLETE
            ↓
    Phase 2A
       ↓
    Reactive Semantics
       ↓
       🟢 VALIDATED
            ↓
    Phase 2B
       ↓
    Dependency Graph
       ↓
       ✅ COMPLETE
            ↓
    Phase 2C
       ↓
    Dirty Tracking
       ↓
       ✅ COMPLETE
            ↓
    Phase 2D
       ↓
    Scheduler
       ↓
       ✅ PRE-BATCH COMPLETE
            ↓
    Phase 2E
       ↓
    ✅ BATCHING — COMPLETE
       ↓
    Phase 3 — UI Representation / Snapshot
       ↓
    ✅ COMPLETE
       ↓
    Phase 4 — Diff Engine
       ↓
    ✅ COMPLETE
       ↓
    Phase 5 — Patch Engine
       ↓
    ✅ COMPLETE
       ↓
    Phase 6 — Performance / Benchmarks
       ↓
    🟢 ACTIVE

Current active architectural task:

    Phase 6 — Performance / Benchmarks
            ↓
    Establish benchmark harness
            ↓
    Measure state update latency
            ↓
    Measure event latency
            ↓
    Measure WebSocket latency
            ↓
    Measure update throughput
            ↓
    Measure patch size
            ↓
    Measure CPU / memory usage
            ↓
    Measure component-count scaling
            ↓
    Measure dependency-graph scaling

---

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

---

# 🔐 CHECKPOINT POLICY

Create a Git checkpoint before every major phase.

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

Until the reactive runtime is stable:

- Do not build 100+ components
- Do not build desktop backend
- Do not build mobile backend
- Do not build GPU backend
- Do not build cloud platform
- Do not build authentication
- Do not build AI layer
- Do not build a huge CSS framework
- Do not build a huge compiler

Priority:

    State
      ↓
    Dependency
      ↓
    Dirty
      ↓
    Scheduler
      ↓
    Diff
      ↓
    Patch
      ↓
    Performance

---

# 📌 CURRENT CHECKPOINT

Commits:

    1834443 feat: complete phase 2e reactive batching pipeline
    38efd85 test: add phase 2e batching benchmark

Message:

    complete phase 2e reactive batching pipeline

Tag:

    phase-2e-complete (pending)

Tests:

    126 passed

Working tree:

    Phase 2E batching implementation stable
    Benchmark committed


Milestone:

    Component Mutation
          ↓
    Mutation Events
          ↓
    Tree Protocol
          ↓
    WebSocket Runtime
          ↓
    Recursive Client DOM Patches
          ↓
    Reactive Semantics
          ↓
    Dependency Graph
          ↓
    Dirty Nodes
          ↓
    Scheduler

Current next task:

    Phase 6 — Performance / Benchmarks
          ↓
    Benchmark harness
          ↓
    Runtime measurements
          ↓
    Patch/network measurements
          ↓
    Scaling measurements
          ↓
    Benchmark-backed performance baseline

---

# 📝 PHASE UPDATE RULE

When a phase progresses, update ONLY this file.

For each phase update:

1. Change `Status`
2. Update completed items
3. Update remaining items
4. Update definition of done if architecture changed
5. Record the latest checkpoint commit/tag

Do not rewrite the complete master blueprint unless the overall architecture itself changes.

---

# 🧠 ASSISTANT + DEVELOPER WORKING RULE

Before changing code:

1. Read this phase tracker.
2. Identify the current phase.
3. Identify the current sub-phase/task.
4. Inspect the existing implementation.
5. Make the smallest architectural change.
6. Add focused tests.
7. Run relevant tests.
8. Run full suite.
9. Review diff.
10. Commit checkpoint when milestone is stable.

Never skip architecture review just because a feature appears simple.

---

# 🏁 FINAL SUCCESS CRITERIA

PySkin succeeds when:

    Python-only developer API
            +
    Fine-grained reactivity
            +
    Dependency-aware updates
            +
    Minimal DOM/network patches
            +
    Low event latency
            +
    Scalable component tree
            +
    Generic registry architecture
            +
    Extensible renderer system
            +
    Multiple backends
            +
    Benchmark-backed performance

---

# ⭐ PROJECT NORTH STAR

> PySkin ka goal “Python se HTML banana” nahi hai.
>
> Goal hai Python ko ek serious, low-latency, fine-grained reactive UI
> programming model banana jiske peeche browser/native rendering
> complexity completely hidden ho.
