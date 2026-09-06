from pylage.ENGINE import Divider as EngineDivider
from pylage.ENGINE import Style
from pylage.ENGINE.core.renderer import render

import pylage.UI as ui


def test_divider_returns_existing_divider_component():
    divider = ui.divider()

    assert divider.type == "Divider"
    assert isinstance(divider, type(EngineDivider()))


def test_divider_default_contract():
    divider = ui.divider()

    style = divider.props["style"]

    assert style.width == "100%"
    assert style.border == "0"
    assert style.border_top == "1px solid #e2e8f0"
    assert style.margin == "1rem 0"


def test_divider_renders_as_hr():
    html = render(ui.divider())

    assert "<hr " in html
    assert "</hr>" not in html


def test_divider_custom_style_overrides_defaults():
    divider = ui.divider(
        style=Style(
            width="50%",
            border_top="2px solid #111827",
            margin="2rem 0",
        )
    )

    style = divider.props["style"]

    assert style.width == "50%"
    assert style.border_top == "2px solid #111827"
    assert style.margin == "2rem 0"
    assert style.border == "0"


def test_divider_forwards_engine_props():
    divider = ui.divider(
        class_name="section-divider",
        title="Section divider",
    )

    html = render(divider)

    assert 'class="section-divider"' in html
    assert 'title="Section divider"' in html


def test_divider_forwards_events():
    clicked = []

    def on_click():
        clicked.append(True)

    divider = ui.divider(on_click=on_click)

    assert "click" in divider.events
    assert 'data-pylage-events="click"' in render(divider)
