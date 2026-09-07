import pylage as ps
from pylage.ENGINE import Style, Text, Theme


def test_theme_token_can_be_used_as_style_value():
    theme = Theme(
        colors={
            "primary": "#2563eb",
        },
    )

    style = Style(
        color=theme.color("primary"),
    )

    assert style.color == "#2563eb"
    assert style.to_css() == "color:#2563eb"


def test_theme_spacing_token_can_be_used_as_style_value():
    theme = Theme(
        spacing={
            "md": "16px",
        },
    )

    style = Style(
        padding=theme.spacing_value("md"),
        gap=theme.spacing_value("md"),
    )

    assert style.to_css() == "padding:16px;gap:16px"


def test_theme_tokens_can_build_component_style():
    theme = Theme(
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
        spacing={
            "md": "16px",
        },
        radius={
            "md": "8px",
        },
    )

    style = Style(
        color=theme.color("primary"),
        background_color=theme.color("background"),
        padding=theme.spacing_value("md"),
        border_radius=theme.radius_value("md"),
    )

    component = Text(
        "Hello",
        style=style,
    )

    from pylage.ENGINE.core.renderer import render

    html = render(component)

    assert 'color:#2563eb' in html
    assert 'background-color:#ffffff' in html
    assert 'padding:16px' in html
    assert 'border-radius:8px' in html


def test_theme_does_not_mutate_style():
    theme = Theme(
        colors={"primary": "red"},
    )

    style = Style(color="blue")

    themed_style = Style(
        color=theme.color("primary"),
    )

    assert style.color == "blue"
    assert themed_style.color == "red"


def test_theme_and_style_remain_independent():
    theme = Theme(
        colors={"primary": "red"},
    )

    style = Style(color="blue")

    assert theme.color("primary") == "red"
    assert style.color == "blue"
