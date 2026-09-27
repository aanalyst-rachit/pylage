import pylage as pl


def test_drawer_is_publicly_available():
    assert callable(pl.drawer)


def test_navigation_drawer_is_publicly_available():
    assert callable(pl.navigation_drawer)


def test_mobile_sidebar_is_publicly_available():
    assert callable(pl.mobile_sidebar)


def test_drawer_creates_drawer_component():
    component = pl.drawer(pl.text("Navigation"))

    assert component.type == "Drawer"


def test_navigation_drawer_creates_drawer_component():
    component = pl.navigation_drawer(pl.text("Navigation"))

    assert component.type == "Drawer"


def test_mobile_sidebar_creates_drawer_component():
    component = pl.mobile_sidebar(pl.text("Mobile"))

    assert component.type == "Drawer"


def test_drawer_accepts_public_navigation_item():
    component = pl.drawer(
        pl.navigation_item("Dashboard", href="/dashboard"),
    )

    assert component.type == "Drawer"


def test_drawer_accepts_public_open_boolean():
    closed = pl.drawer(open=False)
    opened = pl.drawer(open=True)

    assert closed.props["open"] is False
    assert opened.props["open"] is True


def test_drawer_accepts_public_reactive_open_state():
    open_state = pl.state(False)
    component = pl.drawer(open=open_state)

    assert component.props["open"] is open_state

    open_state.set(True)

    assert open_state.value is True


def test_drawer_accepts_public_style():
    style = pl.style(width="280px")
    component = pl.drawer(style=style)

    assert component.props["style"] is style


def test_drawer_accepts_public_modal_prop():
    component = pl.drawer(modal=False)
    assert component.props["modal"] is False


def test_drawer_forwards_public_props():
    component = pl.drawer(
        class_name="custom-drawer",
        title="Navigation drawer",
    )

    assert component.props["class_name"] == "custom-drawer"
    assert component.props["title"] == "Navigation drawer"


def test_drawer_variants_accept_public_children():
    children = (
        pl.text("Navigation"),
        pl.navigation_item("Dashboard", href="/dashboard"),
        pl.navigation_item("Settings", href="/settings"),
    )

    assert pl.drawer(*children).type == "Drawer"
    assert pl.navigation_drawer(*children).type == "Drawer"
    assert pl.mobile_sidebar(*children).type == "Drawer"


def test_drawer_public_api_boundaries_are_stable():
    import pylage.UI.layout as layout
    import pylage.UI.layout.drawer as layout_drawer

    assert {"drawer", "navigation_drawer", "mobile_sidebar"} <= set(pl.__all__)

    assert callable(pl.drawer)
    assert callable(pl.navigation_drawer)
    assert callable(pl.mobile_sidebar)

    assert not hasattr(layout, "Drawer")
    assert not hasattr(layout, "NavigationDrawer")
    assert not hasattr(layout, "MobileSidebar")

    assert set(layout_drawer.__all__) == {
        "Drawer",
        "NavigationDrawer",
        "MobileSidebar",
    }
