from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI import dialog


def test_dialog_wraps_existing_engine_dialog():
    component = dialog("Hello")

    assert isinstance(component, Component)
    assert component.type == "Dialog"


def test_dialog_renders_text():
    html = render(dialog(Text("Hello Dialog")))

    assert "<dialog" in html
    assert "Hello Dialog" in html
    assert "</dialog>" in html


def test_dialog_supports_open_boolean():
    closed = dialog(Text("Closed"), open=False)
    opened = dialog(Text("Open"), open=True)

    assert " open" not in render(closed)
    assert " open" in render(opened)


def test_dialog_supports_reactive_open_state():
    state = State(False)
    component = dialog(Text("Reactive"), open=state)

    assert " open" not in render(component)

    state.set(True)

    assert " open" in render(component)


def test_dialog_forwards_engine_props():
    component = dialog(
        Text("Message"),
        title="Confirmation",
        class_name="custom-dialog",
    )

    assert component.props["title"] == "Confirmation"
    assert component.props["class_name"] == "custom-dialog"


def test_dialog_supports_custom_style_override():
    component = dialog(
        Text("Message"),
        style=Style(padding="32px"),
    )

    assert component.props["style"].padding == "32px"


def test_dialog_preserves_component_children():
    child = Component("Text", children=["Child"])
    component = dialog(child)

    assert component.children == [child]


def test_dialog_is_publicly_exported():
    from pylage.UI.components import dialog as component_dialog

    assert component_dialog is dialog
