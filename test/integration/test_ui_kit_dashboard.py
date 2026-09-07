from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_dashboard_composition():
    dash = ui.dashboard(
        title="Executive Overview",
        metrics=[
            ui.metric(label="Revenue", value="$50,000", delta="+12%"),
            ui.metric(label="Customers", value="1,200", delta="+5%"),
        ],
        content=ui.card(heading="Performance Insights", body="Strong quarterly growth."),
        table=ui.table(
            [["APAC", "$30,000"], ["EMEA", "$20,000"]],
            headers=["Region", "Sales"],
        ),
    )
    html = render(dash)
    assert "Executive Overview" in html
    assert "Revenue" in html
    assert "$50,000" in html
    assert "Performance Insights" in html
    assert "APAC" in html
    assert "$30,000" in html

def test_dashboard_with_header_and_sidebar():
    header = ui.dashboard_header("Header Title")
    dash = ui.dashboard(
        header=header,
        sidebar=ui.card(body="Navigation Links"),
        content=ui.card(body="Main Dashboard Body"),
    )
    html = render(dash)
    assert "Header Title" in html
    assert "Navigation Links" in html
    assert "Main Dashboard Body" in html
