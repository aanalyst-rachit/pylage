from pylage.ENGINE import Column, Style, Badge
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_data_list_returns_column():
    dl = ui.data_list({"Status": "Active"})
    assert dl.type == "Column"
    assert isinstance(dl, type(Column()))

def test_data_list_renders_dict():
    data = {
        "User": "Alex Carter",
        "Role": "Administrator",
        "Plan": "Enterprise",
    }
    html = render(ui.data_list(data))
    assert "User" in html
    assert "Alex Carter" in html
    assert "Administrator" in html
    assert "Enterprise" in html

def test_data_list_renders_tuples():
    data = [
        ("Database", "PostgreSQL 16"),
        ("Region", "us-central1"),
    ]
    html = render(ui.data_list(data))
    assert "Database" in html
    assert "PostgreSQL 16" in html
    assert "us-central1" in html

def test_data_list_renders_list_of_mappings():
    data = [
        {"label": "CPU", "value": "4 Cores"},
        {"label": "Memory", "value": "16 GB"},
    ]
    html = render(ui.data_list(data))
    assert "CPU" in html
    assert "4 Cores" in html
    assert "Memory" in html
    assert "16 GB" in html

def test_data_list_vertical_orientation():
    dl = ui.data_list({"Server": "prod-api-1"}, orientation="vertical")
    child = dl.children[0]
    assert child.type == "Column"

def test_data_list_supports_components_as_values():
    badge = ui.badge("Active", variant="success")
    dl = ui.data_list({"Status": badge})
    html = render(dl)
    assert "Status" in html
    assert "Active" in html

def test_data_list_custom_style_override():
    dl = ui.data_list(
        {"Env": "Staging"},
        style=Style(background_color="#f8fafc", padding="2rem"),
    )
    style = dl.props["style"]
    assert style.background_color == "#f8fafc"
    assert style.padding == "2rem"

def test_data_list_forwards_engine_props():
    dl = ui.data_list(
        {"Version": "2.4.0"},
        class_name="app-specs-list",
        id="specs-list",
    )
    html = render(dl)
    assert 'id="specs-list"' in html
    assert "app-specs-list" in html
