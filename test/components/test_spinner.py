from pylage.ENGINE import Spinner
from pylage.ENGINE.core.renderer import render


def test_spinner_renders_as_visual_element():
    spinner = Spinner()

    html = render(spinner)

    assert '<span' in html
    assert 'class="pylage-spinner"' in html
    assert 'animation: pylage-spinner-spin' in html


def test_spinner_supports_props():
    spinner = Spinner(
        class_name="loading-spinner",
        title="Loading",
    )

    html = render(spinner)

    assert 'class="pylage-spinner loading-spinner"' in html
    assert 'title="Loading"' in html


def test_spinner_supports_size():
    spinner = Spinner(size="large")

    html = render(spinner)

    assert 'size="large"' in html


def test_spinner_supports_text():
    spinner = Spinner(
        text="Please wait",
    )

    html = render(spinner)

    assert "Please wait" in html
