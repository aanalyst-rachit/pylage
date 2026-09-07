"""UI Kit Layout API regression tests for Phase 11."""

from pylage import UI as ui
from pylage.ENGINE import Style, ResponsiveStyle


def test_responsive_shorthand_creates_responsive_style():
    component = ui.row(
        ui.text("A"),
        responsive={
            "base": {"flex_direction": "column"},
            "md": {"flex_direction": "row"},
            "lg": {"gap": "xl"},
        },
    )

    style = component.props["style"]

    assert isinstance(style, ResponsiveStyle)
    assert style.base.flex_direction == "column"
    assert style.md.flex_direction == "row"
    assert style.lg.gap == "var(--spacing-xl)"


def test_spacing_shorthand_resolves_tokens():
    component = ui.column(
        ui.text("Content"),
        p="lg",
        px="md",
        py="sm",
        gap="md",
    )

    style = component.props["style"]
    base = style.base

    assert base.padding == "var(--spacing-lg)"
    assert base.padding_left == "var(--spacing-md)"
    assert base.padding_right == "var(--spacing-md)"
    assert base.padding_top == "var(--spacing-sm)"
    assert base.padding_bottom == "var(--spacing-sm)"
    assert base.gap == "var(--spacing-md)"


def test_spacing_shorthand_explicit_style_wins():
    component = ui.column(
        ui.text("Content"),
        p="lg",
        style=Style(padding="4rem"),
    )

    style = component.props["style"]

    assert style.padding == "4rem"



def test_row_spacing_shorthand_resolves_tokens():
    component = ui.row(
        ui.text("A"),
        ui.text("B"),
        px="md",
        py="lg",
        gap="sm",
    )

    style = component.props["style"]
    base = style.base

    assert base.padding_left == "var(--spacing-md)"
    assert base.padding_right == "var(--spacing-md)"
    assert base.padding_top == "var(--spacing-lg)"
    assert base.padding_bottom == "var(--spacing-lg)"
    assert base.gap == "var(--spacing-sm)"
