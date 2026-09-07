from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer


def test_foundation_includes_print_media_rules():
    html = HTMLRenderer().render(Component("Text", text="Print"))

    assert "@media print" in html


def test_print_foundation_hides_nonessential_elements():
    html = HTMLRenderer().render(Component("Text", text="Print"))

    assert "nav," in html
    assert "aside," in html
    assert "button" in html
    assert "display: none !important" in html


def test_print_foundation_preserves_document_colors():
    html = HTMLRenderer().render(Component("Text", text="Print"))

    assert "print-color-adjust: exact" in html
    assert "-webkit-print-color-adjust: exact" in html
