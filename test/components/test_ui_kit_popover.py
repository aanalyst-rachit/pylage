from pylage.ENGINE import Text, Button
from pylage.ENGINE.core.renderer import render
from pylage.UI.recipes import popover


def test_ui_kit_popover_wraps_existing_popover():
    component = popover(
        Text("Popover content"),
        title="Additional information",
    )
    html = render(component)

    assert "<div" in html
    assert 'title="Additional information"' in html
    assert "Popover content" in html


def test_ui_kit_popover_preserves_children_and_props():
    component = popover(
        Text("Details"),
        Button(text="Close"),
        class_name="popover",
        title="Quick information",
    )
    html = render(component)

    assert 'class="popover"' in html
    assert 'title="Quick information"' in html
    assert "Details" in html
    assert "Close" in html
