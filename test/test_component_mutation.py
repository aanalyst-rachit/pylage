from pyskin.core.component import Component


def test_add_appends_children_and_returns_parent():
    parent = Component(type="Column")
    first = Component(type="Heading")
    second = Component(type="Button")

    result = parent.add(first, second)

    assert result is parent
    assert parent.children == [first, second]


def test_add_supports_chaining():
    parent = Component(type="Column")
    first = Component(type="Heading")
    second = Component(type="Button")

    parent.add(first).add(second)

    assert parent.children == [first, second]


def test_add_preserves_existing_children():
    first = Component(type="Heading")
    second = Component(type="Button")
    third = Component(type="Input")

    parent = Component(
        type="Column",
        children=[first],
    )

    parent.add(second, third)

    assert parent.children == [first, second, third]


def test_remove_child():
    parent = Component(type="Column")
    child = Component(type="Button")

    parent.add(child)
    result = parent.remove(child)

    assert result is parent
    assert child not in parent.children


def test_remove_notifies_tree_mutation_listener():
    parent = Component(type="Column")
    child = Component(type="Button")

    parent.add(child)

    mutations = []
    parent.subscribe_mutation(
        lambda event: mutations.append(event)
    )

    parent.remove(child)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "remove"
    assert mutations[0]["parent"] is parent
    assert mutations[0]["children"] == [child]

def test_move_child_between_parents():
    parent_a = Component(type="Column")
    parent_b = Component(type="Column")
    child = Component(type="Button")

    parent_a.add(child)

    result = child.move_to(parent_b)

    assert result is child
    assert child not in parent_a.children
    assert child in parent_b.children


def test_insert_child_at_index():
    parent = Component(type="Column")
    first = Component(type="Button")
    third = Component(type="Button")
    second = Component(type="Button")

    parent.add(first, third)

    result = parent.insert(1, second)

    assert result is parent
    assert parent.children == [first, second, third]


def test_insert_multiple_children_at_index():
    parent = Component(type="Column")
    first = Component(type="Button")
    last = Component(type="Button")
    middle_one = Component(type="Button")
    middle_two = Component(type="Button")

    parent.add(first, last)

    result = parent.insert(1, middle_one, middle_two)

    assert result is parent
    assert parent.children == [
        first,
        middle_one,
        middle_two,
        last,
    ]


def test_replace_child():
    parent = Component(type="Column")
    old_child = Component(type="Button")
    new_child = Component(type="Text")

    parent.add(old_child)

    result = parent.replace(old_child, new_child)

    assert result is parent
    assert parent.children == [new_child]


def test_clear_children():
    parent = Component(type="Column")
    first = Component(type="Button")
    second = Component(type="Text")

    parent.add(first, second)

    result = parent.clear()

    assert result is parent
    assert parent.children == []


def test_set_children_replaces_all_children():
    parent = Component(type="Column")

    old_first = Component(type="Button")
    old_second = Component(type="Text")

    new_first = Component(type="Text")
    new_second = Component(type="Button")

    parent.add(old_first, old_second)

    result = parent.set_children(new_first, new_second)

    assert result is parent
    assert parent.children == [new_first, new_second]

    assert old_first._parent is None
    assert old_second._parent is None

    assert new_first._parent is parent
    assert new_second._parent is parent
