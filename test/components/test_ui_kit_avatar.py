from pylage.ENGINE import Image, Style, State
from pylage.ENGINE.core.renderer import render
import pylage.UI as ps


def test_avatar_returns_existing_avatar_component():
    avatar = ps.avatar("RK")
    assert avatar.type == "Avatar"


def test_avatar_renders_primitive_content():
    html = render(ps.avatar("RK"))
    assert "RK" in html


def test_avatar_default_style_contract():
    avatar = ps.avatar("RK")
    style = avatar.props["style"]
    assert style.width == "40px"
    assert style.height == "40px"
    assert style.border_radius == "9999px"
    assert style.display == "inline-flex"
    assert style.align_items == "center"
    assert style.justify_content == "center"


def test_avatar_supports_sizes():
    assert ps.avatar("S", size="sm").props["style"].width == "32px"
    assert ps.avatar("M", size="md").props["style"].width == "40px"
    assert ps.avatar("L", size="lg").props["style"].width == "48px"


def test_avatar_rejects_invalid_size():
    try:
        ps.avatar("X", size="xl")
    except ValueError as exc:
        assert "Unknown avatar size" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_avatar_supports_image_component():
    avatar = ps.avatar(Image(src="avatar.png", alt="Rachit"))
    html = render(avatar)
    assert "avatar.png" in html
    assert "Rachit" in html


def test_avatar_supports_reactive_content():
    state = State("RK")
    html = render(ps.avatar(state))
    assert "RK" in html


def test_avatar_custom_style_overrides_defaults():
    avatar = ps.avatar("RK", style=Style(width="56px"))
    assert avatar.props["style"].width == "56px"


def test_avatar_forwards_props_and_events():
    def handle_click(event=None):
        pass

    avatar = ps.avatar("RK", title="Profile", on_click=handle_click)
    assert avatar.props["title"] == "Profile"
    assert avatar.events["click"] is handle_click


def test_avatar_does_not_leak_size_prop():
    avatar = ps.avatar("RK", size="sm")
    assert "size" not in avatar.props
