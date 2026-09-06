"""Phase 14.10 - Component-level style override contract."""

import pylage as pl
from pylage.ENGINE.styling.style import Style


def test_card_user_style_overrides_variant():
    component = pl.card("Hello", variant="elevated", style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.box_shadow == "0 10px 15px -3px rgba(0,0,0,0.1)"


def test_button_user_style_overrides_variant_and_size():
    component = pl.button("Save", variant="primary", size="lg", style=Style(color="black"))
    style = component.props["style"]
    assert style.color == "black"
    assert style.background_color == "var(--color-primary)"
    assert style.font_size == "1.125rem"


def test_navbar_user_style_preserves_base_defaults():
    component = pl.navbar("Menu", style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.display == "flex"
    assert style.width == "100%"


def test_header_user_style_preserves_base_defaults():
    component = pl.Header("Header", style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.display == "flex"
    assert style.width == "100%"


def test_footer_user_style_preserves_base_defaults():
    component = pl.Footer("Footer", style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.display == "flex"


def test_navigation_controls_user_style_preserves_base_defaults():
    component = pl.navigation_controls(style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.display == "flex"
    assert style.gap == "0.5rem"


def test_dashboard_card_delegates_style_override():
    component = pl.dashboard_card("Body", style=Style(color="red"))
    style = component.props["style"]
    assert style.color == "red"
    assert style.box_shadow == "0 10px 15px -3px rgba(0,0,0,0.1)"
