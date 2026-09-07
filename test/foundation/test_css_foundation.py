from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer


def test_renderer_includes_css_foundation():
    html = HTMLRenderer().render(Component("Text", text="Foundation"))

    assert "box-sizing: border-box" in html
    assert "html, body" in html
    assert "margin: 0" in html
    assert "font-family: system-ui" in html
    assert "button, input, textarea, select" in html
    assert "[hidden]" in html


def test_renderer_includes_foundation_once():
    html = HTMLRenderer().render(Component("Text", text="Foundation"))

    assert html.count("*, *::before, *::after") == 1


def test_foundation_does_not_remove_theme_tokens():
    from pylage.UI.themes.light import LIGHT_THEME

    html = HTMLRenderer(theme=LIGHT_THEME).render(Component("Text", text="Theme"))

    assert ":root{" in html
    assert "--color-primary" in html
    assert "box-sizing: border-box" in html

    foundation_index = html.find("*, *::before, *::after")
    theme_index = html.find('<style data-pylage-theme="true">:root{')

    assert foundation_index >= 0
    assert theme_index >= 0
    assert foundation_index < theme_index



def test_foundation_includes_interactive_focus_states():
    html = HTMLRenderer().render(Component("Button", text="Focus"))

    assert "button:focus-visible" in html
    assert "input:focus-visible" in html
    assert "textarea:focus-visible" in html
    assert "select:focus-visible" in html
    assert "outline: 2px solid var(--color-primary)" in html
    assert "outline-offset: 2px" in html


def test_foundation_includes_disabled_states():
    html = HTMLRenderer().render(Component("Button", text="Disabled"))

    assert "button:disabled" in html
    assert "input:disabled" in html
    assert "textarea:disabled" in html
    assert "select:disabled" in html
    assert "cursor: not-allowed" in html
    assert "opacity: 0.6" in html


def test_foundation_includes_readonly_and_checked_states():
    html = HTMLRenderer().render(Component("Input", text="States"))

    assert "input[readonly]" in html
    assert "textarea[readonly]" in html
    assert "input[type=\"checkbox\"]:checked" in html
    assert "accent-color: var(--color-primary)" in html
