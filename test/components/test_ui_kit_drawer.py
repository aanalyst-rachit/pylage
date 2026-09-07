from pylage.ENGINE import State, Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.recipes.drawer import drawer


def test_drawer_returns_component():
    component = drawer(Text("Navigation"))
    assert isinstance(component, Component)
    assert component.type == "Drawer"


def test_drawer_renders_aside():
    html = render(drawer(Text("Navigation")))
    assert "<aside" in html
    assert "Navigation" in html


def test_drawer_supports_open_boolean():
    closed_html = render(drawer(open=False))
    open_html = render(drawer(open=True))

    assert " open" not in closed_html
    assert " open" in open_html


def test_drawer_supports_reactive_open_state():
    state = State(False)
    component = drawer(open=state)

    assert " open" not in render(component)

    state.set(True)

    assert " open" in render(component)


def test_drawer_forwards_props():
    component = drawer(
        Text("Navigation"),
        class_name="custom-drawer",
        title="Navigation drawer",
    )

    html = render(component)

    assert 'class="pylage-drawer custom-drawer"' in html
    assert 'title="Navigation drawer"' in html


def test_drawer_supports_style():
    component = drawer(
        Text("Navigation"),
        style=Style(width="280px"),
    )

    assert component.props["style"].width == "280px"


def test_drawer_is_publicly_exported():
    from pylage.UI.recipes import drawer as exported_drawer

    assert exported_drawer is drawer


def test_drawer_is_available_from_pylage():
    import pylage as pl

    assert hasattr(pl, "drawer")
    assert pl.drawer is drawer


def test_navigation_drawer_is_publicly_exported():
    from pylage.UI.recipes import navigation_drawer

    assert callable(navigation_drawer)


def test_mobile_sidebar_is_publicly_exported():
    from pylage.UI.recipes import mobile_sidebar

    assert callable(mobile_sidebar)


def test_navigation_drawer_reuses_existing_drawer():
    from pylage.UI.layout.drawer import NavigationDrawer
    from pylage.UI.recipes import navigation_drawer

    assert navigation_drawer(Text("Navigation")).type == "Drawer"
    assert NavigationDrawer(Text("Navigation")).type == "Drawer"


def test_mobile_sidebar_reuses_existing_drawer():
    from pylage.UI.layout.drawer import MobileSidebar
    from pylage.UI.recipes import mobile_sidebar

    assert mobile_sidebar(Text("Mobile")).type == "Drawer"
    assert MobileSidebar(Text("Mobile")).type == "Drawer"


def test_navigation_and_mobile_are_available_from_pylage():
    import pylage as pl

    assert hasattr(pl, "navigation_drawer")
    assert hasattr(pl, "mobile_sidebar")
