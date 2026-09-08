from pylage.ENGINE import Column, Style, Button
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_error_state_returns_column():
    es = ui.error_state()
    assert es.type == "Column"
    assert isinstance(es, type(Column()))

def test_error_state_default_content():
    html = render(ui.error_state())
    assert "Something went wrong" in html
    assert "An error occurred" in html
    assert "⚠️" in html

def test_error_state_custom_content():
    es = ui.error_state(
        title="Failed to load dashboard",
        description="Network connection timed out.",
        icon="❌",
    )
    html = render(es)
    assert "Failed to load dashboard" in html
    assert "Network connection timed out." in html
    assert "❌" in html

def test_error_state_supports_action():
    retry_btn = ui.button("Retry request", variant="danger")
    es = ui.error_state(
        title="Server unreachable",
        action=retry_btn,
    )
    html = render(es)
    assert "Server unreachable" in html
    assert "Retry request" in html

def test_error_state_custom_style_override():
    es = ui.error_state(
        style=Style(padding="3.5rem", background_color="#fff5f5"),
    )
    style = es.props["style"]
    assert style.padding == "3.5rem"
    assert style.background_color == "#fff5f5"

def test_error_state_forwards_engine_props():
    es = ui.error_state(
        class_name="error-boundary-card",
        id="error-view",
    )
    html = render(es)
    assert 'id="error-view"' in html
    assert "error-boundary-card" in html
