import pylage as ps
from pylage.ENGINE import Column, Grid, Row, State, Style, Text
from pylage.ENGINE.core.renderer import render


def test_layout_exports():
    assert callable(Row)
    assert callable(Column)
    assert callable(Grid)


def test_row_default_and_override():
    html = render(
        Row(
            Text("A"),
            Text("B"),
            style=Style(
                gap="10px",
                justify_content="center",
            ),
        )
    )

    assert html.count('style="') == 1
    assert "display:flex" in html
    assert "flex-direction:row" in html
    assert "gap:10px" in html
    assert "justify-content:center" in html


def test_column_default_and_override():
    html = render(
        Column(
            Text("A"),
            Text("B"),
            style=Style(
                gap="10px",
                align_items="center",
            ),
        )
    )

    assert html.count('style="') == 1
    assert "display:flex" in html
    assert "flex-direction:column" in html
    assert "gap:10px" in html
    assert "align-items:center" in html


def test_grid_style_is_preserved():
    html = render(
        Grid(
            Text("A"),
            Text("B"),
            style=Style(
                display="grid",
                grid_template_columns="repeat(2, 1fr)",
                gap="12px",
            ),
        )
    )

    assert html.count('style="') == 1
    assert "display:grid" in html
    assert "grid-template-columns:repeat(2, 1fr)" in html
    assert "gap:12px" in html


def test_nested_layouts_render_correctly():
    html = render(
        Column(
            Row(
                Text("A"),
                Text("B"),
            ),
            Grid(
                Text("C"),
                Text("D"),
                style=Style(
                    display="grid",
                    grid_template_columns="repeat(2, 1fr)",
                ),
            ),
        )
    )

    assert html.count('style="') == 3
    assert "flex-direction:column" in html
    assert "flex-direction:row" in html
    assert "display:grid" in html
    assert all(x in html for x in ["A", "B", "C", "D"])


def test_state_layout_values_render():
    width = State("80%")
    gap = State("16px")

    html = render(
        Row(
            Text("State"),
            style=Style(
                width=width,
                gap=gap,
            ),
        )
    )

    assert "width:80%" in html
    assert "gap:16px" in html
    assert "State(&#x27;80%&#x27;)" not in html
    assert "State(&#x27;16px&#x27;)" not in html
