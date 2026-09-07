import pylage as ps
from pylage.ENGINE import Column, Heading, State

from pylage.ENGINE.core.binding import StateBinding
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.scheduler import Scheduler


def test_multiple_state_changes_are_coalesced_into_one_flush():
    state = State(0)
    heading = Heading(text=state)
    app = Column(heading)

    graph = DependencyGraph()
    dirty = DirtyNodes()
    processed = []

    scheduler = Scheduler(
        dirty,
        lambda component: processed.append(component),
    )

    StateBinding(
        app,
        lambda component, props: None,
        graph=graph,
        dirty=dirty,
        scheduler=scheduler,
    )

    state.set(1)
    state.set(2)
    state.set(3)

    # State changes should accumulate before the explicit
    # batching boundary.
    assert len(dirty) == 1
    assert dirty.contains(heading)

    assert processed == []

    scheduler.flush()

    assert processed == [heading]
    assert len(dirty) == 0
    assert state.value == 3
