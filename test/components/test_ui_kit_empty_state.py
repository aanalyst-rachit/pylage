from pylage.ENGINE import Column, Style, Text, Button
from pylage.ENGINE.core.renderer import render
import pylage.UI as ui

def test_empty_state_returns_column():
    es = ui.empty_state()
    assert es.type == "Column"
    assert isinstance(es, type(Column()))

def test_empty_state_default_content():
    html = render(ui.empty_state())
    assert "No data found" in html
    assert "There are no items or records to display" in html

def test_empty_state_custom_content():
    es = ui.empty_state(
        title="Inbox Zero",
        description="All pending tasks have been completed.",
    )
    html = render(es)
    assert "Inbox Zero" in html
    assert "All pending tasks have been completed." in html

def test_empty_state_supports_icon():
    html = render(ui.empty_state(
        title="No Orders",
        description="You have not placed any orders yet.",
        icon="📦",
    ))
    assert "📦" in html
    assert "No Orders" in html

def test_empty_state_supports_action():
    btn = ui.button("Create project", variant="primary")
    es = ui.empty_state(
        title="No projects",
        description="Get started by creating a new project.",
        action=btn,
    )
    html = render(es)
    assert "No projects" in html
    assert "Create project" in html

def test_empty_state_custom_style_override():
    es = ui.empty_state(
        style=Style(padding="3rem", background_color="#f8fafc"),
    )
    style = es.props["style"]
    assert style.padding == "3rem"
    assert style.background_color == "#f8fafc"

def test_empty_state_forwards_engine_props():
    es = ui.empty_state(
        class_name="custom-empty-state",
        title="Empty",
        id="empty-state-1",
    )
    html = render(es)
    assert 'id="empty-state-1"' in html
    assert "custom-empty-state" in html
