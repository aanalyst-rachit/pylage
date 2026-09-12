from pylage.ENGINE import Select, Text, Button, Option, State
from pylage.ENGINE.core.renderer import render


def test_select_renders_as_select():
    select = Select()

    html = render(select)

    assert "<select" in html
    assert "</select>" in html


def test_select_renders_children():
    select = Select(
        Text("Option A"),
        Button("Option B"),
    )

    html = render(select)

    assert "Option A" in html
    assert "Option B" in html


def test_select_supports_props():
    select = Select(
        class_name="country-select",
        title="Choose country",
    )

    html = render(select)

    assert 'class="country-select"' in html
    assert 'title="Choose country"' in html


def test_select_value_state_updates_from_change_event():
    selected = State("india")
    select = Select(
        Option("India", value="india"),
        Option("Japan", value="japan"),
        value=selected,
    )

    assert "change" in select.events

    select.events["change"]({
        "value": "japan",
        "selectedIndex": 1,
    })

    assert selected.value == "japan"


def test_select_value_state_preserves_custom_change_callback():
    selected = State("india")
    received = []

    select = Select(
        Option("India", value="india"),
        Option("Japan", value="japan"),
        value=selected,
        on_change=received.append,
    )

    payload = {
        "value": "japan",
        "selectedIndex": 1,
    }
    select.events["change"](payload)

    assert selected.value == "japan"
    assert received == [payload]
