from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.dirty import DirtyNodes


def test_state_change_marks_dependent_component_dirty():
    state = State(0)
    component = Component("Heading")

    graph = DependencyGraph()
    graph.add_dependency(state, component, "text")

    dirty = DirtyNodes()
    dirty.mark_from_state(state, graph)

    assert dirty.contains(component)
    assert len(dirty) == 1


def test_multiple_states_mark_same_component_only_once():
    state1 = State(0)
    state2 = State(0)
    component = Component("Heading")

    graph = DependencyGraph()
    graph.add_dependency(state1, component, "text")
    graph.add_dependency(state2, component, "disabled")

    dirty = DirtyNodes()

    dirty.mark_from_state(state1, graph)
    dirty.mark_from_state(state2, graph)

    assert dirty.contains(component)
    assert len(dirty) == 1


def test_clear_removes_all_dirty_nodes():
    component1 = Component("Heading")
    component2 = Component("Button")

    dirty = DirtyNodes()

    dirty.mark(component1)
    dirty.mark(component2)

    assert len(dirty) == 2

    dirty.clear()

    assert len(dirty) == 0
    assert not dirty.contains(component1)
    assert not dirty.contains(component2)


def test_dirty_nodes_track_changed_props_per_component():
    from pylage.ENGINE import Text

    component = Text("Test")
    dirty = DirtyNodes()

    dirty.mark(component, "text")
    dirty.mark(component, "class_name")
    dirty.mark(component, "text")

    assert dirty.contains(component)
    assert dirty.changed_props(component) == {"text", "class_name"}

    dirty.clear()

    assert dirty.changed_props(component) is None
