from pylage.ENGINE import Column, Style, State
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_loading_state_returns_column():
    ls = ui.loading_state()
    assert ls.type == "Column"
    assert isinstance(ls, type(Column()))

def test_loading_state_default_style_contract():
    ls = ui.loading_state()
    style = ls.props["style"]
    assert style.padding == "var(--spacing-2xl)"
    assert style.background_color == "var(--color-background)"
    assert style.border_radius == "var(--radius-xl)"


def test_loading_state_default_content():
    html = render(ui.loading_state())
    assert "Loading..." in html
    assert "Spinner" in str([c.type for c in ui.loading_state().children])

def test_loading_state_custom_text_and_description():
    ls = ui.loading_state(
        text="Processing transaction...",
        description="This might take a few seconds.",
    )
    html = render(ls)
    assert "Processing transaction..." in html
    assert "This might take a few seconds." in html

def test_loading_state_supports_reactive_state():
    status = State("Connecting to server...")
    ls = ui.loading_state(text=status)
    html = render(ls)
    assert "Connecting to server..." in html

def test_loading_state_can_disable_spinner():
    ls = ui.loading_state(text="Syncing...", spinner=False)
    types = [c.type for c in ls.children]
    assert "Spinner" not in types

def test_loading_state_custom_style_override():
    ls = ui.loading_state(
        style=Style(padding="4rem", background_color="#f1f5f9"),
    )
    style = ls.props["style"]
    assert style.padding == "4rem"
    assert style.background_color == "#f1f5f9"

def test_loading_state_forwards_engine_props():
    ls = ui.loading_state(
        class_name="custom-loading-class",
        id="loader-1",
    )
    html = render(ls)
    assert 'id="loader-1"' in html
    assert "custom-loading-class" in html
