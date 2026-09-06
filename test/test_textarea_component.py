from pylage.ENGINE import State, Style
from pylage.ENGINE.core.registry import registry
from pylage.ENGINE.core.renderer import render
from pylage.UI import textarea


def test_textarea_creates_textarea_component():
    component = textarea("Hello PyLage")

    assert component.type == "Textarea"
    assert component.props["value"] == "Hello PyLage"


def test_textarea_renders_as_html_textarea():
    component = textarea("Hello PyLage")

    html = render(component)

    assert "<textarea" in html
    assert ">Hello PyLage</textarea>" in html


def test_textarea_escapes_html():
    component = textarea("<script>alert(1)</script>")

    html = render(component)

    assert "&lt;script&gt;" in html
    assert "<script>alert(1)</script>" not in html


def test_textarea_supports_common_props():
    component = textarea(
        "Message",
        placeholder="Write here",
        name="message",
        rows=5,
        cols=40,
        disabled=True,
        required=True,
        readonly=True,
        title="Message field",
        minlength=3,
        maxlength=500,
    )

    html = render(component)

    assert 'placeholder="Write here"' in html
    assert 'name="message"' in html
    assert 'rows="5"' in html
    assert 'cols="40"' in html
    assert "disabled" in html
    assert "required" in html
    assert "readonly" in html
    assert 'title="Message field"' in html
    assert 'minlength="3"' in html
    assert 'maxlength="500"' in html


def test_textarea_supports_style():
    style = Style(color="red")

    component = textarea(
        "Styled",
        style=style,
    )

    resolved = component.props["style"]
    assert resolved.color == "red"
    assert resolved.background_color == "var(--color-background)"
    assert resolved.border_radius == "var(--radius-md)"


def test_textarea_supports_state():
    state = State("Initial")

    component = textarea(state)

    assert component.props["value"] is state
    assert "Initial" in render(component)


def test_textarea_state_input_handler_updates_state():
    state = State("Initial")

    component = textarea(state)

    assert "input" in component.events

    component.events["input"]({"value": "Updated"})

    assert state.value == "Updated"


def test_textarea_custom_input_handler_is_preserved():
    calls = []

    def on_input(payload):
        calls.append(payload)

    component = textarea(
        "Initial",
        on_input=on_input,
    )

    component.events["input"]({"value": "Updated"})

    assert calls == [{"value": "Updated"}]


def test_textarea_registry_contract():
    definition = registry.get("Textarea")

    assert definition is not None
    assert definition.type == "Textarea"
    assert definition.tag == "textarea"
    assert definition.void is False
    assert definition.props is not None

    assert definition.props["value"].kind == "text"
    assert definition.props["placeholder"].kind == "attribute"
    assert definition.props["disabled"].kind == "boolean"
    assert definition.props["required"].kind == "boolean"
    assert definition.props["readonly"].kind == "boolean"
