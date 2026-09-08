from pylage.ENGINE import State, Style
from pylage.ENGINE.core.renderer import render
from pylage.UI import heading


def test_heading_wraps_existing_heading_component():
    component = heading("Dashboard")

    assert component.type == "Heading"
    assert component.props["text"] == "Dashboard"


def test_heading_renders_existing_h1_contract():
    html = render(heading("Dashboard"))

    assert "<h1" in html
    assert "Dashboard" in html


def test_heading_preserves_reactive_state():
    state = State("Initial")
    component = heading(state)

    assert component.props["text"] is state
    assert "Initial" in render(component)


def test_heading_supports_custom_style():
    component = heading(
        "Revenue",
        style=Style(
            font_size="2rem",
            font_weight="700",
        ),
    )

    style = component.props["style"]

    assert style.font_size == "2rem"
    assert style.font_weight == "700"


def test_heading_forwards_event_handler():
    called = []

    def clicked():
        called.append(True)

    component = heading("Click", on_click=clicked)

    assert component.events["click"] is clicked
