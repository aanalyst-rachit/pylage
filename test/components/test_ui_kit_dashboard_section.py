from pylage.ENGINE import Column, Card, Style, Text
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_dashboard_section_returns_column():
    ds = ui.dashboard_section(title="Performance")
    assert ds.type == "Column"
    assert isinstance(ds, type(Column()))

def test_dashboard_section_renders_header_and_children():
    ds = ui.dashboard_section(
        Card(Text("Chart content")),
        title="Revenue Trends",
        description="Weekly breakdown of subscription and license sales.",
    )
    html = render(ds)
    assert "Revenue Trends" in html
    assert "Weekly breakdown" in html
    assert "Chart content" in html

def test_dashboard_section_renders_action():
    view_all_btn = ui.button("View All", variant="ghost")
    ds = ui.dashboard_section(
        title="Recent Transactions",
        action=view_all_btn,
    )
    html = render(ds)
    assert "Recent Transactions" in html
    assert "View All" in html

def test_dashboard_section_custom_style_override():
    ds = ui.dashboard_section(
        title="Custom",
        style=Style(padding="1.5rem", background_color="#f8fafc"),
    )
    style = ds.props["style"]
    assert style.padding == "1.5rem"
    assert style.background_color == "#f8fafc"

def test_dashboard_section_forwards_engine_props():
    ds = ui.dashboard_section(
        title="Secured Section",
        class_name="dash-section-wrapper",
        id="section-sec",
    )
    html = render(ds)
    assert 'id="section-sec"' in html
    assert "dash-section-wrapper" in html
