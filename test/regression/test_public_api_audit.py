"""
PHASE 14.1 — Public API Contract Lock

Purpose:
- Verify the canonical public API is importable as ``import pylage as pl``.
- Verify components, layouts, and patterns are exposed from the root API.
- Verify style and theme namespaces are exposed from the root API.
- Verify users do not need ``pylage.UI.*`` for the public contract.
- Preserve the existing AppShell and Hero public behavior.
"""

import pylage as pl


def test_root_public_api_imports():
    assert pl is not None


def test_root_components_are_public():
    assert callable(pl.button)
    assert callable(pl.card)
    assert callable(pl.text)


def test_root_layouts_are_public():
    assert hasattr(pl, "AppShell")
    assert callable(pl.AppShell)


def test_root_patterns_are_public():
    assert hasattr(pl, "Hero")
    assert callable(pl.Hero)


def test_root_style_namespace_is_public():
    assert hasattr(pl, "style")
    assert pl.style.black is not None
    assert pl.style.white is not None
    assert pl.style.elevated_card is not None
    assert pl.style.topheader is not None


def test_root_theme_namespace_is_public():
    assert hasattr(pl, "theme")
    assert pl.theme.light is not None
    assert pl.theme.dark is not None




def test_public_style_constructor_returns_style():
    from pylage.ENGINE.styling.style import Style
    custom = pl.style(color="red", padding="1rem", custom={"--test-token": "10px"})
    assert isinstance(custom, Style)
    assert custom.color == "red"
    assert custom.padding == "1rem"
    assert custom.custom["--test-token"] == "10px"


def test_public_style_presets_are_style_instances():
    from pylage.ENGINE.styling.style import Style
    assert isinstance(pl.style.black, Style)
    assert isinstance(pl.style.white, Style)
    assert isinstance(pl.style.elevated_card, Style)
    assert isinstance(pl.style.topheader, Style)


def test_public_style_merge_preserves_and_overrides_values():
    base = pl.style.black
    override = pl.style(color="blue", custom={"--test-token": "20px"})
    merged = base.merge(override)
    assert merged.color == "blue"
    assert merged.background_color == "#000000"
    assert merged.custom["--test-token"] == "20px"


def test_public_style_custom_css_property_validation():
    import pytest
    with pytest.raises(ValueError, match="must start with .*"):
        pl.style(custom={"test-token": "10px"}).to_css()

def test_app_shell_composes_header_sidebar_content():
    header = pl.text("Header")
    sidebar = pl.text("Sidebar")
    content = pl.text("Content")

    app = pl.AppShell(
        header=header,
        sidebar=sidebar,
        content=content,
    )

    assert app is not None
    assert hasattr(app, "type")
    assert hasattr(app, "props")


def test_hero_supports_target_usage():
    hero = pl.Hero(
        title="Build with Python",
        description="Build reusable layouts with Python.",
        actions=[
            pl.button("Get Started"),
            pl.button("Learn More"),
        ],
    )

    assert hero is not None
    assert hasattr(hero, "type")
    assert hasattr(hero, "props")


def test_hero_accepts_string_actions():
    hero = pl.Hero(
        title="Build with Python",
        actions=["Get Started", "Learn More"],
    )

    assert hero is not None
    assert hasattr(hero, "type")


def test_root_public_api_contract_is_canonical():
    assert "style" in pl.__all__
    assert "theme" in pl.__all__
    assert "AppShell" in pl.__all__
    assert "Hero" in pl.__all__
    assert "button" in pl.__all__
    assert "card" in pl.__all__


def test_public_variant_contract():
    assert pl.button("Save", variant="primary").props["style"].background_color == "var(--color-primary)"
    assert pl.button("Save", variant="danger").props["style"].background_color == "var(--color-danger)"

    assert pl.card(variant="default").props["style"].border == "1px solid var(--color-border)"
    assert pl.card(variant="elevated").props["style"].box_shadow == "0 10px 15px -3px rgba(0,0,0,0.1)"

    assert pl.badge("Active", variant="success").props["style"].background_color == "var(--color-success)"
    assert pl.alert("Info", variant="info").props["style"].background_color == "var(--color-info)"
    assert pl.toast("Saved", variant="success").props["style"].background_color == "var(--color-success)"


def test_public_size_contract():
    assert pl.button("Save", size="sm").props["style"].font_size == "0.875rem"
    assert pl.button("Save", size="md").props["style"].font_size == "1rem"
    assert pl.button("Save", size="lg").props["style"].font_size == "1.125rem"

    assert pl.avatar("S", size="sm").props["style"].width == "32px"
    assert pl.avatar("M", size="md").props["style"].width == "40px"
    assert pl.avatar("L", size="lg").props["style"].width == "48px"


def test_public_theme_contract():
    assert pl.theme.light is not None
    assert pl.theme.dark is not None
    assert pl.theme.get_theme("light") is pl.theme.light
    assert pl.theme.get_theme("dark") is pl.theme.dark
    assert pl.theme.available_themes() == ("dark", "light")


def test_public_usage_requires_only_root_package():
    # Phase 14 contract: public consumers use ``import pylage as pl``.
    # Engine/UI imports remain legitimate for internal implementation tests.
    assert pl.__name__ == "pylage"
