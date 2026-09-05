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
    assert style.lg.gap == "2rem"


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

    assert base.padding == "1.5rem"
    assert base.padding_left == "1rem"
    assert base.padding_right == "1rem"
    assert base.padding_top == "0.5rem"
    assert base.padding_bottom == "0.5rem"
    assert base.gap == "1rem"


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

    assert base.padding_left == "1rem"
    assert base.padding_right == "1rem"
    assert base.padding_top == "1.5rem"
    assert base.padding_bottom == "1.5rem"
    assert base.gap == "0.5rem"
