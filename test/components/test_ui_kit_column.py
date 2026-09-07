from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.layout import column


def test_ui_kit_column_wraps_existing_engine_column():
    component = column(Text("Hello"))
    assert isinstance(component, Component)
    assert component.type == "Column"


def test_ui_kit_column_renders_as_div():
    html = render(column(Text("Hello Column")))
    assert "<div" in html
    assert "Hello Column" in html


def test_ui_kit_column_forwards_props():
    html = render(column(Text("Content"), class_name="custom-column", title="Column title"))
    assert 'class="custom-column"' in html
    assert 'title="Column title"' in html


def test_ui_kit_column_supports_style():
    component = column(Text("Styled"), style=Style(padding="20px"))
    assert component.props["style"].padding == "20px"


def test_ui_kit_column_resolves_default_style():
    component = column(Text("Default"))
    assert component.props["style"] is not None


def test_ui_kit_column_supports_reactive_style_values():
    gap = State("12px")
    html = render(column(Text("Reactive"), style=Style(gap=gap)))
    assert "gap:12px" in html


def test_ui_kit_column_preserves_component_children():
    child = Component("Text", children=["Child"])
    component = column(child)
    assert component.children == [child]


def test_ui_kit_column_filters_none_children():
    component = column(None, Text("A"), None, Text("B"))
    assert len(component.children) == 2


def test_ui_kit_column_is_publicly_exported():
    from pylage.UI.layout import column as exported_column
    assert exported_column is column
