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
