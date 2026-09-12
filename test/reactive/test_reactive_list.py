from pylage.ENGINE.core.reactive_list import ReactiveList


def test_initial_values_and_value_snapshot():
    items = ReactiveList([1, 2, 3])
    assert items.value == [1, 2, 3]
    snapshot = items.value
    snapshot.append(4)
    assert items.value == [1, 2, 3]


def test_append_emits_one_atomic_delta():
    items = ReactiveList([1])
    deltas = []
    items.subscribe(deltas.append)
    items.append(2)
    assert items.value == [1, 2]
    assert deltas == [{"type": "append", "index": 1, "value": 2}]


def test_remove_emits_one_atomic_delta():
    items = ReactiveList(["a", "b", "c"])
    deltas = []
    items.subscribe(deltas.append)
    items.remove("b")
    assert items.value == ["a", "c"]
    assert deltas == [{"type": "remove", "index": 1, "value": "b"}]


def test_insert_emits_one_atomic_delta():
    items = ReactiveList(["a", "c"])
    deltas = []
    items.subscribe(deltas.append)
    items.insert(1, "b")
    assert items.value == ["a", "b", "c"]
    assert deltas == [{"type": "insert", "index": 1, "value": "b"}]


def test_move_emits_one_atomic_delta():
    items = ReactiveList(["a", "b", "c"])
    deltas = []
    items.subscribe(deltas.append)
    items.move(0, 2)
    assert items.value == ["b", "c", "a"]
    assert deltas == [{"type": "move", "from_index": 0, "to_index": 2, "value": "a"}]


def test_update_emits_one_atomic_delta():
    items = ReactiveList(["a", "b"])
    deltas = []
    items.subscribe(deltas.append)
    items.update(1, "updated")
    assert items.value == ["a", "updated"]
    assert deltas == [{"type": "update", "index": 1, "old_value": "b", "value": "updated"}]


def test_update_same_value_does_not_notify():
    items = ReactiveList(["a"])
    deltas = []
    items.subscribe(deltas.append)
    items.update(0, "a")
    assert items.value == ["a"]
    assert deltas == []


def test_multiple_mutations_preserve_delta_order():
    items = ReactiveList()
    deltas = []
    items.subscribe(deltas.append)
    items.append("a")
    items.append("b")
    items.insert(1, "middle")
    items.update(0, "updated")
    items.move(0, 2)
    items.remove("b")
    assert [delta["type"] for delta in deltas] == ["append", "append", "insert", "update", "move", "remove"]


def test_unsubscribe_stops_future_notifications():
    items = ReactiveList()
    deltas = []
    unsubscribe = items.subscribe(deltas.append)
    items.append(1)
    unsubscribe()
    items.append(2)
    assert len(deltas) == 1
    assert deltas[0]["value"] == 1


def test_unsubscribe_is_idempotent():
    items = ReactiveList()
    deltas = []
    unsubscribe = items.subscribe(deltas.append)
    unsubscribe()
    unsubscribe()
    items.append(1)
    assert deltas == []


def test_subscriber_iteration_is_stable():
    items = ReactiveList()
    deltas = []
    def first(delta):
        deltas.append(("first", delta["value"]))
        items.subscribe(lambda delta: deltas.append(("late", delta["value"])))
    items.subscribe(first)
    items.append(1)
    items.append(2)
    assert deltas == [("first", 1), ("first", 2), ("late", 2)]


def test_bind_is_subscription_alias():
    items = ReactiveList()
    deltas = []
    unsubscribe = items.bind(deltas.append)
    items.append("value")
    unsubscribe()
    assert len(deltas) == 1


def test_move_same_index_is_noop():
    items = ReactiveList(["a", "b"])
    deltas = []
    items.subscribe(deltas.append)
    items.move(1, 1)
    assert items.value == ["a", "b"]
    assert deltas == []


def test_remove_missing_value_raises():
    items = ReactiveList(["a"])
    import pytest
    with pytest.raises(ValueError):
        items.remove("missing")


def test_move_empty_list_raises_index_error():
    items = ReactiveList()
    import pytest
    with pytest.raises(IndexError):
        items.move(0, 0)


def test_list_protocol_helpers():
    items = ReactiveList(["a", "b"])
    assert len(items) == 2
    assert list(items) == ["a", "b"]
    assert items[1] == "b"


def test_public_reactive_list_api():
    import pylage as pl
    from pylage.ENGINE import ReactiveList

    items = pl.reactive_list([1, 2])

    assert isinstance(items, ReactiveList)
    assert items.value == [1, 2]
    assert "reactive_list" in pl.__all__


def test_insert_negative_index_reports_actual_index():
    from pylage.ENGINE import ReactiveList

    items = ReactiveList([1, 3])
    deltas = []
    items.subscribe(deltas.append)

    items.insert(-1, 2)

    assert items.value == [1, 2, 3]
    assert deltas == [{"type": "insert", "index": 1, "value": 2}]
