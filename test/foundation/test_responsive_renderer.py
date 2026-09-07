import pylage as ps
from pylage.ENGINE import ResponsiveStyle, Style, Text, Theme

from pylage.ENGINE.core.renderer import HTMLRenderer


def test_renderer_can_render_responsive_style():
    responsive = ResponsiveStyle(
        base=Style(
            color="black",
            font_size="16px",
        ),
        sm=Style(
            color="blue",
        ),
        md=Style(
            color="green",
            font_size="20px",
        ),
    )

    renderer = HTMLRenderer()

    html = renderer.render(
        Text(
            "Hello",
            style=responsive,
        )
    )

    assert "color:black" in html
    assert "font-size:16px" in html
    assert "@media" in html
    assert "color:blue" in html
    assert "color:green" in html
    assert "font-size:20px" in html


def test_renderer_without_responsive_style_remains_compatible():
    renderer = HTMLRenderer()

    html = renderer.render(
        Text(
            "Hello",
            style=Style(color="red"),
        )
    )

    assert "color:red" in html
    assert "@media" not in html


def test_responsive_style_can_use_theme_variables_in_renderer():
    theme = Theme(
        colors={
            "primary": "#2563eb",
            "background": "#ffffff",
        },
    )

    responsive = ResponsiveStyle(
        base=Style(
            color="var(--color-primary)",
        ),
        md=Style(
            color="var(--color-background)",
        ),
    )

    renderer = HTMLRenderer(theme=theme)

    html = renderer.render(
        Text(
            "Hello",
            style=responsive,
        )
    )

    assert "--color-primary:#2563eb" in html
    assert "--color-background:#ffffff" in html
    assert "var(--color-primary)" in html
    assert "var(--color-background)" in html
    assert "@media" in html
