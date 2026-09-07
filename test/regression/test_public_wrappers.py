from pylage.ENGINE import State
from pylage.ENGINE.core.renderer import render
from pylage.UI import (
    checkbox,
    datepicker,
    form,
    input,
    select,
    slider,
    switch,
)
from pylage.ENGINE import Option


def test_public_input_wraps_engine_input():
    component = input(
        value="Rachit",
        placeholder="Name",
        input_type="email",
    )

    html = render(component)

    assert component.type == "Input"
    assert 'value="Rachit"' in html
    assert 'placeholder="Name"' in html
    assert 'type="email"' in html


def test_public_input_preserves_state_binding():
    state = State("initial")

    component = input(value=state)

    assert component.type == "Input"
    assert component.props["value"] is state
    assert "input" in component.events


def test_public_select_wraps_engine_select():
    component = select(
        Option("India", value="in"),
        Option("USA", value="us"),
        value="in",
    )

    html = render(component)

    assert component.type == "Select"
    assert "India" in html
    assert "USA" in html
    assert 'value="in"' in html


def test_public_checkbox_wraps_engine_checkbox():
    component = checkbox(
        name="terms",
        checked=True,
    )

    html = render(component)

    assert component.type == "Checkbox"
    assert 'name="terms"' in html
    assert "checked" in html


def test_public_switch_wraps_engine_switch():
    component = switch(
        name="notifications",
        checked=True,
    )

    html = render(component)

    assert component.type == "Switch"
    assert 'name="notifications"' in html
    assert "checked" in html


def test_public_slider_wraps_engine_slider():
    state = State(50)

    component = slider(
        value=state,
        min=0,
        max=100,
        step=5,
    )

    assert component.type == "Slider"
    assert component.props["value"] is state
    assert "input" in component.events

    html = render(component)

    assert 'min="0"' in html
    assert 'max="100"' in html
    assert 'step="5"' in html


def test_public_datepicker_wraps_engine_datepicker():
    state = State("2026-09-03")

    component = datepicker(
        value=state,
    )

    assert component.type == "DatePicker"
    assert component.props["value"] is state
    assert "input" in component.events

    html = render(component)

    assert 'type="date"' in html


def test_public_form_wraps_engine_form():
    component = form(
        input(name="email"),
        checkbox(name="terms"),
        method="post",
        action="/submit",
    )

    html = render(component)

    assert component.type == "Form"
    assert "<form" in html
    assert "</form>" in html
    assert 'method="post"' in html
    assert 'action="/submit"' in html
    assert "<input" in html


def test_public_form_preserves_submit_event():
    received = []

    def on_submit(payload):
        received.append(payload)
        return "submitted"

    component = form(on_submit=on_submit)

    html = render(component)

    assert 'data-pylage-events="submit"' in html
    assert "submit" in component.events
