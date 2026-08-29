from pyskin.core.component import Component
from pyskin.core.tree import TreeMutationObserver


def test_observer_receives_nested_add_mutations():
    child = Component(type="Column")
    root = Component(
        type="Column",
        children=[child],
    )

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    grandchild = Component(type="Button")
    child.add(grandchild)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "add"
    assert mutations[0]["parent"] is child
    assert mutations[0]["children"] == [grandchild]

    observer.stop()


def test_observer_can_be_stopped():
    root = Component(type="Column")
    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    root.add(Component(type="Heading"))

    assert len(mutations) == 1

    observer.stop()

    root.add(Component(type="Button"))

    assert len(mutations) == 1


def test_observer_stop_is_idempotent():
    root = Component(type="Column")

    observer = TreeMutationObserver(
        root,
        lambda event: None,
    )

    observer.stop()
    observer.stop()


def test_observer_tracks_components_added_after_observer_creation():
    root = Component(type="Column")

    mutations = []

    observer = TreeMutationObserver(
        root,
        lambda event: mutations.append(event),
    )

    child = Component(type="Column")
    root.add(child)

    # The add to root is observed.
    assert len(mutations) == 1

    button = Component(type="Button")
    child.add(button)

    # The newly-added child is now also observed.
    assert len(mutations) == 2
    assert mutations[1]["parent"] is child
    assert mutations[1]["children"] == [button]

    observer.stop()
