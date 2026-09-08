from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.recipes.modal import modal


def test_modal_composes_dialog_and_card():
    component = modal(Text("Hello"))

    assert isinstance(component, Component)
    assert component.type == "Dialog"
    assert component.children[0].type == "Card"


def test_modal_renders_content():
    html = render(modal(Text("Hello Modal"), open=True))

    assert "<dialog" in html
    assert "<div" in html
    assert "Hello Modal" in html
    assert " open" in html


def test_modal_supports_reactive_open_state():
    state = State(False)
    component = modal(Text("Reactive Modal"), open=state)

    assert " open" not in render(component)

    state.set(True)

    assert " open" in render(component)


def test_modal_supports_title():
    component = modal(Text("Message"), title=Text("Confirm"))
    html = render(component)

    assert "Confirm" in html
    assert "Message" in html


def test_modal_forwards_dialog_props():
    component = modal(
        Text("Message"),
        class_name="custom-modal",
    )

    assert component.props["class_name"] == "custom-modal"


def test_modal_supports_custom_style():
    component = modal(
        Text("Message"),
        style=Style(padding="32px"),
    )

    card_component = component.children[0]
    assert card_component.props["style"].padding == "32px"


def test_modal_preserves_component_content():
    content = Component("Text", children=["Child"])
    component = modal(content)

    card_component = component.children[0]
    assert card_component.children == [content]


def test_modal_is_publicly_exported():
    from pylage.UI.recipes import modal as exported_modal

    assert exported_modal is modal
