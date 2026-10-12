import pytest

from pylage.ENGINE import Iframe
from pylage.ENGINE.core.renderer import render


def test_iframe_creates_iframe_component():
    iframe = Iframe()
    assert iframe.type == "Iframe"


def test_iframe_renders_as_iframe():
    iframe = Iframe(src="https://example.com", title="Example")
    html = render(iframe)

    assert "<iframe" in html
    assert 'src="https://example.com"' in html
    assert 'title="Example"' in html
    assert "</iframe>" in html


def test_iframe_supports_props():
    iframe = Iframe(
        src="https://example.com",
        title="Example",
        width="800",
        height="600",
        allow="camera; microphone",
        allowfullscreen=True,
        loading="lazy",
        referrerpolicy="strict-origin-when-cross-origin",
        class_name="embed-frame",
    )
    html = render(iframe)

    assert 'src="https://example.com"' in html
    assert 'title="Example"' in html
    assert 'width="800"' in html
    assert 'height="600"' in html
    assert 'allow="camera; microphone"' in html
    assert "allowfullscreen" in html
    assert 'loading="lazy"' in html
    assert 'referrerpolicy="strict-origin-when-cross-origin"' in html
    assert 'class="embed-frame"' in html


def test_iframe_rejects_dangerous_src_scheme():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Iframe(src="javascript:alert(1)"))


def test_iframe_rejects_dangerous_src_with_leading_control_whitespace():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Iframe(src=chr(9) + chr(10) + "javascript:alert(1)"))


def test_iframe_allows_safe_src_urls():
    for src in (
        "embed.html",
        "/embed.html",
        "//cdn.example/embed.html",
        "https://example.com/embed.html",
    ):
        html = render(Iframe(src=src))
        assert f'src="{src}"' in html
