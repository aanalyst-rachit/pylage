from pylage.ENGINE import Video
from pylage.ENGINE.core.renderer import render


def test_video_creates_video_component():
    video = Video()

    assert video.type == "Video"


def test_video_renders_as_video():
    video = Video(
        src="movie.mp4",
        controls=True,
    )

    html = render(video)

    assert "<video" in html
    assert 'src="movie.mp4"' in html
    assert "controls" in html
    assert "</video>" in html


def test_video_supports_props():
    video = Video(
        src="demo.mp4",
        class_name="hero-video",
        title="Demo",
        controls=True,
    )

    html = render(video)

    assert 'src="demo.mp4"' in html
    assert 'class="hero-video"' in html
    assert 'title="Demo"' in html
    assert "controls" in html
import pytest

def test_video_rejects_dangerous_src_scheme():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Video(src="javascript:alert(1)"))

def test_video_rejects_dangerous_src_with_leading_control_whitespace():
    with pytest.raises(ValueError, match="unsafe URL scheme"):
        render(Video(src=chr(9) + chr(10) + "javascript:alert(1)"))

def test_video_allows_safe_src_urls():
    for src in ("movie.mp4", "/assets/movie.mp4", "//cdn.example/movie.mp4", "https://example.com/movie.mp4"):
        html = render(Video(src=src))
        assert ("src=\"" + src + "\"") in html
