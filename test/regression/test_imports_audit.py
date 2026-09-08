import pylage as pl
from pathlib import Path



PUBLIC_API = (
    "run",
    "colors",
    "style",
    "theme",
    "derived",
    "set_theme",
    "get_current_theme",
    "button",
    "tabs",
    "navigation_item",
    "app_shell",
    "two_column",
    "three_column",
    "top_header",
    "drawer",
    "spinner",
    "state",
)



def test_public_package_imports():
    assert pl is not None
    assert pl.__name__ == "pylage"



def test_public_api_symbols_are_importable():
    missing = [name for name in PUBLIC_API if not hasattr(pl, name)]
    assert missing == []



def test_public_root_has_no_uppercase_api_leaks():
    uppercase = [name for name in dir(pl) if not name.startswith("_") and name[:1].isupper()]
    assert uppercase == []



def test_canonical_internal_imports_resolve():
    from pylage.ENGINE.core.component import Component
    from pylage.ENGINE.core.registry import ComponentRegistry
    from pylage.ENGINE.core.state import State
    from pylage.ENGINE.styling.global_theme import get_global_theme, set_global_theme
    from pylage.ENGINE.styling.theme import Theme

    assert Component is not None
    assert ComponentRegistry is not None
    assert State is not None
    assert get_global_theme is not None
    assert set_global_theme is not None
    assert Theme is not None


def test_ui_implementation_uses_canonical_engine_imports():
    forbidden = []
    for path in Path("pylage/UI").rglob("*.py"):
        for line_no, line in enumerate(path.read_text().splitlines(), 1):
            if line.startswith("from pylage.ENGINE import") or line.startswith("import pylage.ENGINE"):
                forbidden.append(f"{path}:{line_no}: {line}")
    assert forbidden == []
