from pylage.ENGINE import State, Style
from pylage.ENGINE.core.renderer import render
from pylage.UI import text


def test_text_wraps_existing_text_component():
    component = text("Hello")

    assert component.type == "Text"
    assert component.props["text"] == "Hello"


def test_text_renders_value():
    html = render(text("Hello PyLage"))

    assert "<div" in html
    assert "Hello PyLage" in html


def test_text_preserves_reactive_state():
    state = State("Initial")
    component = text(state)

    assert component.props["text"] is state
    assert "Initial" in render(component)


def test_text_supports_muted_style():
    component = text("Secondary", muted=True)

    assert component.props["style"].color == "var(--color-text-muted)"


def test_text_supports_label_style():
    component = text("Email", label=True)
    style = component.props["style"]

    assert style.font_size == "0.875rem"
    assert style.font_weight == "500"


def test_text_supports_caption_style():
    component = text("Updated recently", caption=True)
    style = component.props["style"]

    assert style.font_size == "0.75rem"
    assert style.color == "var(--color-text-muted)"


def test_text_custom_style_overrides_semantic_style():
    component = text(
        "Custom",
        muted=True,
        style=Style(
            color="#ff0000",
            font_size="2rem",
        ),
    )

    style = component.props["style"]

    assert style.color == "#ff0000"
    assert style.font_size == "2rem"


def test_text_does_not_leak_semantic_flags_to_component_props():
    component = text(
        "Metadata",
        muted=True,
        label=True,
        caption=True,
    )

    assert "muted" not in component.props
    assert "label" not in component.props
    assert "caption" not in component.props


def test_text_forwards_event_handler():
    called = []

    def clicked():
        called.append(True)

    component = text("Click", on_click=clicked)

    assert component.events["click"] is clicked
