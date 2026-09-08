from pylage.ENGINE import Row, Style, Button
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_dashboard_header_returns_row():
    dh = ui.dashboard_header("Overview")
    assert dh.type == "Row"
    assert isinstance(dh, type(Row()))

def test_dashboard_header_renders_title_and_description():
    dh = ui.dashboard_header(
        "Analytics Dashboard",
        "Real-time usage and platform statistics.",
    )
    html = render(dh)
    assert "Analytics Dashboard" in html
    assert "Real-time usage and platform statistics." in html

def test_dashboard_header_renders_actions():
    btn = ui.button("Download Report", variant="outline")
    dh = ui.dashboard_header(
        "Financial Report",
        actions=btn,
    )
    html = render(dh)
    assert "Financial Report" in html
    assert "Download Report" in html

def test_dashboard_header_renders_multiple_actions():
    btn1 = ui.button("Export CSV")
    btn2 = ui.button("Create Project", variant="primary")
    dh = ui.dashboard_header(
        "Projects",
        actions=[btn1, btn2],
    )
    html = render(dh)
    assert "Export CSV" in html
    assert "Create Project" in html

def test_dashboard_header_custom_style_override():
    dh = ui.dashboard_header(
        "Custom Header",
        style=Style(padding="2rem", background_color="#ffffff"),
    )
    style = dh.props["style"]
    assert style.padding == "2rem"
    assert style.background_color == "#ffffff"

def test_dashboard_header_forwards_engine_props():
    dh = ui.dashboard_header(
        "Dashboard",
        class_name="app-header-class",
        id="dash-header",
    )
    html = render(dh)
    assert 'id="dash-header"' in html
    assert "app-header-class" in html
