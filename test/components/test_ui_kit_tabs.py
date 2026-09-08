from pylage.ENGINE import Tabs, Text, Button, State
from pylage.ENGINE.core.renderer import render


def test_tabs_renders():
    tabs = Tabs(
        Text("Home"),
        Button("Profile"),
    )

    html = render(tabs)

    assert "<div" in html
    assert "Home" in html
    assert "Profile" in html


def test_tabs_supports_props():
    tabs = Tabs(
        class_name="main-tabs",
        title="Sections",
    )

    html = render(tabs)

    assert 'class="main-tabs"' in html
    assert 'title="Sections"' in html


def test_tabs_supports_value_and_reactivity():
    import pylage as ps
    tab_state = State("profile")
    tabs = Tabs(value=tab_state)

    assert 'value="profile"' in render(tabs)

    tab_state.set("settings")
    assert 'value="settings"' in render(tabs)


def test_tabs_is_exported():
    assert callable(Tabs)
