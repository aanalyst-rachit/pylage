from __future__ import annotations

import pytest

import pylage as pl
from pylage.ENGINE.core.component import Component


def test_public_cond_api_is_exported():
    assert hasattr(pl, "cond")
    assert "cond" in pl.__all__


def test_cond_renders_true_branch_initially():
    condition = pl.state(True)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")

    conditional = pl.cond(condition, shown, hidden)

    assert isinstance(conditional, Component)
    assert conditional.children == [shown]


def test_cond_renders_false_branch_initially():
    condition = pl.state(False)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")

    conditional = pl.cond(condition, shown, hidden)

    assert conditional.children == [hidden]


def test_cond_switches_from_true_to_false_reactively():
    condition = pl.state(True)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")

    conditional = pl.cond(condition, shown, hidden)

    condition.set(False)

    assert conditional.children == [hidden]


def test_cond_switches_from_false_to_true_reactively():
    condition = pl.state(False)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")

    conditional = pl.cond(condition, shown, hidden)

    condition.set(True)

    assert conditional.children == [shown]


def test_cond_without_else_has_no_children_when_false():
    condition = pl.state(False)
    shown = pl.text("Shown")

    conditional = pl.cond(condition, shown)

    assert conditional.children == []


def test_cond_without_else_reacts_to_true_then_false():
    condition = pl.state(False)
    shown = pl.text("Shown")

    conditional = pl.cond(condition, shown)

    condition.set(True)
    assert conditional.children == [shown]

    condition.set(False)
    assert conditional.children == []


def test_cond_preserves_branch_component_identity():
    condition = pl.state(True)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")

    conditional = pl.cond(condition, shown, hidden)

    condition.set(False)
    assert conditional.children[0] is hidden

    condition.set(True)
    assert conditional.children[0] is shown


def test_cond_emits_set_children_mutation_on_branch_change():
    condition = pl.state(True)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")
    conditional = pl.cond(condition, shown, hidden)

    mutations = []
    conditional.subscribe_mutation(mutations.append)

    condition.set(False)

    assert len(mutations) == 1
    assert mutations[0]["type"] == "set_children"
    assert mutations[0]["parent"] is conditional
    assert mutations[0]["old_children"] == [shown]
    assert mutations[0]["children"] == [hidden]


def test_cond_rejects_non_state_condition():
    with pytest.raises(TypeError, match="condition"):
        pl.cond(True, pl.text("Shown"))


def test_cond_dispose_stops_future_reactive_updates():
    condition = pl.state(True)
    shown = pl.text("Shown")
    hidden = pl.text("Hidden")
    conditional = pl.cond(condition, shown, hidden)

    conditional.dispose()
    condition.set(False)

    assert conditional.children == [shown]


def test_cond_dispose_is_idempotent():
    condition = pl.state(True)
    conditional = pl.cond(
        condition,
        pl.text("Shown"),
        pl.text("Hidden"),
    )

    conditional.dispose()
    conditional.dispose()


def test_cond_rejects_more_than_two_branches():
    condition = pl.state(True)

    with pytest.raises(TypeError, match="takes from 2 to 3 positional arguments"):
        pl.cond(
            condition,
            pl.text("One"),
            pl.text("Two"),
            pl.text("Three"),
        )


def test_cond_renders_through_existing_generic_div_fallback():
    condition = pl.state(True)
    conditional = pl.cond(condition, pl.text("Shown"), pl.text("Hidden"))

    from pylage.ENGINE.core.renderer import render

    html = render(conditional)

    assert "<div" in html
    assert "<cond" not in html
    assert "Shown" in html
    assert "Hidden" not in html

def test_cond_renderer_updates_to_existing_branch_after_reactive_switch():
    condition = pl.state(True)
    conditional = pl.cond(condition, pl.text("Shown"), pl.text("Hidden"))

    from pylage.ENGINE.core.renderer import render

    condition.set(False)
    html = render(conditional)

    assert "<div" in html
    assert "<cond" not in html
    assert "Hidden" in html
    assert "Shown" not in html
