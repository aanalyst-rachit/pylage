from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI import confirmation_dialog


def test_confirmation_dialog_wraps_existing_dialog():
    component = confirmation_dialog(Text("Are you sure?"))
    assert isinstance(component, Component)
    assert component.type == "Dialog"


def test_confirmation_dialog_renders_message_and_actions():
    component = confirmation_dialog(
        Text("Delete this item?"),
        confirm_text="Delete",
        cancel_text="Keep",
    )
    html = render(component)

    assert "<dialog" in html
    assert "Delete this item?" in html
    assert "Delete" in html
    assert "Keep" in html


def test_confirmation_dialog_supports_title():
    component = confirmation_dialog(
        Text("This action cannot be undone."),
        title=Text("Delete Item"),
    )
    html = render(component)

    assert "Delete Item" in html
    assert "This action cannot be undone." in html


def test_confirmation_dialog_supports_reactive_open_state():
    state = State(False)
    component = confirmation_dialog(Text("Confirm"), open=state)

    assert " open" not in render(component)

    state.set(True)

    assert " open" in render(component)


def test_confirmation_dialog_forwards_callbacks():
    confirmed = []
    cancelled = []

    def on_confirm(event=None):
        confirmed.append(True)

    def on_cancel(event=None):
        cancelled.append(True)

    component = confirmation_dialog(
        Text("Confirm action"),
        on_confirm=on_confirm,
        on_cancel=on_cancel,
    )

    actions = component.children[-1]
    cancel_button = actions.children[0]
    confirm_button = actions.children[1]

    assert cancel_button.events["click"] is on_cancel
    assert confirm_button.events["click"] is on_confirm


def test_confirmation_dialog_supports_confirm_variant():
    component = confirmation_dialog(
        Text("Delete item?"),
        confirm_variant="danger",
    )
    confirm_button = component.children[-1].children[1]

    style = confirm_button.props["style"]
    assert style.background_color is not None


def test_confirmation_dialog_supports_custom_style():
    component = confirmation_dialog(
        Text("Confirm"),
        style=Style(padding="32px"),
    )

    assert component.props["style"].padding == "32px"


def test_confirmation_dialog_is_publicly_exported():
    from pylage.UI.recipes import confirmation_dialog as exported

    assert exported is confirmation_dialog
