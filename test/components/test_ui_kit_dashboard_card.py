from pylage.ENGINE import Card, Style, Text
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_dashboard_card_returns_card():
    dc = ui.dashboard_card(title="System Status")
    assert dc.type == "Card"
    assert isinstance(dc, type(Card()))

def test_dashboard_card_renders_title_and_body():
    dc = ui.dashboard_card(
        title="Active Jobs",
        body="34 running, 2 queued",
        footer="Updated 1m ago",
    )
    html = render(dc)
    assert "Active Jobs" in html
    assert "34 running, 2 queued" in html
    assert "Updated 1m ago" in html

def test_dashboard_card_renders_action():
    btn = ui.button("Details", variant="ghost")
    dc = ui.dashboard_card(
        title="Alerts",
        action=btn,
    )
    html = render(dc)
    assert "Alerts" in html
    assert "Details" in html

def test_dashboard_card_custom_style_override():
    dc = ui.dashboard_card(
        title="Custom",
        style=Style(background_color="#f8fafc", padding="2rem"),
    )
    style = dc.props["style"]
    assert style.background_color == "#f8fafc"
    assert style.padding == "2rem"
