from pylage.ENGINE import Dialog, Text, Button, State
from pylage.ENGINE.core.renderer import render


def test_dialog_renders_as_dialog():
    dialog = Dialog()

    html = render(dialog)

    assert "<dialog" in html
    assert "</dialog>" in html


def test_dialog_renders_children():
    dialog = Dialog(
        Text("Hello Dialog"),
        Button("Close"),
    )

    html = render(dialog)

    assert "Hello Dialog" in html
    assert "Close" in html


def test_dialog_supports_props():
    dialog = Dialog(
        class_name="app-dialog",
        title="Confirmation",
    )

    html = render(dialog)

    assert 'class="app-dialog"' in html
    assert 'title="Confirmation"' in html


def test_dialog_supports_open_boolean():
    closed_dialog = Dialog(open=False)
    open_dialog = Dialog(open=True)

    closed_html = render(closed_dialog)
    open_html = render(open_dialog)

    assert " open" not in closed_html
    assert " open" in open_html


def test_dialog_supports_reactive_open_state():
    import pylage as ps
    open_state = State(False)
    dialog = Dialog(open=open_state)

    assert " open" not in render(dialog)

    open_state.set(True)
    assert " open" in render(dialog)
