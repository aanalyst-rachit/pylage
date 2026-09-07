import pylage as ps
from pylage.ENGINE import ResponsiveStyle, Style


def test_responsive_style_can_be_created():
    responsive = ResponsiveStyle(
        base=Style(color="black"),
        sm=Style(color="blue"),
        md=Style(color="green"),
    )

    assert responsive.base.color == "black"
    assert responsive.sm.color == "blue"
    assert responsive.md.color == "green"


def test_responsive_style_generates_media_queries():
    responsive = ResponsiveStyle(
        base=Style(font_size="16px"),
        sm=Style(font_size="18px"),
        md=Style(font_size="20px"),
    )

    css = responsive.to_css()

    assert "font-size:16px" in css
    assert "@media" in css
    assert "font-size:18px" in css
    assert "font-size:20px" in css


def test_responsive_style_can_use_theme_variables():
    responsive = ResponsiveStyle(
        base=Style(
            color="var(--color-primary)",
        ),
        md=Style(
            color="var(--color-background)",
        ),
    )

    css = responsive.to_css()

    assert "color:var(--color-primary)" in css
    assert "color:var(--color-background)" in css


def test_responsive_style_is_immutable():
    responsive = ResponsiveStyle(
        base=Style(color="black"),
    )

    try:
        responsive.base = Style(color="red")
    except Exception:
        pass
    else:
        raise AssertionError(
            "ResponsiveStyle must be immutable"
        )


def test_empty_responsive_style_generates_empty_css():
    responsive = ResponsiveStyle()

    assert responsive.to_css() == ""
