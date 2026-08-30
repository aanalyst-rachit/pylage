from pyskin import Text
from pyskin.core.renderer import render


def test_text_creates_text_component():
    text = Text("Hello PySkin")

    assert text.type == "Text"
    assert text.props["text"] == "Hello PySkin"


def test_text_renders_as_plain_text():
    text = Text("Hello PySkin")

    html = render(text)

    assert "Hello PySkin" in html
    assert "<div" in html


def test_text_escapes_html():
    text = Text("<script>alert(1)</script>")

    html = render(text)

    assert "&lt;script&gt;" in html
    assert "<script>" not in html


def test_text_supports_state():
    from pyskin import State

    state = State("Initial")
    text = Text(state)

    assert text.props["text"] is state
    assert "Initial" in render(text)
