from pathlib import Path

import pytest

import pylage as pl
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.routing import Router
from pylage.ENGINE.routing.runtime import RoutingRuntime


def write_page(pages: Path, name: str, source: str) -> Path:
    path = pages / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8")
    return path


def make_shell() -> Component:
    """Stable root whose children are replaced on route transition."""
    return pl.column()


def test_navigate_resolves_static_page_and_sets_root_children(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n",
    )
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    result = runtime.navigate("/dashboard")

    assert isinstance(result, Component)
    assert list(root.children) == [result]
    assert runtime.current_path == "/dashboard"


def test_navigate_passes_dynamic_params_to_page(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard/[user_id].py",
        "import pylage as pl\n\ndef page(user_id):\n    return pl.text(f\"User {user_id}\")\n",
    )
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    result = runtime.navigate("/dashboard/42")

    assert list(root.children) == [result]
    assert runtime.current_path == "/dashboard/42"
    props = getattr(result, "props", None) or {}
    text = props.get("text") or props.get("content") or str(result)
    assert "42" in str(text)


def test_navigate_unknown_path_raises(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "index.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Home\")\n",
    )
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    with pytest.raises(LookupError, match="No route"):
        runtime.navigate("/missing")


def test_second_navigate_replaces_previous_page(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n",
    )
    write_page(
        pages,
        "analytics.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Analytics\")\n",
    )
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    first = runtime.navigate("/dashboard")
    second = runtime.navigate("/analytics")

    assert list(root.children) == [second]
    assert first not in list(root.children)
    assert runtime.current_path == "/analytics"


def test_navigate_normalizes_path(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n",
    )
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    runtime.navigate("dashboard")
    assert runtime.current_path == "/dashboard"
    runtime.navigate("/dashboard/")
    assert runtime.current_path == "/dashboard"

def test_current_path_state_tracks_successful_navigation_only(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(pages, "dashboard.py", "import pylage as pl\n\ndef page():\n    return pl.text(\"Dashboard\")\n")
    write_page(pages, "analytics.py", "import pylage as pl\n\ndef page():\n    return pl.text(\"Analytics\")\n")
    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    assert runtime.current_path_state.value is None

    runtime.navigate("/dashboard/")
    assert runtime.current_path == "/dashboard"
    assert runtime.current_path_state.value == "/dashboard"

    runtime.navigate("/analytics")
    assert runtime.current_path_state.value == "/analytics"

    with pytest.raises(LookupError):
        runtime.navigate("/missing")

    assert runtime.current_path_state.value == "/analytics"


def test_navigation_item_tracks_routing_runtime_current_path(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard.py",
        'import pylage as pl\n\ndef page():\n    return pl.text("Dashboard")\n',
    )
    write_page(
        pages,
        "analytics.py",
        'import pylage as pl\n\ndef page():\n    return pl.text("Analytics")\n',
    )

    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    dashboard = pl.navigation_item(
        "Dashboard",
        href="/dashboard",
        current_path=runtime.current_path_state,
    )
    analytics = pl.navigation_item(
        "Analytics",
        href="/analytics",
        current_path=runtime.current_path_state,
    )

    assert dashboard.props["style"].background_color.value == "transparent"
    assert analytics.props["style"].background_color.value == "transparent"

    runtime.navigate("/dashboard")

    assert dashboard.props["style"].background_color.value == "var(--color-primary)"
    assert analytics.props["style"].background_color.value == "transparent"

    runtime.navigate("/analytics")

    assert dashboard.props["style"].background_color.value == "transparent"
    assert analytics.props["style"].background_color.value == "var(--color-primary)"


def test_navigation_runtime_updates_content_root_without_replacing_shell(
    tmp_path,
):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "dashboard.py",
        'import pylage as pl\n\ndef page():\n    return pl.text("Dashboard")\n',
    )
    write_page(
        pages,
        "analytics.py",
        'import pylage as pl\n\ndef page():\n    return pl.text("Analytics")\n',
    )

    router = Router(pages)

    navbar = pl.navigation(pl.text("Navbar"))
    content = pl.column()
    root = pl.column(navbar, content)

    runtime = RoutingRuntime(router, root, content_root=content)

    runtime.navigate("/dashboard")

    assert root.children == [navbar, content]
    assert content.children[0].props["text"] == "Dashboard"
    assert runtime.current_path == "/dashboard"

    runtime.navigate("/analytics")

    assert root.children == [navbar, content]
    assert content.children[0].props["text"] == "Analytics"
    assert runtime.current_path == "/analytics"


def test_navigation_runtime_rejects_invalid_content_root(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()

    write_page(
        pages,
        "index.py",
        'import pylage as pl\n\ndef page():\n    return pl.text("Home")\n',
    )

    router = Router(pages)
    root = make_shell()

    with pytest.raises(TypeError, match="content_root"):
        RoutingRuntime(router, root, content_root="invalid")


def test_current_route_exposes_optional_route_label(tmp_path):
    pages = tmp_path / "pages"
    pages.mkdir()
    write_page(
        pages,
        "dashboard.py",
        "import pylage as pl\n"
        "label = 'Control Center'\n"
        "\ndef page():\n"
        "    return pl.text('Dashboard')\n",
    )

    router = Router(pages)
    root = make_shell()
    runtime = RoutingRuntime(router, root)

    assert runtime.current_route is None

    runtime.navigate("/dashboard")

    assert runtime.current_route is not None
    assert runtime.current_route.path == "/dashboard"
    assert runtime.current_route.label == "Control Center"
