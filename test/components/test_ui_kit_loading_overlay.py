from pylage.ENGINE import State, Style
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI import loading_overlay


def test_loading_overlay_wraps_existing_dialog():
    component = loading_overlay()

    assert isinstance(component, Component)
    assert component.type == "Dialog"


def test_loading_overlay_is_closed_by_default():
    html = render(loading_overlay())

    assert "<dialog" in html
    assert " open" not in html


def test_loading_overlay_supports_open_boolean():
    closed = loading_overlay(open=False)
    opened = loading_overlay(open=True)

    assert " open" not in render(closed)
    assert " open" in render(opened)


def test_loading_overlay_supports_reactive_open_state():
    state = State(False)
    component = loading_overlay(open=state)

    assert " open" not in render(component)

    state.set(True)

    assert " open" in render(component)

    state.set(False)

    assert " open" not in render(component)


def test_loading_overlay_renders_spinner_and_text():
    html = render(loading_overlay("Please wait...", open=True))

    assert "Please wait..." in html
    assert 'class="pylage-spinner"' in html
    assert "pylage-spinner-spin" in html


def test_loading_overlay_can_disable_spinner():
    component = loading_overlay("Loading", spinner=False)

    assert len(component.children) == 1
    content = component.children[0]
    assert content.type == "Column"
    assert len(content.children) == 1


def test_loading_overlay_has_full_viewport_style():
    component = loading_overlay(open=True)
    style = component.props["style"]

    assert style.position == "fixed"
    assert style.top == 0
    assert style.right == 0
    assert style.bottom == 0
    assert style.left == 0
    assert style.width == "100vw"
    assert style.height == "100vh"
    assert style.display is None
    assert style.border_radius == 0

    content = component.children[0]
    content_style = content.props["style"]
    assert content_style.width == "100vw"
    assert content_style.height == "100vh"
    assert content_style.display == "flex"
    assert content_style.align_items == "center"
    assert content_style.justify_content == "center"


def test_loading_overlay_supports_custom_style_override():
    component = loading_overlay(
        style=Style(z_index=2000, background_color="rgba(0, 0, 0, 0.7)")
    )

    style = component.props["style"]

    assert style.z_index == 2000
    assert style.background_color == "rgba(0, 0, 0, 0.7)"
    assert style.position == "fixed"


def test_loading_overlay_forwards_engine_props():
    component = loading_overlay(
        open=True,
        title="Loading overlay",
        class_name="custom-loading-overlay",
    )

    assert component.props["title"] == "Loading overlay"
    assert component.props["class_name"] == "custom-loading-overlay"


def test_loading_overlay_preserves_existing_column_content():
    component = loading_overlay("Working...")

    content = component.children[0]

    assert isinstance(content, Component)
    assert content.type == "Column"
    assert len(content.children) == 2


def test_loading_overlay_renders_dialog_content():
    html = render(loading_overlay("Working...", open=True))

    assert "<dialog" in html
    assert "Working..." in html
    assert "position:fixed" in html
    assert "width:100vw" in html
    assert "height:100vh" in html


def test_loading_overlay_is_publicly_exported():
    from pylage.UI.components import loading_overlay as component_loading_overlay

    assert component_loading_overlay is loading_overlay
