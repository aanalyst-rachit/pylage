from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.ENGINE.core.component import Component


def test_spinner_animation_contract_is_rendered():
    html = HTMLRenderer().render(Component("Spinner"))

    assert "pylage-spinner" in html
    assert "animation: pylage-spinner-spin 0.75s linear infinite" in html


def test_spinner_keyframe_contract_is_rendered():
    html = HTMLRenderer().render(Component("Spinner"))

    assert "@keyframes pylage-spinner-spin" in html
    assert "transform: rotate(360deg)" in html


def test_spinner_animation_and_keyframes_are_emitted_together():
    html = HTMLRenderer().render(Component("Spinner"))

    animation_index = html.find(
        "animation: pylage-spinner-spin 0.75s linear infinite"
    )
    keyframes_index = html.find("@keyframes pylage-spinner-spin")

    assert animation_index >= 0
    assert keyframes_index >= 0
    assert animation_index < keyframes_index
