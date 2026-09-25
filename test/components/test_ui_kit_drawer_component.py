from pylage.ENGINE import Button, Drawer, State, Text
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


def test_drawer_backdrop_supports_on_dismiss_event():
    drawer = Drawer(on_dismiss=lambda: None)
    html = render(drawer)
    backdrop, aside = html.split("<aside", 1)
    assert "class=\"pylage-drawer-backdrop\"" in backdrop
    assert "data-pylage-events=\"dismiss\"" in backdrop
    assert "data-pylage-events=\"dismiss\"" not in aside


def test_drawer_has_backdrop_when_closed():
    html = render(Drawer(open=False))
    assert "pylage-drawer-backdrop" in html
    assert "visibility: hidden" in html


def test_drawer_has_backdrop_when_open():
    html = render(Drawer(open=True))
    assert "pylage-drawer-backdrop" in html
    assert "visibility: visible" in html
    assert "z-index: 999" in html


def test_drawer_is_visible_when_open():
    drawer = Drawer(open=True)
    html = render(drawer)

    assert 'class="pylage-drawer"' in html
    assert 'open' in html
    assert "transform: translate(0, 0)" in html


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

def test_drawer_defaults_to_left_position():
    html = render(Drawer())

    assert 'data-pylage-position="left"' in html
    assert 'transform: translateX(-100%)' in html


def test_drawer_supports_right_position():
    html = render(Drawer(position="right"))

    assert 'data-pylage-position="right"' in html
    assert 'transform: translateX(100%)' in html


def test_drawer_supports_top_position():
    html = render(Drawer(position="top"))

    assert 'data-pylage-position="top"' in html
    assert 'transform: translateY(-100%)' in html


def test_drawer_supports_bottom_position():
    html = render(Drawer(position="bottom"))

    assert 'data-pylage-position="bottom"' in html
    assert 'transform: translateY(100%)' in html


def test_drawer_open_state_resets_position_transform():
    for position in ("left", "right", "top", "bottom"):
        html = render(Drawer(position=position, open=True))

        assert 'data-pylage-position="' + position + '"' in html
        assert "transform: translate(0, 0)" in html


def test_drawer_rejects_invalid_position():
    try:
        render(Drawer(position="center"))
    except ValueError as exc:
        assert str(exc) == (
            "Drawer position must be one of: left, right, top, bottom"
        )
    else:
        raise AssertionError("invalid Drawer position was accepted")
