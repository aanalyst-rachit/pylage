import pylage as ps
from pylage.ENGINE import Column, Heading, State

from pylage.ENGINE.core.binding import StateBinding
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.scheduler import Scheduler


def test_state_change_flows_through_reactive_pipeline():
    state = State(0)
    heading = Heading(text=state)
    app = Column(heading)

    graph = DependencyGraph()
    dirty = DirtyNodes()
    updates = []

    StateBinding(
        app,
        lambda component, props: updates.append(
            (component, props)
        ),
        graph=graph,
    )

    state.set(1)

    dirty.mark_from_state(state, graph)

    scheduler = Scheduler(
        dirty,
        lambda component: updates.append(
            (component, {"scheduled": True})
        ),
    )

    scheduler.flush()

    assert heading in [item[0] for item in updates]
    assert len(dirty) == 0
