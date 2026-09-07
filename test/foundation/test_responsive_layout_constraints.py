import pylage as ps
from pylage.ENGINE import Column, Grid, ResponsiveStyle, Style, Text

from pylage.ENGINE.core.renderer import HTMLRenderer


def test_responsive_layout_constraints():
    responsive = ResponsiveStyle(
        base=Style(
            width="100%",
            padding="8px",
        ),
        sm=Style(
            width="90%",
            padding="12px",
        ),
        md=Style(
            width="80%",
            max_width="1200px",
            padding="16px",
        ),
    )

    renderer = HTMLRenderer()

    html = renderer.render(
        Column(
            Text("Responsive"),
            style=responsive,
        )
    )

    assert "width:100%" in html
    assert "padding:8px" in html

    assert "@media" in html
    assert "width:90%" in html
    assert "padding:12px" in html

    assert "width:80%" in html
    assert "max-width:1200px" in html
    assert "padding:16px" in html


def test_responsive_flex_constraints():
    responsive = ResponsiveStyle(
        base=Style(
            display="flex",
            flex_direction="column",
            gap="8px",
        ),
        md=Style(
            flex_direction="row",
            gap="16px",
        ),
    )

    renderer = HTMLRenderer()

    html = renderer.render(
        Column(
            Text("One"),
            Text("Two"),
            style=responsive,
        )
    )

    assert "display:flex" in html
    assert "flex-direction:column" in html
    assert "gap:8px" in html

    assert "@media" in html
    assert "flex-direction:row" in html
    assert "gap:16px" in html


def test_responsive_grid_constraints():
    responsive = ResponsiveStyle(
        base=Style(
            display="grid",
            grid_template_columns="1fr",
        ),
        md=Style(
            grid_template_columns="repeat(3, 1fr)",
        ),
    )

    renderer = HTMLRenderer()

    html = renderer.render(
        Grid(
            Text("One"),
            Text("Two"),
            Text("Three"),
            style=responsive,
        )
    )

    assert "display:grid" in html
    assert "grid-template-columns:1fr" in html

    assert "@media" in html
    assert "grid-template-columns:repeat(3, 1fr)" in html
