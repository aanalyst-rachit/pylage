from pylage.ENGINE import Grid, Style
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_stat_group_returns_grid():
    sg = ui.stat_group(
        ui.metric(label="Users", value="1,200"),
    )
    assert sg.type == "Grid"
    assert isinstance(sg, type(Grid()))

def test_stat_group_renders_metrics():
    sg = ui.stat_group(
        ui.metric(label="Revenue", value="₹85,000", delta="+14%"),
        ui.metric(label="Signups", value="430", delta="+8%"),
    )
    html = render(sg)
    assert "Revenue" in html
    assert "₹85,000" in html
    assert "Signups" in html
    assert "430" in html

def test_stat_group_accepts_mappings():
    sg = ui.stat_group(
        items=[
            {"label": "MRR", "value": "$12,400", "delta": "+5%"},
            {"label": "Churn", "value": "1.2%", "delta": "-0.4%"},
        ]
    )
    html = render(sg)
    assert "MRR" in html
    assert "$12,400" in html
    assert "Churn" in html
    assert "1.2%" in html

def test_stat_group_accepts_tuples():
    sg = ui.stat_group(
        ("Active Nodes", "32"),
        ("Avg Latency", "18ms", "-4ms"),
    )
    html = render(sg)
    assert "Active Nodes" in html
    assert "32" in html
    assert "Avg Latency" in html
    assert "18ms" in html

def test_stat_group_column_formatting():
    sg_int = ui.stat_group(columns=4)
    assert sg_int.props["style"].grid_template_columns == "repeat(4, minmax(0, 1fr))"

    sg_custom = ui.stat_group(columns="1fr 2fr 1fr")
    assert sg_custom.props["style"].grid_template_columns == "1fr 2fr 1fr"

def test_stat_group_forwards_engine_props():
    sg = ui.stat_group(
        class_name="kpi-group",
        id="dashboard-kpis",
    )
    html = render(sg)
    assert 'id="dashboard-kpis"' in html
    assert "kpi-group" in html
