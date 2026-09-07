from pylage.ENGINE import Accordion, Text, Button, State
from pylage.ENGINE.core.renderer import render


def test_accordion_creates_accordion_component():
    accordion = Accordion()

    assert accordion.type == "Accordion"


def test_accordion_supports_children():
    accordion = Accordion(
        Text("Content"),
        Button("Action"),
    )

    html = render(accordion)

    assert "Content" in html
    assert "Action" in html


def test_accordion_supports_props():
    accordion = Accordion(
        class_name="faq-accordion",
        title="FAQ",
    )

    html = render(accordion)

    assert 'class="faq-accordion"' in html
    assert 'title="FAQ"' in html


def test_accordion_supports_value_and_reactivity():
    import pylage as ps
    sec_state = State("sec_1")
    accordion = Accordion(value=sec_state)

    assert 'value="sec_1"' in render(accordion)

    sec_state.set("sec_2")
    assert 'value="sec_2"' in render(accordion)
