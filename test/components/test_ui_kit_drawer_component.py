from pylage.ENGINE import Drawer, Text, Button, State
from pylage.ENGINE.core.renderer import render


def test_drawer_renders_as_aside():
    drawer = Drawer(
        Text("Navigation"),
        Button(text="Home"),
    )

    html = render(drawer)

    assert "<aside" in html


def test_drawer_supports_props():
    drawer = Drawer(
        class_name="sidebar",
        title="Navigation drawer",
    )

    html = render(drawer)

    assert 'class="pylage-drawer sidebar"' in html
    assert 'title="Navigation drawer"' in html


def test_drawer_renders_children():
    drawer = Drawer(
        Text("Dashboard"),
        Button(text="Settings"),
    )

    html = render(drawer)

    assert "Dashboard" in html
    assert "Settings" in html


def test_drawer_supports_open_boolean():
    closed_drawer = Drawer(open=False)
    open_drawer = Drawer(open=True)

    closed_html = render(closed_drawer)
    open_html = render(open_drawer)

    assert " open" not in closed_html
    assert " open" in open_html


def test_drawer_supports_reactive_open_state():
    import pylage as ps
    open_state = State(False)
    drawer = Drawer(open=open_state)

    assert " open" not in render(drawer)

    open_state.set(True)
    assert " open" in render(drawer)

def test_drawer_is_hidden_when_closed():
    drawer = Drawer(open=False)
    html = render(drawer)

    assert 'class="pylage-drawer"' in html
    assert "transform: translateX(-100%)" in html
    assert "visibility: hidden" in html


def test_drawer_is_visible_when_open():
    drawer = Drawer(open=True)
    html = render(drawer)

    assert 'class="pylage-drawer"' in html
    assert 'open' in html
    assert "transform: translateX(0)" in html


def test_drawer_has_fixed_off_canvas_positioning():
    drawer = Drawer()
    html = render(drawer)

    assert "position: fixed" in html
    assert "top: 0" in html
    assert "left: 0" in html
    assert "height: 100vh" in html
    assert "z-index: 1000" in html


def test_drawer_preserves_custom_class_and_title():
    drawer = Drawer(
        class_name="my-drawer",
        title="Navigation",
    )
    html = render(drawer)

    assert 'class="pylage-drawer my-drawer"' in html
    assert 'title="Navigation"' in html
