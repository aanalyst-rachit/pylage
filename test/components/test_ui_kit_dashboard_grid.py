from pylage.ENGINE import Grid, Card, Style, Text
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_dashboard_grid_returns_grid():
    dg = ui.dashboard_grid(Card(Text("Widget 1")))
    assert dg.type == "Grid"
    assert isinstance(dg, type(Grid()))

def test_dashboard_grid_renders_widgets():
    dg = ui.dashboard_grid(
        ui.card(heading="Sales Overview", body="12,000 units"),
        ui.card(heading="Traffic Sources", body="Direct: 40%"),
    )
    html = render(dg)
    assert "Sales Overview" in html
    assert "Traffic Sources" in html

def test_dashboard_grid_preset_layouts():
    dg_main_side = ui.dashboard_grid(layout="main-side")
    assert dg_main_side.props["style"].grid_template_columns == "2fr 1fr"

    dg_2col = ui.dashboard_grid(layout="2-col")
    assert dg_2col.props["style"].grid_template_columns == "repeat(2, minmax(0, 1fr))"

def test_dashboard_grid_custom_columns_and_gap():
    dg = ui.dashboard_grid(columns=3, gap="2rem")
    style = dg.props["style"]
    assert style.grid_template_columns == "repeat(3, minmax(0, 1fr))"
    assert style.gap == "2rem"

def test_dashboard_grid_custom_style_override():
    dg = ui.dashboard_grid(
        style=Style(padding="2rem", background_color="#f8fafc"),
    )
    style = dg.props["style"]
    assert style.padding == "2rem"
    assert style.background_color == "#f8fafc"

def test_dashboard_grid_forwards_engine_props():
    dg = ui.dashboard_grid(
        class_name="primary-dashboard-grid",
        id="main-dash-grid",
    )
    html = render(dg)
    assert 'id="main-dash-grid"' in html
    assert "primary-dashboard-grid" in html
