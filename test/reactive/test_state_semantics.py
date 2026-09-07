import pytest

from pylage.ENGINE.core.state import DerivedState, State


def test_same_value_does_not_notify():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(0)

    assert changes == []


def test_different_value_notifies_once():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)

    assert changes == [(0, 1)]


def test_multiple_changes_preserve_order():
    state = State(0)
    changes = []

    state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)
    state.set(2)
    state.set(3)

    assert changes == [
        (0, 1),
        (1, 2),
        (2, 3),
    ]


def test_multiple_subscribers_all_receive_update():
    state = State("initial")

    first = []
    second = []

    state.subscribe(
        lambda old, new: first.append((old, new))
    )

    state.subscribe(
        lambda old, new: second.append((old, new))
    )

    state.set("updated")

    assert first == [("initial", "updated")]
    assert second == [("initial", "updated")]


def test_unsubscribe_stops_future_notifications():
    state = State(0)
    changes = []

    unsubscribe = state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    state.set(1)
    unsubscribe()
    state.set(2)

    assert changes == [(0, 1)]


def test_unsubscribe_is_idempotent():
    state = State(0)
    changes = []

    unsubscribe = state.subscribe(
        lambda old, new: changes.append((old, new))
    )

    unsubscribe()
    unsubscribe()

    state.set(1)

    assert changes == []


def test_subscriber_can_unsubscribe_during_notification():
    state = State(0)
    changes = []

    unsubscribe = None

    def listener(old, new):
        changes.append((old, new))
        unsubscribe()

    unsubscribe = state.subscribe(listener)

    state.set(1)
    state.set(2)

    assert changes == [(0, 1)]


def test_subscriber_iteration_is_stable():
    state = State(0)
    changes = []

    def first(old, new):
        changes.append(("first", old, new))

        state.subscribe(
            lambda old, new: changes.append(
                ("late", old, new)
            )
        )

    state.subscribe(first)

    state.set(1)

    assert changes == [
        ("first", 0, 1),
    ]

    state.set(2)

    assert changes == [
        ("first", 0, 1),
        ("first", 1, 2),
        ("late", 1, 2),
    ]



def test_derived_state_initial_value():
    source = State(10)
    derived = DerivedState(source, compute=lambda value: value * 2)

    assert derived.value == 20


def test_derived_state_recomputes_when_source_changes():
    source = State(10)
    derived = DerivedState(source, compute=lambda value: value * 2)

    source.set(15)

    assert derived.value == 30


def test_derived_state_notifies_only_when_derived_value_changes():
    source = State(1)
    derived = DerivedState(source, compute=lambda value: value % 2)
    changes = []

    derived.subscribe(lambda old, new: changes.append((old, new)))

    source.set(3)
    source.set(4)

    assert changes == [(1, 0)]


def test_derived_state_is_read_only():
    source = State(1)
    derived = DerivedState(source, compute=lambda value: value)

    with pytest.raises(TypeError, match="read-only"):
        derived.set(2)


def test_derived_state_dispose_stops_source_updates():
    source = State(1)
    derived = DerivedState(source, compute=lambda value: value * 2)

    derived.dispose()
    source.set(5)

    assert derived.value == 2


def test_derived_state_dispose_is_idempotent():
    source = State(1)
    derived = DerivedState(source, compute=lambda value: value * 2)

    derived.dispose()
    derived.dispose()

    assert derived.value == 2

def test_public_derived_api():
    import pylage as pl

    source = pl.State("Dashboard")
    active = pl.derived(source, compute=lambda page: page == "Dashboard")

    assert active.value is True
    source.set("Projects")
    assert active.value is False


def test_public_derived_api_supports_multiple_sources():
    import pylage as pl

    page = pl.State("Dashboard")
    enabled = pl.State(True)
    active = pl.derived(page, enabled, compute=lambda current_page, is_enabled: current_page == "Dashboard" and is_enabled)

    assert active.value is True
    enabled.set(False)
    assert active.value is False
    page.set("Projects")
    enabled.set(True)
    assert active.value is False

