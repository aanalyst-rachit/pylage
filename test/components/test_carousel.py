from pylage.ENGINE import Carousel, Text, Button, State
from pylage.ENGINE.core.renderer import render


def test_carousel_creates_carousel_component():
    carousel = Carousel()

    assert carousel.type == "Carousel"


def test_carousel_supports_children():
    carousel = Carousel(
        Text("Slide 1"),
        Text("Slide 2"),
        Button("Next"),
    )

    html = render(carousel)

    assert "Slide 1" in html
    assert "Slide 2" in html
    assert "Next" in html


def test_carousel_supports_props():
    carousel = Carousel(
        class_name="hero-carousel",
        title="Featured",
    )

    html = render(carousel)

    assert 'class="hero-carousel"' in html
    assert 'title="Featured"' in html


def test_carousel_supports_value_and_reactivity():
    import pylage as ps
    slide_state = State(0)
    carousel = Carousel(value=slide_state)

    assert 'value="0"' in render(carousel)

    slide_state.set(1)
    assert 'value="1"' in render(carousel)
