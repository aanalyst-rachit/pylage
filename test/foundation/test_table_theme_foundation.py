from pylage.ENGINE.core.renderer import render
from pylage.ENGINE import Table



def test_table_cells_use_theme_aware_backgrounds():
    html = render(Table(headers=["ID", "Name"], data=[[1, "Rachit"]]))
    css = html.split("<style>", 1)[1].split("</style>", 1)[0]
    assert "td {" in css
    assert "background-color: var(--color-background);" in css
    assert "th {" in css
    assert "background-color: var(--color-surface-variant);" in css


def test_table_foundation_keeps_spacing_and_border_contract():
    html = render(Table(headers=["ID", "Name"], data=[[1, "Rachit"]]))
    css = html.split("<style>", 1)[1].split("</style>", 1)[0]
    assert "th," in css
    assert "td {" in css
    assert "padding: 0.75rem 1rem;" in css
    assert "text-align: left;" in css
    assert "border-bottom: 1px solid var(--color-border);" in css
