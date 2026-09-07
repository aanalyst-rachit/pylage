from pylage.ENGINE import Grid, Style
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_metric_grid_returns_grid():
    mg = ui.metric_grid(
        ui.metric(label="Visits", value="1,000"),
    )
    assert mg.type == "Grid"
    assert isinstance(mg, type(Grid()))

def test_metric_grid_renders_metrics():
    mg = ui.metric_grid(
        ui.metric(label="Signups", value="500", delta="+10%"),
        ui.metric(label="Upgrades", value="40", delta="+2%"),
    )
    html = render(mg)
    assert "Signups" in html
    assert "500" in html
    assert "Upgrades" in html
    assert "40" in html

def test_metric_grid_with_items_and_columns():
    mg = ui.metric_grid(
        items=[
            {"label": "NPS Score", "value": "72"},
            {"label": "CSAT", "value": "98%"},
        ],
        columns=2,
    )
    html = render(mg)
    assert "NPS Score" in html
    assert "CSAT" in html
    assert mg.props["style"].grid_template_columns == "repeat(2, minmax(0, 1fr))"
