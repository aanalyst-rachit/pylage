from pylage.ENGINE import Image
from pylage.ENGINE.core.renderer import render


def test_image_creates_image_component():
    image = Image()

    assert image.type == "Image"


def test_image_renders_as_img():
    image = Image(
        src="photo.jpg",
        alt="A photo",
    )

    html = render(image)

    assert "<img" in html
    assert 'src="photo.jpg"' in html
    assert 'alt="A photo"' in html


def test_image_supports_props():
    image = Image(
        src="avatar.png",
        alt="Avatar",
        class_name="profile-image",
        title="Profile",
    )

    html = render(image)

    assert 'src="avatar.png"' in html
    assert 'alt="Avatar"' in html
    assert 'class="profile-image"' in html
    assert 'title="Profile"' in html
import pytest

def test_image_rejects_dangerous_src_scheme():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Image(src="javascript:alert(1)"))

def test_image_rejects_dangerous_src_with_leading_control_whitespace():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Image(src=chr(9) + chr(10) + "javascript:alert(1)"))

def test_image_allows_safe_src_urls():
    for src in ("photo.jpg", "/assets/photo.jpg", "//cdn.example/photo.jpg", "https://example.com/photo.jpg"):
        html = render(Image(src=src))
        assert ('src="' + src + '"') in html
