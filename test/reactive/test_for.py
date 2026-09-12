from __future__ import annotations

import pytest

import pylage as pl
from pylage.ENGINE.core.component import Component


def test_public_for_each_api_is_exported():
    assert hasattr(pl, "for_each")
    assert "for_each" in pl.__all__


def test_for_renders_initial_items():
    items = pl.reactive_list(["A", "B", "C"])
    rendered = pl.for_each(items, lambda item: pl.text(item))

    assert [child.props["text"] for child in rendered.children] == [
        "A", "B", "C"
    ]


def test_for_append_adds_rendered_component():
    items = pl.reactive_list(["A"])
    first = pl.for_each(items, lambda item: pl.text(item))

    items.append("B")

    assert [child.props["text"] for child in first.children] == ["A", "B"]


def test_for_remove_uses_delta_index():
    items = pl.reactive_list(["A", "B", "C"])
    rendered = pl.for_each(items, lambda item: pl.text(item))

    items.remove("B")

    assert [child.props["text"] for child in rendered.children] == ["A", "C"]


def test_for_insert_preserves_existing_component_identity():
    items = pl.reactive_list(["A", "C"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    first = rendered.children[0]
    last = rendered.children[1]

    items.insert(1, "B")

    assert rendered.children[0] is first
    assert rendered.children[2] is last
    assert [child.props["text"] for child in rendered.children] == [
        "A", "B", "C"
    ]


def test_for_move_preserves_component_identity():
    items = pl.reactive_list(["A", "B", "C"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    first = rendered.children[0]
    second = rendered.children[1]
    third = rendered.children[2]

    items.move(0, 2)

    assert rendered.children == [second, third, first]


def test_for_update_replaces_only_updated_component():
    items = pl.reactive_list(["A", "B", "C"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    first = rendered.children[0]
    third = rendered.children[2]

    items.update(1, "Updated")

    assert rendered.children[0] is first
    assert rendered.children[2] is third
    assert rendered.children[1].props["text"] == "Updated"


def test_for_emits_one_set_children_mutation_per_delta():
    items = pl.reactive_list(["A"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    mutations = []
    rendered.subscribe_mutation(mutations.append)

    items.append("B")

    assert len(mutations) == 1
    assert mutations[0]["type"] == "set_children"


def test_for_rejects_non_reactive_list():
    with pytest.raises(TypeError, match="ReactiveList"):
        pl.for_each(["A"], lambda item: pl.text(item))


def test_for_rejects_non_callable_renderer():
    items = pl.reactive_list(["A"])

    with pytest.raises(TypeError, match="callable"):
        pl.for_each(items, "not callable")


def test_for_requires_renderer_to_return_component():
    items = pl.reactive_list(["A"])

    with pytest.raises(TypeError, match="Component"):
        pl.for_each(items, lambda item: item)


def test_for_dispose_stops_future_updates():
    items = pl.reactive_list(["A"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    original = rendered.children[0]

    rendered.dispose()
    items.append("B")

    assert rendered.children == [original]


def test_for_dispose_is_idempotent():
    items = pl.reactive_list(["A"])
    rendered = pl.for_each(items, lambda item: pl.text(item))

    rendered.dispose()
    rendered.dispose()


def test_for_duplicate_values_use_delta_index():
    items = pl.reactive_list(["A", "A", "B"])
    rendered = pl.for_each(items, lambda item: pl.text(item))
    first = rendered.children[0]
    second = rendered.children[1]
    third = rendered.children[2]

    items.remove("A")

    assert rendered.children == [second, third]
    assert rendered.children[0] is second
    assert first is not second


def test_for_renders_through_existing_generic_fallback():
    items = pl.reactive_list(["A"])
    rendered = pl.for_each(items, lambda item: pl.text(item))

    from pylage.ENGINE.core.renderer import render

    html = render(rendered)

    assert "<div" in html
    assert "<for" not in html
    assert "A" in html


def test_for_reactive_append_updates_existing_renderer_path():
    items = pl.reactive_list(["A"])
    rendered = pl.for_each(items, lambda item: pl.text(item))

    from pylage.ENGINE.core.renderer import render

    items.append("B")
    html = render(rendered)

    assert "A" in html
    assert "B" in html
