from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.layout import row


def test_ui_kit_row_wraps_existing_engine_row():
    component = row(Text("Hello"))
    assert isinstance(component, Component)
    assert component.type == "Row"


def test_ui_kit_row_renders_as_div():
    html = render(row(Text("Hello Row")))
    assert "<div" in html
    assert "Hello Row" in html


def test_ui_kit_row_forwards_props():
    html = render(row(Text("Content"), class_name="custom-row", title="Row title"))
    assert 'class="custom-row"' in html
    assert 'title="Row title"' in html


def test_ui_kit_row_supports_style():
    component = row(Text("Styled"), style=Style(padding="20px"))
    assert component.props["style"].padding == "20px"


def test_ui_kit_row_resolves_default_style():
    component = row(Text("Default"))
    assert component.props["style"] is not None


def test_ui_kit_row_supports_reactive_style_values():
    gap = State("12px")
    html = render(row(Text("Reactive"), style=Style(gap=gap)))
    assert "gap:12px" in html


def test_ui_kit_row_preserves_component_children():
    child = Component("Text", children=["Child"])
    component = row(child)
    assert component.children == [child]


def test_ui_kit_row_filters_none_children():
    component = row(None, Text("A"), None, Text("B"))
    assert len(component.children) == 2


def test_ui_kit_row_is_publicly_exported():
    from pylage.UI.layout import row as exported_row
    assert exported_row is row
