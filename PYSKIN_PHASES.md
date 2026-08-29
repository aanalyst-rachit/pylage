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
- Commit: e23b73d
- Tag: phase-2-precheck
- Tests: 8 passed
- Status: Stable before Phase 2

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Definition of done:

- Current UI state can be represented deterministically.
- Previous and current representations can be compared.

---

# PHASE 4 — DIFF ENGINE

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

Status: 🔴 NOT STARTED

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

# 🔥 CURRENT PHASE — PHASE 2

Current priority:

    Phase 2A
       ↓
    Reactive Semantics
       ↓
    Phase 2B
       ↓
    Dependency Graph
       ↓
    Phase 2C
       ↓
    Dirty Tracking
       ↓
    Phase 2D
       ↓
    Scheduler
       ↓
    Phase 2E
       ↓
    Batching

Then:

    Phase 3
       ↓
    UI Representation
       ↓
    Phase 4
       ↓
    Diff
       ↓
    Phase 5
       ↓
    Patch
       ↓
    Phase 6
       ↓
    Benchmarks

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

Commit:

    e23b73d

Message:

    checkpoint: complete registry reactive runtime foundation

Tag:

    phase-2-precheck

Tests:

    8 passed

Working tree:

    Stable checkpoint

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
