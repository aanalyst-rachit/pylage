from pylage.ENGINE import Text, Button
from pylage.ENGINE.core.renderer import render
from pylage.UI.recipes import tooltip


def test_ui_kit_tooltip_wraps_existing_tooltip():
    component = tooltip(
        Text("Info"),
        title="Helpful information",
    )
    html = render(component)

    assert "<span" in html
    assert "title=\"Helpful information\"" in html
    assert "Info" in html


def test_ui_kit_tooltip_preserves_children_and_props():
    component = tooltip(
        Text("Info"),
        Button(text="Action"),
        class_name="tooltip",
        title="Quick help",
    )
    html = render(component)

    assert "class=\"tooltip\"" in html
    assert "title=\"Quick help\"" in html
    assert "Info" in html
    assert "Action" in html
