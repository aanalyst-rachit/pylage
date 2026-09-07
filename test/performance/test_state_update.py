from time import perf_counter

from pylage.ENGINE import Heading, State
from pylage.ENGINE.core.binding import StateBinding
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.scheduler import Scheduler
from pylage.UI.components.text import text


def _build_pipeline(component):
    state = component.props["text"]
    dirty = DirtyNodes()
    processed = []
    scheduler = Scheduler(
        dirty,
        lambda node: processed.append(node),
    )
    StateBinding(
        component,
        lambda component, props: None,
        dirty=dirty,
        scheduler=scheduler,
    )
    return state, scheduler, processed


def _measure(fn, iterations=1000):
    start = perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = perf_counter() - start
    return {
        "total": elapsed,
        "per_operation": elapsed / iterations,
    }


def test_phase16_state_update_overhead():
    iterations = 1000

    ui_state = State(0)
    ui_component = text(ui_state)
    ui_state, ui_scheduler, ui_processed = _build_pipeline(ui_component)

    core_state = State(0)
    core_component = Heading(text=core_state)
    core_state, core_scheduler, core_processed = _build_pipeline(core_component)

    ui_result = _measure(
        lambda: ui_state.set(ui_state.value + 1),
        iterations,
    )
    core_result = _measure(
        lambda: core_state.set(core_state.value + 1),
        iterations,
    )

    ui_scheduler.flush()
    core_scheduler.flush()

    assert ui_state.value == iterations
    assert core_state.value == iterations
    assert len(ui_processed) == 1
    assert len(core_processed) == 1

    print()
    print("===== PHASE 16 — STATE UPDATE OVERHEAD =====")
    print(f"iterations        : {iterations}")
    print()
    print("ui_text")
    print(f"  total           : {ui_result['total']:.9f}s")
    print(f"  per update      : {ui_result['per_operation']:.9f}s")
    print()
    print("core_heading")
    print(f"  total           : {core_result['total']:.9f}s")
    print(f"  per update      : {core_result['per_operation']:.9f}s")
    print()
    print(f"ui processing     : {len(ui_processed)}")
    print(f"core processing   : {len(core_processed)}")

    assert ui_result["total"] >= 0
    assert core_result["total"] >= 0
