import pylage as pl

from pylage.ENGINE import Breadcrumbs, Button, Text
from pylage.ENGINE.core.renderer import render


def test_breadcrumbs_renders_as_nav():
    breadcrumbs = Breadcrumbs(
        Text("Home"),
        Text("Products"),
        Text("Details"),
    )

    html = render(breadcrumbs)

    assert "<nav" in html


def test_breadcrumbs_supports_props():
    breadcrumbs = Breadcrumbs(
        class_name="breadcrumbs",
        title="Page navigation",
    )

    html = render(breadcrumbs)

    assert 'class="breadcrumbs"' in html
    assert 'title="Page navigation"' in html


def test_breadcrumbs_renders_children():
    breadcrumbs = Breadcrumbs(
        Text("Home"),
        Button(text="Products"),
    )

    html = render(breadcrumbs)

    assert "Home" in html
    assert "Products" in html


def test_breadcrumb_trail_accepts_route_items():
    from pylage.UI.patterns.breadcrumbs import breadcrumb_trail

    breadcrumbs = breadcrumb_trail(
        Text("Home"),
        Text("Dashboard"),
    )

    html = render(breadcrumbs)

    assert '<nav' in html
    assert '<ol>' in html
    assert "Home" in html
    assert "Dashboard" in html


def test_breadcrumb_trail_reacts_to_current_path():
    from pylage.ENGINE.core.state import State
    from pylage.UI.patterns.breadcrumbs import breadcrumb_trail

    current_path = State("/dashboard/reports")
    breadcrumbs = breadcrumb_trail(current_path=current_path)

    assert "Home" in render(breadcrumbs)
    assert "Dashboard" in render(breadcrumbs)
    assert "Reports" in render(breadcrumbs)

    current_path.set("/dashboard")

    html = render(breadcrumbs)

    assert "Home" in html
    assert "Dashboard" in html
    assert "Reports" not in html


def test_breadcrumb_trail_cleans_up_path_subscription():
    from pylage.ENGINE.core.state import State
    from pylage.UI.patterns.breadcrumbs import breadcrumb_trail

    current_path = State("/dashboard")
    breadcrumbs = breadcrumb_trail(current_path=current_path)

    assert len(current_path._subscribers) == 1

    breadcrumbs.cleanup()

    assert len(current_path._subscribers) == 0


def test_breadcrumb_trail_uses_route_label_metadata(tmp_path):
    from pylage.ENGINE.routing import Router
    from pylage.ENGINE.routing.runtime import RoutingRuntime
    from pylage.UI.patterns.breadcrumbs import breadcrumb_trail

    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "dashboard.py").write_text(
        "import pylage as pl\n"
        "label = 'Control Center'\n"
        "\ndef page():\n"
        "    return pl.text('Dashboard')\n",
        encoding="utf-8",
    )

    router = Router(pages)
    root = pl.column()
    runtime = RoutingRuntime(router, root)

    breadcrumbs = breadcrumb_trail(
        current_path=runtime.current_path_state,
        current_route=runtime.current_route_state,
    )

    runtime.navigate("/dashboard")

    html = render(breadcrumbs)

    assert "Control Center" in html
    assert "Dashboard" not in html
