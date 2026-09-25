import pylage as pl
from pylage.ENGINE import State, Style
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render


def test_navigation_item_returns_existing_component():
    item = pl.navigation_item("Home")

    assert isinstance(item, Component)
    assert item.type == "Button"
    assert item.props["text"] == "Home"


def test_navigation_item_forwards_href():
    item = pl.navigation_item("Dashboard", href="/dashboard")

    assert item.type == "Link"
    assert item.props["href"] == "/dashboard"

    html = render(item)
    assert "<a " in html
    assert 'href="/dashboard"' in html


def test_navigation_item_default_contract():
    item = pl.navigation_item("Home")
    style = item.props["style"]

    assert style.display == "flex"
    assert style.align_items == "center"
    assert style.width == "100%"
    assert style.text_align == "left"
    assert style.background_color == "transparent"
    assert style.color == "var(--color-text)"
    assert style.border == "none"
    assert style.border_radius == "0.375rem"
    assert style.padding == "0.5rem 0.75rem"
    assert style.cursor == "pointer"


def test_navigation_item_active_style():
    item = pl.navigation_item("Home", active=True)
    style = item.props["style"]

    assert style.display == "flex"
    assert style.width == "100%"
    assert style.text_align == "left"
    assert style.background_color == "var(--color-primary)"
    assert style.color == "var(--color-primary-contrast)"
    assert style.border == "none"


def test_navigation_item_custom_style_overrides_defaults():
    item = pl.navigation_item("Home", style=Style(color="#123456", padding="1rem", border_radius="999px"))
    style = item.props["style"]

    assert style.color == "#123456"
    assert style.padding == "1rem"
    assert style.border_radius == "999px"
    assert style.cursor == "pointer"


def test_navigation_item_forwards_event_handler():
    called = []

    def clicked():
        called.append(True)

    item = pl.navigation_item("Home", on_click=clicked)

    assert item.events["click"] is clicked

    html = render(item)
    assert 'data-pylage-events="click"' in html
    assert "clicked" not in html


def test_navigation_item_does_not_leak_active_prop_to_engine():
    item = pl.navigation_item("Home", active=True)

    assert "active" not in item.props



def test_navigation_item_reactive_active_state():
    active = State(False)
    item = pl.navigation_item("Products", active=active)

    assert item.props["style"].background_color.value == "transparent"
    assert item.props["style"].color.value == "var(--color-text)"

    active.set(True)

    assert item.props["style"].background_color.value == "var(--color-primary)"
    assert item.props["style"].color.value == "var(--color-primary-contrast)"
    assert item.props["style"].border == "none"

    active.set(False)

    assert item.props["style"].background_color.value == "transparent"
    assert item.props["style"].color.value == "var(--color-text)"


def test_navigation_item_reactive_active_state_does_not_leak_prop():
    active = State(False)
    item = pl.navigation_item("Products", active=active)

    assert "active" not in item.props

    active.set(True)

    assert "active" not in item.props


def test_navigation_item_auto_active_from_current_path():
    current_path = State("/dashboard")
    item = pl.navigation_item(
        "Dashboard",
        href="/dashboard",
        current_path=current_path,
    )

    assert item.props["style"].background_color.value == "var(--color-primary)"
    assert item.props["style"].color.value == "var(--color-primary-contrast)"


def test_navigation_item_auto_active_updates_with_current_path():
    current_path = State("/dashboard")
    dashboard = pl.navigation_item(
        "Dashboard",
        href="/dashboard",
        current_path=current_path,
    )
    analytics = pl.navigation_item(
        "Analytics",
        href="/analytics",
        current_path=current_path,
    )

    assert dashboard.props["style"].background_color.value == "var(--color-primary)"
    assert analytics.props["style"].background_color.value == "transparent"

    current_path.set("/analytics")

    assert dashboard.props["style"].background_color.value == "transparent"
    assert analytics.props["style"].background_color.value == "var(--color-primary)"


def test_navigation_item_auto_active_cleans_up_derived_state():
    current_path = State("/dashboard")
    item = pl.navigation_item(
        "Dashboard",
        href="/dashboard",
        current_path=current_path,
    )

    derived = item.props["style"].background_color
    assert len(current_path._subscribers) == 1

    item.cleanup()

    assert len(current_path._subscribers) == 0
    assert derived.value == "var(--color-primary)"
