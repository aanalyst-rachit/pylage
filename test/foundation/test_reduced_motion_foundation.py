from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer


def test_renderer_includes_reduced_motion_foundation():
    html = HTMLRenderer().render(Component("Text", text="Reduced motion"))

    assert "@media (prefers-reduced-motion: reduce)" in html
    assert "animation-duration: 0.01ms !important" in html
    assert "animation-iteration-count: 1 !important" in html
    assert "scroll-behavior: auto !important" in html
    assert "transition-duration: 0.01ms !important" in html


def test_reduced_motion_foundation_is_emitted_once():
    html = HTMLRenderer().render(Component("Text", text="Reduced motion"))

    assert html.count("@media (prefers-reduced-motion: reduce)") == 1
