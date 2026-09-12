from pylage.ENGINE import Column, Drawer, Spinner
from pylage.ENGINE.core.renderer import HTMLRenderer


def test_renderer_deduplicates_repeated_component_css():
    root = Column(Spinner(), Spinner(), Drawer(), Drawer())

    html = HTMLRenderer().render(root)

    assert html.count(".pylage-spinner {") == 1
    assert html.count(".pylage-drawer {") == 1
    assert html.count("<style>") >= 3

    first_style = html.find("<style>")
    first_component = html.find("<div")
    assert first_style != -1
    assert first_component != -1
    assert first_style < first_component
