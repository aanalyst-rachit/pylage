"""
RULE 0 — Canonical PyLage Package Audit

The old pylage_ui and pylage_layout packages have been removed.

Canonical architecture:

pylage/
├── __init__.py
├── UI/
│   ├── components/
│   ├── layout/
│   ├── patterns/
│   ├── recipes/
│   ├── themes/
│   └── tokens/
└── ENGINE/
    ├── components/
    ├── core/
    ├── renderers/
    ├── runtime/
    └── styling/
"""

from pathlib import Path
import importlib


ROOT = Path(__file__).resolve().parents[2]
PYLAGE = ROOT / "pylage"
UI = PYLAGE / "UI"
ENGINE = PYLAGE / "ENGINE"


def _import(name):
    return importlib.import_module(name)


# ======================================================================
# RULE 1 — Canonical package exists
# ======================================================================

def test_canonical_pylage_package_exists():
    assert PYLAGE.is_dir()
    assert (PYLAGE / "__init__.py").is_file()


def test_canonical_ui_package_exists():
    assert UI.is_dir()
    assert (UI / "__init__.py").is_file()


def test_canonical_engine_package_exists():
    assert ENGINE.is_dir()
    assert (ENGINE / "__init__.py").is_file()


# ======================================================================
# RULE 2 — Canonical UI subpackages
# ======================================================================

def test_ui_subpackages_exist():
    expected = {
        "components",
        "layout",
        "patterns",
        "recipes",
        "themes",
        "tokens",
    }

    actual = {
        path.name
        for path in UI.iterdir()
        if path.is_dir() and (path / "__init__.py").is_file()
    }

    assert expected <= actual


# ======================================================================
# RULE 3 — Canonical ENGINE subpackages
# ======================================================================

def test_engine_subpackages_exist():
    expected = {
        "components",
        "core",
        "renderers",
        "runtime",
        "styling",
    }

    actual = {
        path.name
        for path in ENGINE.iterdir()
        if path.is_dir() and (path / "__init__.py").is_file()
    }

    assert expected <= actual


# ======================================================================
# RULE 4 — Legacy packages are gone
# ======================================================================

def test_legacy_packages_are_removed():
    assert not (ROOT / "pylage_ui").exists()
    assert not (ROOT / "pylage_layout").exists()


# ======================================================================
# RULE 5 — Canonical UI packages import
# ======================================================================

def test_ui_packages_import():
    modules = [
        "pylage.UI",
        "pylage.UI.components",
        "pylage.UI.layout",
        "pylage.UI.patterns",
        "pylage.UI.recipes",
        "pylage.UI.themes",
        "pylage.UI.tokens",
    ]

    for module_name in modules:
        assert _import(module_name) is not None


# ======================================================================
# RULE 6 — Canonical layout modules import
# ======================================================================

def test_layout_modules_import():
    modules = [
        "center",
        "container",
        "drawer",
        "factories",
        "footer",
        "header",
        "menu",
        "navbar",
        "navigation",
        "navigation_controls",
        "pagination",
        "section",
        "sidebar",
        "split",
        "stack",
        "tabs",
        "three_column",
        "topbar",
        "two_column",
    ]

    for module_name in modules:
        assert _import(f"pylage.UI.layout.{module_name}") is not None


# ======================================================================
# RULE 7 — Canonical pattern modules import
# ======================================================================

def test_pattern_modules_import():
    modules = [
        "auth",
        "breadcrumbs",
        "contact",
        "content",
        "cta",
        "faq",
        "feature",
        "hero",
        "list",
        "newsletter",
        "pricing",
        "search",
        "states",
        "stats",
        "testimonial",
    ]

    for module_name in modules:
        assert _import(f"pylage.UI.patterns.{module_name}") is not None


# ======================================================================
# RULE 8 — Canonical recipe modules import
# ======================================================================

def test_recipe_modules_import():
    modules = [
        "admin",
        "admin_panel",
        "authentication",
        "dashboard",
        "documentation",
        "landing",
        "profile",
        "settings",
    ]

    for module_name in modules:
        assert _import(f"pylage.UI.recipes.{module_name}") is not None


# ======================================================================
# RULE 9 — Themes and tokens import
# ======================================================================

def test_theme_modules_import():
    modules = [
        "api",
        "dark",
        "factory",
        "light",
    ]

    for module_name in modules:
        assert _import(f"pylage.UI.themes.{module_name}") is not None


def test_token_modules_import():
    modules = [
        "colors",
        "fonts",
        "radius",
        "spacing",
        "validate",
    ]

    for module_name in modules:
        assert _import(f"pylage.UI.tokens.{module_name}") is not None


# ======================================================================
# RULE 10 — Root public facade imports
# ======================================================================

def test_public_root_imports():
    pylage = _import("pylage")

    assert hasattr(pylage, "run")
    assert hasattr(pylage, "style")
    assert hasattr(pylage, "theme")


# ======================================================================
# RULE 11 — UI public namespace
# ======================================================================

def test_ui_public_namespace():
    ui = _import("pylage.UI")

    assert hasattr(ui, "__all__")

    for name in ui.__all__:
        assert hasattr(ui, name), (
            f"pylage.UI.__all__ contains missing symbol: {name}"
        )


# ======================================================================
# RULE 12 — ENGINE is internal and separate
# ======================================================================

def test_engine_is_not_reexported_by_public_all():
    pylage = _import("pylage")

    public = set(getattr(pylage, "__all__", []))

    forbidden = {
        "ENGINE",
        "State",
        "Style",
        "Theme",
        "ResponsiveStyle",
        "Component",
        "Runtime",
        "Renderer",
    }

    assert public.isdisjoint(forbidden)
